<script>
import axios from 'axios';
import NavBar from '@/components/NavBar.vue';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
  name: "UserSummary",
  components: { NavBar },
  data() {
    return {
      user: '',
      scoreData: [],
      quiz:'',
      export_id:'',
      selectedQuizId: null,
      token: localStorage.getItem('token'),
      chartType: 'accuracy',  // or 'percentage'
    };
  },
  computed: {
    uniqueQuizzes() {
      const map = new Map();
      for (const score of this.scoreData) {
        const quiz = score.quiz;
        if (quiz && !map.has(quiz.id)) {
          map.set(quiz.id, quiz);
        }
      }
      return Array.from(map.values());
    }
  },
  mounted() {
    this.fetchUser();
  },
  methods: {
    async fetchUser() {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/user`, {
          headers: { Authorization: `Bearer ${this.token}` }
        });
        console.log(response.data)
        this.user = response.data;
        this.scoreData = response.data.scores;
        // After setting scoreData, check for available quizzes and render the chart
        if (this.scoreData.length > 0) {
          this.selectedQuizId = this.scoreData[0].quiz_id;
          await this.getQuiz(this.selectedQuizId);
          this.$nextTick(() => {
            this.renderChart();
          });
        }
      }
      catch (error) {
        if (error.response && error.response.data && error.response.data.error) {
          this.errorMessage = error.response.data.error;
        } else {
          this.errorMessage = 'An error occurred while fetching the Quiz.';
        }
      }
    },
    async getQuiz(quiz_id) {
      try {
        const res = await axios.get(`http://127.0.0.1:5000/api/quiz/${quiz_id}`, {
          headers: { Authorization: `Bearer ${this.token}` }
        });
        console.log(res.data);
        this.quiz = res.data;
      } catch (error) {
        if (error.response && error.response.data && error.response.data.error) {
          this.errorMessage = error.response.data.error;
        } else {
          this.errorMessage = 'An error occurred while fetching the Quiz.';
        }
      }
    },
    async fetchSummaryData() {
      const res = await axios.get(`http://127.0.0.1:5000/api/score?user_id=${this.user.id}`, {
        headers: { Authorization: `Bearer ${this.token}` }
      });
      const data = Array.isArray(res.data) ? res.data : res.data.scores || [];
      this.scoreData = data;
      this.selectedQuizId = data.length > 0 ? data[0].quiz_id : null;
      this.$nextTick(() => {
        this.renderChart();
      });
    },
    async exporting_id() {
          try {
            const res = await axios.get(`http://127.0.0.1:5000/api/export_quiz_csv/${this.selectedQuizId}`, {
              headers: { Authorization: `Bearer ${this.token}`}
            });
            console.log(res.data);
            this.export_id = res.data.id;
            // Call CSV download after export_id is fetched
            window.open(`http://127.0.0.1:5000/api/csv_result/${this.export_id}`, '_blank');
          } catch (error) {
              this.errorMessage = 'Failed to fetch export_id or download CSV';
          }
        },

    renderChart() {
      const canvas = document.getElementById('scoreChart');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const filteredAttempts = this.scoreData.filter(score => this.selectedQuizId === null || score.quiz_id === this.selectedQuizId);
      const sortedAttempts = filteredAttempts.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
      const labels = sortedAttempts.map((_, index) => `Attempt ${index + 1}`);
      const accuracyData = sortedAttempts.map(a => a.accuracy);
      const percentageData = sortedAttempts.map(a => a.percentage_score);
      const time_taken = sortedAttempts.map(a => a.time_taken);  // convert to minutes
      let datasets = [];

      if (this.chartType === 'accuracy') {
        datasets.push({
          label: 'Accuracy (%)',
          data: accuracyData,
          backgroundColor: 'rgba(153, 102, 255, 0.6)',
          borderColor: 'rgba(153, 102, 255, 1)',
          borderWidth: 1
        });
      } else if (this.chartType === 'percentage') {
        datasets.push({
          label: 'Percentage Score (%)',
          data: percentageData,
          backgroundColor: 'rgba(255, 159, 64, 0.6)',
          borderColor: 'rgba(255, 159, 64, 1)',
          borderWidth: 1
        });
      }
        else if (this.chartType === 'time_taken') {
        datasets.push({
          label: 'Time Taken',
          data: time_taken,
          backgroundColor: 'rgba(25, 159, 64, 0.6)',
          borderColor: 'rgba(25, 100, 164, 4)',
          borderWidth: 1
        });
      }
      const chartData = {
        labels,
        datasets
      };
      

      if (this.chartInstance) {
        this.chartInstance.destroy();
      }

      this.chartInstance = new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: this.chartType === 'time_taken'
                  ? 'Time Taken (seconds)'
                  : this.chartType === 'accuracy'
                  ? 'Accuracy (%)'
                  : 'Percentage Score (%)'
              },
              ticks: {
                callback: function(value) {
                  return this.chart.options.plugins.title.text.includes('Time Taken')
                    ? value.toFixed(2)
                    : value;
                }
              }
            },
            x: {
              title: {
                display: true,
                text: 'Attempts'
              },
              ticks: {
                maxRotation: 0,
                autoSkip: true
              },
              grid: {
                display: false
              },
              stacked: false,
              barThickness: Math.max(10, 100 / sortedAttempts.length)  // dynamic bar width
            }
          },
          plugins: {
            title: {
              display: true,
              text: `Quiz Title - ${this.quiz.title || ''} - Number of Questions: ${this.quiz.questions.length}`
            },
            legend: {
              position: 'top'
            }
          }
        }
      });
    },
    async handleQuizChange(event) {
      this.selectedQuizId = parseInt(event.target.value);
      await this.getQuiz(this.selectedQuizId);
      this.renderChart();
    }
  }
}
</script>



<template>
  <NavBar />
  <div class="summary-container">
    <h1 class="summary-title">Summary Statistics</h1>
    <div class="controls">
      <div class="control-group">
        <label for="quizSelect">Select Quiz:</label>
        <select id="quizSelect" @change="handleQuizChange">
          <option v-for="quiz in uniqueQuizzes" :key="quiz.id" :value="quiz.id">
            {{ quiz.title }}
          </option>
        </select>
      </div>
      <div class="control-group">
        <label for="statSelect">Select Stat Type:</label>
        <select id="statSelect" v-model="chartType" @change="renderChart">
          <option value="accuracy">Accuracy</option>
          <option value="percentage">Percentage</option>
          <option value="time_taken">Time Taken</option>
        </select>
      </div>
      <button class="download" @click="exporting_id">Download CSV Result</button>
    </div>
    <div class="chart-wrapper">
      <canvas id="scoreChart"></canvas>
    </div>
  </div>
</template>

<style>
.summary-container {
  padding: 50px;
  max-width: 1000px;
  margin: auto;
  background: #ffffff;
  border-radius: 18px;
}

.summary-title {
  text-align: center;
  margin-top: 40px;
  margin-bottom: 20px;
  font-size: 42px;
  font-weight: bold;
  color: #333;
}

.controls {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  gap: 10px;
}

.control-group {
  display: flex;
  flex-direction: column;
}

.control-group label {
  font-weight: bold;
  margin-bottom: 4px;
}

select {
  padding: 6px 10px;  
  border-radius: 15px;
  border: 1px solid #ccc;
  min-width: 180px;
}

button.download {
  padding: 12px 16px;
  border-radius: 15px;
  background-color: #4CAF50;
  color: white;
  font-weight: bold;
  border: none;
  cursor: pointer;
  transition: background 0.3s;
}

button.download:hover {
  background-color: #54db5ad2;
  color: #000;
}

.chart-wrapper {
  width: 100%;
  height: 500px;
}
</style>
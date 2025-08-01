<script>
import NavBar from '@/components/NavBar.vue';
import axios from 'axios';
export default {
    data(){
        return{
            marks: 0,
            export_id:'',
            quiz_id: 0,
            questions:[],
            token: localStorage.getItem('token'),
            errorMessage: '',
            totalques: 0,
            correctcount:0,
            incorrect:0,
            missed:0,
            percentage:0,
            time_taken:0,
            maxscore:0,
            scored:0,
            scoreId:this.$route.params.score_id,
            accuracy: 0,
        };
    },
    components:{
      NavBar
    },
    created() {
      this.loadScore().then(() => {
        this.getQuiz();
      });
    },
    
    methods:{
      async exporting_id() {
          try {
            const res = await axios.get(`http://127.0.0.1:5000/api/export_csv/${this.scoreId}`, {
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

      async loadScore() {
          try {
            const res = await axios.get(`http://127.0.0.1:5000/api/score/${this.scoreId}`, {
              headers: { Authorization: `Bearer ${this.token}` }
            });
            console.log(res.data)
            if (res.data) {
              this.quiz_id = res.data.quiz_id;
              this.correctcount = res.data.correct_answers;
              this.incorrect = res.data.incorrect_answers;
              const totalSeconds = res.data.time_taken;
              const hours = Math.floor(totalSeconds / 3600);
              const minutes = Math.floor((totalSeconds % 3600) / 60);
              const seconds = totalSeconds % 60;
              if (hours > 0) {
                this.time_taken = `${hours} hr ${minutes} min ${seconds} sec`;
              } else if (minutes > 0) {
                this.time_taken = `${minutes} min ${seconds} sec`;
              } else {
                this.time_taken = `${seconds} sec`;
              }
              this.maxscore = res.data.quiz_score;
              this.scored = res.data.total_scored;
              this.accuracy = parseFloat(res.data.accuracy).toFixed(2);
              this.percentage = parseFloat(res.data.percentage_score).toFixed(2);
            }
          } catch (error) {
            this.errorMessage = 'Failed to load Score.';
          }
        },
        async getQuiz() {
          try {
            const res = await axios.get(`http://127.0.0.1:5000/api/quiz/${this.quiz_id}`, {
              headers: { Authorization: `Bearer ${this.token}`}
            });
            console.log(res.data)
            // this.quiz= res.data;
            this.totalques = res.data.questions.length;  
            this.questions = res.data.questions;
          } catch (error) {
            this.errorMessage = 'Failed to load Quiz.';
          }
        },
        
      },
}

</script>



<template>
<div>
  <NavBar/>
  <h1>Quiz Statistics</h1>
  <div v-if="scoreId" style="position: relative;">
    <router-link :to="`/quiz-attempt/${quiz_id}`" class="reattempt-btn"> ↪️Reattempt Quiz </router-link>
    <router-link to="/dashboard" class="attempt-btn"> 🏁 Attempt Another Quiz </router-link>
    <button class="download" @click="exporting_id">Download CSV Result</button>
    <h2>Quiz Summary</h2>
    <p><strong>Time Taken:</strong> {{ time_taken }}</p>
    <p><strong>Correct Answers:</strong> {{ correctcount }}</p>
    <p><strong>Incorrect Answers:</strong> {{ incorrect }}</p>
    <p><strong>Total Score:</strong> {{ scored }} / {{ maxscore }}</p>
    <p><strong>Percentage :</strong> {{ percentage}} %</p>
    <p><strong>Accuracy:</strong> {{ accuracy }}%</p>

    <p v-if="accuracy === 100 && percentage>=80" style="color: green; font-weight: bold;">🎉 Perfect Score! You're a genius!</p>
    <p v-else-if="accuracy >= 75 && percentage>=60" style="color: teal;">👏 Great job! Keep practicing!</p>
    <p v-else style="color:red; background-color: white; padding: 10px; width: 300px ; display:contents;border: 1cm; border-color: black; border-radius: 60px;">💡 Review your answers to improve.</p>
  </div>
</div>
</template>

<style scoped>
.review-btn {
  display: inline-block;
  margin: 10px;
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: bold;
  transition: background-color 0.3s;
}

.review-btn:hover {
  background-color: #45a049;
}

.reattempt-btn {
  display: inline-block;
  margin: 10px;
  padding: 10px 20px;
  background-color: #94913d;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: bold;
  transition: background-color 0.3s;
}

.reattempt-btn:hover {
  background-color: #d6d13e;
  color: rgb(255, 255, 255);
}

.attempt-btn {
  display: inline-block;
  margin: 10px;
  padding: 12px 20px;
  background-color: #2196F3;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: bold;
  transition: background-color 0.3s;
}

.attempt-btn:hover {
  background-color: #1976D2;
}

.download {
 display: inline-block;
  margin: 10px;
  padding: 10px 20px;
  background-color: #4b21f3;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: bold;
  transition: background-color 0.3s; 
}

.download:hover {
 background-color: #5d19d2; 
}
</style>
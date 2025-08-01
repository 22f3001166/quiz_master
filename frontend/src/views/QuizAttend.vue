<script>
import axios from 'axios';
export default {
    data(){
        return{
            questions:[],
            currentIndex: 0,
            selected_answer: '',
            userAnswers: {},
            marks: '',
            quizId: this.$route.params.quiz_id,
            quiz: '',
            token: localStorage.getItem('token'),
            errorMessage: '',
            timeLeft: 0,
            timerInterval: null,
            jumpIndex: 1,
            isSubmitted: false,
            attempt_count:0,
            scoreId:'',
            submittedAnswers: {}
        };
    },

    created() {
      this.getQuiz();
      this.checkAttempts();
      this.getQuestions(this.quizId);
    },
    
    computed: {
        currentQuestion() {
            return this.questions[this.currentIndex];
        },
        options() {
            if (!this.currentQuestion) return [];
            return [
            { key: 'A', text: this.currentQuestion.option_a },
            { key: 'B', text: this.currentQuestion.option_b },
            { key: 'C', text: this.currentQuestion.option_c },
            { key: 'D', text: this.currentQuestion.option_d },
            ];
        },
        formattedTime() {
          const min = Math.floor(this.timeLeft / 60);
          const sec = this.timeLeft % 60;
          return `${min}:${sec < 10 ? '0' : ''}${sec}`;
        }
    },
    methods: {
        async checkAttempts() {
              try {
                const res = await axios.get(`http://127.0.0.1:5000/api/score?quiz_id=${this.quizId}`, {
                  headers: { Authorization: `Bearer ${this.token}` }
                });
                console.log(res.data);
                this.isSubmitted = res.data.isSubmitted;
                this.attempt_count = res.data.attempt_count;
                if (this.isSubmitted) this.loadSubmittedAnswers();
              } catch (error) {
                this.errorMessage = 'Failed to check submission status.';
              }
            },
        async getQuiz() {
          try {
            const res = await axios.get(`http://127.0.0.1:5000/api/quiz/${this.quizId}`, {
              headers: { Authorization: `Bearer ${this.token}`}
            });
            console.log(res.data)
            this.quiz= res.data;  // same quiz object gives us two things
            if (!this.isSubmitted) {
              const storedStart = sessionStorage.getItem(`quiz_${this.quizId}_start_time`);
              if (!storedStart) {
                const now = Date.now();
                sessionStorage.setItem(`quiz_${this.quizId}_start_time`, now);
                this.timeLeft = this.quiz.duration * 60;
              } else {
                const now = Date.now();
                const startTime = parseInt(storedStart, 10);
                const elapsedSeconds = Math.floor((now - startTime) / 1000);
                this.timeLeft = this.quiz.duration * 60 - elapsedSeconds;
                if (this.timeLeft <= 0) {
                  this.submitQuiz();
                  return;
                }
              }
              this.timerInterval = setInterval(() => {
                if (this.timeLeft > 0) this.timeLeft--;
                else this.submitQuiz();
              }, 1000);
            }
          } catch (error) {
            this.errorMessage = 'Failed to load Quiz.';
          }
        },
        async getQuestions(id){
            try {
                const res = await axios.get(`http://127.0.0.1:5000/api/question?quiz_id=${id}`, { headers: { Authorization: `Bearer ${this.token}` }});
                console.log(res.data)
                this.questions = res.data.questions;
                }

            catch (error) {
            this.errorMessage = 'Failed to load Quiz.';
                            }
        },

        nextQuestion() { if (this.currentIndex < this.questions.length - 1) this.currentIndex++; },
        prevQuestion() { if (this.currentIndex > 0) this.currentIndex--; },
        clearAnswer() {
          if (!this.isSubmitted) {
            this.userAnswers[this.currentQuestion.id] = null;
          }
        },
        cancelQuiz() { this.$router.push('/dashboard'); },
        async submitQuiz() {
          if (this.isSubmitted) return;
          try {
            sessionStorage.removeItem(`quiz_${this.quizId}_start_time`);
            const timeTaken = this.quiz.duration * 60 - this.timeLeft;
            const submission = {
              quiz_id: this.quizId,
              answers: Object.entries(this.userAnswers).map(([question_id, selected_answer]) => ({
                question_id,
                selected_answer
              })),
              time_taken: timeTaken
            };

            const response = await axios.post(`http://127.0.0.1:5000/api/answer`, submission, {
              headers: { Authorization: `Bearer ${this.token}` }
            });
            clearInterval(this.timerInterval);
            this.isSubmitted = true;
            this.scoreId=response.data.score_id

            if (response.data && response.data.answers) {
              this.submittedAnswers = {};
              response.data.answers.forEach(ans => {
                this.submittedAnswers[ans.question_id] = ans.selected_answer;
              });
            } else {
              this.submittedAnswers = { ...this.userAnswers };
            }
            this.$router.push(`/quiz-summary/${this.scoreId}`);
          } catch (error) {
            this.errorMessage = 'Failed to submit Quiz.';
          }
        },
        jumpToQuestion(index) {
          if (index >= 0 && index < this.questions.length) {
            this.currentIndex = index;
            this.jumpIndex = '';
          }
        },
        async loadSubmittedAnswers() {
          try {
            const res = await axios.get(`http://127.0.0.1:5000/api/answer?quiz_id=${this.quizId}`, {
              headers: { Authorization: `Bearer ${this.token}` }
            });
            if (res.data && res.data.answers && res.data.answers.length > 0) {
              this.submittedAnswers = {};
              res.data.answers.forEach(ans => {
                this.submittedAnswers[ans.question_id] = ans.selected_answer;
              });
              this.userAnswers = { ...this.submittedAnswers };
            }
          } catch (error) {
            this.errorMessage = 'Failed to load submitted answers.';
          }
        },
        resubmitQuiz() {
          sessionStorage.removeItem(`quiz_${this.quizId}_start_time`);
          this.isSubmitted = false;
          this.submittedAnswers = {};
          this.scoreId = '';
          this.timeLeft = this.quiz.duration * 60;
          if (this.timerInterval) clearInterval(this.timerInterval);
          this.timerInterval = setInterval(() => {
            if (this.timeLeft > 0) this.timeLeft--;
            else this.submitQuiz();
          }, 1000);
        }
    },
    beforeUnmount() {
      clearInterval(this.timerInterval);
    }
}

</script>


<template>
  <div style="margin-top: 10px; display: flex; flex-direction: column; align-items: center;">
    <div class="quiz-top-bar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; width: 100%; max-width: 900px;">
          <h2> Quiz Title: {{ quiz.title }} </h2>
          <div class="quiz-actions" style="display: flex; gap: 15px; align-items: center;">
            <span class="analog-timer" v-if="!isSubmitted">⏰ {{ formattedTime }}</span>
            <button v-if="!isSubmitted" @click="submitQuiz" class="submit-btn" :disabled="isSubmitted">Submit Quiz</button>
            <button v-if="!isSubmitted" @click="cancelQuiz" class="cancel-btn">Cancel Quiz</button>
            <button v-if="isSubmitted" @click="resubmitQuiz" class="submit-btn">Reattempt Quiz</button>
          </div>
        </div>

    <div class="question-box-wrapper">
      <h3 style="margin-bottom: 10px;">Question Navigation</h3>
      <div class="question-indicators-top" style="display: flex; flex-wrap: wrap; gap: 6px; padding: 10px; border: 1px solid #ccc; border-radius: 6px; margin-bottom: 20px; justify-content: center; width: 100%; max-width: 900px;">
        <div v-for="(q, index) in questions" :key="index" 
             class="question-indicator" 
             :class="userAnswers[q.id] === undefined ? 'not-visited' : (userAnswers[q.id] ? 'attempted' : 'not-attempted')"
             @click="jumpToQuestion(index)">
          {{ index + 1 }}
        </div>
      </div>
    </div>

        <div v-if="currentQuestion" class="quiz-card">
          <h4 style="line-height: 0.5; font-size: 1rem; margin-right: 90%; margin-bottom: 2%;">Marks: {{ currentQuestion.marks}}</h4>
          <h2 style="line-height: 1.6; font-size: 1.25rem;">Q{{ currentIndex + 1 }}: {{ currentQuestion.Statement }}</h2>
          <div class="options">
            <label v-for="option in options" :key="option.key" class="option-label"
              :class="{
                'correct-option': isSubmitted && option.key === currentQuestion.correct_answer,
                'user-selected': isSubmitted && submittedAnswers[currentQuestion.id] === option.key
              }">
              <input type="radio" :value="option.key" v-model="userAnswers[currentQuestion.id]" :disabled="isSubmitted" />
              {{ option.key }}. {{ option.text }}
              <span v-if="isSubmitted && submittedAnswers[currentQuestion.id] === option.key" style="margin-left: 6px;">✔</span>
            </label>
          </div>
          <div class="question-actions">
            <button @click="prevQuestion" :disabled="currentIndex === 0"> Prev</button>
            <button @click="nextQuestion" :disabled="currentIndex === questions.length - 1">Next</button>
            <button v-if="!isSubmitted" @click="clearAnswer">Clear</button>
          </div>
          <h3 v-if="isSubmitted" style="line-height: 1.6; font-size: 1.25rem; margin-right: 75%; margin-bottom: 2%;">Correct Answer: {{ currentQuestion.answer}}</h3>
        </div>
      </div>
          <div style="flex: 1; width: 100%; max-width: 900px;">
      <div class="question-section" style="display: flex; gap: 20px; flex-direction: column;">
    </div>
    </div>
</template>

<style scoped>

  /* Styles moved inline in template */


.question-indicator {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  color: white;
  font-weight: 600;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  user-select: none;
  transition: background-color 0.3s ease;
  margin: 0;
  font-size: 0.9rem;
  padding: 0;
}

.question-indicator.attempted {
  background-color: #28a745; /* green */
}

.question-indicator.not-attempted {
  background-color: #dc3545; /* red */
}

.question-indicator.not-visited {
  background-color: #6c757d; /* grey */
}

.question-indicator:hover {
  opacity: 0.8;
}

.quiz-card {
  background: #fff;
  padding: 20px 25px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  border-radius: 8px;
  width: 100%;
  max-width: 900px;
  margin-bottom: 20px;
}

.option-label {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 20px;
  cursor: pointer;
  user-select: none;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.option-label input[type="radio"] {
  cursor: pointer;
}

.option-label:hover {
  background-color: #f0f8ff;
}

.option-label.correct-option {
  background-color: #d4edda;
  border-color: #28a745;
  color: #155724;
}

.option-label.user-selected {
  background-color: #fff3cd;
  border-color: #ffeeba;
  color: #856404;
}

.quiz-actions button, .question-actions button {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
  user-select: none;
}

.submit-btn {
  background-color: #28a745;
  color: white;
}

.submit-btn:hover {
  background-color: #218838;
}

.cancel-btn {
  background-color: #dc3545;
  color: white;
}

.cancel-btn:hover {
  background-color: #c82333;
}

.question-actions button {
  background-color: #007bff;
  color: white;
  margin-right: 8px;
  min-width: 40px;
  font-size: 1.25rem;
  padding: 6px 12px;
}

.question-actions button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.question-actions button:hover:not(:disabled) {
  background-color: #0056b3;
}

.analog-timer {
  font-family: 'Georgia', serif;
  font-weight: 700;
  font-size: 1.5rem;
  background: linear-gradient(135deg, #6b8ce3, #3a5bbf);
  color: white;
  padding: 6px 14px;
  border-radius: 25px;
  box-shadow: 0 2px 8px rgba(58, 91, 191, 0.6);
  user-select: none;
}

.question-box-wrapper {
  width: 100%;
  max-width: 900px;
  background-color: #f9f9f9;
  padding: 15px;
  border: 2px solid #ccc;
  border-radius: 8px;
  margin-bottom: 20px;
  text-align: center;
}

.question-indicators-top {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}
</style>

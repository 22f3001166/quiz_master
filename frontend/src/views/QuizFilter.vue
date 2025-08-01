<script>
import NavBar from "@/components/NavBar.vue";
import axios from "axios";
export default {
  name: "UserDashboardQuizzes",
  components: {
    NavBar,
  },
  data() {
    return {
      user: '',
      token:localStorage.getItem("token"),
      quizzes: [],
      subjects: [],
      chapters: [],
      scores:[],
      selectedSubject: '',
      selectedChapter: '',
      attemptFilter: '',
      searchQuery: '',
      page: 1,
      perPage: 3,
      errorMessage:''
    };
  },
  computed: {

    filteredChapters() {
    if (!this.selectedSubject) return this.chapters;
    return this.chapters.filter(ch => ch.subject_id == this.selectedSubject);
    },
    filteredSubjects() {
    if (!this.selectedChapter) return this.subjects;
    const chapter = this.chapters.find(ch => ch.id == this.selectedChapter);
    return chapter ? this.subjects.filter(s => s.id == chapter.subject_id) : [];
    },

    filteredQuizzes() {
      return this.quizzes.filter(quiz => {
        const subjectMatch = !this.selectedSubject || quiz.subject_id == this.selectedSubject;
        const chapterMatch = !this.selectedChapter || quiz.chapter_id == this.selectedChapter;
        const userAttempts = this.user && this.user.id ? this.scores.filter(score => score.quiz_id === quiz.id && score.user_id === this.user.id).length : 0;
        const attemptMatch = this.attemptFilter === 'attempted' ? userAttempts > 0 :
                            this.attemptFilter === 'not_attempted' ? userAttempts === 0 : true;

        const searchLower = this.searchQuery.toLowerCase();
        const searchMatch = quiz.title.toLowerCase().includes(searchLower) ||
                            quiz.description.toLowerCase().includes(searchLower) ||
                            String(userAttempts).includes(searchLower);

        return subjectMatch && chapterMatch && attemptMatch && searchMatch;
      });
    },
    paginatedQuizzes() {
      const start = (this.page - 1) * this.perPage;
      return this.filteredQuizzes.slice(start, start + this.perPage);
    },
    totalPages() {
      return Math.ceil(this.filteredQuizzes.length / this.perPage);
    },
    quizAttempts() {
      return (quizId) => {
        return this.scores.filter(score => score.quiz_id === quizId && score.user_id === this.user.id).length;
      }
    },
    totalScore() {
      return (quiz) => {
        return quiz.questions.reduce((sum, q) => sum + (q.marks || 0), 0);
      };
    }
  },
  methods: {
    reviewPreviousAttempt(quizId) {
      const lastattempt = this.scores.filter(score => score.quiz_id === quizId && score.user_id === this.user.id).length; 
      const matchedScore = this.scores.find(
        score => score.quiz_id === quizId &&
                 score.user_id === this.user.id &&
                 score.user_attempts === lastattempt
      );
      if (matchedScore) {
        this.$router.push(`/quiz-summary/${matchedScore.id}`);
      } else {
        console.warn("No matching score found.");
      }
    },
    handleSearch(search){
      this.searchQuery = search
    },
    startQuiz(quizId) {
      this.$router.push(`/quiz-attempt/${quizId}`);
    },
    prevPage() {
      if (this.page > 1) this.page--;
    },
    nextPage() {
      if (this.page < this.totalPages) this.page++;
    },
    async fetchUser() {
        try{
        const response = await axios.get(`http://127.0.0.1:5000/api/user`, {
            headers: { Authorization: `Bearer ${this.token}` }
            });
        this.user = response.data;
        }
        catch(error){
                if (error.response && error.response.data && error.response.data.message) {
                      this.errorMessage = error.response.data.message;
                    } else {
                      this.errorMessage = 'An error occurred while fetching the Quiz.';
                    }
            }  
    },

    async fetchQuizes() {
      try {
        const res = await axios.get(`http://127.0.0.1:5000/api/quiz`, {
          headers: { Authorization: `Bearer ${this.token}` }
        });
        console.log(res.data);
        this.quizzes = res.data.quizzes;
      } 
      catch(error){
                if (error.response && error.response.data && error.response.data.message) {
                      this.errorMessage = error.response.data.message;
                    } else {
                      this.errorMessage = 'An error occurred while fetching the Quizes.';
                    }
            }  
    },
    async fetchChapters() {
        try{
        const res = await axios.get(`http://127.0.0.1:5000/api/chapter`, {
            headers: { Authorization: `Bearer ${this.token}` }
            });
        console.log(res.data)
        this.chapters=res.data.chapters
        }

        catch(error){
                if (error.response && error.response.data && error.response.data.message) {
                      this.errorMessage = error.response.data.message;
                    } else {
                      this.errorMessage = 'An error occurred while fetching the chapters.';
                    }
            }  
    },
    async fetchSubjects() {
        try{
        const res = await axios.get(`http://127.0.0.1:5000/api/subject`, {
            headers: { Authorization: `Bearer ${this.token}` }
            });
        console.log(res.data)
        this.subjects=res.data.subjects
        }
        catch(error){
                if (error.response && error.response.data && error.response.data.message) {
                      this.errorMessage = error.response.data.message;
                    } else {
                      this.errorMessage = 'An error occurred while fetching the Subjects.';
                    }
            } 
    },
     async fetchScores() {
        try{
        const res = await axios.get(`http://127.0.0.1:5000/api/score`, {
            headers: { Authorization: `Bearer ${this.token}` }
            });
        console.log(res.data)
        this.scores=res.data.scores;
        }

        catch(error){
                if (error.response && error.response.data && error.response.data.message) {
                      this.errorMessage = error.response.data.message;
                    } else {
                      this.errorMessage = 'An error occurred while fetching the Scores.';
                    }
            }  
    },
    toggleSidebar() {
      this.showSidebar = !this.showSidebar;
    }
  },
  async created(){
    this.fetchUser();
  },
  mounted() {
        this.fetchQuizes();
        this.fetchChapters();
        this.fetchSubjects();
        this.fetchScores();
  },
  watch: {
  selectedSubject(newVal) {
    if (this.selectedChapter) {
      const chapter = this.chapters.find(ch => ch.id == this.selectedChapter);
      if (!chapter || chapter.subject_id != newVal) {
        this.selectedChapter = '';
      }
    }
  }
}
  
};
</script>


<template>
  <div >
    <div class="navbar">
      <NavBar @search="handleSearch"/>
    </div>
    
    <div class="dashboard-container">
      <aside class="sidebar">
        <h2 class="quiz-heading">Quizes Available: {{this.filteredQuizzes.length}}</h2>
          <h3>Filters</h3>

          <label>Filter by Subject:
            <select v-model="selectedSubject">
              <option value="">All</option>
              <option v-for="subject in filteredSubjects" :key="subject.id" :value="subject.id">
                {{ subject.name }}
              </option>
            </select>
          </label>

          <label>Filter by Chapter:
            <select v-model="selectedChapter">
              <option value="">All</option>
              <option v-for="chapter in filteredChapters" :key="chapter.id" :value="chapter.id">
                {{ chapter.name.slice(0, 10) }}
              </option>
            </select>
          </label>

          <label>Attempt Status:
            <select v-model="attemptFilter">
              <option value="">All</option>
              <option value="attempted">Attempted</option>
              <option value="not_attempted">Not Attempted</option>
            </select>
          </label>
          
      </aside>
      
      <main class="quiz-grid">
        <div class="quiz-card" v-for="quiz in paginatedQuizzes" :key="quiz.id">
          <h2>{{ quiz.title }}</h2>
          <p class="description">{{ quiz.description }}</p>
          <p>Duration: {{ quiz.duration }} min</p>
          <p>Attempts: {{ quizAttempts(quiz.id) }}</p>
          <p>Remarks: {{ quiz.remarks }}</p>
          <p>Questions: {{ quiz.questions.length }}</p>
          <p>Total Marks: {{ totalScore(quiz) }}</p>
          <div class="quiz-card-buttons" v-if="true">
            <button
              class="quiz-attempt-btn"
              @click="startQuiz(quiz.id)"
            >
              Attempt Quiz
            </button>
            <button
              v-if="quizAttempts(quiz.id) > 0"
              class="quiz-prev-btn"
              @click="reviewPreviousAttempt(quiz.id)"
            >
              Previous Attempt
            </button>
          </div>
        </div>
      </main>
    </div>
    <footer class="footer-nav">
      <button @click="prevPage" :disabled="page === 1">Previous</button>
      <span>Page {{ page }} of {{ totalPages }}</span>
      <button @click="nextPage" :disabled="page >= totalPages">Next</button>
    </footer>
  </div>
</template>

<style scoped>
.dashboard-container {
  display: flex;
  padding: 20px;
  gap: 30px;
  margin-top: 75px;
}
.sidebar {
  width: 200px;
  max-width: 40%;
  padding: 16px;
  box-shadow: 2px 0 8px rgba(0,0,0,0.1);
  background-color: #f0fafed6;
  color: #333;
  border-radius: 8px;
}
.sidebar select {
  text-overflow:initial;
  white-space:inherit;
  overflow:scroll;
  width: 100%;
}

.sidebar input[type="text"] {
  width: 100%;
  padding: 6px;
  margin-bottom: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.sidebar input[type="radio"] {
  margin-right: 5px;
}
.quiz-heading {
  margin-left: 20px;
  font-size: 1rem;
  color: #001037;
  font-weight: bold;
  margin-bottom: 10px;
}
.quiz-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  margin-top: 50px;
  margin-bottom: 3%;
  flex: 1;
}

/* --- QUIZ CARD REVISED STYLES --- */
.quiz-card {
  border: none;
  padding: 20px 24px;
  border-radius: 12px;
  background-color: #a6bcc6e6;
  border-color: #091638;
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
  text-align: left;
}
.quiz-card h2 {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 8px;
}
.quiz-card .description {
  font-style: italic;
  color: #3b3a3a;
  margin-bottom: 5%;
}
.quiz-card p {
  margin-bottom: 6px;
}

.quiz-card-buttons {
  display: flex;
  gap: 14px;
  margin-top: 16px;
}

.quiz-card button {
  flex: 1 1 0px;
  min-width: 0;
  height: 45px;
  font-size: 1rem;
  border-radius: 16px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.2s, color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0px 10px;
}

.quiz-attempt-btn {
  background-color: #2e5fa1;
  color: #fff;
  border: 2px solid #20406d;
}
.quiz-attempt-btn:hover {
  background-color: #20406d;
  color: #e6f0fa;
}

.quiz-prev-btn {
  background-color: #eeeeee;
  color: #212143;
  border: 2px solid #0505d2;
}
.quiz-prev-btn:hover {
  background-color: #e5e1f9;
  color: #22224d;
}

.quiz-pagination {
  display:flow-root;
  justify-content: center;
  gap: 2%;
  margin-top: 40px;
}

.quiz-pagination button {
  padding: 6px 12px;
  border: none;
  background-color: #3a83d7;
  color: rgb(255, 255, 255);
  border-radius: 20px;
  cursor: pointer;
  font-weight: bold;
}

.quiz-pagination button:disabled {
  padding: 6px 12px;
  background-color: #ccc;
  cursor: not-allowed;
}

body {
  background-color: #f0f4f8;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

@media (max-width: 768px) {
  .dashboard-container {
    flex-direction: column;
  }

  .sidebar {
    width: 80%;
    position: static;
    box-shadow: none;
    border-right: none;
  }

  .quiz-grid {
    grid-template-columns: 1fr;
  }
}

.footer-nav {
  position: static;
  top:40;
  width: 95%;
  margin-left: 20px;
  color: #ffffff;
  background-color: #35424fc1;
  padding: 20px;
  display:flex;
  justify-content: center;
  gap: 30px;
  border-top: 2px solid #2e2e2e;
}

.footer-nav button{
  padding: 12px 16px;
  border-radius: 15px;
  background-color: #4CAF50;
  color: white;
  font-weight: bold;
  border: none;
  cursor: pointer;
  transition: background 0.3s;
}

.footer-nav span{
  padding: 8px 12px;
  color: white;
  font-size: 20px;
  font-weight: bold;
}
.footer-nav button:hover{
  background-color: #54db5ad2;
  color: #000;
}
</style>
<script>
// import { AddQuizes } from '@/api';
import NavBar from '@/components/NavBar.vue';
import axios from 'axios';
export default {
    data(){
        return{
            quizzes:[],
            title: '',
            description: '',
            duration: 0,
            remarks: '',
            quizId: null,
            subjectId: null,
            chapterId: this.$route.params.chapter_id,
            chapter: '',
            isPosting: false,
            isEditing: false,
            errorMessage: '',
            searchText:''
        };
    },

    created() {
      this.getChapter();
      this.fetchQuizes(this.chapterId);
    },
    components: {
      NavBar
    },
    computed:{
      filterQuiz() {
          if (!this.searchText) return this.quizzes;

          const query = this.searchText.toLowerCase();

          return this.quizzes.filter(quiz => {
            return (
              quiz.title.toLowerCase().includes(query) ||
              quiz.description.toLowerCase().includes(query) ||
              quiz.remarks.toLowerCase().includes(query) ||
              quiz.duration.toString().includes(query) ||
              quiz.created_on.toString().includes(query) ||
              quiz.questions.length.toString().includes(this.searchText)
            );
          });
        }
      },

    methods: {
      handleSearch(searchQuery){
        this.searchText = searchQuery;
      },
    async getChapter() {
          const token = localStorage.getItem('token');
          try {
            const res = await axios.get(`http://127.0.0.1:5000/api/chapter/${this.chapterId}`, {
              headers: { Authorization: `Bearer ${token}`}
            });
            console.log(res.data)
            this.chapter= res.data;  
            this.subjectId = res.data.subject_id; // chapter object is enough for getting subject id too
          } catch (error) {
            this.errorMessage = 'Failed to load subject id.';
          }
        },
    cancelPosting() {
      this.isPosting = false;
      this.title = '';
      this.description = '';
    },

    cancelEdit() {
      this.isEditing = false;
      this.title = '';
      this.description = '';
    },

    editQuiz(quiz) {
      this.quizId = quiz.id;
      this.title = quiz.title;
      this.description = quiz.description;
      this.duration = quiz.duration;
      this.remarks = quiz.remarks;
      this.isEditing = true;
    },

    async fetchQuizes(id) {
        const token = localStorage.getItem('token');
        try{
        const res = await axios.get(`http://127.0.0.1:5000/api/quiz?chapter_id=${id}`, {
            headers: { Authorization: `Bearer ${token}` }
            });
        console.log(res.data)
        this.quizzes = res.data.quizzes;
        }

        catch(error){
                if (error.response && error.response.data && error.response.data.error) {
                      this.errorMessage = error.response.data.error;
                    } else {
                      this.errorMessage = 'An error occurred while fetching the Quiz.';
                    }
            }  
    },
    

    async AddQuizes(){ 
            const data = {title: this.title, description: this.description, duration: parseInt(this.duration), 
                          remarks: this.remarks, chapter_id: this.chapterId, subject_id: this.subjectId};
            const token = localStorage.getItem('token');
            try{
                const response = await axios.post("http://127.0.0.1:5000/api/quiz",data, {
                headers: {
                  Authorization: `Bearer ${token}`}}); 

            console.log(response.data.message);
            this.fetchQuizes(this.chapterId);
            this.isPosting = false;
            this.title = '';
            this.description = '';
            this.remarks= '';
            this.duration = '';
            }
            catch(error){
                if (error.response && error.response.data && error.response.data.error) {
                      this.errorMessage = error.response.data.error;
                    } else {
                      this.errorMessage = 'An error occurred while adding the Quiz.';
                    }
            } 

        },
      async UpdateQuiz(){
            this.errorMessage = ''; // clear previous error
            const token = localStorage.getItem('token');
            try{ 
                const response = await axios.put(`http://127.0.0.1:5000/api/quiz/${this.quizId}`,
              {title: this.title, description: this.description, duration: parseInt(this.duration), remarks: this.remarks},
              {headers: { Authorization: `Bearer ${token}` } } ); 

              console.log(response.data);
              this.fetchQuizes(this.chapterId);
              this.title = '';
              this.description = '';
              this.duration = '';
              this.remarks = '' ;
              this.isEditing = false;
              }
              catch(error){
                  if (error.response && error.response.data && error.response.data.error) {
                      this.errorMessage = error.response.data.error;
                    } else {
                      this.errorMessage = 'An error occurred while updating the Quiz.';
                    }
              } 
        },
      async RemoveQuiz(quiz){
            this.errorMessage = ''; // clear previous error
            const token = localStorage.getItem('token');
            this.quizId = quiz.id;
          try{ 
              const response = await axios.delete(`http://127.0.0.1:5000/api/quiz/${this.quizId}`,
             {headers: { Authorization: `Bearer ${token}` }}); 
            console.log(response.data);
            this.fetchQuizes(this.chapterId);
            this.quizId = null;
            }
            catch(error){
                if (error.response && error.response.data && error.response.data.error) {
                    this.errorMessage = error.response.data.error;
                  } else {
                    this.errorMessage = 'An error occurred while delete the subject. It may be already in the database';
                  }
            } 
         },

    }
}

</script>

<template>
<NavBar @search="handleSearch"/>
<div class="quiz-list">
  <div class="chapter-header">
    <div v-if="chapter">
      <h2>Quizzes in "{{ chapter.name }} Chapter"</h2>
    </div>
    <div v-else>
      <h2>Loading chapters...</h2>
    </div>

    <div class="quiz-actions">
      <router-link :to="`/subject`"><button class="subject-btn">Choose Other Subject</button></router-link>
      <router-link :to="`/subject/${subjectId}/chapter`"><button class="subject-btn">Choose Other Chapter</button></router-link>
      <button @click="isPosting = true" class="add-btn">Add Quiz ✚</button>
    </div>
  </div>

  <div v-if="isPosting">
    <div class="overlay"></div>
    <div class="modal-form">
      <h3>Add New Quiz</h3>
      <div class="form-input">
        <input v-model="title" placeholder="Enter quiz title" />
      </div>
      <div class="form-input">
        <input v-model="description" placeholder="Enter quiz description" />
      </div>
      <div class="form-input">
        <input v-model="duration" placeholder="Enter quiz duration (in minutes)" type="number" />
      </div>
      <div class="form-input">
        <input v-model="remarks" placeholder="Enter any remarks" />
      </div>
      <button @click="AddQuizes">Save</button>
      <button @click="isPosting = false">Cancel</button>
    </div>
  </div>

  <div v-if="isEditing">
  <div class="overlay"></div>
    <div class="modal-form">
      <h3>Edit Quiz</h3>

      <div class="form-input">
        <input v-model="title" placeholder="Edit chapter name" />
      </div>
      <div class="form-input">
        <input v-model="description" placeholder="Edit chapter description" />
      </div>
      <div class="form-input">
        <input v-model="duration" placeholder="Edit quiz duration (in minutes)" type="number" />
      </div>
      <div class="form-input">
        <input v-model="remarks" placeholder="Edit remarks" />
      </div>

      <button @click="UpdateQuiz">Update</button>
      <button @click="cancelEdit">Cancel</button>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </div>
  </div>

  <h2 >Quizes </h2>
  <div class="quiz-card-container">
      <div class="quiz-grid" v-for="quiz in filterQuiz" :key="quiz.id" >
          <h2>Title: {{ quiz.title }}</h2>
          <p>Description: {{ quiz.description }}</p>
          <p>Time Duration: {{ quiz.duration }}</p>
          <p>Quiz Remarks: {{ quiz.remarks }}</p>
          <p> Created on: {{ quiz.created_on }}</p>
          <p> Number of Questions: {{ quiz.questions.length }}</p>

          <router-link :to="`/quiz-manage/${quiz.id}`"><button> Manage Quiz Questions 🚀</button></router-link>
          <!-- <router-link v-id="userRole=='student'" :to="`/dashboard/quiz-attend/${quiz.id}`"><button> Attempt Quiz 🚀</button></router-link> -->
          <button  @click="editQuiz(quiz)" >Edit ✍️</button>
          <button  @click="RemoveQuiz(quiz)" >Delete 🗑️</button>
      </div>
  </div>
    <p v-if="quizzes.length === 0">No quizzes available for this chapter.</p>
  
</div>

</template>


<style scoped>
.quiz-list {
  color: black;
  margin-top: 75px;

}

.chapter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.chapter-header h2 {
  font-size: 24px;
  color: #ffffff;
}

.quiz-actions {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.quiz-card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  margin-top: 20px;
}

.quiz-grid {
  flex: 1 1 300px;
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.08);
  max-width: 300px;
  text-align: left;
  transition: transform 0.2s ease;
}

.quiz-grid:hover {
  transform: scale(1.03);
}

.quiz-grid h2 {
  font-size: 18px;
  margin-bottom: 8px;
}

.quiz-grid p {
  font-size: 14px;
  margin-bottom: 6px;
  color: #444;
}

.quiz-grid button {
  margin-right: 8px;
  margin-top: 10px;
  padding: 8px 14px;
  background-color: #284b63;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.quiz-grid button:hover {
  background-color: #4e8db3;
  color: #fff;
  transform: scale(1.05);
}

.quiz-card {
  background: #ffffff;
  padding: 10px;
  width: 300px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  text-align: left;
  text-decoration: none;
  color: inherit;
  border-radius: 8px;
  transition: transform 0.1s;
}

.quiz-card:hover {
  transform: scale(1.1);
  cursor: pointer;
}

.quiz-card h2 {
  margin: 0 0 10px;
  color: #333;
}

.quiz-card p {
  font-size: 14px;
  color: #555;
}
.quiz-card button {
  margin-top: 50px;
  padding: 10px 16px;
  background-color:#004e7b;
  color: rgb(255, 247, 247);
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.quiz-card button:hover {
  background-color: #1698e3;
  color: #0b0110;
  transform: scale(1.07);
}


.subject-btn {
  padding: 10px 14px;
  background-color: #3d5a80;
  color: white;
  border-radius: 20px;
  border: none;
  cursor: pointer;
}

.subject-btn:hover {
  background-color: #5ea4c3;
  color: white;
}

.add-btn {
  padding: 10px 14px;
  background-color: #8338ec;
  color: white;
  border-radius: 6px;
  border: none;
  cursor: pointer;
}

.add-btn:hover {
  background-color: #b08dfd;
  color: white;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(5px);
  z-index: 100;
}

.modal-form {
  position: fixed;
  top: 50%;
  left: 50%;
  width: 400px;
  transform: translate(-50%, -50%);
  background: #fff;
  padding: 30px;
  border-radius: 12px;
  z-index: 101;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.modal-form h3 {
  margin-bottom: 20px;
  font-size: 24px;
  color: #2c3e50;
}

.form-input {
  width: 100%;
  margin-bottom: 15px;
}

.form-input input {
  width: 100%;
  padding: 10px;
  font-size: 14px;
  border-radius: 6px;
  border: 1px solid #ccc;
  color: #333;
}

.form-input input::placeholder {
  color: #000000;
  font-style: italic;
}

.modal-form button {
  margin-right: 10px;
  padding: 10px 16px;
  font-size: 14px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.modal-form button:first-of-type {
  background-color: #1d3557;
  color: white;
}

.modal-form button:last-of-type {
  background-color: #adb5bd;
  color: white;
}
</style>

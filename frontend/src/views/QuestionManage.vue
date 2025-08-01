<script>
import NavBar from '@/components/NavBar.vue';
import axios from 'axios';
export default {
    data(){
        return{
            questions:[],
            Statement: '',
            option_a: '',
            option_b: '',
            option_c: '',
            option_d: '',
            correct_ans: '',
            marks: '',
            questionId: null, // for editing purposes
            quizId: this.$route.params.quiz_id,
            subjectId: null,
            chapterId: null,
            quiz: '',
            isPosting: false,
            isEditing: false,
            searchText:'',
            errorMessage: ''
        };
    },
    components:{
      NavBar
    },
    computed:{
      filterQues() {
          if (!this.searchText) return this.questions;

          const query = this.searchText.toLowerCase();

          return this.questions.filter(ques => {
            return (
              ques.Statement.toLowerCase().includes(query) ||
              ques.option_a.toLowerCase().includes(query) ||
              ques.option_b.toLowerCase().includes(query) ||
              ques.option_c.toLowerCase().includes(query) ||
              ques.option_d.toLowerCase().includes(query) ||
              ques.answer.toLowerCase().includes(query) ||
              ques.marks.toString().includes(this.searchText)
            );
          });
        }
    },
    created() {
      this.getQuiz();
      this.fetchQuestions(this.quizId);
    },

    methods: {
      handleSearch(query){
        this.searchText = query;
      },
    async getQuiz() {
          const token = localStorage.getItem('token');
          try {
            const res = await axios.get(`http://127.0.0.1:5000/api/quiz/${this.quizId}`, {
              headers: { Authorization: `Bearer ${token}`}
            });
            console.log(res.data)
            this.quiz= res.data;  // same quiz object gives us two things
            this.subjectId = res.data.subject ; // quiz object has subject_id that return in subject in json format
            this.chapterId = res.data.chapter ;  // quiz object has chapter_id that return in subject in json format
          } catch (error) {
            this.errorMessage = 'Failed to load quiz id.';
          }
        },

     async fetchQuestions(id) {
        const token = localStorage.getItem('token');
        const res = await axios.get(`http://127.0.0.1:5000/api/question?quiz_id=${id}`, {
            headers: { Authorization: `Bearer ${token}` }
            });
        console.log(res.data)
        this.questions = res.data.questions;
    },
    async AddQuestions(){ 
            const data = {Statement:this.Statement , option_a: this.option_a , option_b: this.option_b, option_c: this.option_c , option_d: this.option_d, 
                            answer: this.correct_ans, marks: this.marks, subject_id: this.subjectId, quiz_id: this.quizId};
            const token = localStorage.getItem('token');

            try{
                const response = await axios.post("http://127.0.0.1:5000/api/question",data, {
                headers: {
                  Authorization: `Bearer ${token}`}}); 
            console.log(response.data.message);
            this.fetchQuestions(this.quizId);
            this.isPosting = false;
            this.Statement = '';
            this.option_a = '';
            this.option_b = '';
            this.option_c = '';
            this.option_d = '';
            this.correct_ans = '';
            this.marks = '' 

            }
            catch(error){
                console.error(error);
            } 

        },

    cancelPosting() {
        this.isPosting = false;
        this.Statement = '';
        this.option_a = '';
        this.option_b = '';
        this.option_c = '';
        this.option_d = '';
        this.correct_ans = '';
        this.marks = '' 
    },
       
      async UpdateQuestion(){
            this.errorMessage = ''; // clear previous error
            const token = localStorage.getItem('token');
            const data = {Statement:this.Statement , option_a: this.option_a , option_b: this.option_b, option_c: this.option_c , option_d: this.option_d, 
                            answer: this.correct_ans, marks: this.marks}; 
            try{ 
                const response = await axios.put(`http://127.0.0.1:5000/api/question/${this.questionId}`,data,
              {headers: { Authorization: `Bearer ${token}` } } ); 

                console.log(response.data.message);
                this.Statement = '';
                this.option_a = '';
                this.option_b = '';
                this.option_c = '';
                this.option_d = '';
                this.correct_ans = '';
                this.marks = '' 
                this.isEditing = false;
                this.questionId = null;
                this.fetchQuestions(this.quizId);
              }
              catch(error){
                  if (error.response && error.response.data && error.response.data.error) {
                      this.errorMessage = error.response.data.error;
                    } else {
                      this.errorMessage = 'An error occurred while updating the questions';
                    }
              } 
        },

        cancelEdit() {
            this.isEditing = false;
            this.questionId = null;
            this.Statement = '';
            this.option_a = '';
            this.option_b = '';
            this.option_c = '';
            this.option_d = '';
            this.correct_ans = '';
            this.marks = '' 
        },

        editQuestion(ques) {
            this.questionId = ques.id
            this.Statement = ques.Statement;
            this.option_a = ques.option_a;
            this.option_b = ques.option_b;
            this.option_c = ques.option_c;
            this.option_d = ques.option_d;
            this.correct_ans = ques.answer;
            this.marks = ques.marks ;
            this.isEditing = true;
        },

      async RemoveQuestion(question){
            this.errorMessage = ''; // clear previous error
            const token = localStorage.getItem('token');
            this.questionId = question.id;
          try{ 
              const response = await axios.delete(`http://127.0.0.1:5000/api/question/${this.questionId}`,
             {headers: { Authorization: `Bearer ${token}` }}); 

            console.log(response.data.message);
            this.fetchQuestions(this.quizId);
            this.questionId = null;
            }
            catch(error){
                if (error.response && error.response.data && error.response.data.error) {
                    this.errorMessage = error.response.data.error;
                  } else {
                    this.errorMessage = 'An error occurred while delete the subject';
                  }
            } 
         },

    }
}

</script>

<template>
  <NavBar @search="handleSearch"/>
  <div class="question-section">
    <div class="quiz-header">
      <h2>Managing Questions in "{{ quiz.title }}" Quiz</h2>
      <div class="quiz-actions">
      <router-link :to="`/subject`"><button class="subject-btn">Choose Other Subject</button></router-link>
      <router-link :to="`/subject/${subjectId}/chapter`"><button class="chapter-btn">Choose Other Chapter</button></router-link>
      <router-link :to="`/chapter/${chapterId}/quiz`"><button class="quiz-btn">Choose Other Quiz</button></router-link>
      <button @click="isPosting = true" class="add-btn">Add Question ✚</button>
      <router-link :to="`/quiz-attempt/${quizId}`"><button  class="preview-btn"> 👀 Preview Quiz </button></router-link>
      </div>

    
    </div>
    <table class="question-table">
      <thead>
        <tr>
          <th>#</th>
          <th>Statement</th>
          <th>Options</th>
          <th>Correct Answer</th>
          <th>Marks</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(q, index) in filterQues" :key="q.id">
          <td>{{ index + 1 }}</td>
          <td>{{ q.Statement }}</td>
          <td>
            A. {{ q.option_a }}<br />
            B. {{ q.option_b }}<br />
            C. {{ q.option_c }}<br />
            D. {{ q.option_d }}
          </td>
          <td>{{ q.answer }}</td>
          <td>{{ q.marks }}</td>
          <td>
            <button class="edit-btn" @click="editQuestion(q)">Edit</button>
            <button class="delete-btn" @click="RemoveQuestion(q)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>


  <div v-if="isPosting">
    <div class="overlay"></div>
    <div class="modal-form">
      <h3>Add New Question</h3>
      <div class="form-input">
        <input v-model="Statement" placeholder="Enter question statement" />
      </div>
      <div class="form-input">
        <input v-model="option_a" placeholder="Option A" />
      </div>
      <div class="form-input">
        <input v-model="option_b" placeholder="Option B" />
      </div>
      <div class="form-input">
        <input v-model="option_c" placeholder="Option C" />
      </div>
      <div class="form-input">
        <input v-model="option_d" placeholder="Option D" />
      </div>
       <div class="form-input">
        <label>Correct Answer</label>
          <select v-model="correct_ans">
            <option disabled value="">Select Correct Answer</option>
            <option value="A">A</option>
            <option value="B">B</option>
            <option value="C">C</option>
            <option value="D">D</option>
          </select>
      </div>

      
      <div class="form-input">
        <input v-model="marks" placeholder="Marks" type="number" />
      </div>
      <button @click="AddQuestions">Save</button>
      <button @click="cancelPosting">Cancel</button>
    </div>
  </div>

  <div v-if="isEditing">
    <div class="overlay"></div>
    <div class="modal-form">
      <h3>Edit Question</h3>
      <div class="form-input">
        <input v-model="Statement" placeholder="Enter question statement" />
      </div>
      <div class="form-input">
        <input v-model="option_a" placeholder="Option A" />
      </div>
      <div class="form-input">
        <input v-model="option_b" placeholder="Option B" />
      </div>
      <div class="form-input">
        <input v-model="option_c" placeholder="Option C" />
      </div>
      <div class="form-input">
        <input v-model="option_d" placeholder="Option D" />
      </div>

       <div class="form-input">
        <input v-model="marks" placeholder="Marks" type="number" />
      </div>
       <div class="form-input">
          <label>Correct Answer</label>
          <select v-model="correct_ans" placeholder="Correct Answer (A/B/C/D)" >
            <option disabled value="">Select Correct Answer</option>
            <option value="A">A</option>
            <option value="B">B</option>
            <option value="C">C</option>
            <option value="D">D</option>
          </select>
        </div>
     
      <button @click="UpdateQuestion">Save</button>
      <button @click="cancelEdit">Cancel</button>
    </div>
  </div>

</template>


<style scoped>
.question-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  margin-top: 40px;
}

.question-section h2 {
  font-size: 22px;
  color: #2c3e50;
  margin-bottom: 20px;
}

.quiz-actions {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  gap: 10px;
}

.quiz-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  margin-top: 40px;
  flex-wrap: wrap;
}

.quiz-header h2 {
  font-size: 20px;
  color: #000000;
}

.question-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
  color: #000;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-radius: 8px;
  overflow: hidden;
}

.question-table th,
.question-table td {
  border: 1px solid #ddd;
  padding: 12px 14px;
  text-align: left;
  font-size: 14px;
}

.question-table th {
  background-color: #284b63;
  color: white;
  font-weight: 600;
}

.question-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.edit-btn,
.delete-btn {
  padding: 6px 10px;
  margin-right: 6px;
  font-size: 13px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.edit-btn {
  background-color: #ffc107;
  color: #000;
}

.delete-btn {
  background-color: #dc3545;
  color: #fff;
}

.edit-btn:hover {
  background-color: #e0a800;
}

.delete-btn:hover {
  background-color: #c82333;
}


.subject-btn {
  padding: 10px 14px;
  background-color: #2636ab;
  color: white;
  border-radius: 20px;
  border: none;
  cursor: pointer;
}

.subject-btn:hover {
  background-color: #5ea4c3;
  color: white;
}

.chapter-btn {
  padding: 10px 14px;
  background-color: #bc7f29;
  color: white;
  border-radius: 20px;
  border: none;
  cursor: pointer;
}

.chapter-btn:hover {
  background-color: #5ea4c3;
  color: white;
}

.quiz-btn {
  padding: 10px 14px;
  background-color: #42a54f;
  color: white;
  border-radius: 20px;
  border: none;
  cursor: pointer;
}

.quiz-btn:hover {
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

.preview-btn {
  padding: 10px 14px;
  background-color: #4b0009;
  color: rgb(213, 213, 213);
  border-radius: 60px;
  border:#ffffff;
  cursor: pointer;
  margin-left: 50px;
}

.preview-btn:hover {
  background-color: #871140;
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

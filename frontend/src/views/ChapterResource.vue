<script>
import NavBar from '@/components/NavBar.vue';
import axios from 'axios';
export default {
    data(){
        return{
            chapters:[],
            name: '',
            description: '',
            subject: '',
            chapterId: null,  // store ID of subject being edited
            subjectId: Number(this.$route.params.subject_id),
            isPosting: false,
            isEditing: false,
            errorMessage: '',
            searchText:''
        };
    },
    components:{
      NavBar
    },
    
    created() {
    this.getSubject();
    this.getChapters(this.subjectId);
    },
    computed:{
      filterChapters(){
        return this.chapters.filter(chap=>{
          const card = chap.name.toLowerCase().includes(this.searchText.toLowerCase()) || 
          chap.description.toLowerCase().includes(this.searchText.toLowerCase()) ;
          return card
        });
        }
    },

    methods: {
      handleSearch(searchQuery){
        this.searchText = searchQuery;
      },
      
    async getChapters(subject_id) {
        const token = localStorage.getItem('token');
        try{
        const res = await axios.get(`http://127.0.0.1:5000/api/chapter?subject_id=${subject_id}`,
         { headers: { Authorization: `Bearer ${token}` } });
        this.chapters = res.data.chapters;
          }
          catch(error){if (error.response && error.response.status === 404) {
                    this.errorMessage = "Subject not found or may have been deleted.";}
                     else {
                    this.errorMessage = "Something went wrong while loading chapters."; }
                  // setTimeout(() => this.$router.push('/'), 3000);
                    }
          },
    async getSubject() {
          const token = localStorage.getItem('token');
          try {
            const res = await axios.get(`http://127.0.0.1:5000/api/subject/${this.subjectId}`, {
              headers: { Authorization: `Bearer ${token}` }
            });
            this.subject = res.data;  // assuming backend returns { subject: { id, name, description } }
            console.log(res.data)
          } catch (error) {
            this.errorMessage = 'Failed to load subject details.';
          }
        },
    async AddChapter(){
            this.errorMessage = ''; // clear previous error
            const token = localStorage.getItem('token');
            const subjectId = Number(this.$route.params.subject_id);
            try{ 
              const response = await axios.post("http://127.0.0.1:5000/api/chapter",
             {name: this.name , description: this.description, subject_id: subjectId},
             {headers: { Authorization: `Bearer ${token}`}}); 
            console.log(response.data);
            this.getChapters(Number(this.$route.params.subject_id));
            this.isPosting = false;
            this.name = '';
            this.description = '';
            }
            catch(error){
                if (error.response && error.response.data && error.response.data.error) {
                    this.errorMessage = error.response.data.error;
                  } else {
                    this.errorMessage = 'An error occurred while adding the subject. It may be already in the database';
                  }
            } 
        },

    async UpdateChapter(){
            this.errorMessage = ''; // clear previous error
            const token = localStorage.getItem('token');
          try{ 
              const response = await axios.put(`http://127.0.0.1:5000/api/chapter/${this.chapterId}`,
             {name: this.name , description: this.description},
             {headers: { Authorization: `Bearer ${token}` }}); 
            console.log(response.data);
            this.getChapters(Number(this.$route.params.subject_id));
            this.name = '';
            this.description = '';
            this.isEditing = false;
            this.chapterId = null;
            }
            catch(error){
                if (error.response && error.response.data && error.response.data.error) {
                    this.errorMessage = error.response.data.error;
                  } else {
                    this.errorMessage = 'An error occurred while updating the subject. It may be already in the database';
                  }
            } 
    },
    async RemoveChapter(chapter){
            this.errorMessage = ''; // clear previous error
            const token = localStorage.getItem('token');
            this.chapterId = chapter.id;
          try{ 
              const response = await axios.delete(`http://127.0.0.1:5000/api/chapter/${this.chapterId}`,
             {headers: { Authorization: `Bearer ${token}` }}); 
            console.log(response.data);
            this.getChapters(Number(this.$route.params.subject_id));
            this.chapterId = null;
            }
            catch(error){
                if (error.response && error.response.data && error.response.data.error) {
                    this.errorMessage = error.response.data.error;
                  } else {
                    this.errorMessage = 'An error occurred while delete the subject. It may be already in the database';
                  }
            } 
    },
    cancelPosting() {
      this.isPosting = false;
      this.name = '';
      this.description = '';
    },

    cancelEdit() {
      this.isEditing = false;
      this.chapterId = null;
      this.name = '';
      this.description = '';
    },

    editChapter(chapter) {
      this.chapterId = chapter.id;
      this.name = chapter.name;
      this.description = chapter.description;
      this.isEditing = true;
    }
    
    }
};
</script>

<template>
  <NavBar  @search="handleSearch"/>
<div class="chapter-list">
  

  <div class="chapter-header">
    <div v-if="subject">
      <h2>Chapters in "{{ subject.name }}"</h2>
    </div>
    <div v-else>
      <h2>Loading subject...</h2>
    </div>

    <div class="chapter-actions">
    <router-link :to="`/subject`"><button class="subject-btn">Choose Other Subject</button></router-link>
    <button @click="isPosting = true" class="add-btn">Add Chapter ✚</button>
    </div>
  </div>
    
  

  
    
  
  <div class="chapter-grid">
    <div class="chapter-card" v-for="chapter in filterChapters" :key="chapter.id">
      <h2>{{ chapter.name }}</h2>
      <p>{{ chapter.description }}</p>
      <router-link :to="`/chapter/${chapter.id}/quiz`"><button> Manage Quiz</button></router-link>
      <button @click="editChapter(chapter)" id="but2">Edit ✍️</button>
      <button @click="RemoveChapter(chapter)" id="but3">Delete 🗑️</button>
    </div>
  </div>
  
</div>
<div v-if="errorMessage" class="error-message">
  {{ errorMessage }}
</div>



<div v-if="isPosting">
  <div class="overlay"></div>
  <div class="modal-form">
    <h3>Add Chapter</h3>
    <div class="form-input">
      <input v-model="name" placeholder="Enter chapter name" />
    </div>
    <div class="form-input">
      <input v-model="description" placeholder="Enter chapter description" />
    </div>
    <button @click="AddChapter">Save</button>
    <button @click="cancelPosting">Cancel</button>
  </div>
</div>

<div v-if="isEditing">
  <div class="overlay"></div>
  <div class="modal-form">
    <h3>Edit Chapter</h3>
    <div class="form-input">
      <input v-model="name" placeholder="Edit chapter name" />
    </div>
    <div class="form-input">
      <input v-model="description" placeholder="Edit chapter description" />
    </div>
    <button @click="UpdateChapter">Update</button>
    <button @click="cancelEdit">Cancel</button>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
  
</div>
</template>

<style>

.chapter-actions {
  display: flex;
  justify-content: left;
  align-items: center;
  gap: 10px;
  margin-bottom: 5px;
}

.chapter-actions .subject-btn {
  padding: 10px 14px;
  background-color:#128538;
  color: white;
  border-radius: 30px;
  cursor: pointer;
  border: none;
}

.chapter-actions .subject-btn:hover {
  background-color: #11a35f;
  color: black;
  transform: scale(1.1);
}

.chapter-actions .add-btn {
  padding: 10px 14px;
  background-color: #4d028a;
  color: white;
  border-radius: 30px;
  border: none;
  cursor: pointer;
}

.chapter-actions .add-btn:hover {
  background-color: #a245ea;
  color: #0b0110;
  transform: scale(1.07);
}

.add-chapter button {
  display:inline;
  margin-top:15px;
  margin-bottom: 5px;
  padding: 8px 10px;
  background-color: #4d028a;
  color: rgb(255, 255, 255);
  margin-inline: 2px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.add-chapter :hover {
  background-color: #a245ea;
  color: #0b0110;
  transform: scale(1.12);
}


.chapter-list{
  padding: 30px;
  margin-top: 60px;
  text-align: right;
}

.chapter-header {
  display: flex ;
  flex-wrap: wrap;
  gap: 20px;
  background-color: #333333;
  color: #ffffff;
  padding: 2px;
  border-radius: 8px; 
}

.chapter-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 25px;
  background-color: #dcdbdb;
  padding: 50px;
  border-radius: 8px;
}

.chapter-card {
  background: #ffffff;
  padding: 20px;
  width: 250px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  text-align: left;
  text-decoration: none;
  color: inherit;
  border-radius: 8px;
  transition: transform 0.2s;
}

.chapter-card:hover {
  transform: scale(1.2);
  cursor: pointer;
}

.chapter-card h2 {
  margin: 0 0 10px;
  color: #333;
}

.chapter-card p {
  font-size: 14px;
  color: #555;
}
.chapter-card button {
  margin-top: 10px;
  padding: 8px 10px;
  background-color:#004e7b;
  color: rgb(255, 247, 247);
  margin-inline: 2px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.chapter-card button:hover {
  background-color: #1698e3;
  color: #0b0110;
  transform: scale(1.07);
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
  color: #9a9a9a;
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
  background-color: #d3e070;
  color: rgb(36, 36, 36);
}
</style>
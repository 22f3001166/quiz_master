<script>
import NavBar from "@/components/NavBar.vue";
import axios from "axios";
export default {
  data() {
    return {
      subjects: [],
      name: '',
      description: '',
      subjectId: null,  // store ID of subject being edited
      isPosting: false,
      isEditing: false,
      errorMessage: '',
      searchText:''
    };
  },
  components:{
    NavBar
  },
  computed: {
    filteredSubject(){
      return this.subjects.filter(sub=> {
        const name_desc = sub.name.toLowerCase().includes(this.searchText.toLowerCase()) ||
        sub.description.toLowerCase().includes(this.searchText.toLowerCase()) ;
        return name_desc
        });
    }
  },
  created() {
    this.getSubjects();
  },

  methods: {
    handleSearch(searchQuery){
      this.searchText = searchQuery;
    },
    async getSubjects() {
      const token = localStorage.getItem('token');
      const res = await axios.get('http://127.0.0.1:5000/api/subject', {
        headers: { Authorization: `Bearer ${token}` }
      });
      this.subjects = res.data.subjects;
    },
    
        editSubject(subject) {
            this.subjectId = subject.id;
            this.name = subject.name;
            this.description = subject.description;
            this.isEditing = true;
        },
        cancelEdit(){
          this.isEditing=false,
          this.subjectId=null
        },

    async AddSubject(){
            this.errorMessage = ''; // clear previous error
            const token = localStorage.getItem('token');
            try{ 
              const response = await axios.post("http://127.0.0.1:5000/api/subject",
             {name: this.name , description: this.description},
             {headers: { Authorization: `Bearer ${token}`}}); 

            console.log(response.data);
            this.getSubjects();
            this.isPosting=false
            this.name=''
            this.description=''
            }
            catch(error){
                if (error.response && error.response.data && error.response.data.error) {
                    this.errorMessage = error.response.data.error;
                  } else {
                    this.errorMessage = 'An error occurred while adding the subject. It may be already in the database';
                  }
            } 
        },
        
    async UpdateSubject(){
            this.errorMessage = ''; // clear previous error
            const token = localStorage.getItem('token');
          try{ 
              const response = await axios.put(`http://127.0.0.1:5000/api/subject/${this.subjectId}`,
             {name: this.name , description: this.description},
             {headers: { Authorization: `Bearer ${token}` }}); 
            console.log(response.data);
            this.getSubjects();
            this.name = '';
            this.description = '';
            this.subjectId = null;
            this.isEditing = false;
            }
            catch(error){
                if (error.response && error.response.data && error.response.data.error) {
                    this.errorMessage = error.response.data.error;
                  } else {
                    this.errorMessage = 'An error occurred while updating the subject. It may be already in the database';
                  }
            } 
    },

    async RemoveSubject(subject){
            this.errorMessage = ''; // clear previous error
            const token = localStorage.getItem('token');
            this.subjectId = subject.id;
          try{ 
              const response = await axios.delete(`http://127.0.0.1:5000/api/subject/${this.subjectId}`,
             {headers: { Authorization: `Bearer ${token}` }}); 
            console.log(response.message);
            this.getSubjects();
            this.subjectId = null;
            }
            catch(error){
                if (error.response && error.response.data && error.response.data.error) {
                    this.errorMessage = error.response.data.error;
                  } else {
                    this.errorMessage = 'An error occurred while delete the subject. It may be already in the database';
                  }
            } 
    }


  }
};
</script>

<template>
  <NavBar @search="handleSearch"/>
  <div class="subject-container">
    
    <h1>📘 Available Subjects</h1>
     <div class="add-subject">
      <button @click="isPosting = true">Add Subject ✚</button>
    </div>
    
    <div class="subject-grid">
      <div class="subject-card" v-for="sub in filteredSubject" :key="sub.id">
        <h2>{{ sub.name }}</h2>
        <p>{{ sub.description }}</p>
        <router-link :to="`subject/${sub.id}/chapter`"><button id="but1">Manage ✍️</button></router-link>
        <button @click="editSubject(sub)" id="but2">Edit ✍️</button>
        <button @click="RemoveSubject(sub)" id="but3">Delete 🗑️</button>
      </div>
      

    </div>
   
    <div v-if="isPosting">
      <div class="overlay"></div>
      <div class="modal-form">
        <h3>Add Subject</h3>
        <div class="form-input">
          <input v-model="name" placeholder="Enter subject name" />
        </div>
        <div class="form-input">
          <input v-model="description" placeholder="Enter subject description" />
        </div>
        <button @click="AddSubject">POST</button>
        <button @click="isPosting = false">Cancel</button>
      </div>
    </div>

    <div v-if="isEditing">
      <div class="overlay"></div>
      <div class="modal-form">
        <h3>Edit Subject</h3>
        <div class="form-input">
          <input v-model="name" placeholder="Enter new subject name" />
        </div>
        <div class="form-input">
          <input v-model="description" placeholder="Enter new description" />
        </div>
        <button @click="UpdateSubject">Save</button>
        <button @click="cancelEdit">Cancel</button>
      </div>
    </div>3


    
  </div>
</template>



<style scoped>

.add-subject button {
  margin-top:5px;
  margin-bottom: 4px;
  padding: 10px 14px;
  background-color: #4d028a;
  color: rgb(255, 255, 255);
  margin-inline: 4px;
  border: none;
  border-radius: 30px;
  cursor: pointer;
}

.add-subject :hover {
  background-color: #a245ea;
  color: #0b0110;
  transform: scale(1.07);
}



.subject-container {
  padding: 20px;
  margin-top: 70px;
  text-align: center;
}

.subject-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  background-color: #dcdbdb;
  padding: 20px;
  border-radius: 40px;
}

.subject-card {
  background: #ffffff;
  padding: 30px;
  width: 300px;
  border-radius: 20px;
  box-shadow: 2px 4px 12px rgba(0,0,0,0.1);
  text-align: left;
}
.subject-card h2 {
  margin: 0 0 10px;
  color: #333;
}

.subject-card p {
  font-size: 14px;
  color: #555;
}

.subject-card button {
  margin-top: 10px;
  padding: 8px 10px;
  background-color:#004e7b;
  color: rgb(255, 247, 247);
  margin-inline: 4px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.subject-card button:hover {
  background-color: #1698e3;
  color: #0b0110;
  transition: transform 0.1s;

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
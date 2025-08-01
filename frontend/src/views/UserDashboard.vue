<template>
  <div>
    <NavBar :role="user.role"/>
   </div>
  
   <div class="attend-quiz-container">
     <div v-if="userRole === 'student'" class="attend-quiz-card">
  <div class="welcome">Welcome, {{ user.name }}</div>
  <h1 class="quiz-title">🎯 Attend Quiz Here 📝</h1>
  <button class="start-btn" @click="$router.push('quizes')">Click to Start ☛</button>
  
</div>

<div v-if="userRole === 'admin'" class="attend-quiz-card">
  <div class="welcome">Welcome, {{ user.name }}</div>
  <button class="start-btn" @click="$router.push('subject')">Manage Quiz Here ☛</button>
  <button class="leaderboard-btn" @click="$router.push('/user-details')">Track Users 🖥️</button>
</div>
   </div>

</template>




<script>
// import UserProfile from "./UserProfile.vue";
import axios from "axios";
import NavBar from "@/components/NavBar.vue";

  export default {
    data() {
      return {
          user: '',
          userRole: this.$store.getters.userRole,
          token: localStorage.getItem('token'),
          quizzes: [],
          attemptHistory: [],
          scoreData: {}, // Computed from history
          editing: false,
          errorMessage: '',
      };
    },
    created(){
      this.fetchUser();
    },
    components:{
      NavBar,
      // UserProfile
    },
    methods: {
    async fetchUser() {
        try{
        const res = await axios.get(`http://127.0.0.1:5000/api/user`, {
            headers: { Authorization: `Bearer ${this.token}` }
            });
        console.log(res.data)
        this.user = res.data;
        }

        catch(error){
                if (error.response && error.response.data && error.response.data.error) {
                      this.errorMessage = error.response.data.error;
                    } else {
                      this.errorMessage = 'An error occurred while fetching the Quiz.';
                    }
            }  
      }
    }
  }
  </script>


<style>

.attend-quiz-container {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #deeeed;
  height: 110vh;
}



.attend-quiz-card {
  background: #bcbcbc;
  padding: 50px 60px;
  border-radius: 18px;
  box-shadow: 0px 20px 40px rgba(7, 208, 208, 0.415);
  text-align: center;
}
.attend-quiz-card .welcome {
  font-size: 40px;
  font-weight: bold;
  color: #000000;
  margin-bottom: 20px;
}
.quiz-title {
  font-size: 30px;
  font-weight: 600;
  margin-bottom: 40px;
  margin-top: 20px;
  color: #050505;
}

.start-btn {
  font-size: 24px;
  padding: 8px 20px;
  background-color: #24ab1f;
  color: rgb(255, 255, 255);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.start-btn:hover {
  background-color: #19ef56a0;
  color: #000;
}

.leaderboard-btn {
  font-size: 24px;
  padding: 8px 20px;
  margin-left:14px;
  background-color: #0096e1;
  color: rgb(255, 255, 255);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.leaderboard-btn:hover {
  background-color: #31c5ffd9;
  color: #000;
}
</style>




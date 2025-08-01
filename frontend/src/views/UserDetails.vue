<script>
import NavBar from '@/components/NavBar.vue';
import axios from 'axios';
export default{
    name:"UserDetails",
    components:{
        NavBar
    },
    data(){
        return {
            users: [],
            token: localStorage.getItem("token"),
            errorMessage: '',
        };
    },
    created() {
        this.fetchUser();
    },
    methods:{
        async fetchUser() {
            try{
                const response = await axios.get(`http://127.0.0.1:5000/api/users`, {
                    headers: { Authorization: `Bearer ${this.token}` }
                });
                console.log(response.data)
                this.users = response.data.users;
            }
            catch(error){
                if (error.response && error.response.data && error.response.data.message) {
                    this.errorMessage = error.response.data.message;
                } else {
                    this.errorMessage = 'An error occurred while fetching the Quiz.';
                }
            }  
        }

    }
}
</script>


<template>
    <NavBar/>
    <div style="margin: 80px 20px;">
      <h2>User Details (Academic View)</h2>
  
      <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
        <thead>
          <tr style="background-color: #f2f2f2;">
            <th style="padding: 10px; border: 1px solid #ddd;">Name</th>
            <th style="padding: 10px; border: 1px solid #ddd;">DOB</th>
            <th style="padding: 10px; border: 1px solid #ddd;">Qualification</th>
            <th style="padding: 10px; border: 1px solid #ddd;">Email</th>
            <th style="padding: 10px; border: 1px solid #ddd;">Role</th>
            <th style="padding: 10px; border: 1px solid #ddd;">Timezone</th>
            <th style="padding: 10px; border: 1px solid #ddd;">Quizzes Attempted</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td style="padding: 10px; border: 1px solid #ddd;">{{ user.name }}</td>
            <td style="padding: 10px; border: 1px solid #ddd;">{{ user.dob }}</td>
            <td style="padding: 10px; border: 1px solid #ddd;">{{ user.qualification }}</td>
            <td style="padding: 10px; border: 1px solid #ddd;">{{ user.email }}</td>
            <td style="padding: 10px; border: 1px solid #ddd;">{{ user.role }}</td>
            <td style="padding: 10px; border: 1px solid #ddd;">{{ user.timezone }}</td>
            <td style="padding: 10px; border: 1px solid #ddd;">{{ new Set(user.scores.map(s => s.quiz_id)).size }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-if="errorMessage" style="margin-top: 20px;">{{errorMessage}}</p>
</template>
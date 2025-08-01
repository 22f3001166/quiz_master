<template>
        <NavBar/> 
       
       <div class="profile-container">
       <h2 class="profile">Profile Details</h2>

          <p><strong>Name:</strong> {{ user.name }}</p>
          <p><strong>Email:</strong> {{ user.email }}</p>
          <p><strong>Role:</strong> {{ user.role }}</p>
          <p><strong>Age:</strong> {{ calculateAge(user.dob)}}</p>
          <p>Qualification: {{ user.qualification  }}</p>
          <p>Timezone: {{ user.timezone  }}</p>
          <button class="edit-btn" @click="editing = true">Edit Profile</button>
          <div v-if="editing" class="modal">
            <div class="modal-content">
                <h2>Edit Profile</h2>
                <form @submit.prevent="updateProfile">
                <input v-model="user.name" type="text" placeholder="Full Name"/>
                <input v-model="user.dob" type="date" placeholder="Date of Birth"/>
                <input v-model="user.timezone" type="text" placeholder="like Asia/kolkata">
                <input v-model="user.qualification" type="text" placeholder="Highest Qualification">
                <button @click="updateProfile">Save Changes</button>
                <button type="button" @click="editing = false">Cancel</button>
                </form>
                <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
                <p v-if="message" class="error">{{ message }}</p>

            </div>
            </div>
        </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import axios from 'axios';
export default {
    name: "userProfile",
    components:{
      NavBar
    },
    // props: {
    //   user_det: Object
    // },
    data() {
      return {
        user: '',
        editing: false,
        token: localStorage.getItem("token"),
        message:'',
        errorMessage: ''
      };
    },
    created() {
      this.fetchuserDetails();
    },
    methods: {
      calculateAge(dob) {
            if (!dob) return "N/A";  // Handle missing DOB
            const birthDate = new Date(dob);
            const today = new Date();
            let age = today.getFullYear() - birthDate.getFullYear();
            const monthDiff = today.getMonth() - birthDate.getMonth();

            // Adjust age if the birthday hasn't happened yet this year
            if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
              age--;
            }
            return age;
          },
      async fetchuserDetails() {
        try {
            const response = await axios.get(`http://127.0.0.1:5000/api/user`, {
              headers: { Authorization: `Bearer ${this.token}` }
            });
            if (response.data) {
              console.log(response.data);
              this.user = response.data
          } else {
            console.error("Invalid response format:", response.data);
          }
          }
         catch (error) {
          console.error("Error fetching user details", error);
        }
      },
      async updateProfile() {
        try {
          const token = localStorage.getItem("token");
          const updatedData = { name: this.user.name, timezone: this.user.timezone, dob:this.user.dob, qualification:this.user.qualification}
          const response = await axios.put(`http://127.0.0.1:5000/api/user`, updatedData,
                              {headers: {"Content-Type": "application/json", Authorization: `Bearer ${token}`}});
                              
          await this.fetchuserDetails();    // Refetch user details to ensure the UI is up-to-date
          this.editing = false;
          this.errorMessage = "";
          this.message = response.data.message;
            }
        catch (error) {
          console.error("Error updating profile:", error.response?.data);
          this.errorMessage = error.response?.data?.message || "Failed to update profile.";
                      }
                            }
            }
}
</script>

<style>

body {
  background-color: #f5f7fa;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.profile-container {
  max-width: 800px;
  margin: 120px auto 40px;
  padding: 30px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.profile {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 30px;
  color: #2c3e50;
  border-bottom: 2px solid #2196f3;
  padding-bottom: 10px;
}

.profile-container p {
  font-size: 17px;
  color: #444;
  margin: 12px 0;
  line-height: 1.5;
}

.profile-container p strong {
  color: #2c3e50;
}

.profile {
  margin-top: 100px;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  backdrop-filter: blur(5px);
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  padding: 30px 40px;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
  width: 100%;
  max-width: 500px;
  text-align: center;
}

.modal-content h2 {
  margin-bottom: 20px;
  color: #333;
}

.modal-content form input {
  width: 100%;
  padding: 12px;
  margin-bottom: 15px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 16px;
}

.modal-content form button {
  padding: 10px 20px;
  margin: 8px;
  font-size: 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.modal-content form button:first-of-type {
  background-color: #4CAF50;
  color: white;
}

.modal-content form button:last-of-type {
  background-color: #f44336;
  color: white;
}

.edit-btn {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 15px;
  background-color: #2196f3;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}

.error {
  color: red;
  margin-top: 10px;
}
</style>
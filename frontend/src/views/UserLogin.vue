<template>
  <div class="login-page">
    <div class="form">
      <h1>User Login</h1>
      <form class="login-form" @submit.prevent="login">
        <input v-model="email" type="email" placeholder="Enter email" required />
        <input v-model="password" type="password" placeholder="Enter password" required />
        <button type="submit">Login</button>
        <p class="message">Not registered? <router-link to="/signup">Create an account</router-link></p>
        <p v-if="error" class="error-message">{{ error }}</p>
      </form>
    </div>
  </div>
  </template>

<script>

import axios from "axios";

export default {
  name: "UserLogin",
  props:{
    parentmessage: String
  },
  data() {
    return {
      email: "",     // Stores email input
      password: "",  // Stores password input
      error: null,   // Stores error message if login fails
    };
  },
  methods: {
    async login(this.email, this.password) {
      try {
      const response = await axios.post("http://127.0.0.1:5000/api/login", { this.email, this.password });
        };
        const {token} = response.data; 
        await this.$store.dispatch("login", { 'token': token });
        this.$router.push("/dashboard");
        }
        catch (err) {
        console.error("Login Error:", err.response?.data || err.message);
        this.error = "Invalid email or password!";
        }
    },
  },
};
</script>



<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60vh;
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  margin: 0;
}

.form {
  background: rgba(224, 224, 224, 0.85);
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 250px;
  height: 280px;
}

.form h1 {
  color: #0b172e;
  margin-bottom: 5px;
  margin-top: 5px;
  font-size: 1.8rem;
  text-align: center;
}

.login-form input {
  width: 80%;
  padding: 10px 10px;
  margin-bottom: 5px;
  margin-top: 5%;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.form button {
  width: 80%;
  padding: 10px;
  background-color: #2d3e50;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin-bottom: 5px;
  margin-top: 5%;
  font-weight: bold;
}

.form button:hover {
  background-color: #4666b2;
}

.message {
  font-size: 1.0rem;
  text-align: center;
  margin-top: 5%;
  color: #444;
}

.message a {
  color: #006a97;
  text-decoration: underline;
}

.message a:hover {
  color: #00a9e7;
}

.error-message {
  color: #b10000;
  font-size: 0.9rem;
  text-align: center;
  margin-top: 12px;
}
</style>

  <!-- <style>
  /* Add your custom styles here */
  .login-page {
    display: -webkit-flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-image: linear-gradient(#9c9c9c, #303030);
  }
  
  .form {
    background-color: #164a93;
    background-image: linear-gradient(#006aff, #000c2f);
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(131, 75, 96, 0.1);
  }
  
  .form input {
    width: 80%;
    height: 200%;
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #000000;
    border-radius: 4px;
  }
  
  .form button {
    width: 50%;
    padding: 10px;
    background-color: #ff9d00;
    color: #464444;
    border:#ff9d00;
    border-radius: 4px;
    cursor: pointer;
    size:0cqmax;
  }
  
  .form button:hover {
    background-color: #00c327;
  }
  
  .form .message {
    font-size: 18px;
    text-align: center;
    margin-top: 15px;
    text-size-adjust:inherit;
    color:rgb(218, 19, 19)
  }
  
  .form .message a {
    color: #ffe600;
    text-decoration: sandybrown;
    font-style:oblique ;
  }
  
  /* Additional styling as needed */
  </style> -->

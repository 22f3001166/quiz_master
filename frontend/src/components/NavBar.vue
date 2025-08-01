<template>
  <nav class="navbar">
    <div class="navbar-left">
      <img width="60px" id="logo" src="../assets/LogoQ.png" alt="Logo" />
    </div>
    <div class="navbar-center">
      <input
        type="text"
        class="search-input"
        v-model="searchQuery"
        @input="$emit('search', searchQuery)"
        placeholder="🔎 Search subjects, chapters, quizzes..."
      /> 
    </div>
    <div class="navbar-right">
      
      <div class="nav-group nav-group-main">
        <button class="home-btn" @click="$router.push('/dashboard')">🏠 Home</button>
        <button class="summary-btn" @click="$router.push('/summary')">📊 Summary</button>
        <button class="profile-btn" @click="$router.push('/profile')">👤 Profile</button>
        <button class="logout-btn" @click="handleLogout">🚪 Logout</button>
      </div>

    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  data() {
    return {
      searchQuery: '',
      userRole: this.$store.state.userRole 
    };
  },
  // computed: {
  //   userRole() {
  //     return this.$store.state.userRole;
  //   }
  // },
  methods: {
  handleLogout() {
    return this.$store.dispatch("logout");
  }
}
};
</script>


<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background-color: #888888;
  color: #000000;
  padding: 10px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0px 2px 8px rgba(75, 245, 194, 0.299);
  z-index: 100;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo {
  font-size: 22px;
  font-weight: bold;
}

.navbar-center {
  flex-grow: 1;
  display: flex;
  justify-content: center;
}

.search-input {
  width: 50%;
  padding: 8px 10px;
  border-radius: 2px;
  /* border:hwb(from color h w b); */
  border: 2px solid rgb(0, 0, 0);
  font-size: 16px;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.nav-group {
  display: flex;
  align-items: center;
}

.nav-group-main button {
  margin-left: 10px;
  margin-right: 25px;
}

.navbar-right button {
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  font-size: 15px;
  cursor: pointer;
  font-weight: 600;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
}

.navbar-right .home-btn:hover {
  background-color: #08b911;
  color: white;
  box-shadow: 0px 2px 10px #4caf50;;
}

.navbar-right .summary-btn:hover {
  background-color: #008cff;
  color: white;
  box-shadow: 0px 2px 10px #2196f3;
}

.navbar-right .leaderboard-btn:hover {
  background-color: #a232fdc2;
  color: white;
  box-shadow: 0px 2px 10px  #a232fdc2;
}

.navbar-right .profile-btn:hover {
  background-color: #ff9900;
  box-shadow: 0px 2px 10px #ff9900c9;
  color: white;
}

.navbar-right .logout-btn:hover {
  background-color: #f44336;
  color: white;
  box-shadow: 0px 2px 10px rgba(255, 97, 97, 0.695);
}

.navbar-right button:not(:last-child) {
  margin-right: 10px;
} 

.navbar-right button {
  transform: translateY(-2px);
  background-color: #faf4f4cb;
  color: #000000; 
}
</style>
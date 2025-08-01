<template>
  <div>
    <h1>Master Effortlessly with QuizApp</h1>
    <div class="home">
      <img src="../assets/Gurmukhi.png" class="side-image" alt="Gurmukhi Script" />
      <!-- <div class="Login"> -->
        <UserLogin />
      <!-- </div> -->
      <img src="../assets/Gurmukhi.png" class="side-image" alt="Gurmukhi Script" />
    </div>
  </div>
</template>

<script>
import UserLogin from './UserLogin.vue';

export default {
  name: 'HomeView',
  components: {
    UserLogin
  }
};
</script>
<style scoped>
h1 {
  margin: 2px 20px 80px;
  font-size: 2.4rem;
  font-weight: bold;
  text-align: center;
}

.home {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  gap: 30px;
  padding: 0 20px 40px;
  flex-wrap: wrap;
  height: auto;
  margin-bottom: 20px;
}

.side-image {
  height: 320px;
  object-fit: contain;
  border-radius: 12px;
  background: rgba(181, 180, 180, 0.85);
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 250px;
}
</style>

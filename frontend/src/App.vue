<script>
export default {
  name: 'App',
  data() {
    return { 
      isAuthenticated: this.$store.getters.isAuthenticated,
      userRole: this.$store.getters.userRole
    };
   },
};
</script>

<style>
#app {
  font-family: Georgia, 'Times New Roman', Times, serif;
  scroll-behavior: auto;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #0c0c0c;
}


.homeview{
  width: 100;
}


</style>

 

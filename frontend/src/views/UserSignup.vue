<template>

    <div class="main-w3layouts">
		<div class="main-agileinfo">
			<div class="agileits-top">
				<form @submit.prevent="UserSignup">
          <h1>SignUp Form</h1>
          <input class="text" type="text" name="name" placeholder="Full Name" v-model="name" required> 
					<input class="text email" type="email" name="email" placeholder="Email" v-model="email" required>
					<input class="text" type="password" name="password" placeholder="Password" v-model="password" required>
					<input class="text w3lpass" type="password" name="confirm_password" placeholder="Confirm Password" v-model="confirm_password" required>
          <input class="text" type="date" name="birthday" v-model="dob" placeholder="Birth Date" required>
          <input class="text" type="text" name="timezone" placeholder="Your Timezone (e.g. Asia/Kolkata)" v-model="timezone" required>
					<input type="submit" value="SIGNUP"/>
          <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
				</form>
				<p>Already have an Account? <router-link to="/">Login Now!</router-link></p>
			</div>
		</div>
	
	</div>
</template>

<script>
import axios from 'axios';

export default{
  data(){
    return {
      name: "",
      email: "",
      password: "",
      confirm_password: "",
      dob: "",
      timezone: "",
      errorMessage: "",
    };
  },
  methods:{
    async UserSignup(){
      if (this.password !== this.confirm_password) {
        this.errorMessage = "Both Password do not match!";
        return;
      }
      try{
        const response = await axios.post('http://127.0.0.1:5000/api/signup',{
          name: this.name,
          email: this.email,
          password: this.password,
          confirm_password: this.confirm_password,
          dob: this.dob,
          timezone: this.timezone,
        });

        alert(response.data.message);
        this.$router.push('/');
      }
      catch(error){
        this.errorMessage = error.response ? error.response.data.message:'Signup failed Please try again.'
      }
    }
  }
};

</script>




<style scoped>
html, body, div, span, applet, object, iframe, h1, h2, h3, h4, h5, h6, p, blockquote, pre, a, abbr, acronym, address, big, cite, code, del, dfn, em, img, ins, kbd, q, s, samp, small, strike, strong, sub, sup, tt, var, b, u, i, dl, dt, dd, ol, nav ul, nav li, fieldset, form, label, legend, table, caption, tbody, tfoot, thead, tr, th, td, article, aside, canvas, details, embed, figure, figcaption, footer, header, hgroup, menu, nav, output, ruby, section, summary, time, mark, audio, video {
  margin: 0;
  padding: 0;
  border: 0;
  font-size: 100%;
  font: inherit;
  vertical-align: baseline;
}

article, aside, details, figcaption, figure, footer, header, hgroup, menu, nav, section {
  display: block;
}

ol, ul {
  list-style: none;
  margin: 0px;
  padding: 0px;
}

blockquote, q {
  quotes: none;
}

blockquote:before, blockquote:after, q:before, q:after {
  content: '';
  content: none;
}

table {
  border-collapse: collapse;
  border-spacing: 0;
}

/*-- start editing from here --*/
a {
  text-decoration: none;
}

.txt-rt {
  text-align: right;
}

/* text align right */
.txt-lt {
  text-align: left;
}

/* text align left */
.txt-center {
  text-align: center;
}

/* text align center */
.float-rt {
  float: right;
}

/* float right */
.float-lt {
  float: left;
}

/* float left */
.clear {
  clear: both;
}

/* clear float */
.pos-relative {
  position: relative;
}

/* Position Relative */
.pos-absolute {
  position: absolute;
}

/* Position Absolute */
.vertical-base {
  vertical-align: baseline;
}

/* vertical align baseline */
.vertical-top {
  vertical-align: top;
}

/* vertical align top */
nav.vertical ul li {
  display: block;
}

/* vertical menu */
nav.horizontal ul li {
  display: inline-block;
}

/* horizontal menu */
img {
  max-width: 100%;
}

/*-- end reset --*/
body {
  background: #f5f6fa;
  font-family: 'Roboto', Arial, Helvetica, sans-serif;
}

h1 {
  font-size: 2em;
  text-align: center;
  color: #222;
  font-weight: 400;
  margin-bottom: 1.5em;
  letter-spacing: 1px;
}

.main-w3layouts {
  padding: 2em 0 1em;
  background: none;
}

.main-agileinfo {
  width: 100%;
  max-width: 420px;
  margin: 3em auto;
  background: #fff;
  border: 1px solid #e2e2e2;
  border-radius: 8px;
  box-shadow: 0 2px 8px 0 rgba(30,30,30,0.04);
}

.agileits-top {
  padding: 2.5em 2em 2em 2em;
}

label{
  font-size: 1em;
  color: #222;
  font-weight: 400;
  font-family:Verdana, Geneva, Tahoma, sans-serif;
}

input[type="text"], input[type="email"], input[type="password"], input[type="date"] {
  font-size: 1em;
  color: #222;
  font-weight: 400;
  width: 100%;
  display: block;
  border: 1px solid #d1d1d1;
  border-radius: 4px;
  padding: 0.85em 0.9em;
  margin-bottom: 1.2em;
  background: #fafbfc;
  transition: border-color 0.2s;
  font-family:Verdana, Geneva, Tahoma, sans-serif;
}

input[type="text"]:focus, input[type="email"]:focus, input[type="password"]:focus, input[type="date"]:focus {
  outline: none;
  border-color: #7a8cff;
  background: #fff;
}

input[type="submit"] {
  font-size: 1.1em;
  color: #fff;
  background: #2d3e50;
  outline: none;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  padding: 0.9em;
  width: 100%;
  margin-top: 1.5em;
  letter-spacing: 2px;
  font-weight: 500;
  transition: background 0.2s;
}

input[type="submit"]:hover {
  background: #4666b2;
}

.agileits-top p {
  font-size: 1em;
  color: #555;
  text-align: center;
  letter-spacing: 0.5px;
  font-weight: 400;
  margin-top: 1.5em;
}

.agileits-top p a {
  color: #2d3e50;
  transition: color 0.2s;
  font-weight: 500;
  text-decoration: underline;
}

.agileits-top p a:hover {
  color: #4666b2;
}

.error {
  color: #b10000;
  background: #ffeaea;
  border: 1px solid #ffcccc;
  border-radius: 3px;
  padding: 0.5em 1em;
  margin-top: 1em;
  text-align: center;
  font-size: 1em;
}
/*-- checkbox --*/
.wthree-text label {
  font-size: 0.9em;
  color: #ccff00;
  font-weight: 100;
  cursor: pointer;
  position: relative;
}

input.checkbox {
  background: hsl(119, 100%, 8%);
  cursor: pointer;
  width: 1.2em;
  height: 1.2em;
}

input.checkbox:before {
  content: "";
  position: absolute;
  width: 1.2em;
  height: 1.2em;
  background: inherit;
  cursor: pointer;
}

input.checkbox:after {
  content: "";
  position: absolute;
  top: 0px;
  left: 0;
  z-index: 1;
  width: 1.2em;
  height: 1.2em;
  border: 1px solid #ffffff;
  -webkit-transition: .4s ease-in-out;
  -moz-transition: .4s ease-in-out;
  -o-transition: .4s ease-in-out;
  transition: .4s ease-in-out;
}

input.checkbox:checked:after {
  -webkit-transform: rotate(-45deg);
  -moz-transform: rotate(-45deg);
  -o-transform: rotate(-45deg);
  -ms-transform: rotate(-45deg);
  transform: rotate(-45deg);
  height: .5rem;
  border-color: #ff0000;
  border-top-color: transparent;
  border-right-color: transparent;
}

.anim input.checkbox:checked:after {
  -webkit-transform: rotate(-45deg);
  -moz-transform: rotate(-45deg);
  -o-transform: rotate(-45deg);
  -ms-transform: rotate(-45deg);
  transform: rotate(-45deg);
  height: .5rem;
  border-color: transparent;
  border-right-color: transparent;
  animation: .4s rippling .4s ease;
  animation-fill-mode: forwards;
}

@keyframes rippling {
  50% {
    border-left-color: #ee0000;
  }

  100% {
    border-bottom-color: #ff0000;
    border-left-color: #ff0000;
  }
}

/*-- //checkbox --*/
/*-- copyright --*/
.colorlibcopy-agile {
  margin: 2em 0 1em;
  text-align: center;
}

.colorlibcopy-agile p {
  font-size: .9em;
  color: #ff0000;
  line-height: 1.8em;
  letter-spacing: 1px;
  font-weight: 100;
}

.colorlibcopy-agile p a {
  color: #fff;
  transition: 0.5s all;
  -webkit-transition: 0.5s all;
  -moz-transition: 0.5s all;
  -o-transition: 0.5s all;
  -ms-transition: 0.5s all;
}

.colorlibcopy-agile p a:hover {
  color: #3c3c3c;
}

/*-- //copyright --*/
.wrapper {
  position: relative;
  overflow: hidden;
}

.colorlib-bubbles {
  position: left;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}

.colorlib-bubbles li {
  position: absolute;
  list-style: none;
  display: block;
  width: 200px;
  height: 200px;
  background-color: rgba(138, 255, 166, 0.15);
  bottom: -160px;
  -webkit-animation: square 20s infinite;
  -moz-animation: square 250s infinite;
  -o-animation: square 20s infinite;
  -ms-animation: square 20s infinite;
  animation: square 20s infinite;
  -webkit-transition-timing-function: linear;
  -moz-transition-timing-function: linear;
  -o-transition-timing-function: linear;
  -ms-transition-timing-function: linear;
  transition-timing-function: step-end;
  -webkit-border-radius: 50%;
  -moz-border-radius: 50%;
  -o-border-radius: 50%;
  -ms-border-radius: 50%;
  border-radius: 50%;
}

.colorlib-bubbles li:nth-child(1) {
  left: 95%;
  background-color: rgba(71, 71, 71, 0.594);
}

.colorlib-bubbles li:nth-child(2) {
  left: 2%;
  width: 80px;
  height: 80px;
  -webkit-animation-delay: 2s;
  -moz-animation-delay: 2s;
  -o-animation-delay: 2s;
  -ms-animation-delay: 2s;
  animation-delay: 2s;
  -webkit-animation-duration: 17s;
  -moz-animation-duration: 17s;
  -o-animation-duration: 17s;
  animation-duration: 17s;
  background-color: rgb(0, 204, 255);
}

.colorlib-bubbles li:nth-child(3) {
  left: 90%;
  -webkit-animation-delay: 4s;
  -moz-animation-delay: 4s;
  -o-animation-delay: 4s;
  -ms-animation-delay: 4s;
  animation-delay: 4s;
  background-color: rgba(39, 144, 182, 0.45);
}

.colorlib-bubbles li:nth-child(4) {
  left: 20%;
  width: 60px;
  height: 60px;
  -webkit-animation-duration: 22s;
  -moz-animation-duration: 22s;
  -o-animation-duration: 22s;
  -ms-animation-duration: 22s;
  animation-duration: 22s;
  background-color: rgba(0, 255, 132, 0.439);
}

.colorlib-bubbles li:nth-child(5) {
  left: 10%;
  width: 50px;
  height: 50px;
  background-color: rgba(165, 190, 0, 0.663);
}

.colorlib-bubbles li:nth-child(6) {
  left: 10%;
  width: 50px;
  height: 50px;
  -webkit-animation-delay: 3s;
  -moz-animation-delay: 3s;
  -o-animation-delay: 3s;
  -ms-animation-delay: 3s;
  animation-delay: 3s;
  background-color: rgb(0, 245, 253);
}

.colorlib-bubbles li:nth-child(7) {
  left: 82%;
  width: 60px;
  height: 60px;
  -webkit-animation-delay: 3s;
  -moz-animation-delay: 7s;
  -o-animation-delay: 7s;
  -ms-animation-delay: 7s;
  animation-delay: 3s;
  background-color: #2b2b2b84;
}

.colorlib-bubbles li:nth-child(8) {
  left: 9%;
  width: 110px;
  height: 110px;
  -webkit-animation-delay: 15s;
  -moz-animation-delay: 15s;
  animation-delay: 1s;
  -webkit-animation-duration: 40s;
  -moz-animation-duration: 40s;
  animation-duration: 40s;
  background-color: #70ecff89;
}



.colorlib-bubbles li:nth-child(10) {
  left: 80%;
  width: 60px;
  height: 60px;
  -webkit-animation-delay: 11s;
  animation-delay: 11s;
  background-color: #59fff49b;
}

@-webkit-keyframes square {
  0% {
    -webkit-transform: translateY(0);
    -moz-transform: translateY(0);
    -o-transform: translateY(0);
    -ms-transform: translateY(0);
    transform: translateY(0);
  }

  100% {
    -webkit-transform: translateY(-700px) rotate(600deg);
    -moz-transform: translateY(-700px) rotate(600deg);
    -o-transform: translateY(-700px) rotate(600deg);
    -ms-transform: translateY(-700px) rotate(600deg);
    transform: translateY(-700px) rotate(600deg);
  }
}

@keyframes square {
  0% {
    -webkit-transform: translateY(0);
    -moz-transform: translateY(0);
    -o-transform: translateY(0);
    -ms-transform: translateY(0);
    transform: translateY(0);
  }

  100% {
    -webkit-transform: translateY(-700px) rotate(600deg);
    -moz-transform: translateY(-700px) rotate(600deg);
    -o-transform: translateY(-700px) rotate(600deg);
    -ms-transform: translateY(-700px) rotate(600deg);
    transform: translateY(-700px) rotate(600deg);
  }
}

/*-- responsive-design --*/
@media(max-width:1440px) {
  input[type="text"], input[type="email"], input[type="password"] {
    width: 94%;
  }
}

@media(max-width:1366px) {
  h1 {
    font-size: 2.6em;
  }

  .agileits-top {
    padding: 2.5em;
  }

  .main-agileinfo {
    margin: 2em auto;
  }

  .main-agileinfo {
    width: 36%;
  }
}

@media(max-width:1280px) {
  .main-agileinfo {
    width: 40%;
  }
}

@media(max-width:1080px) {
  .main-agileinfo {
    width: 46%;
  }
}

@media(max-width:1024px) {
  .main-agileinfo {
    width: 49%;
  }
}

@media(max-width:991px) {
  h1 {
    font-size: 2.4em;
  }

  .main-w3layouts {
    padding: 2em 0 1em;
  }
}

@media(max-width:900px) {
  .main-agileinfo {
    width: 58%;
  }

  input[type="text"], input[type="email"], input[type="password"] {
    width: 93%;
  }
}

@media(max-width:800px) {
  h1 {
    font-size: 2.2em;
  }
}

@media(max-width:736px) {
  .main-agileinfo {
    width: 62%;
  }
}

@media(max-width:667px) {
  .main-agileinfo {
    width: 67%;
  }
}

@media(max-width:600px) {
  .agileits-top {
    padding: 2.2em;
  }

  input.email, input.text.w3lpass {
    margin: 1.5em 0;
  }

  input[type="submit"] {
    margin: 2em 0;
  }

  h1 {
    font-size: 2em;
    letter-spacing: 3px;
  }
}

@media(max-width:568px) {
  .main-agileinfo {
    width: 75%;
  }

  .colorlibcopy-agile p {
    padding: 0 2em;
  }
}

@media(max-width:480px) {
  h1 {
    font-size: 1.8em;
    letter-spacing: 3px;
  }

  .agileits-top {
    padding: 1.8em;
  }

  input[type="text"], input[type="email"], input[type="password"] {
    width: 91%;
  }

  .agileits-top p {
    font-size: 0.9em;
  }
}

@media(max-width:414px) {
  h1 {
    font-size: 1.8em;
    letter-spacing: 2px;
  }

  .main-agileinfo {
    width: 85%;
    margin: 1.5em auto;
  }

  .text:focus, .text:valid {
    background-position: 0 0px;
  }

  .wthree-text ul li, .wthree-text ul li:nth-child(2) {
    display: block;
    float: none;
  }

  .wthree-text ul li:nth-child(2) {
    margin-top: 1.5em;
  }

  input[type="submit"] {
    margin: 2em 0 1.5em;
    letter-spacing: 3px;
  }

  input[type="submit"] {
    margin: 2em 0 1.5em;
  }

  .colorlibcopy-agile {
    margin: 1em 0 1em;
  }
}

@media(max-width:384px) {
  .main-agileinfo {
    width: 88%;
  }

  .colorlibcopy-agile p {
    padding: 0 1em;
  }
}

@media(max-width:375px) {
  .agileits-top p {
    letter-spacing: 0px;
  }
}

@media(max-width:320px) {
  .main-w3layouts {
    padding: 1.5em 0 0;
  }

  .agileits-top {
    padding: 1.2em;
  }

  .colorlibcopy-agile {
    margin: 0 0 1em;
  }

  input[type="text"], input[type="email"], input[type="password"] {
    width: 89.5%;
    font-size: 0.85em;
  }

  h1 {
    font-size: 1.7em;
    letter-spacing: 0px;
  }

  .main-agileinfo {
    width: 92%;
    margin: 1em auto;
  }

  .text:focus, .text:valid {
    background-position: 0 0px;
  }

  input[type="submit"] {
    margin: 1.5em 0;
    padding: 0.8em;
    font-size: .85em;
  }

  .colorlibcopy-agile p {
    font-size: .85em;
  }

  .wthree-text label {
    font-size: 0.85em;
  }

  .main-w3layouts {
    padding: 1em 0 0;
  }
}
</style>
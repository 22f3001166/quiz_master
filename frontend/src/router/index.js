import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UserSignup from '@/views/UserSignup.vue'
import UserDashboard from "../views/UserDashboard.vue";
// import QuizManagement from '@/views/QuizManagement.vue';
import UserProfile from '@/views/UserProfile.vue';
import UserSummary from '@/views/UserSummary.vue';
import UserDetails from '@/views/UserDetails.vue';
import store from '../store/store';
// import QuizDetail from '@/components/QuizDetail.vue';
import SubjectResource from '@/views/SubjectResource.vue';
import ChapterResource from '@/views/ChapterResource.vue';
import QuizResource from '@/views/QuizResource.vue';
import QuestionManage from '@/views/QuestionManage.vue';
import QuizAttend from '@/views/QuizAttend.vue';
import QuizSummary from '@/views/QuizSummary.vue';
import QuizFilter from '@/views/QuizFilter.vue';

const routes = [
  {path: '/', name: 'home', component: HomeView },
  {path: '/signup', name: 'signup', component: UserSignup},
  
  {path: "/dashboard",name: 'dashboard', component: UserDashboard, meta:{ isAuthenticated:true,roles:['admin','student']}},
  {path: "/profile",name: 'profile', component: UserProfile, meta:{ isAuthenticated:true,roles:['admin','student']}} ,
  {path: "/summary",name: 'summary',component: UserSummary, meta:{ isAuthenticated:true,roles:['admin','student']}},
  {path: "/user-details",name: 'leaderboard',component: UserDetails, meta:{ isAuthenticated:true,roles:['admin','student']}},
  {path: "/quizes",name: 'QuizFiltering', component: QuizFilter, meta:{ isAuthenticated:true,roles:['student']}},
  
  {path: "/subject",name: 'subject_manager',component: SubjectResource, meta:{ isAuthenticated:true,roles:['admin']}},
  {path: "/subject/:subject_id/chapter",name: 'chapter_manager',  component: ChapterResource, meta:{ isAuthenticated:true,roles:['admin']}},
  {path: "/chapter/:chapter_id/quiz",name: 'Quiz_manage', component: QuizResource, meta:{ isAuthenticated:true,roles:['admin']}},
  {path: "/quiz-manage/:quiz_id",name: 'Question_Manage', component: QuestionManage, meta:{ isAuthenticated:true,roles:['admin']}},
  {path: "/quiz-attempt/:quiz_id",name: 'Question_Attempting', component: QuizAttend, meta:{ isAuthenticated:true,roles:['admin','student']}},
  {path: "/quiz-summary/:score_id",name: 'Question_Summary', component: QuizSummary, meta:{ isAuthenticated:true,roles:['admin','student']}}, 
];


const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});


router.beforeEach((to,from,next) =>{
  const userRole = store.getters.userRole; 
  if (to.meta.isAuthenticated){
    if (!store.getters.isAuthenticated){
     next({ path: '/' });
    }
    if (to.meta.roles && !to.meta.roles.includes(userRole)){
        next({ path: '/' });
      } 
    }
    next();
  });

export default router;

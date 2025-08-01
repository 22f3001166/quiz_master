import { createStore } from 'vuex';
import router from '../router';
const store = createStore({
    state :{
        token : localStorage.getItem('token') || '',
        role: null
    },
    getters:{
        isAuthenticated: state => !!state.token,
        userRole: state => state.role
    },
    mutations :{
        // functions that change state
        setToken(state,token){
            state.token=token
            if (token){
                localStorage.setItem('token',token);
            }
            else{
                localStorage.removeItem('token');  
            }

        },
        setRole(state, role) {
            state.role = role;
        },
 
        logout(state){
            state.token = '';
            state.role = null;
        },
    },
    actions:{
        //actions commit mutations can be async
        login({commit},{token}){
            commit('setToken',token);
            localStorage.setItem('token', token); // ensure token is stored immediately
            const payload = JSON.parse(atob(token.split('.')[1]));
            const role = payload.role || "student"; // adjust based on actual structure
            commit('setRole', role);
        },
        logout({commit}){
            localStorage.removeItem("token");
            commit('logout');
            router.push('/');
        }

    }
});
const token = localStorage.getItem('token');
if (token) {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const role = payload.role || 'student';
    store.commit('setRole', role);
  } catch (e) {
    console.error('Invalid token in localStorage');
    store.commit('logout');
  }
}

export default store;
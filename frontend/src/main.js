import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './assets/font.css'
import axios from 'axios'
import VueAxios from 'vue-axios'

// import Vconsole from 'vconsole'
// const vConsole = new Vconsole()
// console.log(vConsole)
createApp(App).use(store).use(router).use(VueAxios, axios).mount('#app')

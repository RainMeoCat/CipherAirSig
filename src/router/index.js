import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../views/LoginPage.vue'
import HomePage from '../views/HomePage.vue'
import RegisterPage from '../views/RegisterPage.vue'
import TwoFactorPage from '../views/2FAPage.vue'
import Hash from '../views/AirSignPage.vue'
import User from '../views/UserPage.vue'
const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterPage
  },
  {
    path: '/2fa',
    name: '2FA',
    component: TwoFactorPage
  },
  {
    path: '/user',
    name: 'user',
    component: User
  },
  {
    path: '/hash',
    name: 'Hash',
    component: Hash
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})
// router.beforeEach((to, from, next) => {
//   if (to.name !== 'Login' && !isAuthenticated) next({ name: 'Login' })
//   else next()
// })
export default router

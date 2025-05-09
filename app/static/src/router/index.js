// In your router/index.js file
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import DeliveryView from '../views/DeliveryView.vue'
import Register_gen_view from '../views/Register_gen_view.vue'
import LoginView from '../views/LoginView.vue'
import PreferenceForm from '..views/PreferenceForm.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView
  },
  {
    path: '/delivery',
    name: 'delivery',
    component: DeliveryView
  },
  {
    path: '/register/personal',
    name: 'register_general',
    component: Register_gen_view
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/preference',
    name: 'preference',
    component: PreferenceForm
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
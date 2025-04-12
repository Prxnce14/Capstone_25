// In your router/index.js file
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import DeliveryView from '../views/DeliveryView.vue'

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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
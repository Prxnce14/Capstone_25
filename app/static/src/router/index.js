// In your router/index.js file
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import DeliveryView from '../views/DeliveryView.vue'
import Register_gen_view from '../views/Register_gen_view.vue'
import Register_driver_view from '../views/Register_driver_view.vue'
import Register_restaurant_view from '../views/Register_restaurant_view.vue'
import RestaurantMenuView from '../views/RestaurantMenuView.vue'


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
    path: '/register/driver',
    name: 'register_driver',
    component: Register_driver_view
  },
  {
    path: '/register/restaurant',
    name: 'register_restaurant',
    component: Register_restaurant_view
  },
  {
    path:'/restaurantmenu',
    name: 'RestaurantMenu',
    component: RestaurantMenuView
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
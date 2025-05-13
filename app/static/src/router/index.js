import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import DeliveryView from '../views/DeliveryView.vue'
import Register_gen_view from '../views/Register_gen_view.vue'
import LoginView from '../views/LoginView.vue'
import Register_driver_view from '../views/register_driver_view.vue'
import Register_restaurant_view from '../views/Register_restaurant_view.vue'
import Restaurant_Add_Product_View from '../views/Restaurant_Add_Product_View.vue'
import Restaurant_Edit_Product_View from '../views/Restaurant_Edit_Product_View.vue'
import RestaurantDashboard from '../views/RestaurantDashboard.vue'
import RestaurantMenu from '../views/RestaurantMenu.vue'
import RestaurantOrders from '../views/RestaurantOrders.vue'
import RestaurantSalesReport from '../views/RestaurantSalesReport.vue'
import RestaurantProfile from '../views/RestaurantProfile.vue'
import RestaurantSettings from '../views/RestaurantSettings.vue'
import GenUser_Dashboard from '../views/GenUser_Dashboard.vue'
import Gen_Order from '../views/Gen_Order.vue'
import Gen_Setting from '../views/gen_setting.vue'
import Onboarding_view from '../views/Onboarding_view.vue'
import User_Dashboard from '../views/User_Dashboard.vue'



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
    name: 'Restaurant_Add_Product',
    component: Restaurant_Add_Product_View,
    meta: { requiresAuth: true, userType: 'restaurant' }
  },
  {
    path:'/restaurantmenu/edit',
    name: 'Restaurant_Edit_Product',
    component: Restaurant_Edit_Product_View,
    meta: { requiresAuth: true, userType: 'restaurant' }
  },
  {
    path: '/restaurant',
    name: 'restaurant_dashboard',
    component: RestaurantDashboard,
    meta: { requiresAuth: true, userType: 'restaurant' }
  },
  {
    path: '/restaurant/menu',
    name: 'restaurant_menu',
    component: RestaurantMenu,
    meta: { requiresAuth: true, userType: 'restaurant' }
  },
  {
    path: '/restaurant/orders',
    name: 'restaurant_orders',
    component: RestaurantOrders,
    meta: { requiresAuth: true, userType: 'restaurant' }
  },
  {
    path: '/restaurant/sales',
    name: 'restaurant_sales',
    component: RestaurantSalesReport,
    meta: { requiresAuth: true, userType: 'restaurant' }
  },
  {
    path: '/restaurant/profile',
    name: 'restaurant_profile',
    component: RestaurantProfile,
    meta: { requiresAuth: true, userType: 'restaurant' }
  },
  {
    path: '/restaurant/settings',
    name: 'restaurant_settings',
    component: RestaurantSettings,
    meta: { requiresAuth: true, userType: 'restaurant' }
  },
  {
    path: '/orders',
    name: 'gen_orders',
    component: Gen_Order,
  },
  {
    path: '/settings',
    name: 'gen_setting',
    component: Gen_Setting,
  },
  {
    path: '/gen/onboarding',
    name: 'onboarding',
    component: Onboarding_view

  },
  {
    path: '/gen/dashboard',
    name: 'dashboard',
    component: User_Dashboard
  }
  
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard to protect routes that require authentication
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token');
  const userType = localStorage.getItem('user_type');
  const isAuthenticated = !!token;
  
  // Check if route requires authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      // User is not authenticated, redirect to login
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      });
    } else if (to.meta.userType && to.meta.userType !== userType) {
      // User is authenticated but doesn't have the right user type
      switch (userType) {
        case 'restaurant':
          next('/restaurant');
          break;
        case 'driver':
          next('/driver/dashboard');
          break;
        case 'gen_user':
          next('/gen/dashboard');
          break;
        default:
          next('/');
      }
    } else {
      // User is authenticated and has the right user type
      next();
    }
  } else {
    // Route doesn't require authentication
    next();
  }
});

// Global after hook for analytics or other purposes
router.afterEach((to, from) => {
  // Reset scroll position to top
  window.scrollTo(0, 0);
});

export default router
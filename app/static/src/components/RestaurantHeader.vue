<template>
  <nav class="navbar navbar-expand-lg navbar-dark pelican-navbar">
    <div class="container">
      <router-link class="navbar-brand" to="/restaurant">Pelican Eats - Restaurant</router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#restaurantNavbarNav" aria-controls="restaurantNavbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="restaurantNavbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/restaurant" active-class="active">Dashboard</router-link>
          </li>
          
          <li class="nav-item">
            <router-link class="nav-link" to="/restaurant/menu" active-class="active">Menu</router-link>
          </li>
          
          <li class="nav-item">
            <router-link class="nav-link" to="/restaurantmenu" active-class="active">Add Product</router-link>
          </li>
          
          <li class="nav-item">
            <router-link class="nav-link" to="/restaurant/orders" active-class="active">Orders</router-link>
          </li>
          
          <li class="nav-item">
            <router-link class="nav-link" to="/restaurant/sales" active-class="active">Sales Report</router-link>
          </li>
          
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="restaurantAccountDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Account
            </a>
            <ul class="dropdown-menu" aria-labelledby="restaurantAccountDropdown">
              <li><router-link class="dropdown-item" to="/restaurant/profile">Profile</router-link></li>
              <li><router-link class="dropdown-item" to="/restaurant/settings">Settings</router-link></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item" href="#" @click.prevent="logout">Logout</a></li>
            </ul>
          </li>
          
          <!-- Display restaurant name if available -->
          <li class="nav-item" v-if="restaurantName">
            <span class="navbar-text">{{ restaurantName }}</span>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

const router = useRouter()
const restaurantName = ref('')

// Fetch restaurant info on component mount
onMounted(async () => {
  await fetchRestaurantInfo()
})

// Fetch restaurant information
async function fetchRestaurantInfo() {
  try {
    console.log('Fetching restaurant info...') // Debug
    const data = await api.get('/current-user')
    console.log('Restaurant info response:', data) // Debug
    
    if (data.user && data.user.user_type === 'restaurant') {
      restaurantName.value = data.user.store_name || data.user.username
    }
  } catch (error) {
    console.error('Failed to fetch restaurant info:', error)
  }
}

// Logout function
async function logout() {
  try {
    // Call logout endpoint
    await api.post('/logout')
    
    // Clear tokens and redirect
    api.clearAuthTokens()
    router.push('/login')
  } catch (error) {
    console.error('Logout error:', error)
    // Even if logout fails, clear local data and redirect
    api.clearAuthTokens()
    router.push('/login')
  }
}
</script>

<style scoped>
/* Restaurant navbar styles */
.pelican-navbar {
  background-color: #FF8C00;
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
}

.container {
  padding-left: 2rem;
  padding-right: 2rem;
}

.navbar-brand {
  font-size: 1.5rem;
  color: white !important;
}

.nav-link, .dropdown-toggle {
  color: white !important;
}

.nav-link:hover, .dropdown-toggle:hover {
  color: rgba(255, 255, 255, 0.8) !important;
}

.nav-link.active,
.nav-link.router-link-active {
  color: white !important;
  font-weight: 600;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.dropdown-menu {
  margin-top: 0.5rem;
  border-radius: 6px;
}

.dropdown-item {
  padding: 0.5rem 1.5rem;
}

.navbar-text {
  color: white !important;
  margin-left: 1rem;
  font-weight: 500;
}

/* Ensure proper spacing and layout for mobile */
@media (max-width: 991px) {
  .navbar-nav {
    text-align: center;
    padding-top: 1rem;
  }
  
  .dropdown-menu {
    text-align: center;
  }
  
  .navbar-text {
    display: block;
    margin-left: 0;
    margin-top: 0.5rem;
  }
}

.navbar-toggler {
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.navbar-toggler-icon {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='rgba%28255, 255, 255, 0.75%29' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e");
}
</style>
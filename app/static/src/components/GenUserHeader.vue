<template>
  <nav class="navbar navbar-expand-lg navbar-dark pelican-navbar">
    <div class="container">
      <router-link class="navbar-brand" to="/gen/dashboard">
        <span class="brand-name">Pelican Eats</span>
      </router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#genUserNavbar" aria-controls="genUserNavbar" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="genUserNavbar">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/gen/dashboard" active-class="active">Home</router-link>
          </li>
          
          <li class="nav-item">
            <router-link class="nav-link" to="/orders" active-class="active">Orders</router-link>
          </li>
          
          <li class="nav-item">
            <router-link class="nav-link" to="/grocery" active-class="active">Grocery</router-link>
          </li>
          
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="userAccountDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Account
            </a>
            <ul class="dropdown-menu" aria-labelledby="userAccountDropdown">
              <li><router-link class="dropdown-item" to="/profile">Profile</router-link></li>
              <li><router-link class="dropdown-item" to="/settings">Settings</router-link></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item" href="#" @click.prevent="logout">Logout</a></li>
            </ul>
          </li>
          
          <!-- Cart Icon -->
          <li class="nav-item">
            <router-link class="nav-link cart-link" to="/cart">
              <i class="fas fa-shopping-cart"></i>
              <span v-if="cartCount > 0" class="cart-badge">{{ cartCount }}</span>
            </router-link>
          </li>
          
          <!-- Display user name if available -->
          <li class="nav-item" v-if="userName">
            <span class="navbar-text">{{ userName }}</span>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const userName = ref('')
const cartCount = ref(0)

// Fetch user info and cart count on component mount
onMounted(async () => {
  await fetchUserInfo()
  await fetchCartCount()
})

// Fetch user information
async function fetchUserInfo() {
  try {
    // This would be replaced with your actual API call
    const response = await fetch('/api/current-user')
    const data = await response.json()
    
    if (data.user) {
      userName.value = data.user.firstName || data.user.username
    }
  } catch (error) {
    console.error('Failed to fetch user info:', error)
  }
}

// Fetch cart count
async function fetchCartCount() {
  try {
    // This would be replaced with your actual API call
    const response = await fetch('/api/cart/count')
    const data = await response.json()
    cartCount.value = data.count || 0
  } catch (error) {
    console.error('Failed to fetch cart count:', error)
    cartCount.value = 0
  }
}

// Logout function
async function logout() {
  try {
    // Call logout endpoint
    await fetch('/api/logout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    // Clear tokens and storage
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_type')
    
    // Redirect to login page
    router.push('/login')
  } catch (error) {
    console.error('Logout error:', error)
    // Even if logout fails, clear local data and redirect
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_type')
    router.push('/login')
  }
}
</script>

<style scoped>
/* User navbar styles - matching Pelican Eats branding */
.pelican-navbar {
  background-color: #FF8C00; /* Dark Orange from your original headers */
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
  padding: 0.5rem 0;
}

.container {
  padding-left: 2rem;
  padding-right: 2rem;
}

.navbar-brand {
  font-size: 1.5rem;
  color: white !important;
  display: flex;
  align-items: center;
}

.brand-name {
  margin-left: 0.5rem;
}

.nav-link, .dropdown-toggle {
  color: white !important;
  font-weight: 500;
  padding: 0.5rem 1rem;
  position: relative;
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
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.dropdown-item {
  padding: 0.5rem 1.5rem;
}

.dropdown-item:active {
  background-color: #FF8C00;
}

.navbar-text {
  color: white !important;
  margin-left: 1rem;
  font-weight: 500;
}

/* Cart styles */
.cart-link {
  position: relative;
  font-size: 1.2rem;
  padding-right: 1.5rem;
}

.cart-badge {
  position: absolute;
  top: 0;
  right: 5px;
  background-color: white;
  color: #FF8C00;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

/* Responsive styles */
@media (max-width: 991px) {
  .navbar-nav {
    text-align: center;
    padding-top: 1rem;
  }
  
  .dropdown-menu {
    text-align: center;
    background-color: rgba(255, 255, 255, 0.95);
  }
  
  .navbar-text {
    display: block;
    margin-left: 0;
    margin-top: 0.5rem;
  }
  
  .cart-link {
    display: inline-block;
    padding-right: 2rem;
  }
}

.navbar-toggler {
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.navbar-toggler-icon {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='rgba%28255, 255, 255, 0.75%29' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e");
}
</style>
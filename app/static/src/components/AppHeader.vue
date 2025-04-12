<template>
  <nav class="navbar navbar-expand-lg navbar-dark pelican-navbar">
    <div class="container">
      <router-link class="navbar-brand" to="/">Pelican Eats</router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/about">About</router-link>
          </li>
          
          <!-- Register dropdown -->
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="registerDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Register
            </a>
            <ul class="dropdown-menu" aria-labelledby="registerDropdown">
              <li><router-link class="dropdown-item" to="/register/personal">Sign up for personal account</router-link></li>
              <li><router-link class="dropdown-item" to="/register/restaurant">Register your restaurant</router-link></li>
              <li><router-link class="dropdown-item" to="/register/driver">Sign up as a driver</router-link></li>
            </ul>
          </li>
          
          <li class="nav-item">
            <router-link class="nav-link" to="/login">Login</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/delivery">Delivery</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
  
<!-- <script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isAuthenticated = ref(false);

// Function to check authentication status
const checkAuth = () => {
  // This would typically be a call to check a token in localStorage or a session cookie
  const token = localStorage.getItem('auth_token');
  isAuthenticated.value = !!token;
};

// Logout function
const logout = async () => {
  try {
    // Call your backend logout endpoint if needed
    await fetch('/api/v1/logout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
      }
    });
    
    // Clear local storage/cookies
    localStorage.removeItem('auth_token');
    isAuthenticated.value = false;
    
    // Redirect to home page
    router.push('/');
  } catch (error) {
    console.error('Logout failed:', error);
  }
};

// Check authentication status when component mounts
onMounted(() => {
  checkAuth();
  
  // Optional: listen for auth changes (could be from a global event bus)
  window.addEventListener('auth-change', checkAuth);
});
</script> -->
  
<style scoped>
.pelican-navbar {
  background-color:  #FF8C00; /* Dark Orange */
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
}
</style>

<!-- <template>
  <nav class="navbar navbar-expand-lg navbar-dark pelican-navbar">
    <div class="container">
      <router-link class="navbar-brand" to="/">Pelican Eats</router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/about">About</router-link>
          </li>
          Conditional navigation based on authentication
          <template v-if="isAuthenticated">
            <li class="nav-item">
              <router-link class="nav-link" to="/profile">My Profile</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/orders">My Orders</router-link>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#" @click.prevent="logout">Logout</a>
            </li>
          </template>
          <template v-else>
            <li class="nav-item">
              <router-link class="nav-link" to="/register">Register</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/login">Login</router-link>
            </li>
          </template>
          <li class="nav-item">
            <router-link class="nav-link" to="/locations">Delivery</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template> -->
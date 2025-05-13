<script setup>
import { RouterView, useRoute } from 'vue-router'
import { computed } from 'vue'
import AppHeader from "@/components/AppHeader.vue"
import AppFooter from "@/components/AppFooter.vue"
import RestaurantHeader from "@/components/RestaurantHeader.vue"
import GenUserHeader from "@/components/GenUserHeader.vue" // Add this import

const route = useRoute()

// Check if current route is a restaurant route
const isRestaurantRoute = computed(() => {
  return route.path.startsWith('/restaurant')
})

// Check if current route is a general user route
const isGenUserRoute = computed(() => {
  return route.path.startsWith('/gen') || route.path === '/orders' || route.path === '/grocery' || 
         route.path === '/profile' || route.path === '/settings' || route.path === '/cart'
})
</script>

<template>
  <!-- Conditional headers -->
  <RestaurantHeader v-if="isRestaurantRoute" />
  <GenUserHeader v-else-if="isGenUserRoute" />
  <AppHeader v-else />

  <main class="container">
    <RouterView />
  </main>
  
  <AppFooter />
</template>
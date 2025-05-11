<script setup>
import { RouterView, useRoute } from 'vue-router'
import { computed } from 'vue'
import AppHeader from "@/components/AppHeader.vue"
import AppFooter from "@/components/AppFooter.vue"
import RestaurantHeader from "@/components/RestaurantHeader.vue"

const route = useRoute()

// Check if current route is a restaurant route
const isRestaurantRoute = computed(() => {
  return route.path.startsWith('/restaurant')
})
</script>

<template>
  <!-- Conditional headers -->
  <RestaurantHeader v-if="isRestaurantRoute" />
  <AppHeader v-else />

  <main class="container">
    <RouterView />
  </main>
  
  <AppFooter />
</template>

<style>
body 
{
  padding-top: 75px;
}
</style>
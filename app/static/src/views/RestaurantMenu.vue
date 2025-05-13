<template>
  <div class="restaurant-menu">
    <h1>Restaurant Menu</h1>
    <div class="menu-controls">
      <router-link to="/restaurantmenu" class="btn btn-primary">Add New Item</router-link>
    </div>
    
    <div class="menu-items">
      <div v-if="loading" class="loading-indicator">Loading menu items...</div>
      <div v-else-if="error" class="error-message">{{ error }}</div>
      <p v-else-if="menuItems.length === 0">No menu items yet. Start by adding your first item!</p>
      
      <div v-else class="menu-grid">
        <div v-for="item in menuItems" :key="item.id" class="menu-item-card">
          <!-- Replace the current img with this conditional rendering -->
          <div v-if="item.image_url" class="item-image-container">
            <img 
              :src="item.image_url" 
              :alt="item.name" 
              class="item-image"
              @error="handleImageError($event, item)"
            >
          </div>
          <div v-else class="no-image-container">
            <span>No Image</span>
          </div>
          
          <div class="item-details">
            <h3>{{ item.name }}</h3>
            <p class="item-description">{{ item.description }}</p>
            <p class="item-price">${{ item.price.toFixed(2) }}</p>
            <div class="item-actions">
              <button class="btn btn-sm btn-edit" @click="editItem(item)">Edit</button>
              <button class="btn btn-sm btn-delete" @click="deleteItem(item.id)">Delete</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'
import { useRouter } from 'vue-router'

const router = useRouter()
const menuItems = ref([])
const loading = ref(true)
const error = ref(null)

/// Updated error handling
const handleImageError = (event, item) => {
  console.error(`Image failed to load for "${item.name}": ${item.image_url}`)
  
  // Try a different URL format if it's a path issue
  if (item.image_url?.startsWith('/uploads/')) {
    console.log("Trying alternative URL format...")
    const filename = item.image_url.split('/').pop()
    item.image_url = `/static/uploads/${filename}`
    return // Let the image try to load with the new URL
  }
  
  // If we've already tried alternative formats or it's not a path issue
  console.log("Showing no-image placeholder")
  item.image_url = null
}

// Function to load menu items
const loadMenuItems = async () => {
  try {
    loading.value = true
    
    // Try to get the current user to check if they're a restaurant owner
    let isRestaurant = false
    try {
      const userResponse = await api.get('/current-user')
      isRestaurant = userResponse?.user?.user_type === 'restaurant'
    } catch (err) {
      console.log("Not logged in or not a restaurant owner")
    }
    
    let response
    if (isRestaurant) {
      // Restaurant owners see only their products
      response = await api.get('/restaurant/products')
    } else {
      // General users see all products
      response = await api.get('/menu/products')
    }
    
    menuItems.value = response.products || []
    console.log("Loaded menu items:", menuItems.value)
    
  } catch (err) {
    console.error('Failed to fetch menu items:', err)
    error.value = 'Failed to load menu items. Please try again.'
  } finally {
    loading.value = false
  }
}

// Load menu items when component mounts
onMounted(() => {
  loadMenuItems()
})

// Delete function
const deleteItem = async (productId) => {
  if (confirm('Are you sure you want to delete this menu item?')) {
    try {
      await api.delete(`/restaurant/products/${productId}`)
      // Remove the deleted item from the array
      menuItems.value = menuItems.value.filter(item => item.id !== productId)
    } catch (err) {
      console.error('Failed to delete product:', err)
      alert('Failed to delete the product. Please try again.')
    }
  }
}

// Edit function
const editItem = (item) => {
  router.push(`/restaurantmenu/edit/${item.id}`)
}
</script>

<style scoped>


.restaurant-menu {
  padding: 20px;
}

.menu-controls {
  margin-bottom: 20px;
}

.btn {
  display: inline-block;
  padding: 8px 16px;
  background-color: #FF8C00;
  color: white;
  text-decoration: none;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn:hover {
  background-color: #e67e00;
}

.btn-primary {
  background-color: #FF8C00;
}

.btn-sm {
  padding: 4px 8px;
  font-size: 12px;
}

.btn-edit {
  background-color: #0d6efd;
  margin-right: 5px;
}

.btn-delete {
  background-color: #dc3545;
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.menu-item-card {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  overflow: hidden;
  transition: box-shadow 0.3s;
}

.menu-item-card:hover {
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.item-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.item-details {
  padding: 15px;
}

.item-description {
  color: #6c757d;
  font-size: 14px;
  margin: 5px 0;
}

.item-price {
  font-weight: bold;
  color: #FF8C00;
  font-size: 18px;
  margin: 10px 0;
}

.item-actions {
  display: flex;
  gap: 5px;
}

.loading-indicator {
  text-align: center;
  padding: 20px;
  color: #666;
}

.error-message {
  padding: 10px;
  background-color: #fee2e2;
  color: #991b1b;
  border: 1px solid #fecaca;
  border-radius: 4px;
  margin-bottom: 20px;
}

.item-image-container, .no-image-container {
  width: 100%;
  height: 150px;
  overflow: hidden;
}

.no-image-container {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f0f0;
  color: #667;
  font-style: italic;
}
</style>
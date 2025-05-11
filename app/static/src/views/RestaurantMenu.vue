<template>
  <div class="restaurant-menu">
    <h1>Restaurant Menu</h1>
    <div class="menu-controls">
      <router-link to="/restaurantmenu" class="btn btn-primary">Add New Item</router-link>
    </div>
    
    <div class="menu-items">
      <p v-if="menuItems.length === 0">No menu items yet. Start by adding your first item!</p>
      
      <div v-else class="menu-grid">
        <div v-for="item in menuItems" :key="item.id" class="menu-item-card">
          <img :src="item.image || '/api/placeholder/200/150'" :alt="item.name" class="item-image">
          <div class="item-details">
            <h3>{{ item.name }}</h3>
            <p class="item-description">{{ item.description }}</p>
            <p class="item-price">${{ item.price.toFixed(2) }}</p>
            <div class="item-actions">
              <button class="btn btn-sm btn-edit">Edit</button>
              <button class="btn btn-sm btn-delete">Delete</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Sample menu items - replace with actual data from backend
const menuItems = ref([
  // {
  //   id: 1,
  //   name: 'Sample Burger',
  //   description: 'Delicious beef burger with cheese',
  //   price: 9.99,
  //   image: '/images/burger.jpg'
  // }
])
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
</style>
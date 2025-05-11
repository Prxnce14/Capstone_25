<template>
  <div class="restaurant-dashboard">
    <h1>Restaurant Dashboard</h1>
    <div class="dashboard-content">
      <p>Welcome to your restaurant management dashboard!</p>
      
      <div class="dashboard-cards">
        <div class="card">
          <h3>Today's Orders</h3>
          <p class="stat">0</p>
        </div>
        
        <div class="card">
          <h3>Today's Revenue</h3>
          <p class="stat">$0.00</p>
        </div>
        
        <div class="card">
          <h3>Menu Items</h3>
          <p class="stat">0</p>
        </div>
      </div>
      
      <div class="quick-actions">
        <h2>Quick Actions</h2>
        <router-link to="/restaurant/menu" class="btn">View Menu</router-link>
        <router-link to="/restaurantmenu" class="btn">Add Product</router-link>
        <router-link to="/restaurant/orders" class="btn">View Orders</router-link>
        <router-link to="/restaurant/sales" class="btn">Sales Report</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
// Add any dashboard logic here
</script>

<style scoped>
.restaurant-dashboard {
  padding: 20px;
}

.dashboard-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.card {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
}

.stat {
  font-size: 24px;
  font-weight: bold;
  color: #FF8C00;
  margin: 10px 0;
}

.quick-actions {
  margin-top: 40px;
}

.btn {
  display: inline-block;
  padding: 10px 20px;
  margin: 5px;
  background-color: #FF8C00;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #e67e00;
}
</style>
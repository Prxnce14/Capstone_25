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
import { ref, onMounted } from 'vue'
import api from '@/api'

const loading = ref(false)
const error = ref(null)
const dashboardData = ref({
  todayOrders: 0,
  todayRevenue: 0,
  menuItems: 0
})

// Load dashboard data when component mounts
onMounted(async () => {
  await loadDashboardData()
})

// Load dashboard data from the server
async function loadDashboardData() {
  loading.value = true
  error.value = null
  
  try {
    // Try to get dashboard stats and menu items
    const [statsResponse, menuResponse] = await Promise.all([
      // You'll need to create these endpoints in your backend
      api.get('/restaurant/dashboard/stats').catch(() => ({ data: {} })),
      api.get('/restaurant/products')
    ])
    
    dashboardData.value = {
      todayOrders: statsResponse.data?.todayOrders || 0,
      todayRevenue: statsResponse.data?.todayRevenue || 0,
      menuItems: menuResponse.data?.products?.length || 0
    }
  } catch (err) {
    console.error('Error loading dashboard data:', err)
    error.value = 'Failed to load dashboard data. Please try again.'
    
    // Set default values on error
    dashboardData.value = {
      todayOrders: 0,
      todayRevenue: 0,
      menuItems: 0
    }
  } finally {
    loading.value = false
  }
}
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
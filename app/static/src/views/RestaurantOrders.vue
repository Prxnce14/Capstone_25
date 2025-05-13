<template>
  <div class="restaurant-orders">
    <h1>Restaurant Orders</h1>
    
    <div class="orders-filters">
      <button :class="['btn', { active: filter === 'all' }]" @click="setFilter('all')">All Orders</button>
      <button :class="['btn', { active: filter === 'pending' }]" @click="setFilter('pending')">Pending</button>
      <button :class="['btn', { active: filter === 'preparing' }]" @click="setFilter('preparing')">Preparing</button>
      <button :class="['btn', { active: filter === 'ready' }]" @click="setFilter('ready')">Ready</button>
      <button :class="['btn', { active: filter === 'completed' }]" @click="setFilter('completed')">Completed</button>
    </div>
    
    <div class="orders-list">
      <p v-if="filteredOrders.length === 0">No orders found.</p>
      
      <div v-else>
        <div v-for="order in filteredOrders" :key="order.id" class="order-card">
          <div class="order-header">
            <div>
              <h3>Order #{{ order.id }}</h3>
              <p class="order-time">{{ formatTime(order.createdAt) }}</p>
            </div>
            <span :class="['status-badge', order.status]">{{ order.status }}</span>
          </div>
          
          <div class="order-details">
            <p><strong>Customer:</strong> {{ order.customerName }}</p>
            <p><strong>Total:</strong> ${{ order.total.toFixed(2) }}</p>
            
            <div class="order-items">
              <h4>Items:</h4>
              <ul>
                <li v-for="item in order.items" :key="item.id">
                  {{ item.quantity }}x {{ item.name }} - ${{ (item.price * item.quantity).toFixed(2) }}
                </li>
              </ul>
            </div>
          </div>
          
          <div class="order-actions">
            <button v-if="order.status === 'pending'" class="btn btn-accept" @click="updateOrderStatus(order.id, 'preparing')">
              Accept Order
            </button>
            <button v-if="order.status === 'preparing'" class="btn btn-ready" @click="updateOrderStatus(order.id, 'ready')">
              Mark as Ready
            </button>
            <button v-if="order.status === 'ready'" class="btn btn-complete" @click="updateOrderStatus(order.id, 'completed')">
              Complete Order
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/api'

const orders = ref([])
const loading = ref(false)
const error = ref(null)
const filter = ref('all')
const updatingOrder = ref(null)

const filteredOrders = computed(() => {
  if (filter.value === 'all') {
    return orders.value
  }
  return orders.value.filter(order => order.status === filter.value)
})

onMounted(() => {
  loadOrders()
})

const setFilter = (newFilter) => {
  filter.value = newFilter
}

async function loadOrders() {
  loading.value = true
  error.value = null
  
  try {
    const response = await api.get('/restaurant/orders')
    orders.value = response.data?.orders || []
  } catch (err) {
    console.error('Error loading orders:', err)
    error.value = 'Failed to load orders. Please try again.'
    orders.value = []
  } finally {
    loading.value = false
  }
}

async function updateOrderStatus(orderId, newStatus) {
  updatingOrder.value = orderId
  
  try {
    await api.put(`/restaurant/orders/${orderId}`, { status: newStatus })
    
    // Update local order status
    const orderIndex = orders.value.findIndex(o => o.id === orderId)
    if (orderIndex !== -1) {
      orders.value[orderIndex].status = newStatus
    }
  } catch (err) {
    console.error('Error updating order status:', err)
    error.value = 'Failed to update order status. Please try again.'
  } finally {
    updatingOrder.value = null
  }
}

const formatTime = (date) => {
  return new Date(date).toLocaleTimeString()
}
</script>

<style scoped>
.restaurant-orders {
  padding: 20px;
}

.orders-filters {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.btn {
  padding: 8px 16px;
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn.active {
  background-color: #FF8C00;
  color: white;
  border-color: #FF8C00;
}

.order-card {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  margin-bottom: 20px;
  padding: 20px;
  background: white;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.order-time {
  color: #6c757d;
  font-size: 14px;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  text-transform: capitalize;
}

.status-badge.pending {
  background-color: #ffc107;
  color: #000;
}

.status-badge.preparing {
  background-color: #0d6efd;
  color: white;
}

.status-badge.ready {
  background-color: #198754;
  color: white;
}

.status-badge.completed {
  background-color: #6c757d;
  color: white;
}

.order-details {
  margin-bottom: 15px;
}

.order-items {
  margin-top: 10px;
}

.order-items ul {
  list-style: none;
  padding-left: 0;
  margin: 5px 0;
}

.order-items li {
  padding: 2px 0;
}

.order-actions {
  display: flex;
  gap: 10px;
}

.btn-accept {
  background-color: #0d6efd;
  color: white;
}

.btn-ready {
  background-color: #198754;
  color: white;
}

.btn-complete {
  background-color: #6c757d;
  color: white;
}

.btn-accept:hover,
.btn-ready:hover,
.btn-complete:hover {
  opacity: 0.9;
}
</style>
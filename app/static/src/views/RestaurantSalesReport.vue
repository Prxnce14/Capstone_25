<template>
  <div class="restaurant-sales-report">
    <h1>Sales Report</h1>
    
    <div class="report-filters">
      <div class="filter-group">
        <label for="date-range">Date Range:</label>
        <select id="date-range" v-model="selectedDateRange" class="form-select">
          <option value="today">Today</option>
          <option value="week">This Week</option>
          <option value="month">This Month</option>
          <option value="custom">Custom Range</option>
        </select>
      </div>
      
      <div v-if="selectedDateRange === 'custom'" class="custom-date-range">
        <input type="date" v-model="customStartDate" class="form-input">
        <input type="date" v-model="customEndDate" class="form-input">
      </div>
      
      <button class="btn btn-primary" @click="generateReport">Generate Report</button>
    </div>
    
    <div class="sales-summary">
      <div class="summary-card">
        <h3>Total Revenue</h3>
        <p class="stat">${{ salesData.totalRevenue.toFixed(2) }}</p>
      </div>
      
      <div class="summary-card">
        <h3>Total Orders</h3>
        <p class="stat">{{ salesData.totalOrders }}</p>
      </div>
      
      <div class="summary-card">
        <h3>Average Order Value</h3>
        <p class="stat">${{ salesData.averageOrderValue.toFixed(2) }}</p>
      </div>
      
      <div class="summary-card">
        <h3>Top Selling Item</h3>
        <p class="stat">{{ salesData.topItem || 'N/A' }}</p>
      </div>
    </div>
    
    <div class="sales-charts">
      <div class="chart-container">
        <h3>Sales Trend</h3>
        <div class="chart-placeholder">
          <p>Sales chart will be displayed here</p>
          <!-- TODO: Integrate a charting library like Chart.js -->
        </div>
      </div>
      
      <div class="chart-container">
        <h3>Top Selling Items</h3>
        <div class="top-items-list">
          <div v-for="item in salesData.topItems" :key="item.id" class="top-item">
            <span class="item-name">{{ item.name }}</span>
            <span class="item-quantity">{{ item.quantity }} sold</span>
            <span class="item-revenue">${{ item.revenue.toFixed(2) }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <div class="sales-table">
      <h3>Recent Orders</h3>
      <table class="table">
        <thead>
          <tr>
            <th>Order ID</th>
            <th>Date</th>
            <th>Customer</th>
            <th>Items</th>
            <th>Total</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in salesData.recentOrders" :key="order.id">
            <td>#{{ order.id }}</td>
            <td>{{ formatDate(order.date) }}</td>
            <td>{{ order.customer }}</td>
            <td>{{ order.itemCount }} items</td>
            <td>${{ order.total.toFixed(2) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const selectedDateRange = ref('today')
const customStartDate = ref('')
const customEndDate = ref('')

// Sample sales data - replace with actual data from backend
const salesData = reactive({
  totalRevenue: 0,
  totalOrders: 0,
  averageOrderValue: 0,
  topItem: '',
  topItems: [
    // { id: 1, name: 'Burger', quantity: 25, revenue: 249.75 }
  ],
  recentOrders: [
    // { id: '001', date: new Date(), customer: 'John Doe', itemCount: 2, total: 15.50 }
  ]
})

const generateReport = () => {
  // TODO: Fetch data from backend based on selected date range
  console.log('Generating report for:', selectedDateRange.value)
  
  // Simulate loading data
  salesData.totalRevenue = 1234.56
  salesData.totalOrders = 45
  salesData.averageOrderValue = salesData.totalRevenue / salesData.totalOrders
  salesData.topItem = 'Burger'
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString()
}

// Generate initial report
generateReport()
</script>

<style scoped>
.restaurant-sales-report {
  padding: 20px;
}

.report-filters {
  display: flex;
  gap: 20px;
  align-items: flex-end;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-select,
.form-input {
  padding: 8px;
  border: 1px solid #dee2e6;
  border-radius: 4px;
}

.custom-date-range {
  display: flex;
  gap: 10px;
}

.btn {
  padding: 8px 16px;
  background-color: #FF8C00;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn:hover {
  background-color: #e67e00;
}

.sales-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.summary-card {
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

.sales-charts {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 40px;
}

@media (max-width: 768px) {
  .sales-charts {
    grid-template-columns: 1fr;
  }
}

.chart-container {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
}

.chart-placeholder {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6c757d;
}

.top-items-list {
  margin-top: 15px;
}

.top-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #dee2e6;
}

.item-name {
  font-weight: 500;
}

.item-quantity {
  color: #6c757d;
}

.item-revenue {
  color: #FF8C00;
  font-weight: bold;
}

.sales-table {
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
}

.table th,
.table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}

.table th {
  background-color: #f8f9fa;
  font-weight: 600;
}

.table tr:hover {
  background-color: #f8f9fa;
}
</style>
<template>
  <div class="orders-page">
    <GenUserHeader :cartCount="cartCount" />
    
    <div class="main-content">
      <h1 class="page-title">My Orders</h1>
      
      <!-- Tabs for Active and Past Orders -->
      <div class="tabs-container">
        <div 
          class="tab" 
          :class="{ active: activeTab === 'current' }"
          @click="activeTab = 'current'"
        >
          Current Orders
          <span v-if="activeOrders.length > 0" class="badge">{{ activeOrders.length }}</span>
        </div>
        <div 
          class="tab" 
          :class="{ active: activeTab === 'past' }"
          @click="activeTab = 'past'"
        >
          Past Orders
        </div>
      </div>
      
      <!-- Loading Indicator -->
      <div v-if="isLoading" class="loading-indicator">
        <div class="loading-spinner"></div>
        <p>Loading your orders...</p>
      </div>
      
      <!-- Error Message -->
      <div v-else-if="error" class="error-message">
        <i class="fas fa-exclamation-circle"></i>
        <p>{{ error }}</p>
        <button @click="fetchOrders" class="retry-button">Try Again</button>
      </div>
      
      <!-- Current Orders Tab Content -->
      <div v-else-if="activeTab === 'current'" class="tab-content">
        <div v-if="activeOrders.length === 0" class="empty-state">
          <div class="empty-icon">
            <i class="fas fa-shopping-bag"></i>
          </div>
          <h3>No active orders</h3>
          <p>You don't have any ongoing orders at the moment.</p>
          <router-link to="/gen/dashboard" class="browse-button">Browse Restaurants</router-link>
        </div>
        
        <div v-else class="orders-list">
          <div v-for="order in activeOrders" :key="order.id" class="order-card">
            <!-- Order Header -->
            <div class="order-header">
              <div class="order-restaurant">
                <img :src="order.restaurant_image || 'https://via.placeholder.com/50x50'" :alt="order.restaurant_name" class="restaurant-logo" />
                <div class="restaurant-details">
                  <h3>{{ order.restaurant_name }}</h3>
                  <p class="order-id">Order #{{ order.order_number }}</p>
                </div>
              </div>
              
              <div class="order-status" :class="getStatusClass(order.status)">
                {{ getStatusText(order.status) }}
              </div>
            </div>
            
            <!-- Order Progress -->
            <div class="order-progress">
              <div class="progress-bar">
                <div class="progress-steps">
                  <div 
                    v-for="(step, index) in orderSteps" 
                    :key="step.id"
                    class="progress-step"
                    :class="{ 
                      active: getStepNumber(order.status) >= index,
                      current: getStepNumber(order.status) === index
                    }"
                  >
                    <div class="step-circle">
                      <i :class="step.icon"></i>
                    </div>
                    <span class="step-label">{{ step.label }}</span>
                  </div>
                </div>
                <div class="progress-line">
                  <div 
                    class="progress-fill"
                    :style="{ width: getProgressPercentage(order.status) + '%' }"
                  ></div>
                </div>
              </div>
              
              <!-- Estimated Time -->
              <div class="estimated-time">
                <i class="fas fa-clock"></i>
                <span>Estimated arrival: {{ formatDeliveryTime(order.estimated_delivery_time) }}</span>
              </div>
            </div>
            
            <!-- Order Content -->
            <div class="order-content">
              <div class="order-items">
                <h4>Order Summary</h4>
                <ul class="items-list">
                  <li v-for="(item, index) in order.items.slice(0, 3)" :key="index">
                    <span class="item-quantity">{{ item.quantity }}x</span>
                    <span class="item-name">{{ item.name }}</span>
                    <span class="item-price">${{ (item.price * item.quantity).toFixed(2) }}</span>
                  </li>
                  
                  <li v-if="order.items.length > 3" class="more-items">
                    <span>+{{ order.items.length - 3 }} more items</span>
                  </li>
                </ul>
              </div>
              
              <div class="order-total">
                <div class="total-row">
                  <span>Subtotal</span>
                  <span>${{ order.subtotal.toFixed(2) }}</span>
                </div>
                <div class="total-row">
                  <span>Delivery Fee</span>
                  <span>${{ order.delivery_fee.toFixed(2) }}</span>
                </div>
                <div v-if="order.discount > 0" class="total-row discount">
                  <span>Discount</span>
                  <span>-${{ order.discount.toFixed(2) }}</span>
                </div>
                <div class="total-row grand-total">
                  <span>Total</span>
                  <span>${{ order.total.toFixed(2) }}</span>
                </div>
              </div>
            </div>
            
            <!-- Order Actions -->
            <div class="order-actions">
              <div v-if="order.status === 'delivered'" class="action-buttons">
                <button class="btn-reorder" @click="reorderItems(order)">
                  <i class="fas fa-redo"></i> Reorder
                </button>
                <button class="btn-review" v-if="!order.is_reviewed" @click="openReviewModal(order)">
                  <i class="fas fa-star"></i> Leave Review
                </button>
              </div>
              
              <div v-else-if="order.status !== 'cancelled'" class="action-buttons">
                <button class="btn-track" @click="trackOrder(order.id)">
                  <i class="fas fa-map-marker-alt"></i> Track Order
                </button>
                <button v-if="canCancel(order.status)" class="btn-cancel" @click="cancelOrder(order.id)">
                  <i class="fas fa-times"></i> Cancel
                </button>
              </div>
              
              <button class="btn-support" @click="contactSupport(order.id)">
                <i class="fas fa-headset"></i> Contact Support
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Past Orders Tab Content -->
      <div v-else-if="activeTab === 'past'" class="tab-content">
        <div v-if="pastOrders.length === 0" class="empty-state">
          <div class="empty-icon">
            <i class="fas fa-history"></i>
          </div>
          <h3>No order history</h3>
          <p>You haven't placed any orders yet.</p>
          <router-link to="/gen/dashboard" class="browse-button">Order Now</router-link>
        </div>
        
        <div v-else class="orders-list past-orders">
          <div v-for="order in pastOrders" :key="order.id" class="order-card past-order">
            <!-- Order Header -->
            <div class="order-header">
              <div class="order-restaurant">
                <img :src="order.restaurant_image || 'https://via.placeholder.com/50x50'" :alt="order.restaurant_name" class="restaurant-logo" />
                <div class="restaurant-details">
                  <h3>{{ order.restaurant_name }}</h3>
                  <p class="order-date">{{ formatOrderDate(order.completed_at || order.created_at) }}</p>
                </div>
              </div>
              
              <div class="order-status" :class="getStatusClass(order.status)">
                {{ getStatusText(order.status) }}
              </div>
            </div>
            
            <!-- Order Content Summary -->
            <div class="order-summary">
              <div class="summary-items">
                <span v-for="(item, index) in getSummaryItems(order.items)" :key="index">
                  {{ item }}{{ index < getSummaryItems(order.items).length - 1 ? ', ' : '' }}
                </span>
              </div>
              
              <div class="summary-total">
                <span>${{ order.total.toFixed(2) }}</span>
              </div>
            </div>
            
            <!-- Order Actions -->
            <div class="order-actions">
              <button class="btn-view-details" @click="viewOrderDetails(order)">
                View Details
              </button>
              
              <button class="btn-reorder" @click="reorderItems(order)">
                <i class="fas fa-redo"></i> Reorder
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Review Modal -->
    <div v-if="showReviewModal" class="modal-overlay" @click="closeReviewModal">
      <div class="review-modal" @click.stop>
        <div class="modal-header">
          <h3>Review your order</h3>
          <button class="close-btn" @click="closeReviewModal">
            <i class="fas fa-times"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="review-restaurant">
            <img 
              :src="currentReviewOrder.restaurant_image || 'https://via.placeholder.com/50x50'" 
              :alt="currentReviewOrder.restaurant_name" 
              class="restaurant-logo" 
            />
            <h4>{{ currentReviewOrder.restaurant_name }}</h4>
          </div>
          
          <div class="rating-section">
            <h5>Rate your experience</h5>
            <div class="star-rating">
              <button 
                v-for="star in 5" 
                :key="star"
                class="star-btn"
                :class="{ active: review.rating >= star }"
                @click="review.rating = star"
              >
                <i class="fas fa-star"></i>
              </button>
            </div>
          </div>
          
          <div class="form-group">
            <label>Add a comment (optional)</label>
            <textarea 
              v-model="review.comment" 
              placeholder="Tell us about your experience..."
              rows="4"
            ></textarea>
          </div>
          
          <div class="form-group">
            <label>Food quality</label>
            <div class="rating-bar">
              <button 
                v-for="value in 5" 
                :key="'food-'+value"
                class="rating-btn"
                :class="{ active: review.foodRating >= value }"
                @click="review.foodRating = value"
              >
                {{ value }}
              </button>
            </div>
          </div>
          
          <div class="form-group">
            <label>Delivery speed</label>
            <div class="rating-bar">
              <button 
                v-for="value in 5" 
                :key="'delivery-'+value"
                class="rating-btn"
                :class="{ active: review.deliveryRating >= value }"
                @click="review.deliveryRating = value"
              >
                {{ value }}
              </button>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button class="btn-cancel" @click="closeReviewModal">Cancel</button>
          <button 
            class="btn-submit" 
            @click="submitReview"
            :disabled="!review.rating"
          >
            Submit Review
          </button>
        </div>
      </div>
    </div>
    
    <!-- Order Details Modal -->
    <div v-if="showDetailsModal" class="modal-overlay" @click="closeDetailsModal">
      <div class="details-modal" @click.stop>
        <div class="modal-header">
          <h3>Order Details</h3>
          <button class="close-btn" @click="closeDetailsModal">
            <i class="fas fa-times"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="details-header">
            <div class="details-restaurant">
              <img 
                :src="selectedOrder.restaurant_image || 'https://via.placeholder.com/50x50'" 
                :alt="selectedOrder.restaurant_name" 
                class="restaurant-logo" 
              />
              <div>
                <h4>{{ selectedOrder.restaurant_name }}</h4>
                <p class="order-date">{{ formatOrderDate(selectedOrder.completed_at || selectedOrder.created_at) }}</p>
              </div>
            </div>
            
            <div class="details-info">
              <p>Order #{{ selectedOrder.order_number }}</p>
              <div class="order-status" :class="getStatusClass(selectedOrder.status)">
                {{ getStatusText(selectedOrder.status) }}
              </div>
            </div>
          </div>
          
          <div class="order-address">
            <div>
              <h5>Delivery Address</h5>
              <p>{{ selectedOrder.delivery_address }}</p>
            </div>
            
            <div v-if="selectedOrder.status === 'delivered'">
              <h5>Delivered on</h5>
              <p>{{ formatOrderDateTime(selectedOrder.completed_at) }}</p>
            </div>
          </div>
          
          <div class="details-items">
            <h5>Items Ordered</h5>
            <ul class="items-list">
              <li v-for="(item, index) in selectedOrder.items" :key="index">
                <span class="item-quantity">{{ item.quantity }}x</span>
                <span class="item-name">{{ item.name }}</span>
                <span class="item-price">${{ (item.price * item.quantity).toFixed(2) }}</span>
              </li>
            </ul>
          </div>
          
          <div class="details-payment">
            <h5>Payment Summary</h5>
            <div class="total-row">
              <span>Subtotal</span>
              <span>${{ selectedOrder.subtotal.toFixed(2) }}</span>
            </div>
            <div class="total-row">
              <span>Delivery Fee</span>
              <span>${{ selectedOrder.delivery_fee.toFixed(2) }}</span>
            </div>
            <div v-if="selectedOrder.discount > 0" class="total-row discount">
              <span>Discount</span>
              <span>-${{ selectedOrder.discount.toFixed(2) }}</span>
            </div>
            <div class="total-row">
              <span>Tax</span>
              <span>${{ selectedOrder.tax.toFixed(2) }}</span>
            </div>
            <div class="total-row grand-total">
              <span>Total</span>
              <span>${{ selectedOrder.total.toFixed(2) }}</span>
            </div>
            <div class="payment-method">
              <span>Paid with {{ selectedOrder.payment_method }}</span>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button class="btn-support" @click="contactSupport(selectedOrder.id)">
            <i class="fas fa-headset"></i> Contact Support
          </button>
          <button class="btn-reorder" @click="reorderItems(selectedOrder)">
            <i class="fas fa-redo"></i> Reorder
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import GenUserHeader from '../components/GenUserHeader.vue';
import { ref, reactive, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'OrdersPage',
  components: {
    GenUserHeader
  },
  setup() {
    const router = useRouter();
    
    // State
    const activeTab = ref('current');
    const isLoading = ref(true);
    const error = ref(null);
    const allOrders = ref([]);
    const cartCount = ref(0);
    
    // Review modal
    const showReviewModal = ref(false);
    const currentReviewOrder = ref({});
    const review = reactive({
      rating: 0,
      comment: '',
      foodRating: 0,
      deliveryRating: 0
    });
    
    // Details modal
    const showDetailsModal = ref(false);
    const selectedOrder = ref({});
    
    // Order status steps
    const orderSteps = [
      { id: 'placed', label: 'Order Placed', icon: 'fas fa-receipt' },
      { id: 'confirmed', label: 'Confirmed', icon: 'fas fa-check-circle' },
      { id: 'preparing', label: 'Preparing', icon: 'fas fa-utensils' },
      { id: 'ready', label: 'Ready for Pickup', icon: 'fas fa-shopping-bag' },
      { id: 'pickup', label: 'Picked Up', icon: 'fas fa-motorcycle' },
      { id: 'delivered', label: 'Delivered', icon: 'fas fa-home' }
    ];
    
    // Computed properties
    const activeOrders = computed(() => {
      return allOrders.value.filter(order => 
        ['placed', 'confirmed', 'preparing', 'ready', 'pickup', 'out_for_delivery'].includes(order.status)
      );
    });
    
    const pastOrders = computed(() => {
      return allOrders.value.filter(order => 
        ['delivered', 'cancelled'].includes(order.status)
      ).sort((a, b) => new Date(b.completed_at || b.created_at) - new Date(a.completed_at || a.created_at));
    });
    
    // Methods
    const fetchOrders = async () => {
      try {
        isLoading.value = true;
        error.value = null;
        
        // Make API call
        const response = await fetch('/api/orders');
        
        if (!response.ok) {
          throw new Error('Failed to fetch orders');
        }
        
        const data = await response.json();
        allOrders.value = data.orders || [];
        
        // If API is not ready, use mock data
        if (allOrders.value.length === 0) {
          useMockOrders();
        }
      } catch (err) {
        console.error('Error fetching orders:', err);
        error.value = 'Unable to load your orders. Please try again.';
        // Use mock data for development
        useMockOrders();
      } finally {
        isLoading.value = false;
      }
    };
    
    // Mock orders for development
    const useMockOrders = () => {
      allOrders.value = [
        {
          id: 1001,
          order_number: '10124',
          status: 'out_for_delivery',
          restaurant_name: 'Island Jerk Spot',
          restaurant_image: 'https://via.placeholder.com/50x50/FF8C00/FFFFFF?text=IJ',
          created_at: new Date(Date.now() - 45 * 60000).toISOString(), // 45 mins ago
          estimated_delivery_time: new Date(Date.now() + 15 * 60000).toISOString(), // 15 mins from now
          delivery_address: 'AZ Preston Hall, UWI Mona Campus, Kingston',
          items: [
            { name: 'Jerk Chicken Meal', quantity: 1, price: 12.99 },
            { name: 'Rice and Peas', quantity: 1, price: 3.50 },
            { name: 'Festival', quantity: 2, price: 1.99 }
          ],
          subtotal: 20.47,
          delivery_fee: 3.99,
          discount: 0,
          tax: 2.05,
          total: 26.51,
          payment_method: 'Credit Card ****1234',
          is_reviewed: false
        },
        {
          id: 1002,
          order_number: '10098',
          status: 'delivered',
          restaurant_name: 'Pizza Paradise',
          restaurant_image: 'https://via.placeholder.com/50x50/FF8C00/FFFFFF?text=PP',
          created_at: new Date(Date.now() - 3 * 24 * 60 * 60000).toISOString(), // 3 days ago
          completed_at: new Date(Date.now() - 3 * 24 * 60 * 60000 + 50 * 60000).toISOString(), // 3 days ago + 50 mins
          delivery_address: 'AZ Preston Hall, UWI Mona Campus, Kingston',
          items: [
            { name: 'Large Pepperoni Pizza', quantity: 1, price: 15.99 },
            { name: 'Garlic Bread', quantity: 1, price: 4.50 },
            { name: 'Soda', quantity: 2, price: 1.99 }
          ],
          subtotal: 24.47,
          delivery_fee: 2.99,
          discount: 5.00,
          tax: 2.25,
          total: 24.71,
          payment_method: 'Cash on Delivery',
          is_reviewed: true
        },
        {
          id: 1003,
          order_number: '10075',
          status: 'cancelled',
          restaurant_name: 'Burger Joint',
          restaurant_image: 'https://via.placeholder.com/50x50/FF8C00/FFFFFF?text=BJ',
          created_at: new Date(Date.now() - 7 * 24 * 60 * 60000).toISOString(), // 7 days ago
          completed_at: new Date(Date.now() - 7 * 24 * 60 * 60000 + 10 * 60000).toISOString(), // 7 days ago + 10 mins
          delivery_address: 'AZ Preston Hall, UWI Mona Campus, Kingston',
          items: [
            { name: 'Double Beef Burger', quantity: 1, price: 9.99 },
            { name: 'French Fries', quantity: 1, price: 3.50 },
            { name: 'Milkshake', quantity: 1, price: 4.99 }
          ],
          subtotal: 18.48,
          delivery_fee: 3.99,
          discount: 0,
          tax: 1.85,
          total: 24.32,
          payment_method: 'Credit Card ****5678',
          is_reviewed: false
        },
        {
          id: 1004,
          order_number: '10056',
          status: 'delivered',
          restaurant_name: 'Green Leaf Salads',
          restaurant_image: 'https://via.placeholder.com/50x50/FF8C00/FFFFFF?text=GL',
          created_at: new Date(Date.now() - 14 * 24 * 60 * 60000).toISOString(), // 14 days ago
          completed_at: new Date(Date.now() - 14 * 24 * 60 * 60000 + 45 * 60000).toISOString(), // 14 days ago + 45 mins
          delivery_address: 'AZ Preston Hall, UWI Mona Campus, Kingston',
          items: [
            { name: 'Greek Salad', quantity: 1, price: 10.99 },
            { name: 'Fruit Smoothie', quantity: 1, price: 5.50 }
          ],
          subtotal: 16.49,
          delivery_fee: 3.99,
          discount: 0,
          tax: 1.65,
          total: 22.13,
          payment_method: 'Credit Card ****9012',
          is_reviewed: true
        }
      ];
    };
    
    // Format delivery time
    const formatDeliveryTime = (time) => {
      if (!time) return 'Unknown';
      
      const date = new Date(time);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    };
    
    // Format order date
    const formatOrderDate = (time) => {
      if (!time) return '';
      
      const date = new Date(time);
      const now = new Date();
      const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24));
      
      if (diffDays === 0) {
        return 'Today';
      } else if (diffDays === 1) {
        return 'Yesterday';
      } else if (diffDays < 7) {
        return `${diffDays} days ago`;
      } else {
        return date.toLocaleDateString();
      }
    };
    
    // Format detailed date time
    const formatOrderDateTime = (time) => {
      if (!time) return '';
      
      const date = new Date(time);
      return date.toLocaleString([], { 
        weekday: 'short',
        month: 'short', 
        day: 'numeric',
        hour: '2-digit', 
        minute: '2-digit'
      });
    };
    
    // Get status class for styling
    const getStatusClass = (status) => {
      const statusMap = {
        'placed': 'status-placed',
        'confirmed': 'status-confirmed',
        'preparing': 'status-preparing',
        'ready': 'status-ready',
        'pickup': 'status-pickup',
        'out_for_delivery': 'status-delivery',
        'delivered': 'status-delivered',
        'cancelled': 'status-cancelled'
      };
      
      return statusMap[status] || '';
    };
    
    // Get status text for display
    const getStatusText = (status) => {
      const statusMap = {
        'placed': 'Order Placed',
        'confirmed': 'Confirmed',
        'preparing': 'Preparing',
        'ready': 'Ready for Pickup',
        'pickup': 'Picked Up',
        'out_for_delivery': 'Out for Delivery',
        'delivered': 'Delivered',
        'cancelled': 'Cancelled'
      };
      
      return statusMap[status] || status;
    };
    
    // Get step number for progress bar
    const getStepNumber = (status) => {
      const statusIndex = {
        'placed': 0,
        'confirmed': 1,
        'preparing': 2,
        'ready': 3,
        'pickup': 4,
        'out_for_delivery': 4,
        'delivered': 5,
        'cancelled': -1
      };
      
      return statusIndex[status] || 0;
    };
    
    // Get progress percentage for progress bar
    const getProgressPercentage = (status) => {
      const stepNumber = getStepNumber(status);
      if (stepNumber === -1) return 0; // Cancelled
      
      return Math.min(100, (stepNumber / (orderSteps.length - 1)) * 100);
    };
    
    // Check if order can be cancelled
    const canCancel = (status) => {
      return ['placed', 'confirmed'].includes(status);
    };
    
    // Get summary items for past orders
    const getSummaryItems = (items) => {
      if (!items || items.length === 0) return [];
      
      return items.slice(0, 2).map(item => {
        if (item.quantity > 1) {
          return `${item.quantity}x ${item.name}`;
        }
        return item.name;
      });
    };
    
    // Open review modal
    const openReviewModal = (order) => {
      currentReviewOrder.value = order;
      showReviewModal.value = true;
      
      // Reset review form
      review.rating = 0;
      review.comment = '';
      review.foodRating = 0;
      review.deliveryRating = 0;
    };
    
    // Close review modal
    const closeReviewModal = () => {
      showReviewModal.value = false;
    };
    
    // Submit review
    const submitReview = async () => {
      if (review.rating === 0) return;
      
      try {
        // Make API call to submit review
        const response = await fetch(`/api/orders/${currentReviewOrder.value.id}/review`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            rating: review.rating,
            comment: review.comment,
            foodRating: review.foodRating,
            deliveryRating: review.deliveryRating
          })
        });
        
        if (!response.ok) {
          throw new Error('Failed to submit review');
        }
        
        // Update local state
        allOrders.value = allOrders.value.map(order => {
          if (order.id === currentReviewOrder.value.id) {
            return { ...order, is_reviewed: true };
          }
          return order;
        });
        
        // Close modal
        closeReviewModal();
        
        // Show success message (could use a toast notification here)
        alert('Thank you for your review!');
        
      } catch (err) {
        console.error('Error submitting review:', err);
        alert('Failed to submit review. Please try again.');
        
        // For development, update local state anyway
        allOrders.value = allOrders.value.map(order => {
          if (order.id === currentReviewOrder.value.id) {
            return { ...order, is_reviewed: true };
          }
          return order;
        });
        
        closeReviewModal();
      }
    };
    
    // View order details
    const viewOrderDetails = (order) => {
      selectedOrder.value = order;
      showDetailsModal.value = true;
    };
    
    // Close details modal
    const closeDetailsModal = () => {
      showDetailsModal.value = false;
    };
    
    // Track order
    const trackOrder = (orderId) => {
      router.push(`/track-order/${orderId}`);
    };
    
    // Cancel order
    const cancelOrder = async (orderId) => {
      if (!confirm('Are you sure you want to cancel this order?')) {
        return;
      }
      
      try {
        // Make API call
        const response = await fetch(`/api/orders/${orderId}/cancel`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          }
        });
        
        if (!response.ok) {
          throw new Error('Failed to cancel order');
        }
        
        // Update local state
        allOrders.value = allOrders.value.map(order => {
          if (order.id === orderId) {
            return { ...order, status: 'cancelled' };
          }
          return order;
        });
        
        // Show success message (could use a toast notification here)
        alert('Order cancelled successfully');
        
      } catch (err) {
        console.error('Error cancelling order:', err);
        alert('Failed to cancel order. Please try again or contact support.');
        
        // For development, update local state anyway
        allOrders.value = allOrders.value.map(order => {
          if (order.id === orderId) {
            return { ...order, status: 'cancelled' };
          }
          return order;
        });
      }
    };
    
    // Reorder items
    const reorderItems = async (order) => {
      try {
        // Make API call
        const response = await fetch('/api/cart/reorder', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            orderId: order.id
          })
        });
        
        if (!response.ok) {
          throw new Error('Failed to reorder items');
        }
        
        // Redirect to cart page
        router.push('/cart');
        
      } catch (err) {
        console.error('Error reordering items:', err);
        alert('Failed to add items to cart. Please try again.');
        
        // For development, redirect to cart anyway
        router.push('/cart');
      }
    };
    
    // Contact support
    const contactSupport = (orderId) => {
      window.open(`/support?order=${orderId}`, '_blank');
    };
    
    // Fetch cart count
    const fetchCartCount = async () => {
      try {
        const response = await fetch('/api/cart/count');
        
        if (response.ok) {
          const data = await response.json();
          cartCount.value = data.count || 0;
        }
      } catch (err) {
        console.error('Error fetching cart count:', err);
        cartCount.value = 0;
      }
    };
    
    // Initialize
    onMounted(() => {
      fetchOrders();
      fetchCartCount();
    });
    
    return {
      activeTab,
      isLoading,
      error,
      activeOrders,
      pastOrders,
      cartCount,
      orderSteps,
      showReviewModal,
      currentReviewOrder,
      review,
      showDetailsModal,
      selectedOrder,
      
      // Methods
      fetchOrders,
      formatDeliveryTime,
      formatOrderDate,
      formatOrderDateTime,
      getStatusClass,
      getStatusText,
      getStepNumber,
      getProgressPercentage,
      canCancel,
      getSummaryItems,
      openReviewModal,
      closeReviewModal,
      submitReview,
      viewOrderDetails,
      closeDetailsModal,
      trackOrder,
      cancelOrder,
      reorderItems,
      contactSupport
    };
  }
}
</script>

<style scoped>
.orders-page {
  background-color: #f8f8f8;
  color: #484848;
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.main-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 80px 20px 50px 20px;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 25px;
  color: #484848;
}

/* Tabs styles */
.tabs-container {
  display: flex;
  border-bottom: 1px solid #ddd;
  margin-bottom: 25px;
}

.tab {
  padding: 12px 20px;
  cursor: pointer;
  font-weight: 500;
  color: #767676;
  position: relative;
  transition: color 0.3s;
}

.tab:hover {
  color: #FF8C00;
}

.tab.active {
  color: #FF8C00;
}

.tab.active:after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: -1px;
  height: 3px;
  background-color: #FF8C00;
}

.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background-color: #FF8C00;
  color: white;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  font-size: 12px;
  margin-left: 5px;
}

/* Loading state */
.loading-indicator {
  text-align: center;
  padding: 40px 0;
}

.loading-spinner {
  display: inline-block;
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255, 140, 0, 0.3);
  border-radius: 50%;
  border-top-color: #FF8C00;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-indicator p {
  margin-top: 15px;
  color: #767676;
}

/* Error state */
.error-message {
  text-align: center;
  padding: 40px 0;
  color: #e53935;
}

.error-message i {
  font-size: 40px;
  margin-bottom: 15px;
}

.retry-button {
  background-color: #FF8C00;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 500;
  margin-top: 15px;
  cursor: pointer;
}

/* Empty state */
.empty-state {
  text-align: center;
  padding: 40px 0;
}

.empty-icon {
  font-size: 60px;
  color: #ddd;
  margin-bottom: 15px;
}

.empty-state h3 {
  font-size: 20px;
  margin-bottom: 10px;
  color: #484848;
}

.empty-state p {
  color: #767676;
  margin-bottom: 20px;
}

.browse-button {
  display: inline-block;
  background-color: #FF8C00;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 500;
}

/* Order card styles */
.orders-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.order-card {
  background-color: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border: 1px solid #e6e6e6;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.order-restaurant {
  display: flex;
  align-items: center;
}

.restaurant-logo {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 12px;
}

.restaurant-details h3 {
  margin: 0;
  font-size: 18px;
  color: #484848;
}

.order-id, .order-date {
  margin: 5px 0 0 0;
  font-size: 14px;
  color: #767676;
}

.order-status {
  font-size: 14px;
  font-weight: 500;
  padding: 5px 10px;
  border-radius: 20px;
}

.status-placed {
  background-color: #f0f0f0;
  color: #767676;
}

.status-confirmed {
  background-color: #e3f2fd;
  color: #1976d2;
}

.status-preparing {
  background-color: #fff8e1;
  color: #ffa000;
}

.status-ready {
  background-color: #e8f5e9;
  color: #388e3c;
}

.status-pickup, .status-delivery {
  background-color: #ede7f6;
  color: #5e35b1;
}

.status-delivered {
  background-color: #e8f5e9;
  color: #388e3c;
}

.status-cancelled {
  background-color: #ffebee;
  color: #d32f2f;
}

/* Progress bar styles */
.order-progress {
  padding: 20px 15px;
  border-bottom: 1px solid #f0f0f0;
}

.progress-bar {
  margin-bottom: 15px;
}

.progress-steps {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  position: relative;
}

.progress-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 1;
  flex: 1;
}

.step-circle {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
}

.step-circle i {
  color: #767676;
  font-size: 14px;
}

.step-label {
  font-size: 12px;
  color: #767676;
  text-align: center;
}

.progress-step.active .step-circle {
  background-color: #FF8C00;
}

.progress-step.active .step-circle i {
  color: white;
}

.progress-step.active .step-label {
  color: #484848;
  font-weight: 500;
}

.progress-step.current .step-circle {
  box-shadow: 0 0 0 3px rgba(255, 140, 0, 0.3);
}

.progress-line {
  height: 6px;
  background-color: #f0f0f0;
  border-radius: 3px;
  position: relative;
  overflow: hidden;
}

.progress-fill {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background-color: #FF8C00;
  border-radius: 3px;
  transition: width 0.3s;
}

.estimated-time {
  display: flex;
  align-items: center;
  color: #484848;
  font-size: 14px;
}

.estimated-time i {
  color: #FF8C00;
  margin-right: 8px;
}

/* Order content styles */
.order-content {
  display: flex;
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.order-items {
  flex: 3;
  padding-right: 15px;
}

.order-items h4,
.order-total h4 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #484848;
}

.items-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.items-list li {
  display: flex;
  margin-bottom: 8px;
  font-size: 14px;
}

.item-quantity {
  font-weight: 500;
  margin-right: 5px;
}

.item-name {
  flex: 1;
}

.item-price {
  font-weight: 500;
}

.more-items {
  font-style: italic;
  color: #767676;
}

.order-total {
  flex: 2;
  border-left: 1px solid #f0f0f0;
  padding-left: 15px;
}

.total-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
}

.total-row.discount {
  color: #4caf50;
}

.total-row.grand-total {
  font-weight: 700;
  font-size: 16px;
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px dashed #f0f0f0;
}

/* Order actions */
.order-actions {
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.btn-reorder,
.btn-review,
.btn-track,
.btn-cancel,
.btn-support,
.btn-view-details {
  padding: 8px 15px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  display: flex;
  align-items: center;
}

.btn-reorder {
  background-color: #FF8C00;
  color: white;
}

.btn-review {
  background-color: #f0f0f0;
  color: #484848;
}

.btn-track {
  background-color: #FF8C00;
  color: white;
}

.btn-cancel {
  background-color: #f0f0f0;
  color: #d32f2f;
}

.btn-support {
  background-color: transparent;
  color: #767676;
  padding: 8px 10px;
}

.btn-view-details {
  background-color: #f0f0f0;
  color: #484848;
}

.btn-reorder i,
.btn-review i,
.btn-track i,
.btn-cancel i,
.btn-support i {
  margin-right: 5px;
}

/* Past orders styles */
.past-order {
  cursor: pointer;
  transition: transform 0.2s;
}

.past-order:hover {
  transform: translateY(-3px);
}

.order-summary {
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #f0f0f0;
}

.summary-items {
  font-size: 14px;
  color: #484848;
}

.summary-total {
  font-weight: 600;
  color: #484848;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.review-modal,
.details-modal {
  background-color: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #f0f0f0;
}

.modal-header h3 {
  margin: 0;
  font-size: 20px;
  color: #484848;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 18px;
  color: #767676;
}

.modal-body {
  padding: 20px;
  max-height: 70vh;
  overflow-y: auto;
}

.review-restaurant {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.review-restaurant .restaurant-logo {
  width: 50px;
  height: 50px;
}

.review-restaurant h4 {
  margin: 0;
  font-size: 18px;
  color: #484848;
}

.rating-section {
  margin-bottom: 20px;
}

.rating-section h5 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #484848;
}

.star-rating {
  display: flex;
  gap: 5px;
}

.star-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 24px;
  color: #ddd;
}

.star-btn.active, .star-btn:hover {
  color: #FF8C00;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #484848;
}

.form-group textarea {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ddd;
  resize: vertical;
  font-family: inherit;
  font-size: 14px;
}

.rating-bar {
  display: flex;
  gap: 10px;
}

.rating-btn {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: #f0f0f0;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: #767676;
}

.rating-btn.active, .rating-btn:hover {
  background-color: #FF8C00;
  color: white;
}

.modal-footer {
  padding: 15px 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  border-top: 1px solid #f0f0f0;
}

.btn-cancel,
.btn-submit {
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  border: none;
}

.btn-cancel {
  background-color: #f0f0f0;
  color: #484848;
}

.btn-submit {
  background-color: #FF8C00;
  color: white;
}

.btn-submit:disabled {
  background-color: #f0f0f0;
  color: #767676;
  cursor: not-allowed;
}

/* Order details modal specific styles */
.details-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.details-restaurant {
  display: flex;
  align-items: center;
}

.details-info {
  text-align: right;
}

.details-info p {
  margin: 0 0 5px 0;
  font-size: 14px;
  color: #767676;
}

.order-address {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.order-address h5 {
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 600;
  color: #484848;
}

.order-address p {
  margin: 0;
  font-size: 14px;
  color: #484848;
}

.details-items {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.details-items h5,
.details-payment h5 {
  margin: 0 0 10px 0;
  font-size: 14px;
  font-weight: 600;
  color: #484848;
}

.payment-method {
  margin-top: 10px;
  font-size: 14px;
  color: #767676;
}

/* Responsive styles */
@media (max-width: 768px) {
  .order-content {
    flex-direction: column;
  }
  
  .order-items {
    padding-right: 0;
    margin-bottom: 20px;
  }
  
  .order-total {
    border-left: none;
    border-top: 1px solid #f0f0f0;
    padding-left: 0;
    padding-top: 15px;
  }
  
  .order-actions {
    flex-direction: column;
    gap: 10px;
  }
  
  .action-buttons {
    width: 100%;
    justify-content: center;
  }
  
  .btn-support {
    width: 100%;
    justify-content: center;
  }
  
  .progress-steps .step-label {
    display: none;
  }
  
  .progress-step.current .step-label {
    display: block;
    position: absolute;
    top: 100%;
    width: 100px;
    text-align: center;
    margin-top: 5px;
    left: 50%;
    transform: translateX(-50%);
  }
}
</style>
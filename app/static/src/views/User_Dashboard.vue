<template>
    <div class="main-container">
        <div class="background-image"></div>
        
        <!-- Main content area -->
        <div class="dashboard-container">
            <!-- Header with user info -->
            <div class="user-header">
                <div class="logo-container">
                    <img src="/uploads/pelican.png" alt="Pelican Eats" class="logo">
                </div>
                <div class="user-greeting">
                    <h2>Welcome, {{ user.firstname }}!</h2>
                    <p>What are you craving today?</p>
                </div>
                <div class="user-actions">
                    <button class="icon-button"><i class="fa fa-bell"></i></button>
                    <button class="icon-button"><i class="fa fa-shopping-cart"></i></button>
                    <div class="user-avatar" @click="toggleUserMenu">
                        <img :src="user.avatar || '/uploads/default-avatar.png'" alt="User Avatar">
                        <div class="user-menu" v-if="showUserMenu">
                            <ul>
                                <li><a href="/profile">My Profile</a></li>
                                <li><a href="/orders">My Orders</a></li>
                                <li><a href="/favorites">Favorites</a></li>
                                <li><a href="#" @click.prevent="logout">Logout</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Address selection -->
            <div class="address-selector">
                <div class="current-address" @click="toggleAddressMenu">
                    <i class="fa fa-map-marker-alt"></i>
                    <span>{{ currentAddress }}</span>
                    <i class="fa fa-chevron-down"></i>
                </div>
                <div class="address-dropdown" v-if="showAddressMenu">
                    <ul>
                        <li v-for="(address, index) in savedAddresses" :key="index" 
                            @click="selectAddress(address)">
                            {{ address }}
                        </li>
                        <li class="add-address"><a href="/add-address">+ Add new address</a></li>
                    </ul>
                </div>
            </div>
            
            <!-- Search bar -->
            <div class="search-container">
                <div class="search-bar">
                    <i class="fa fa-search"></i>
                    <input 
                        type="text" 
                        v-model="searchQuery"
                        @input="handleSearchInput" 
                        placeholder="Search for restaurants or cuisines" 
                    />
                    <button v-if="searchQuery" @click="clearSearch" class="clear-search">
                        <i class="fa fa-times"></i>
                    </button>
                </div>
            </div>
            
            <!-- Categories -->
            <div class="categories-container">
                <div class="category-scroll">
                    <div 
                        v-for="(category, index) in categories" 
                        :key="index"
                        class="category-item"
                        :class="{ active: selectedCategory === category.id }"
                        @click="selectCategory(category.id)"
                    >
                        <div class="category-icon" :style="{ backgroundColor: category.colorClass }">
                            <img :src="category.icon" :alt="category.name">
                        </div>
                        <span>{{ category.name }}</span>
                    </div>
                </div>
            </div>
            
            <!-- Quick filters -->
            <div class="quick-filters">
                <button 
                    v-for="(filter, index) in quickFilters" 
                    :key="index"
                    class="filter-button"
                    :class="{ active: activeFilters.includes(filter.id) }"
                    @click="toggleFilter(filter.id)"
                >
                    <i :class="filter.icon"></i>
                    {{ filter.name }}
                </button>
            </div>
            
            <!-- Alert for unfinished payments -->
            <div v-if="hasUnfinishedPayments" class="alert alert-warning">
                <p>You have some unfinished payments. Please pay to continue using Pelican Eats.</p>
                <button @click="handlePayment" class="action-button">Pay Now</button>
            </div>
            
            <!-- Recommendations section -->
            <div class="recommendations-section">
                <div class="section-header">
                    <h3>Recommended for You</h3>
                    <a href="/all-recommendations" class="see-all">
                        See All
                        <i class="fa fa-arrow-right"></i>
                    </a>
                </div>
                
                <div class="recommendations-container">
                    <div v-if="isLoadingRecommendations" class="loading-indicator">
                        <div class="spinner"></div>
                        <p>Finding the best restaurants for you...</p>
                    </div>
                    
                    <div v-else-if="recommendationError" class="error-message">
                        <p>{{ recommendationError }}</p>
                        <button @click="fetchRecommendations" class="retry-button">Try Again</button>
                    </div>
                    
                    <div v-else class="recommendations-grid">
                        <div 
                            v-for="(restaurant, index) in recommendations" 
                            :key="index"
                            class="restaurant-card"
                            @click="viewRestaurantDetails(restaurant.id)"
                        >
                            <div class="restaurant-image">
                                <img :src="restaurant.image" :alt="restaurant.name">
                                <div v-if="restaurant.promotion" class="promotion-tag">
                                    {{ restaurant.promotion }}
                                </div>
                                <button 
                                    @click.stop="toggleFavorite(restaurant.id)" 
                                    class="favorite-button"
                                    :class="{ 'is-favorite': restaurant.isFavorite }"
                                >
                                    <i class="fa" :class="restaurant.isFavorite ? 'fa-heart' : 'fa-heart-o'"></i>
                                </button>
                            </div>
                            <div class="restaurant-info">
                                <h4>{{ restaurant.name }}</h4>
                                <div class="restaurant-meta">
                                    <span class="rating">
                                        <i class="fa fa-star"></i>
                                        {{ restaurant.rating }} 
                                        <span class="rating-count">({{ restaurant.ratingCount }})</span>
                                    </span>
                                    <span class="delivery-time">
                                        <i class="fa fa-clock-o"></i>
                                        {{ restaurant.deliveryTime }} min
                                    </span>
                                </div>
                                <div class="restaurant-tags">
                                    <span v-if="restaurant.deliveryFee === 0" class="free-delivery">Free Delivery</span>
                                    <span v-else class="delivery-fee">${{ restaurant.deliveryFee }} Delivery Fee</span>
                                </div>
                                <p class="match-percentage" v-if="restaurant.matchPercentage">
                                    <i class="fa fa-bullseye"></i>
                                    {{ restaurant.matchPercentage }}% Match with Your Taste
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Featured Restaurants -->
            <div class="featured-section">
                <div class="section-header">
                    <h3>Featured on Pelican Eats</h3>
                    <a href="/featured" class="see-all">
                        See All
                        <i class="fa fa-arrow-right"></i>
                    </a>
                </div>
                
                <div class="featured-container">
                    <div 
                        v-for="(restaurant, index) in featuredRestaurants" 
                        :key="index"
                        class="featured-card"
                        @click="viewRestaurantDetails(restaurant.id)"
                    >
                        <div class="featured-image">
                            <img :src="restaurant.image" :alt="restaurant.name">
                            <div v-if="restaurant.promotion" class="promotion-tag">
                                {{ restaurant.promotion }}
                            </div>
                        </div>
                        <div class="featured-info">
                            <h4>{{ restaurant.name }}</h4>
                            <div class="restaurant-meta">
                                <span class="rating">
                                    <i class="fa fa-star"></i>
                                    {{ restaurant.rating }} 
                                    <span class="rating-count">({{ restaurant.ratingCount }})</span>
                                </span>
                                <span class="delivery-time">
                                    <i class="fa fa-clock-o"></i>
                                    {{ restaurant.deliveryTime }} min
                                </span>
                            </div>
                            <div class="restaurant-tags">
                                <span v-if="restaurant.deliveryFee === 0" class="free-delivery">Free Delivery</span>
                                <span v-else class="delivery-fee">${{ restaurant.deliveryFee }} Delivery Fee</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Places you might like -->
            <div class="places-section">
                <div class="section-header">
                    <h3>Places You Might Like</h3>
                    <a href="/discover" class="see-all">
                        See All
                        <i class="fa fa-arrow-right"></i>
                    </a>
                </div>
                
                <div class="places-container">
                    <div 
                        v-for="(restaurant, index) in suggestedPlaces" 
                        :key="index"
                        class="place-card"
                        @click="viewRestaurantDetails(restaurant.id)"
                    >
                        <div class="place-image">
                            <img :src="restaurant.image" :alt="restaurant.name">
                        </div>
                        <div class="place-info">
                            <h4>{{ restaurant.name }}</h4>
                            <p class="place-cuisine">{{ restaurant.cuisineType }}</p>
                            <div class="place-meta">
                                <span class="place-distance">{{ restaurant.distance }} km away</span>
                                <span class="place-eta">{{ restaurant.eta }} min</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Recent orders -->
            <div v-if="recentOrders.length > 0" class="recent-orders-section">
                <div class="section-header">
                    <h3>Your Recent Orders</h3>
                    <a href="/orders" class="see-all">
                        View All Orders
                        <i class="fa fa-arrow-right"></i>
                    </a>
                </div>
                
                <div class="recent-orders-container">
                    <div 
                        v-for="(order, index) in recentOrders" 
                        :key="index"
                        class="order-card"
                    >
                        <div class="order-restaurant-image">
                            <img :src="order.restaurantImage" :alt="order.restaurantName">
                        </div>
                        <div class="order-info">
                            <div class="order-header">
                                <h4>{{ order.restaurantName }}</h4>
                                <span class="order-date">{{ formatDate(order.orderDate) }}</span>
                            </div>
                            <p class="order-items">{{ order.items }}</p>
                            <div class="order-footer">
                                <span class="order-total">${{ order.total.toFixed(2) }}</span>
                                <button @click="reorder(order.id)" class="reorder-button">
                                    <i class="fa fa-refresh"></i>
                                    Reorder
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Footer navigation -->
        <div class="bottom-navigation">
            <div class="nav-item" :class="{ active: activeTab === 'home' }" @click="setActiveTab('home')">
                <i class="fa fa-home"></i>
                <span>Home</span>
            </div>
            <div class="nav-item" :class="{ active: activeTab === 'search' }" @click="setActiveTab('search')">
                <i class="fa fa-search"></i>
                <span>Search</span>
            </div>
            <div class="nav-item" :class="{ active: activeTab === 'orders' }" @click="setActiveTab('orders')">
                <i class="fa fa-file-text-o"></i>
                <span>Orders</span>
            </div>
            <div class="nav-item" :class="{ active: activeTab === 'account' }" @click="setActiveTab('account')">
                <i class="fa fa-user"></i>
                <span>Account</span>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';

// User data (would normally come from auth store or API)
const user = reactive({
    firstname: 'John',
    lastname: 'Doe',
    email: 'john.doe@example.com',
    avatar: null
});

// UI State
const activeTab = ref('home');
const showUserMenu = ref(false);
const showAddressMenu = ref(false);
const searchQuery = ref('');
const selectedCategory = ref(null);
const activeFilters = ref([]);
const hasUnfinishedPayments = ref(false);
const isLoadingRecommendations = ref(true);
const recommendationError = ref(null);

// Mock data (would come from API)
const currentAddress = ref('10 Walker Gordon Dr');
const savedAddresses = ref([
    '10 Walker Gordon Dr',
    '425 Market St, San Francisco',
    '789 Broadway, New York'
]);

const categories = ref([
    { id: 'offers', name: 'Offers', icon: '/icons/offers.png', colorClass: '#e9f7ef' },
    { id: 'grocery', name: 'Grocery', icon: '/icons/grocery.png', colorClass: '#e3f4d7' },
    { id: 'convenience', name: 'Convenience', icon: '/icons/convenience.png', colorClass: '#f9e9eb' },
    { id: 'alcohol', name: 'Alcohol', icon: '/icons/alcohol.png', colorClass: '#e6f5f9' },
    { id: 'health', name: 'Health', icon: '/icons/health.png', colorClass: '#f5f1e3' },
    { id: 'retail', name: 'Retail', icon: '/icons/retail.png', colorClass: '#f5e8e4' },
    { id: 'fastfood', name: 'Fast Food', icon: '/icons/fastfood.png', colorClass: '#f9f2d2' },
    { id: 'pizza', name: 'Pizza', icon: '/icons/pizza.png', colorClass: '#f8e5e5' },
    { id: 'gameday', name: 'Gameday', icon: '/icons/gameday.png', colorClass: '#e5e8f9' },
    { id: 'icecream', name: 'Ice Cream', icon: '/icons/icecream.png', colorClass: '#f9f9e5' },
    { id: 'chinese', name: 'Chinese', icon: '/icons/chinese.png', colorClass: '#f2e5e5' }
]);

const quickFilters = ref([
    { id: 'uberone', name: 'Uber One', icon: 'fa fa-award' },
    { id: 'pickup', name: 'Pickup', icon: 'fa fa-shopping-bag' },
    { id: 'offers', name: 'Offers', icon: 'fa fa-tag' },
    { id: 'under30min', name: 'Under 30 min', icon: 'fa fa-clock-o' }
]);

// Recommendations data (would come from your prediction endpoint)
const recommendations = ref([]);
const featuredRestaurants = ref([
    {
        id: 1,
        name: 'Wawa',
        image: '/restaurants/wawa.jpg',
        rating: 4.6,
        ratingCount: 26,
        deliveryTime: 20,
        deliveryFee: 0,
        isFavorite: false,
        promotion: 'Buy 1, Get 1 Free'
    },
    {
        id: 2,
        name: 'Taco Bell',
        image: '/restaurants/tacobell.jpg',
        rating: 4.3,
        ratingCount: 1500,
        deliveryTime: 20,
        deliveryFee: 0,
        isFavorite: true,
        promotion: 'LIMITED TIME ONLY'
    }
]);

const suggestedPlaces = ref([
    {
        id: 3,
        name: 'Pizzeria Locale',
        image: '/restaurants/pizzeria.jpg',
        cuisineType: 'Pizza, Italian',
        distance: 1.2,
        eta: 25
    },
    {
        id: 4,
        name: 'Sushi Palace',
        image: '/restaurants/sushi.jpg',
        cuisineType: 'Japanese, Sushi',
        distance: 2.5,
        eta: 35
    }
]);

const recentOrders = ref([
    {
        id: 101,
        restaurantName: 'McDonald\'s',
        restaurantImage: '/restaurants/mcdonalds.jpg',
        orderDate: new Date(2025, 4, 10), // May 10, 2025
        items: 'Big Mac, Large Fries, Coke',
        total: 15.99
    },
    {
        id: 102,
        restaurantName: 'Chipotle',
        restaurantImage: '/restaurants/chipotle.jpg',
        orderDate: new Date(2025, 4, 5), // May 5, 2025
        items: 'Burrito Bowl, Chips & Guacamole',
        total: 18.50
    }
]);

// Fetch recommendations from your endpoint
async function fetchRecommendations() {
    isLoadingRecommendations.value = true;
    recommendationError.value = null;
    
    try {
        // This would be your actual API call
        const response = await fetch('/api/restaurant-recommendations', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
                // Include auth headers as needed
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch recommendations');
        }
        
        const data = await response.json();
        
        // Transform the API response to match our UI needs
        // This is where you would map your prediction model's data to the UI format
        recommendations.value = data.recommendations.map(item => ({
            id: item.restaurant_id,
            name: item.name,
            image: item.image_url || '/restaurants/default.jpg',
            rating: item.rating,
            ratingCount: item.rating_count,
            deliveryTime: item.estimated_delivery_time,
            deliveryFee: item.delivery_fee,
            isFavorite: item.is_favorite || false,
            promotion: item.promotion,
            matchPercentage: item.match_percentage // This would come from your prediction model
        }));
    } catch (error) {
        console.error('Error fetching recommendations:', error);
        recommendationError.value = 'Unable to load recommendations. Please try again later.';
    } finally {
        isLoadingRecommendations.value = false;
    }
}

// Mock recommendations for development
function mockRecommendations() {
    // This simulates your prediction endpoint's response
    return [
        {
            id: 5,
            name: 'Burger Joint',
            image: '/restaurants/burger.jpg',
            rating: 4.8,
            ratingCount: 350,
            deliveryTime: 25,
            deliveryFee: 1.99,
            isFavorite: true,
            promotion: null,
            matchPercentage: 95 // This represents the prediction score from your model
        },
        {
            id: 6,
            name: 'Panda Express',
            image: '/restaurants/panda.jpg',
            rating: 4.2,
            ratingCount: 120,
            deliveryTime: 30,
            deliveryFee: 0,
            isFavorite: false,
            promotion: '20% OFF',
            matchPercentage: 87
        },
        {
            id: 7,
            name: 'Salad Works',
            image: '/restaurants/salad.jpg',
            rating: 4.5,
            ratingCount: 230,
            deliveryTime: 20,
            deliveryFee: 2.99,
            isFavorite: false,
            promotion: null,
            matchPercentage: 83
        }
    ];
}

// Event handlers
function toggleUserMenu() {
    showUserMenu.value = !showUserMenu.value;
    // Close address menu if open
    if (showUserMenu.value && showAddressMenu.value) {
        showAddressMenu.value = false;
    }
}

function toggleAddressMenu() {
    showAddressMenu.value = !showAddressMenu.value;
    // Close user menu if open
    if (showAddressMenu.value && showUserMenu.value) {
        showUserMenu.value = false;
    }
}

function selectAddress(address) {
    currentAddress.value = address;
    showAddressMenu.value = false;
    // Could trigger a refetch of restaurants based on new location
}

function handleSearchInput() {
    // Implement search functionality, possibly with debounce
    console.log('Searching for:', searchQuery.value);
}

function clearSearch() {
    searchQuery.value = '';
}

function selectCategory(categoryId) {
    selectedCategory.value = categoryId === selectedCategory.value ? null : categoryId;
    // Could trigger filtering of restaurants based on category
}

function toggleFilter(filterId) {
    if (activeFilters.value.includes(filterId)) {
        activeFilters.value = activeFilters.value.filter(id => id !== filterId);
    } else {
        activeFilters.value.push(filterId);
    }
    // Could trigger filtering of restaurants based on filters
}

function handlePayment() {
    // Implement payment flow
    console.log('Handling payment');
    hasUnfinishedPayments.value = false;
}

function viewRestaurantDetails(restaurantId) {
    // Navigate to restaurant details page
    console.log('Viewing details for restaurant:', restaurantId);
    // Typically would use router.push here
}

function toggleFavorite(restaurantId) {
    // Find restaurant in any of our lists
    const updateFavoriteStatus = (list) => {
        const restaurant = list.find(r => r.id === restaurantId);
        if (restaurant) {
            restaurant.isFavorite = !restaurant.isFavorite;
            
            // In a real app, you would make an API call here to save the favorite status
            console.log(
                restaurant.isFavorite 
                    ? `Added ${restaurant.name} to favorites` 
                    : `Removed ${restaurant.name} from favorites`
            );
        }
    };
    
    updateFavoriteStatus(recommendations.value);
    updateFavoriteStatus(featuredRestaurants.value);
}

function reorder(orderId) {
    // Implement reorder functionality
    console.log('Reordering order:', orderId);
}

function setActiveTab(tab) {
    activeTab.value = tab;
    // This would typically navigate to different views in a real app
}

function formatDate(date) {
    // Format date as relative time (e.g., "2 days ago")
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) {
        return 'Today';
    } else if (diffDays === 1) {
        return 'Yesterday';
    } else if (diffDays < 7) {
        return `${diffDays} days ago`;
    } else {
        // Format as MM/DD/YYYY for older dates
        return date.toLocaleDateString();
    }
}

function logout() {
    // Implement logout functionality
    console.log('Logging out');
    // Typically would call auth store logout method and redirect
}

// Lifecycle hooks
onMounted(() => {
    // Initialize data
    // In a development environment, use mock data
    recommendations.value = mockRecommendations();
    isLoadingRecommendations.value = false;
    
    // In production, you would uncomment this:
    // fetchRecommendations();
    
    // Check for unfinished payments
    // This would be an API call in a real app
    hasUnfinishedPayments.value = true;
});
</script>

<style>
/* Categories */
.categories-container {
    margin-bottom: 1.5rem;
    overflow: hidden;
}

.category-scroll {
    display: flex;
    overflow-x: auto;
    padding: 0.5rem 0;
    scrollbar-width: none; /* Firefox */
    -ms-overflow-style: none; /* IE and Edge */
}

.category-scroll::-webkit-scrollbar {
    display: none; /* Chrome, Safari, Opera */
}

.category-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-right: 1.2rem;
    cursor: pointer;
}

.category-icon {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 0.5rem;
}

.category-icon img {
    width: 60%;
    height: 60%;
    object-fit: contain;
}

.category-item span {
    font-size: 0.8rem;
    color: #333;
}

.category-item.active .category-icon {
    border: 2px solid #FF8C00;
}

/* Quick filters */
.quick-filters {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
}

.filter-button {
    background-color: white;
    border: 1px solid #eee;
    border-radius: 25px;
    padding: 0.5rem 1rem;
    font-size: 0.8rem;
    display: flex;
    align-items: center;
    cursor: pointer;
}

.filter-button i {
    margin-right: 0.5rem;
    font-size: 0.9rem;
}

.filter-button.active {
    background-color: #FFF3E0;
    color: #FF8C00;
    border-color: #FFE0B2;
}

/* Alert styles */
.alert {
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.alert-warning {
    background-color: #FFF3E0;
    border: 1px solid #FFE0B2;
}

.alert p {
    margin: 0;
    color: #333;
    font-size: 0.9rem;
}

.action-button {
    background-color: #FF8C00;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 0.5rem 1rem;
    font-size: 0.8rem;
    cursor: pointer;
}

/* Section headers */
.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.section-header h3 {
    font-size: 1.2rem;
    margin: 0;
    color: #333;
}

.see-all {
    color: #FF8C00;
    text-decoration: none;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
}

.see-all i {
    margin-left: 0.5rem;
    font-size: 0.8rem;
}

/* Recommendations section */
.recommendations-section {
    margin-bottom: 2rem;
}

.loading-indicator {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem 0;
}

.spinner {
    width: 40px;
    height: 40px;
    border: 3px solid #FFE0B2;
    border-top: 3px solid #FF8C00;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.error-message {
    text-align: center;
    padding: 2rem 0;
}

.retry-button {
    background-color: #FF8C00;
    color: white;
    border: none;
    border-radius: 25px;
    padding: 0.5rem 1.5rem;
    margin-top: 1rem;
    cursor: pointer;
}

.recommendations-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1rem;
}

/* Restaurant cards */
.restaurant-card {
    background-color: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
}

.restaurant-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.restaurant-image {
    height: 150px;
    position: relative;
}

.restaurant-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.promotion-tag {
    position: absolute;
    top: 10px;
    left: 10px;
    background-color: #FF8C00;
    color: white;
    font-size: 0.7rem;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-weight: 500;
}

.favorite-button {
    position: absolute;
    top: 10px;
    right: 10px;
    background-color: white;
    border: none;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    cursor: pointer;
}

.favorite-button.is-favorite i {
    color: #FF436B;
}

.restaurant-info {
    padding: 1rem;
}

.restaurant-info h4 {
    margin: 0 0 0.5rem;
    font-size: 1rem;
    color: #333;
}

.restaurant-meta {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
    font-size: 0.8rem;
}

.rating i {
    color: #FFC107;
    margin-right: 0.25rem;
}

.rating-count {
    color: #999;
}

.restaurant-tags {
    margin-bottom: 0.5rem;
}

.free-delivery, .delivery-fee {
    font-size: 0.8rem;
    color: #666;
}

.free-delivery {
    color: #FF8C00;
}

.match-percentage {
    font-size: 0.8rem;
    color: #4CAF50;
    margin: 0.5rem 0 0;
    display: flex;
    align-items: center;
}

.match-percentage i {
    margin-right: 0.25rem;
}

/* Featured section */
.featured-section {
    margin-bottom: 2rem;
}

.featured-container {
    display: flex;
    overflow-x: auto;
    gap: 1rem;
    padding: 0.5rem 0;
    scrollbar-width: none;
    -ms-overflow-style: none;
}

.featured-container::-webkit-scrollbar {
    display: none;
}

.featured-card {
    flex: 0 0 280px;
    background-color: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    cursor: pointer;
}

.featured-image {
    height: 150px;
    position: relative;
}

.featured-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.featured-info {
    padding: 1rem;
}

/* Places section */
.places-section {
    margin-bottom: 2rem;
}

.places-container {
    display: flex;
    overflow-x: auto;
    gap: 1rem;
    padding: 0.5rem 0;
    scrollbar-width: none;
    -ms-overflow-style: none;
}

.places-container::-webkit-scrollbar {
    display: none;
}

.place-card {
    flex: 0 0 200px;
    background-color: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    cursor: pointer;
}

.place-image {
    height: 120px;
}

.place-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.place-info {
    padding: 0.75rem;
}

.place-info h4 {
    margin: 0 0 0.25rem;
    font-size: 0.9rem;
    color: #333;
}

.place-cuisine {
    margin: 0 0 0.5rem;
    font-size: 0.8rem;
    color: #666;
}

.place-meta {
    display: flex;
    justify-content: space-between;
    font-size: 0.7rem;
    color: #999;
}

/* Recent orders section */
.recent-orders-section {
    margin-bottom: 2rem;
}

.recent-orders-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.order-card {
    display: flex;
    background-color: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.order-restaurant-image {
    flex: 0 0 80px;
}

.order-restaurant-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.order-info {
    flex: 1;
    padding: 1rem;
}

.order-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}

.order-header h4 {
    margin: 0;
    font-size: 1rem;
    color: #333;
}

.order-date {
    font-size: 0.8rem;
    color: #999;
}

.order-items {
    margin: 0 0 0.5rem;
    font-size: 0.9rem;
    color: #666;
}

.order-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.order-total {
    font-weight: 500;
    color: #333;
}

.reorder-button {
    background-color: #FFF3E0;
    color: #FF8C00;
    border: none;
    border-radius: 4px;
    padding: 0.5rem 0.75rem;
    font-size: 0.8rem;
    display: flex;
    align-items: center;
    cursor: pointer;
}

.reorder-button i {
    margin-right: 0.5rem;
}

/* Bottom navigation */
.bottom-navigation {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: white;
    display: flex;
    justify-content: space-around;
    border-top: 1px solid #eee;
    padding: 0.5rem 0;
    z-index: 10;
}

.nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0.5rem 1rem;
    cursor: pointer;
}

.nav-item i {
    font-size: 1.2rem;
    color: #999;
    margin-bottom: 0.25rem;
}

.nav-item span {
    font-size: 0.75rem;
    color: #999;
}

.nav-item.active i,
.nav-item.active span {
    color: #FF8C00;
}

/* Responsive styles */
@media (max-width: 768px) {
    .dashboard-container {
        padding: 0.75rem;
    }
    
    .user-greeting h2 {
        font-size: 1.2rem;
    }
    
    .recommendations-grid {
        grid-template-columns: 1fr;
    }
    
    .user-header {
        margin-bottom: 1rem;
    }
    
    .logo {
        height: 30px;
    }
}

@media (min-width: 769px) {
    .recommendations-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (min-width: 1024px) {
    .dashboard-container {
        max-width: 1000px;
    }
    
    .recommendations-grid {
        grid-template-columns: repeat(3, 1fr);
    }
} Main container styles */
.main-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    width: 100%;
    margin: 0;
    padding: 0;
    position: relative;
    overflow-x: hidden;
    background-color: #f8f8f8;
}

.background-image {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url('/uploads/background.png');
    background-size: cover;
    background-position: center;
    opacity: 0.05;
    z-index: -1;
}

/* Dashboard container */
.dashboard-container {
    flex: 1;
    padding: 1rem;
    padding-bottom: 5rem; /* Space for bottom navigation */
    max-width: 800px;
    margin: 0 auto;
}

/* User header */
.user-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}

.logo-container {
    flex: 0 0 auto;
}

.logo {
    height: 40px;
}

.user-greeting {
    flex: 1;
    padding: 0 1rem;
}

.user-greeting h2 {
    font-size: 1.4rem;
    margin: 0;
    color: #333;
}

.user-greeting p {
    margin: 0.25rem 0 0;
    color: #666;
    font-size: 0.9rem;
}

.user-actions {
    display: flex;
    align-items: center;
}

.icon-button {
    background: none;
    border: none;
    font-size: 1.2rem;
    color: #333;
    margin-left: 1rem;
    cursor: pointer;
}

.user-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    overflow: hidden;
    margin-left: 1rem;
    cursor: pointer;
    position: relative;
}

.user-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.user-menu {
    position: absolute;
    top: 45px;
    right: 0;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    width: 180px;
    z-index: 10;
}

.user-menu ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.user-menu li {
    padding: 0;
}

.user-menu a {
    display: block;
    padding: 0.75rem 1rem;
    color: #333;
    text-decoration: none;
    font-size: 0.9rem;
}

.user-menu a:hover {
    background-color: #f5f5f5;
}

/* Address selector */
.address-selector {
    margin-bottom: 1.5rem;
    position: relative;
}

.current-address {
    display: flex;
    align-items: center;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
}

.current-address i {
    margin-right: 0.5rem;
    color: #FF8C00;
}

.address-dropdown {
    position: absolute;
    top: 30px;
    left: 0;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 350px;
    z-index: 10;
}

.address-dropdown ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.address-dropdown li {
    padding: 0.75rem 1rem;
    cursor: pointer;
}

.address-dropdown li:hover {
    background-color: #f5f5f5;
}

.add-address {
    border-top: 1px solid #eee;
}

.add-address a {
    color: #FF8C00;
    text-decoration: none;
}

/* Search container */
.search-container {
    margin-bottom: 1.5rem;
}

.search-bar {
    display: flex;
    align-items: center;
    background-color: white;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.search-bar i {
    color: #666;
    margin-right: 0.75rem;
}

.search-bar input {
    border: none;
    flex: 1;
    font-size: 1rem;
    outline: none;
    color: #333;
}

.clear-search {
    background: none;
    border: none;
    color: #666;
    cursor: pointer;
}

</style>
<template>
  <div class="app-container">
    <div class="main-content">
      <!-- Location Header -->
      <div class="location-header">
        <div class="location-selector">
          <div class="location-icon">
            <i class="fas fa-map-marker-alt"></i>
          </div>
          <div class="location-text">
            <span class="location-label">Delivery Location</span>
            <span class="location-value">{{ deliveryLocation }}</span>
          </div>
          <i class="fas fa-chevron-down"></i>
        </div>
      </div>

      <!-- Search Bar -->
      <div class="search-container">
        <div class="search-input">
          <i class="fas fa-search"></i>
          <input 
            type="text" 
            placeholder="Search food or restaurant" 
            v-model="searchQuery"
            @input="handleSearch"
          />
          <i class="fas fa-sliders-h"></i>
        </div>
      </div>

      <!-- Promotion Banner -->
      <div class="promo-banner">
        <img :src="currentPromo.image" :alt="currentPromo.title" />
      </div>

      <!-- Food Categories Slider -->
      <div class="categories-container">
        <h2 class="section-title"><i class="fas fa-th-large"></i> Categories</h2>
        <div class="categories-row">
          <div 
            v-for="category in categories" 
            :key="category.id" 
            class="category-item"
            @click="filterByCategory(category.id)"
          >
            <div class="category-circle" :style="{ backgroundColor: category.bgColor }">
              <i :class="category.icon" class="category-icon"></i>
            </div>
            <span class="category-name">{{ category.name }}</span>
          </div>
          <div class="nav-arrow">
            <i class="fas fa-chevron-right"></i>
          </div>
        </div>
      </div>

      <!-- Recommended Section -->
      <div class="recommended-section">
        <div class="section-header">
          <h2 class="section-title"><i class="fas fa-star"></i> Recommended for you</h2>
          <p>Restaurants based on your previous orders</p>
          <button class="close-btn"><i class="fas fa-times"></i></button>
        </div>

        <div class="restaurant-cards">
          <div v-if="isLoading.recommendations" class="loading-skeleton">
            <div v-for="i in 3" :key="`skeleton-${i}`" class="skeleton-card">
              <div class="skeleton-image"></div>
              <div class="skeleton-text"></div>
              <div class="skeleton-text-sm"></div>
            </div>
          </div>
          <div 
            v-else-if="recommendedRestaurants.length > 0"
            v-for="restaurant in recommendedRestaurants" 
            :key="restaurant.id"
            class="restaurant-card"
            @click="viewRestaurant(restaurant.id)"
          >
            <div class="cuisine-tag">{{ restaurant.cuisine }}</div>
            <img :src="restaurant.image" :alt="restaurant.name" class="restaurant-image" />
            <div class="restaurant-details">
              <h3>{{ restaurant.name }}</h3>
              <div class="restaurant-rating">
                <span class="star"><i class="fas fa-star"></i> {{ restaurant.rating }}</span>
                <span v-if="restaurant.fastDelivery" class="fast-delivery"><i class="fas fa-bolt"></i></span>
              </div>
            </div>
          </div>
          <div v-else-if="!isLoading.recommendations" class="no-results">
            <p>No recommendations found. Start ordering to get personalized suggestions!</p>
          </div>
        </div>
      </div>

      <!-- Newly Added Restaurants -->
      <div class="new-restaurants-section">
        <h2 class="section-title"><i class="fas fa-store"></i> Newly Added Restaurants</h2>
        <div class="restaurant-cards">
          <div v-if="isLoading.newRestaurants" class="loading-skeleton">
            <div v-for="i in 3" :key="`skeleton-${i}`" class="skeleton-card">
              <div class="skeleton-image"></div>
              <div class="skeleton-text"></div>
              <div class="skeleton-text-sm"></div>
            </div>
          </div>
          <div 
            v-else-if="newRestaurants.length > 0"
            v-for="restaurant in newRestaurants" 
            :key="restaurant.id"
            class="restaurant-card"
            @click="viewRestaurant(restaurant.id)"
          >
            <img :src="restaurant.image" :alt="restaurant.name" class="restaurant-image" />
            <div class="restaurant-details">
              <h3>{{ restaurant.name }}</h3>
              <div class="restaurant-rating">
                <span class="star"><i class="fas fa-star"></i> {{ restaurant.rating }}</span>
              </div>
            </div>
          </div>
          <div v-else-if="!isLoading.newRestaurants" class="no-results">
            <p>No new restaurants available at the moment.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GenUser_Dashboard',
  data() {
    return {
      deliveryLocation: 'AZ Preston Hall',
      cartCount: 0,
      searchQuery: '',
      currentPromo: {
        id: 1,
        title: 'Free Delivery',
        image: '/images/promo-free-delivery.jpg'
      },
      categories: [
        { id: 1, name: 'Breakfast', icon: 'fas fa-bacon', bgColor: '#FFD7B5' },
        { id: 2, name: 'Lunch', icon: 'fas fa-utensils', bgColor: '#B5EAFF' },
        { id: 3, name: 'Dinner', icon: 'fas fa-drumstick-bite', bgColor: '#FFB5B5' },
        { id: 4, name: 'Dessert', icon: 'fas fa-birthday-cake', bgColor: '#FFE2B5' },
        { id: 5, name: 'Coffee', icon: 'fas fa-mug-hot', bgColor: '#D4B5FF' },
        { id: 6, name: 'Drinks', icon: 'fas fa-glass-martini-alt', bgColor: '#B5FFD9' },
        { id: 7, name: 'Fast Food', icon: 'fas fa-hamburger', bgColor: '#FFECB5' },
        { id: 8, name: 'Vegetarian', icon: 'fas fa-seedling', bgColor: '#B5FFBA' },
        { id: 9, name: 'Vegan', icon: 'fas fa-leaf', bgColor: '#B5FFD0' },
        { id: 10, name: 'Mexican', icon: 'fas fa-pepper-hot', bgColor: '#FFB5D6' },
        { id: 11, name: 'Italian', icon: 'fas fa-pizza-slice', bgColor: '#FFB5B5' },
        { id: 12, name: 'Chinese', icon: 'fas fa-compass', bgColor: '#FFDDB5' }
      ],
      recommendedRestaurants: [],
      newRestaurants: [],
      isLoading: {
        recommendations: true,
        newRestaurants: true
      },
      error: {
        recommendations: null,
        newRestaurants: null
      }
    }
  },
  created() {
    // Fetch user preferences and recommendations when component is created
    this.fetchRecommendations();
    this.fetchNewRestaurants();
    
    // Add FontAwesome script if not already loaded
    if (!document.getElementById('font-awesome-script')) {
      const script = document.createElement('script');
      script.id = 'font-awesome-script';
      script.src = 'https://kit.fontawesome.com/a076d05399.js';
      script.crossOrigin = 'anonymous';
      document.head.appendChild(script);
    }
  },
  methods: {
    filterByCategory(categoryId) {
      console.log('Filtering by category:', categoryId);
      // Implement category filtering logic
      fetch(`/api/restaurants/category/${categoryId}`)
        .then(response => {
          if (!response.ok) {
            throw new Error('Category filtering failed');
          }
          return response.json();
        })
        .then(data => {
          // Update restaurant lists based on category
          console.log('Category results:', data);
        })
        .catch(error => {
          console.error('Error filtering by category:', error);
          // Show user-friendly error message
        });
    },
    
    handleSearch() {
      // Implement search logic here with debounce
      if (this.searchTimeout) {
        clearTimeout(this.searchTimeout);
      }
      
      this.searchTimeout = setTimeout(() => {
        console.log('Searching for:', this.searchQuery);
        // Make API call with the search term
        if (this.searchQuery.length > 2) {
          this.searchRestaurants(this.searchQuery);
        }
      }, 300); // 300ms debounce
    },
    
    searchRestaurants(query) {
      // Implementation for actual search API call
      fetch(`/api/search?q=${encodeURIComponent(query)}`)
        .then(response => {
          if (!response.ok) {
            throw new Error('Search failed');
          }
          return response.json();
        })
        .then(data => {
          // Handle search results
          console.log('Search results:', data);
        })
        .catch(error => {
          console.error('Error searching:', error);
          // Show user-friendly error message
        });
    },
    
    viewRestaurant(restaurantId) {
      console.log('Viewing restaurant:', restaurantId);
      this.$router.push(`/restaurant/${restaurantId}`);
    },
    
    fetchRecommendations() {
      this.isLoading.recommendations = true;
      this.error.recommendations = null;
      
      // Make API call to your Flask backend
      fetch('/api/recommendations')
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to fetch recommendations');
          }
          return response.json();
        })
        .then(data => {
          this.recommendedRestaurants = data.recommendations || [];
        })
        .catch(error => {
          console.error('Error fetching recommendations:', error);
          this.error.recommendations = 'Unable to load recommendations. Please try again later.';
        })
        .finally(() => {
          this.isLoading.recommendations = false;
        });
    },
    
    fetchNewRestaurants() {
      this.isLoading.newRestaurants = true;
      this.error.newRestaurants = null;
      
      // Make API call to your Flask backend
      fetch('/api/restaurants/new')
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to fetch new restaurants');
          }
          return response.json();
        })
        .then(data => {
          this.newRestaurants = data.restaurants || [];
        })
        .catch(error => {
          console.error('Error fetching new restaurants:', error);
          this.error.newRestaurants = 'Unable to load new restaurants. Please try again later.';
        })
        .finally(() => {
          this.isLoading.newRestaurants = false;
        });
    }
  }
}
</script>

<style scoped>
/* Main container styles */
.app-container {
  background-color: #f8f8f8;
  color: #484848;
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding-top: 80px; /* Increased from 20px to account for navbar height */
}

/* Main Content */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px 50px 20px;
}

/* Location Header */
.location-header {
  background-color: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  border: 1px solid #e6e6e6;
}
.location-selector {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.location-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background-color: rgba(255, 140, 0, 0.1);
  border-radius: 50%;
  margin-right: 12px;
}

.location-icon i {
  color: #FF8C00; /* Pelican Eats orange */
  font-size: 18px;
}

.location-text {
  display: flex;
  flex-direction: column;
}

.location-label {
  color: #767676;
  font-size: 12px;
  margin-bottom: 2px;
}

.location-value {
  font-size: 16px;
  font-weight: 500;
}

.location-selector i.fa-chevron-down {
  margin-left: auto;
  color: #767676;
}

/* Search Bar */
.search-container {
  margin-bottom: 20px;
}

.search-input {
  display: flex;
  align-items: center;
  background-color: white;
  border-radius: 50px;
  padding: 12px 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border: 1px solid #e6e6e6;
}

.search-input i {
  color: #767676;
  margin-right: 10px;
}

.search-input i.fa-sliders-h {
  margin-left: auto;
  margin-right: 0;
  color: #FF8C00; /* Pelican Eats orange */
  cursor: pointer;
}

.search-input input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 16px;
  color: #484848;
  background: transparent;
}

.search-input input::placeholder {
  color: #767676;
}

/* Promo Banner */
.promo-banner {
  border-radius: 12px;
  overflow: hidden;
  height: 180px;
  margin-bottom: 25px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border: 1px solid #e6e6e6;
}

.promo-banner img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Categories */
.categories-container {
  margin-bottom: 25px;
  background-color: white;
  border-radius: 12px;
  padding: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  position: relative;
  border: 1px solid #e6e6e6;
}

.categories-container .section-title {
  margin-bottom: 15px;
  padding-left: 5px;
}

.categories-row {
  display: flex;
  overflow-x: auto;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE/Edge */
  position: relative;
  padding: 10px 0;
}

.categories-row::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

.category-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 80px;
  margin-right: 15px;
  cursor: pointer;
}

.category-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
  transition: transform 0.3s;
}

.category-icon {
  font-size: 24px;
  color: #484848;
}

.category-item:hover .category-circle {
  transform: scale(1.1);
}

.category-name {
  font-size: 14px;
  color: #484848;
  text-align: center;
}

.nav-arrow {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  width: 30px;
  height: 30px;
  background-color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  z-index: 2;
  border: 1px solid #e6e6e6;
}

.nav-arrow:hover {
  background-color: #f8f8f8;
}

/* Section Titles */
.section-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 15px;
  color: #484848;
  display: flex;
  align-items: center;
}

.section-title i {
  margin-right: 10px;
  color: #FF8C00; /* Pelican Eats orange */
}

/* Restaurant Sections */
.recommended-section, .new-restaurants-section {
  background-color: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 25px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border: 1px solid #e6e6e6;
}

.section-header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 20px;
  position: relative;
}

.section-header p {
  margin: 0;
  font-size: 14px;
  color: #767676;
  flex: 1;
}

.close-btn {
  background: transparent;
  border: none;
  color: #767676;
  cursor: pointer;
  position: absolute;
  right: 0;
  top: 0;
}

.restaurant-cards {
  display: flex;
  overflow-x: auto;
  gap: 20px;
  padding-bottom: 10px;
  scrollbar-width: none; /* Hide scrollbar for Firefox */
}

.restaurant-cards::-webkit-scrollbar {
  display: none; /* Hide scrollbar for Chrome/Safari/Opera */
}

.restaurant-card {
  min-width: 250px;
  border-radius: 12px;
  overflow: hidden;
  position: relative;
  cursor: pointer;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  background-color: white;
  border: 1px solid #e6e6e6;
}

.restaurant-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.cuisine-tag {
  position: absolute;
  top: 12px;
  left: 12px;
  background-color: #FF8C00; /* Pelican Eats orange */
  color: white;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  z-index: 1;
}

.restaurant-image {
  width: 100%;
  height: 160px;
  object-fit: cover;
}

.restaurant-details {
  padding: 15px;
}

.restaurant-details h3 {
  margin: 0 0 10px 0;
  font-size: 18px;
  color: #484848;
}

.restaurant-rating {
  display: flex;
  align-items: center;
}

.star {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #484848;
}

.star i {
  color: #FF8C00; /* Pelican Eats orange */
  margin-right: 4px;
}

.fast-delivery {
  margin-left: 10px;
  background-color: rgba(255, 140, 0, 0.1);
  padding: 3px 8px;
  border-radius: 20px;
  display: flex;
  align-items: center;
}

.fast-delivery i {
  color: #FF8C00; /* Pelican Eats orange */
  margin-right: 4px;
}

/* Loading skeletons */
.loading-skeleton {
  display: flex;
  gap: 20px;
}

.skeleton-card {
  min-width: 250px;
  background-color: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
  border: 1px solid #e6e6e6;
}

.skeleton-image {
  width: 100%;
  height: 160px;
  background: linear-gradient(90deg, #f0f0f0 25%, #f8f8f8 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

.skeleton-text {
  height: 20px;
  margin: 15px;
  background: linear-gradient(90deg, #f0f0f0 25%, #f8f8f8 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
}

.skeleton-text-sm {
  height: 14px;
  width: 60%;
  margin: 0 15px 15px 15px;
  background: linear-gradient(90deg, #f0f0f0 25%, #f8f8f8 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
}

.no-results {
  width: 100%;
  padding: 20px;
  text-align: center;
  color: #767676;
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

/* Media queries for responsiveness */
@media (max-width: 768px) {
  .main-content {
    padding: 15px;
  }
  
  .category-item {
    min-width: 70px;
  }
  
  .category-circle {
    width: 50px;
    height: 50px;
  }
  
  .restaurant-card {
    min-width: 200px;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .main-content {
    max-width: 900px;
  }
}
</style>
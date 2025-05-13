<template>
  <div class="main-container">
    <div class="background-image"></div>
    
    <div class="content-container">
      <div class="form-wrapper">
        <!-- Logo -->
        <div class="logo-container">
          <img src="/uploads/pelican.png" alt="Pelican Eats" class="logo">
        </div>
        
        <h1>Complete Your Food Profile</h1>
        
        <!-- Progress indicator -->
        <div class="progress-container">
          <div class="progress-bar">
            <div class="progress-fill" :style="`width: ${(currentStep/6)*100}%`"></div>
          </div>
          <span class="progress-text">Step {{ currentStep }} of 6</span>
        </div>
        
        <!-- Alert messages -->
        <div v-if="message || errors.length > 0" :class="{'alert alert-success': message, 'alert alert-danger': errors.length > 0}" role="alert">
          <p v-if="message">{{ message }}</p>
          <ul v-if="errors.length > 0">
            <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
          </ul>
        </div>

        <!-- Step content -->
        <div class="step-container">
          <!-- Step 1: Food Swipe - Updated with only backend-mapped foods -->
          <div v-if="currentStep === 1" class="step-content">
            <h2>What Foods Do You Love?</h2>
            <p class="step-description">Swipe right if you like it, left if you don't!</p>
            
            <div class="swipe-container">
              <div 
                v-for="(food, index) in foodTypes" 
                :key="food.id"
                :class="['swipe-card', { 'top-card': index === currentFoodIndex }]"
                :style="food.style"
              >
                <div class="food-image">
                  <img :src="food.image || '/uploads/ackee_salt.jpg'" :alt="food.name" />
                </div>
                <div class="food-info">
                  <h3>{{ food.name }}</h3>
                </div>
              </div>
            </div>
            
            <div class="swipe-actions">
              <button @click="swipeLeft" class="swipe-btn dislike-btn">✕</button>
              <button @click="swipeRight" class="swipe-btn like-btn">✓</button>
            </div>
          </div>

          <!-- Step 2: Dietary Restrictions -->
          <div v-if="currentStep === 2" class="step-content">
            <h2>Dietary Restrictions</h2>
            <p class="step-description">Let us know about any dietary restrictions (tap for priority)</p>
            
            <div class="restrictions-grid">
              <div 
                v-for="restriction in formData.dietaryRestrictions" 
                :key="restriction.id"
                @click="toggleRestriction(restriction)"
                :class="['restriction-item', {
                  'selected': restriction.selected,
                  'priority': restriction.priority
                }]"
              >
                <div class="restriction-icon">{{ restriction.icon }}</div>
                <div class="restriction-text">{{ restriction.name }}</div>
              </div>
            </div>
          </div>

          <!-- Step 3: Flavor Preferences -->
          <div v-if="currentStep === 3" class="step-content">
            <h2>Your Flavor Profile</h2>
            <p class="step-description">Tell us about your taste preferences</p>
            
            <div class="flavor-section">
              <label>Spice Level</label>
              <input 
                type="range" 
                v-model="formData.flavorPreferences.spiceLevel" 
                min="1" 
                max="5" 
                class="flavor-slider"
              >
              <div class="slider-labels">
                <span>Mild</span>
                <span>{{ getSpiceLabel(formData.flavorPreferences.spiceLevel) }}</span>
                <span>Very Spicy</span>
              </div>
            </div>
            
            <div class="flavor-section">
              <label>Health Preference</label>
              <input 
                type="range" 
                v-model="formData.flavorPreferences.healthyLevel" 
                min="1" 
                max="5" 
                class="flavor-slider"
              >
              <div class="slider-labels">
                <span>Very Healthy</span>
                <span>{{ getHealthLabel(formData.flavorPreferences.healthyLevel) }}</span>
                <span>Indulgent</span>
              </div>
            </div>

            <div class="flavor-section">
              <label>Sweet Preference</label>
              <input 
                type="range" 
                v-model="formData.flavorPreferences.sweetPreference" 
                min="1" 
                max="5" 
                class="flavor-slider"
              >
              <div class="slider-labels">
                <span>Less Sweet</span>
                <span>{{ getSweetLabel(formData.flavorPreferences.sweetPreference) }}</span>
                <span>Very Sweet</span>
              </div>
            </div>
          </div>

          <!-- Step 4: Meat & Cooking Preferences -->
          <div v-if="currentStep === 4" class="step-content">
            <h2>Meat & Cooking Preferences</h2>
            <p class="step-description">Select your meat and cooking style preferences</p>
            
            <div class="preferences-section">
              <h3>Meat Preferences</h3>
              <div class="meat-grid">
                <label v-for="meat in meatOptions" :key="meat.value" class="meat-option">
                  <input 
                    type="checkbox" 
                    v-model="formData.meatPreferences[meat.value]"
                  >
                  <div class="meat-item">
                    <span class="meat-icon">{{ meat.icon }}</span>
                    <span>{{ meat.label }}</span>
                  </div>
                </label>
              </div>
              <div v-if="formData.meatPreferences.other_meat" style="margin-top: 15px;">
                <input 
                  type="text" 
                  v-model="formData.meatPreferences.other_meat" 
                  placeholder="Specify other meat"
                  class="text-input"
                >
              </div>
            </div>

            <div class="preferences-section">
              <h3>Cooking Styles</h3>
              <div class="cooking-grid">
                <label v-for="style in cookingStyles" :key="style.value" class="cooking-option">
                  <input 
                    type="checkbox" 
                    v-model="formData.cookingStyles[style.value]"
                  >
                  <div class="cooking-item">
                    <span class="cooking-icon">{{ style.icon }}</span>
                    <span>{{ style.label }}</span>
                  </div>
                </label>
              </div>
              <div v-if="formData.cookingStyles.other_style" style="margin-top: 15px;">
                <input 
                  type="text" 
                  v-model="formData.cookingStyles.other_style" 
                  placeholder="Specify other cooking style"
                  class="text-input"
                >
              </div>
            </div>
          </div>

          <!-- Step 5: Meal Preferences -->
          <div v-if="currentStep === 5" class="step-content">
            <h2>Meal Preferences</h2>
            <p class="step-description">What do you usually order for breakfast and lunch?</p>
            
            <div class="meal-tabs">
              <button 
                @click="activeMealTab = 'breakfast'" 
                :class="['meal-tab', { active: activeMealTab === 'breakfast' }]"
              >
                Breakfast
              </button>
              <button 
                @click="activeMealTab = 'lunch'" 
                :class="['meal-tab', { active: activeMealTab === 'lunch' }]"
              >
                Lunch
              </button>
              <button 
                @click="activeMealTab = 'juice'" 
                :class="['meal-tab', { active: activeMealTab === 'juice' }]"
              >
                Juice
              </button>
            </div>

            <div v-if="activeMealTab === 'breakfast'" class="meal-options">
              <div class="options-grid">
                <label v-for="item in breakfastItems" :key="item.value" class="meal-option">
                  <input 
                    type="checkbox" 
                    v-model="formData.breakfastPreferences[item.value]"
                  >
                  <div class="meal-item">
                    <span class="meal-icon">{{ item.icon }}</span>
                    <span>{{ item.label }}</span>
                  </div>
                </label>
              </div>
              <div v-if="formData.breakfastPreferences.other_breakfast !== null" style="margin-top: 15px;">
                <input 
                  type="text" 
                  v-model="formData.breakfastPreferences.other_breakfast" 
                  placeholder="Other breakfast preference"
                  class="text-input"
                >
              </div>
            </div>

            <div v-if="activeMealTab === 'lunch'" class="meal-options">
              <div class="options-grid">
                <label v-for="item in lunchItems" :key="item.value" class="meal-option">
                  <input 
                    type="checkbox" 
                    v-model="formData.lunchPreferences[item.value]"
                  >
                  <div class="meal-item">
                    <span class="meal-icon">{{ item.icon }}</span>
                    <span>{{ item.label }}</span>
                  </div>
                </label>
              </div>
              <div v-if="formData.lunchPreferences.other_lunch !== null" style="margin-top: 15px;">
                <input 
                  type="text" 
                  v-model="formData.lunchPreferences.other_lunch" 
                  placeholder="Other lunch preference"
                  class="text-input"
                >
              </div>
            </div>

            <div v-if="activeMealTab === 'juice'" class="meal-options">
              <div class="options-grid">
                <label v-for="item in juiceItems" :key="item.value" class="meal-option">
                  <input 
                    type="checkbox" 
                    v-model="formData.juicePreferences[item.value]"
                  >
                  <div class="meal-item">
                    <span class="meal-icon">{{ item.icon }}</span>
                    <span>{{ item.label }}</span>
                  </div>
                </label>
              </div>
              <div v-if="formData.juicePreferences.other_juice !== null" style="margin-top: 15px;">
                <input 
                  type="text" 
                  v-model="formData.juicePreferences.other_juice" 
                  placeholder="Other juice preference"
                  class="text-input"
                >
              </div>
            </div>
          </div>

          <!-- Step 6: Budget & Schedule -->
          <div v-if="currentStep === 6" class="step-content">
            <h2>Budget & Ordering Preferences</h2>
            <p class="step-description">Help us understand your preferences</p>
            
            <div class="budget-section">
              <h3>Budget Preference</h3>
              <div class="budget-options">
                <label v-for="option in budgetOptions" :key="option.value" class="budget-option">
                  <input 
                    type="radio" 
                    v-model="formData.budget"
                    :value="option.value"
                  >
                  <div class="budget-item">
                    <span class="budget-icon">{{ option.icon }}</span>
                    <span class="budget-label">{{ option.label }}</span>
                    <span class="budget-desc">{{ option.desc }}</span>
                  </div>
                </label>
              </div>
            </div>

            <div class="time-section">
              <h3>Preferred Order Times</h3>
              <div class="time-grid">
                <label v-for="time in orderTimes" :key="time.id" class="time-option">
                  <input 
                    type="checkbox" 
                    v-model="time.selected"
                  >
                  <div class="time-item">
                    <span class="time-icon">{{ time.icon }}</span>
                    <span class="time-label">{{ time.name }}</span>
                    <span class="time-desc">{{ time.time }}</span>
                  </div>
                </label>
              </div>
            </div>

            <div class="additional-notes">
              <h5>Additional Notes</h5>
              <textarea 
                v-model="formData.additional_notes" 
                placeholder="Any other preferences or notes?"
                class="notes-textarea"
              ></textarea>
            </div>


            <!-- Delivery Preferences -->
            
            <div class="delivery-section">
              <h3>Delivery Preferences</h3>
              <div class="form-group">
                <label for="default-address">Default Delivery Address</label>
                <input 
                  id="default-address"
                  type="text" 
                  v-model="formData.deliveryPreferences.default_address" 
                  placeholder="Your preferred delivery address"
                  class="text-input"
                  required
                >
              </div>
              
              <div class="form-group">
                <label for="delivery-instructions">Delivery Instructions</label>
                <textarea 
                  id="delivery-instructions"
                  v-model="formData.deliveryPreferences.delivery_instructions" 
                  placeholder="Any special instructions for delivery?"
                  class="notes-textarea"
                ></textarea>
              </div>
              
              <div class="form-group">
                <label>Preferred Delivery Time</label>
                <div class="delivery-time-options">
                  <label class="delivery-time-option">
                    <input 
                      type="radio" 
                      v-model="formData.deliveryPreferences.preferred_delivery_time"
                      value="morning"
                    >
                    <div class="delivery-time-item">
                      <span class="delivery-time-icon">🌅</span>
                      <span>Morning (9 AM - 12 PM)</span>
                    </div>
                  </label>
                  
                  <label class="delivery-time-option">
                    <input 
                      type="radio" 
                      v-model="formData.deliveryPreferences.preferred_delivery_time"
                      value="afternoon"
                    >
                    <div class="delivery-time-item">
                      <span class="delivery-time-icon">☀️</span>
                      <span>Afternoon (12 PM - 5 PM)</span>
                    </div>
                  </label>
                  
                  <label class="delivery-time-option">
                    <input 
                      type="radio" 
                      v-model="formData.deliveryPreferences.preferred_delivery_time"
                      value="evening"
                    >
                    <div class="delivery-time-item">
                      <span class="delivery-time-icon">🌆</span>
                      <span>Evening (5 PM - 9 PM)</span>
                    </div>
                  </label>
                </div>
              </div>
            </div>


            <!-- Communication Preferences -->  
            <div class="communication-section">
              <h3>Communication Preferences</h3>
              <div class="notification-options">
                <label class="notification-option">
                  <input 
                    type="checkbox" 
                    v-model="formData.communicationPreferences.email_notifications"
                  >
                  <div class="notification-item">
                    <span class="notification-icon">📧</span>
                    <span>Email Notifications</span>
                  </div>
                </label>
                
                <label class="notification-option">
                  <input 
                    type="checkbox" 
                    v-model="formData.communicationPreferences.sms_notifications"
                  >
                  <div class="notification-item">
                    <span class="notification-icon">📱</span>
                    <span>SMS Notifications</span>
                  </div>
                </label>
                
                <label class="notification-option">
                  <input 
                    type="checkbox" 
                    v-model="formData.communicationPreferences.promotional_emails"
                  >
                  <div class="notification-item">
                    <span class="notification-icon">🏷️</span>
                    <span>Promotional Emails</span>
                  </div>
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- Navigation buttons -->
        <div class="navigation">
          <button 
            v-if="currentStep > 1" 
            @click="previousStep" 
            class="nav-btn secondary"
          >
            ← Previous
          </button>
          <button 
            v-if="currentStep < 6" 
            @click="nextStep" 
            class="nav-btn primary"
          >
            Next →
          </button>
          <button 
            v-if="currentStep === 6" 
            @click="submitForm" 
            class="nav-btn primary"
            :disabled="isSubmitting"
          >
            {{ isSubmitting ? 'Saving...' : 'Complete Setup' }}
          </button>
        </div>
      </div>
    </div>

    <div class="login-footer">
      <p>Copyright © {{ new Date().getFullYear() }} Pelican Eats, Inc All rights reserved.</p>
    </div>
  </div>
</template>


<script setup>
  import { ref, reactive, onMounted } from 'vue';
  import { useRouter } from 'vue-router';

  const router = useRouter();

  // Form state
  const currentStep = ref(1);
  const activeMealTab = ref('breakfast');
  const currentFoodIndex = ref(0);
  const isSubmitting = ref(false);
  const message = ref('');
  const errors = ref([]);
  const csrf_token = ref('');


// Food swipe data - matching what you actually have in your image
const foodTypes = reactive([
  { id: 1, name: 'Ackee & Saltfish', liked: false, style: '', image: '/uploads/ackee_salt.jpg' },
  { id: 2, name: 'Jerk Chicken', liked: false, style: '', image: '/uploads/jerk_chicken.jpg' },
  { id: 3, name: 'Curry Goat', liked: false, style: '', image: '/uploads/curry_goat.jpg' },
  { id: 4, name: 'Callaloo', liked: false, style: '', image: '/uploads/callaloo.jpg' },
  { id: 5, name: 'Fried Plantain', liked: false, style: '', image: '/uploads/fried_plantain.jpg' },
  { id: 6, name: 'Festival', liked: false, style: '', image: '/uploads/festival.jpg' },
  { id: 7, name: 'Steamed Fish', liked: false, style: '', image: '/uploads/steamed_fish.jpg' }
]);

// Form data - only including fields that exist in your backend
const formData = reactive({
  // Food preferences
  likedFoods: [],
  
  // Dietary restrictions
  dietaryRestrictions: [
    { id: 1, name: 'Vegetarian', icon: '🥗', selected: false, priority: false },
    { id: 2, name: 'Vegan', icon: '🌱', selected: false, priority: false },
    { id: 3, name: 'Gluten-Free', icon: '🌾', selected: false, priority: false },
    { id: 4, name: 'Dairy-Free', icon: '🥛', selected: false, priority: false },
    { id: 5, name: 'Nut-Free', icon: '🥜', selected: false, priority: false },
    { id: 6, name: 'No Seafood', icon: '🐟', selected: false, priority: false },
    { id: 7, name: 'No Restrictions', icon: '🍽️', selected: true, priority: false }
  ],
  
  // Flavor preferences
  flavorPreferences: {
    spiceLevel: 3,
    healthyLevel: 3,
    sweetPreference: 3
  },
  
  // Meat preferences
  meatPreferences: {
    chicken: false,
    fish: false,
    pork: false,
    goat: false,
    beef: false,
    no_meat: false,
    other_meat: ''
  },
  
  // Cooking styles
  cookingStyles: {
    jamaican: false,
    indian: false,
    chinese: false,
    african: false,
    vegan_ital: false,
    italian: false,
    other_style: ''
  },
  
  // Breakfast preferences - only what your backend expects
  breakfastPreferences: {
    porridge: false,
    scrambled_eggs: false,
    pancakes: false,
    french_toast: false,
    waffles: false,
    bacon: false,
    sausage: false,
    sandwich: false,
    other_breakfast: ''
  },
  
  // Popular breakfast items (separate category in backend)
  popularBreakfastItems: {
    ackee_saltfish: false,
    callaloo: false,
    cooked_saltfish: false,
    kidney: false,
    liver: false,
    fried_plantain: false,
    dumplings: false,
    festival: false,
    breadfruit: false,
    other_breakfast_items: ''
  },
  
  // Lunch preferences
  lunchPreferences: {
    fry_chicken: false,
    bake_chicken: false,
    curry_goat: false,
    soups: false,
    steamed_fish: false,
    escovitch_fish: false,
    patty: false,
    sandwiches: false,
    pasta: false,
    other_lunch: ''
  },
  
  // Juice preferences
  juicePreferences: {
    pine_ginger: false,
    callallo_juice: false, // Note: changed key name
    june_plum: false,
    guava_pine: false,
    beet_root: false,
    orange_juice: false, // Note: changed key name
    other_juice: ''
  },
  
  // Budget and order times
  budget: 'medium',
  orderTimes: [],
  additional_notes: '',
  
  // Required by backend but might be empty
  deliveryPreferences: {
    default_address: ' The University of the West Indies Mona Campus, Students Union, unit 6, Kingston 7, Jamaica ',
    delivery_instructions: 'leave in student union office',
    preferred_delivery_time: 'evening'
  },
  
  communicationPreferences: {
    email_notifications: true,
    sms_notifications: false,
    promotional_emails: false
  }
});

// Options for various preferences
const meatOptions = [
  { value: 'chicken', label: 'Chicken', icon: '🐔' },
  { value: 'fish', label: 'Fish', icon: '🐟' },
  { value: 'pork', label: 'Pork', icon: '🐷' },
  { value: 'goat', label: 'Goat', icon: '🐐' },
  { value: 'beef', label: 'Beef', icon: '🐄' },
  { value: 'no_meat', label: "Don't eat meat", icon: '🥗' }
];

const cookingStyles = [
  { value: 'jamaican', label: 'Jamaican', icon: '🇯🇲' },
  { value: 'indian', label: 'Indian', icon: '🇮🇳' },
  { value: 'chinese', label: 'Chinese', icon: '🇨🇳' },
  { value: 'african', label: 'African', icon: '🌍' },
  { value: 'vegan_ital', label: 'Vegan/Ital', icon: '🌱' },
  { value: 'italian', label: 'Italian', icon: '🇮🇹' }
];

// Combined breakfast items - mixing regular and popular
const breakfastItems = [
  // Regular breakfast items
  { value: 'porridge', label: 'Porridge', icon: '🥣', category: 'regular' },
  { value: 'scrambled_eggs', label: 'Scrambled Eggs', icon: '🍳', category: 'regular' },
  { value: 'pancakes', label: 'Pancakes', icon: '🥞', category: 'regular' },
  { value: 'french_toast', label: 'French Toast', icon: '🍞', category: 'regular' },
  { value: 'waffles', label: 'Waffles', icon: '🧇', category: 'regular' },
  { value: 'bacon', label: 'Bacon', icon: '🥓', category: 'regular' },
  { value: 'sausage', label: 'Sausage', icon: '🌭', category: 'regular' },
  { value: 'sandwich', label: 'Sandwich', icon: '🥪', category: 'regular' },
  
  // Popular Jamaican breakfast items
  { value: 'ackee_saltfish', label: 'Ackee & Saltfish', icon: '🐟', category: 'popular' },
  { value: 'callaloo', label: 'Callaloo', icon: '🥬', category: 'popular' },
  { value: 'cooked_saltfish', label: 'Cooked Saltfish', icon: '🐟', category: 'popular' },
  { value: 'kidney', label: 'Kidney', icon: '🫘', category: 'popular' },
  { value: 'liver', label: 'Liver', icon: '🥩', category: 'popular' },
  { value: 'fried_plantain', label: 'Fried Plantain', icon: '🍌', category: 'popular' },
  { value: 'dumplings', label: 'Dumplings', icon: '🥟', category: 'popular' },
  { value: 'festival', label: 'Festival', icon: '🌽', category: 'popular' },
  { value: 'breadfruit', label: 'Breadfruit', icon: '🍈', category: 'popular' }
];

const lunchItems = [
  { value: 'fry_chicken', label: 'Fried Chicken', icon: '🍗' },
  { value: 'bake_chicken', label: 'Baked Chicken', icon: '🐔' },
  { value: 'curry_goat', label: 'Curry Goat', icon: '🍛' },
  { value: 'steamed_fish', label: 'Steamed Fish', icon: '🐟' },
  { value: 'escovitch_fish', label: 'Escovitch Fish', icon: '🐟' },
  { value: 'pasta', label: 'Pasta', icon: '🍝' },
  { value: 'patty', label: 'Patty', icon: '🥧' },
  { value: 'soups', label: 'Soups', icon: '🍲' },
  { value: 'sandwiches', label: 'Sandwiches', icon: '🥪' }
];

const juiceItems = [
  { value: 'pine_ginger', label: 'Pine & Ginger', icon: '🍍' },
  { value: 'callallo_juice', label: 'Callaloo Juice', icon: '🥬' },
  { value: 'june_plum', label: 'June Plum', icon: '🟠' },
  { value: 'guava_pine', label: 'Guava-Pineapple', icon: '🍊' },
  { value: 'beet_root', label: 'Beet Root', icon: '🟤' },
  { value: 'orange_juice', label: 'Orange', icon: '🍊' }
];

const budgetOptions = [
  { value: 'low', label: '$', desc: 'Budget-friendly', icon: '💰' },
  { value: 'medium', label: '$$', desc: 'Moderate', icon: '💰💰' },
  { value: 'high', label: '$$$', desc: 'Premium', icon: '💰💰💰' }
];

const orderTimes = reactive([
  { id: 'morning', name: 'Morning', time: '6am-11am', icon: '🌅', selected: false },
  { id: 'noon', name: 'Noon', time: '11am-2pm', icon: '☀️', selected: false },
  { id: 'afternoon', name: 'Afternoon', time: '2pm-5pm', icon: '🌤️', selected: false },
  { id: 'evening', name: 'Evening', time: '5pm-9pm', icon: '🌆', selected: false },
  { id: 'night', name: 'Night', time: '9pm-12am', icon: '🌙', selected: false }
]);

// Methods
function getCsrfToken() {
  fetch('/api/csrf-token')
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      csrf_token.value = data.csrf_token;
    })
    .catch(error => {
      console.error("Failed to fetch CSRF token:", error);
      errors.value.push("Server connection issue. Please try again later.");
    });
}

onMounted(() => {
  getCsrfToken();
});

function swipeLeft() {
  const currentFood = foodTypes[currentFoodIndex.value];
  currentFood.style = 'transform: translateX(-100%) rotate(-30deg); opacity: 0;';
  currentFood.liked = false;
  
  setTimeout(() => {
    nextFood();
  }, 300);
}

function swipeRight() {
  const currentFood = foodTypes[currentFoodIndex.value];
  currentFood.style = 'transform: translateX(100%) rotate(30deg); opacity: 0;';
  currentFood.liked = true;
  
  setTimeout(() => {
    nextFood();
  }, 300);
}

function nextFood() {
  currentFoodIndex.value++;
  if (currentFoodIndex.value >= foodTypes.length) {
    currentFoodIndex.value = 0;
    foodTypes.forEach(food => {
      food.style = '';
    });
  }
}

function toggleRestriction(restriction) {
  if (restriction.name === 'No Restrictions') {
    formData.dietaryRestrictions.forEach(r => {
      if (r.id !== restriction.id) {
        r.selected = false;
        r.priority = false;
      }
    });
    restriction.selected = true;
    restriction.priority = false;
  } else {
    const noRestriction = formData.dietaryRestrictions.find(r => r.name === 'No Restrictions');
    if (noRestriction) {
      noRestriction.selected = false;
      noRestriction.priority = false;
    }
    
    if (restriction.selected) {
      restriction.priority = !restriction.priority;
      if (!restriction.priority) {
        restriction.selected = false;
      }
    } else {
      restriction.selected = true;
      restriction.priority = false;
    }
  }
}

function getSpiceLabel(level) {
  const labels = ['Very Mild', 'Mild', 'Medium', 'Spicy', 'Very Spicy'];
  return labels[level - 1] || 'Medium';
}

function getHealthLabel(level) {
  const labels = ['Very Healthy', 'Healthy', 'Balanced', 'Indulgent', 'Very Indulgent'];
  return labels[level - 1] || 'Balanced';
}

function getSweetLabel(level) {
  const labels = ['Not Sweet', 'Slightly Sweet', 'Medium', 'Sweet', 'Very Sweet'];
  return labels[level - 1] || 'Medium';
}

function nextStep() {
  if (currentStep.value < 6) {
    currentStep.value++;
  }
}

function previousStep() {
  if (currentStep.value > 1) {
    currentStep.value--;
  }
}

function validateStep() {
  errors.value = [];
  return true;
}

// Submit function that matches backend expectations exactly
function submitForm() {
  message.value = "";
  
  if (!validateStep()) {
    return;
  }
  
  isSubmitting.value = true;
  
  try {
    // Create FormData object
    const form_data = new FormData();
    
    // Add CSRF token
    form_data.append('csrf_token', csrf_token.value);
    
    // Food preferences - liked foods
    form_data.append('food_preferences-liked_foods', JSON.stringify(formData.likedFoods));
    
    // Dietary restrictions
    const selectedRestrictions = formData.dietaryRestrictions
      .filter(r => r.selected)
      .map(r => ({ 
        name: r.name, 
        priority: r.priority,
        selected: true 
      }));
    form_data.append('food_preferences-dietary_restrictions', JSON.stringify(selectedRestrictions));
    
    // Flavor preferences
    form_data.append('food_preferences-flavor_preferences-spice_level', formData.flavorPreferences.spiceLevel);
    form_data.append('food_preferences-flavor_preferences-healthy_level', formData.flavorPreferences.healthyLevel);
    form_data.append('food_preferences-flavor_preferences-sweet_preference', formData.flavorPreferences.sweetPreference);
    
    // Meat preferences
    for (const [key, value] of Object.entries(formData.meatPreferences)) {
      form_data.append(`food_preferences-meat_preferences-${key}`, value);
    }
    
    // Cooking styles
    for (const [key, value] of Object.entries(formData.cookingStyles)) {
      form_data.append(`food_preferences-cooking_styles-${key}`, value);
    }
    
    // Regular breakfast preferences
    for (const [key, value] of Object.entries(formData.breakfastPreferences)) {
      form_data.append(`food_preferences-breakfast_preferences-${key}`, value);
    }
    
    // Popular breakfast items as FieldList
    for (const [key, value] of Object.entries(formData.popularBreakfastItems)) {
      form_data.append(`food_preferences-popular_preferences-0-${key}`, value);
    }
    
    // Lunch preferences
    for (const [key, value] of Object.entries(formData.lunchPreferences)) {
      form_data.append(`food_preferences-lunch_preferences-${key}`, value);
    }
    
    // Juice preferences
    for (const [key, value] of Object.entries(formData.juicePreferences)) {
      form_data.append(`food_preferences-juice_preferences-${key}`, value);
    }
    
    // Budget and order times
    form_data.append('food_preferences-budget', formData.budget);
    
    // Order times as JSON
    const selectedOrderTimes = orderTimes.filter(t => t.selected).map(t => ({
      id: t.id,
      time: t.time
    }));
    form_data.append('food_preferences-order_times', JSON.stringify(selectedOrderTimes));
    
    // Additional notes
    form_data.append('food_preferences-additional_notes', formData.additional_notes);
    
    // Delivery preferences
    form_data.append('delivery_preferences-default_address', formData.deliveryPreferences.default_address);
    form_data.append('delivery_preferences-delivery_instructions', formData.deliveryPreferences.delivery_instructions);
    form_data.append('delivery_preferences-preferred_delivery_time', formData.deliveryPreferences.preferred_delivery_time);
    
    // Communication preferences
    form_data.append('communication_preferences-email_notifications', formData.communicationPreferences.email_notifications);
    form_data.append('communication_preferences-sms_notifications', formData.communicationPreferences.sms_notifications);
    form_data.append('communication_preferences-promotional_emails', formData.communicationPreferences.promotional_emails);
    
    // Debug: Log form data
    console.log('Submitting form data...');

    for (const [key, value] of form_data.entries()) {
      console.log(`${key}: ${value}`);
    }
    
    fetch("/api/gen/onboarding", {
      method: 'POST',
      body: form_data,
      headers: {
        'X-CSRFToken': csrf_token.value
      }
    })
    .then(async function (response) { 
      console.log('Response status:', response.status);
      
      // Check if response is ok
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      // Get response text first
      const text = await response.text();
      console.log('Response text:', text);
      
      // Try to parse as JSON
      try {
        const data = JSON.parse(text);
        return data;
      } catch (e) {
        console.error('Failed to parse JSON:', e);
        throw new Error('Server returned invalid JSON');
      }
    }) 
    .then(function (data) {
      console.log('Success:', data);
      
      message.value = data.message || 'Your preferences have been saved!';
      
      if (data.redirect) {
        setTimeout(() => {
          router.push(data.redirect);
        }, 1500);
      } else {
        setTimeout(() => {
          router.push('/gen/dashboard');
        }, 1500);
      }
    })
    .catch(function (error) {
      console.error('Submission error:', error);
      errors.value.push(error.message || 'Failed to submit form. Please try again.');
    })
    .finally(() => {
      isSubmitting.value = false;
    });
    
  } catch (error) {
    console.error('Form preparation error:', error);
    errors.value.push('Error preparing form data. Please try again.');
    isSubmitting.value = false;
  }
}
</script>


  
<style scoped>
  /* Global styles */
  .main-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    position: relative;
    overflow-x: hidden;
  }

  .background-image {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><rect width="100" height="100" fill="%23f8f9fa"/><circle cx="50" cy="50" r="2" fill="%23dee2e6"/></svg>');
    opacity: 0.5;
  }

  .content-container {
    position: relative;
    z-index: 1;
    padding: 40px 20px;
  }

  .form-wrapper {
    max-width: 600px;
    margin: 0 auto;
    background: white;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    padding: 40px;
    animation: fadeIn 0.5s ease-out;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* Logo and Header */
  .logo-container {
    text-align: center;
    margin-bottom: 30px;
  }

  .logo {
    width: 100px;
    height: auto;
    border-radius: 10px;
  }

  h1 {
    text-align: center;
    color: #333;
    margin-bottom: 30px;
    font-size: 24px;
    font-weight: 600;
  }

  /* Progress indicator */
  .progress-container {
    margin-bottom: 40px;
  }

  .progress-bar {
    height: 8px;
    background: #e0e0e0;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 10px;
  }

  .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
    border-radius: 10px;
    transition: width 0.5s ease;
  }

  .progress-text {
    display: block;
    text-align: center;
    color: #666;
    font-size: 14px;
  }

  /* Alerts */
  .alert {
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    animation: slideIn 0.3s ease-out;
  }

  .alert-success {
    background: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
  }

  .alert-danger {
    background: #f8d7da;
    border: 1px solid #f5c6cb;
    color: #721c24;
  }

  /* Step container */
  .step-container {
    min-height: 400px;
    animation: stepTransition 0.3s ease-out;
  }

  @keyframes stepTransition {
    from {
      opacity: 0;
      transform: translateX(20px);
    }
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }

  .step-content {
    padding: 20px 0;
  }

  h2 {
    text-align: center;
    color: #333;
    margin-bottom: 10px;
    font-size: 22px;
    font-weight: 600;
  }

  .step-description {
    text-align: center;
    color: #666;
    margin-bottom: 30px;
    font-size: 16px;
  }

  /* Food Swipe Section */
  .swipe-container {
    position: relative;
    height: 400px;
    margin: 40px 0;
    perspective: 1000px;
  }

  .swipe-card {
    position: absolute;
    width: 100%;
    height: 100%;
    background: white;
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    cursor: grab;
    user-select: none;
  }

  .swipe-card.top-card {
    z-index: 10;
    transform: scale(1);
  }

  .swipe-card:not(.top-card) {
    transform: scale(0.95) translateY(20px);
    opacity: 0.7;
  }

  .food-image {
    height: 300px;
    overflow: hidden;
    border-radius: 15px 15px 0 0;
  }

  .food-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .food-info {
    padding: 20px;
    text-align: center;
  }

  .food-info h3 {
    margin: 0;
    font-size: 18px;
    color: #333;
    font-weight: 600;
  }

  .swipe-actions {
    display: flex;
    justify-content: space-around;
    margin-top: 30px;
  }

  .swipe-btn {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    border: none;
    font-size: 24px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .dislike-btn {
    background: #ff4444;
    color: white;
  }

  .like-btn {
    background: #4CAF50;
    color: white;
  }

  .swipe-btn:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
  }

  /* Dietary Restrictions */
  .restrictions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 20px;
    margin-top: 30px;
  }

  .restriction-item {
    padding: 15px;
    border: 2px solid #e0e0e0;
    border-radius: 12px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    background: white;
  }

  .restriction-item:hover {
    border-color: #4CAF50;
    transform: translateY(-2px);
  }

  .restriction-item.selected {
    border-color: #4CAF50;
    background: #f0fdf4;
  }

  .restriction-item.priority {
    background: #4CAF50;
    color: white;
    border-color: #4CAF50;
  }

  .restriction-icon {
    font-size: 24px;
    margin-bottom: 8px;
  }

  .restriction-text {
    font-size: 14px;
    font-weight: 500;
  }

  /* Flavor Preferences */
  .flavor-section {
    margin-bottom: 35px;
  }

  .flavor-section label {
    display: block;
    font-weight: 600;
    color: #333;
    margin-bottom: 15px;
    font-size: 16px;
  }

  .flavor-slider {
    width: 100%;
    -webkit-appearance: none;
    appearance: none;
    height: 6px;
    background: #e0e0e0;
    border-radius: 3px;
    outline: none;
    margin-bottom: 10px;
  }

  .flavor-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 20px;
    height: 20px;
    background: #4CAF50;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .flavor-slider::-webkit-slider-thumb:hover {
    transform: scale(1.2);
    background: #45a049;
  }

  .flavor-slider::-moz-range-thumb {
    width: 20px;
    height: 20px;
    background: #4CAF50;
    border-radius: 50%;
    border: none;
    cursor: pointer;
  }

  .slider-labels {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    color: #666;
    margin-top: 5px;
  }

  .slider-labels span:nth-child(2) {
    font-weight: 600;
    color: #4CAF50;
  }

  /* Preferences Section */
  .preferences-section {
    margin-bottom: 35px;
  }

  .preferences-section h3 {
    font-size: 18px;
    color: #333;
    margin-bottom: 20px;
    font-weight: 600;
  }

  .meat-grid, .cooking-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 15px;
  }

  .meat-option, .cooking-option {
    position: relative;
    cursor: pointer;
  }

  .meat-option input, .cooking-option input {
    position: absolute;
    opacity: 0;
    width: 100%;
    height: 100%;
    cursor: pointer;
  }

  .meat-item, .cooking-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 15px;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    background: white;
    transition: all 0.3s ease;
  }

  .meat-option input:checked + .meat-item,
  .cooking-option input:checked + .cooking-item {
    border-color: #4CAF50;
    background: #f0fdf4;
  }

  .meat-icon, .cooking-icon {
    font-size: 28px;
    margin-bottom: 8px;
  }

  /* Meal Preferences */
  .meal-tabs {
    display: flex;
    gap: 10px;
    margin-bottom: 30px;
    justify-content: center;
  }

  .meal-tab {
    padding: 10px 24px;
    border: none;
    background: #f0f0f0;
    border-radius: 25px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 500;
  }

  .meal-tab.active {
    background: #4CAF50;
    color: white;
  }

  .meal-tab:hover:not(.active) {
    background: #e0e0e0;
  }

  .options-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 15px;
  }

  .meal-option {
    position: relative;
    cursor: pointer;
  }

  .meal-option input {
    position: absolute;
    opacity: 0;
    width: 100%;
    height: 100%;
    cursor: pointer;
  }

  .meal-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 15px;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    background: white;
    transition: all 0.3s ease;
    min-height: 80px;
    justify-content: center;
  }

  .meal-option input:checked + .meal-item {
    border-color: #4CAF50;
    background: #f0fdf4;
  }

  .meal-icon {
    font-size: 24px;
    margin-bottom: 8px;
  }

  /* Budget Section */
  .budget-section {
    margin-bottom: 35px;
  }

  .budget-section h3 {
    font-size: 18px;
    color: #333;
    margin-bottom: 20px;
    font-weight: 600;
  }

  .budget-options {
    display: flex;
    gap: 20px;
    justify-content: space-around;
  }

  .budget-option {
    flex: 1;
    cursor: pointer;
  }

  .budget-option input {
    display: none;
  }

  .budget-item {
    padding: 20px;
    border: 2px solid #e0e0e0;
    border-radius: 12px;
    text-align: center;
    background: white;
    transition: all 0.3s ease;
  }

  .budget-option input:checked + .budget-item {
    border-color: #4CAF50;
    background: #f0fdf4;
  }

  .budget-icon {
    font-size: 28px;
    margin-bottom: 10px;
    display: block;
  }

  .budget-label {
    font-weight: 600;
    font-size: 18px;
    color: #333;
    display: block;
    margin-bottom: 5px;
  }

  .budget-desc {
    font-size: 14px;
    color: #666;
    display: block;
  }

  /* Time Section */
  .time-section h3 {
    font-size: 18px;
    color: #333;
    margin-bottom: 20px;
    font-weight: 600;
  }

  .time-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
  }

  .time-option {
    cursor: pointer;
  }

  .time-option input {
    display: none;
  }

  .time-item {
    padding: 15px;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    background: white;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .time-option input:checked + .time-item {
    border-color: #4CAF50;
    background: #f0fdf4;
  }

  .time-icon {
    font-size: 24px;
    flex-shrink: 0;
  }

  .time-label {
    font-weight: 600;
    color: #333;
  }

  .time-desc {
    font-size: 14px;
    color: #666;
    display: block;
  }

    /* Delivery Preferences */
  .delivery-section,
  .communication-section {
    margin-bottom: 35px;
  }

  .delivery-section h3,
  .communication-section h3 {
    font-size: 18px;
    color: #333;
    margin-bottom: 20px;
    font-weight: 600;
  }

  .form-group {
    margin-bottom: 20px;
  }

  .form-group label {
    display: block;
    font-weight: 500;
    margin-bottom: 8px;
    color: #333;
  }

  .text-input,
  .notes-textarea {
    width: 100%;
    padding: 12px 15px;
    border-radius: 10px;
    border: 2px solid #e0e0e0;
    font-size: 16px;
    transition: all 0.3s ease;
  }

  .text-input:focus,
  .notes-textarea:focus {
    border-color: #4CAF50;
    outline: none;
    box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
  }

    /* Delivery Time Options */
  .delivery-time-options {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin-top: 10px;
  }

  .delivery-time-option {
    position: relative;
    cursor: pointer;
  }

  .delivery-time-option input {
    position: absolute;
    opacity: 0;
    cursor: pointer;
  }

  .delivery-time-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 15px;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    background: white;
    transition: all 0.3s ease;
  }

  .delivery-time-option input:checked + .delivery-time-item {
    border-color: #4CAF50;
    background: #f0fdf4;
  }

  .delivery-time-icon {
    font-size: 24px;
    flex-shrink: 0;
  }

  /* Communication Preferences */
  .notification-options {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
  }

  .notification-option {
    cursor: pointer;
    position: relative;
  }

  .notification-option input {
    position: absolute;
    opacity: 0;
    cursor: pointer;
  }

  .notification-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 15px;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    background: white;
    transition: all 0.3s ease;
  }

  .notification-option input:checked + .notification-item {
    border-color: #4CAF50;
    background: #f0fdf4;
  }

  .notification-icon {
    font-size: 24px;
  }

  /* Navigation */
  .navigation {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 40px;
    padding-top: 30px;
    border-top: 1px solid #e0e0e0;
  }

  .nav-btn {
    padding: 12px 32px;
    border-radius: 25px;
    font-weight: 600;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .nav-btn.primary {
    background: #4CAF50;
    color: white;
    border: none;
  }

  .nav-btn.secondary {
    background: #f0f0f0;
    color: #333;
    border: none;
  }

  .nav-btn:hover.primary {
    background: #45a049;
    transform: translateY(-2px);
  }

  .nav-btn:hover.secondary {
    background: #e0e0e0;
    transform: translateY(-2px);
  }

  .nav-btn:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none !important;
  }

  /* Footer */
  .login-footer {
    position: relative;
    text-align: center;
    color: #666;
    font-size: 14px;
    margin-top: 40px;
    padding: 20px;
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .form-wrapper {
      padding: 30px 20px;
    }
    
    .restrictions-grid {
      grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    }
    
    .budget-options {
      flex-direction: column;
    }
    
    .time-grid {
      grid-template-columns: 1fr;
    }
    
    .navigation {
      flex-direction: column-reverse;
      gap: 15px;
    }
    
    .nav-btn {
      width: 100%;
    }
  }

  /* Custom scrollbar */
  ::-webkit-scrollbar {
    width: 8px;
  }

  ::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
  }

  ::-webkit-scrollbar-thumb {
    background: #4CAF50;
    border-radius: 10px;
  }

  ::-webkit-scrollbar-thumb:hover {
    background: #45a049;
  }

</style>
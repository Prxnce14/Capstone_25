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
            <!-- Step 1: Food Swipe -->
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
                  <input type="hidden" v-model="restriction.selected" :name="`dietary_restrictions[${restriction.id}].selected`">
                  <input type="hidden" v-model="restriction.priority" :name="`dietary_restrictions[${restriction.id}].priority`">
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
                  name="flavor_preferences.spice_level"
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
                  name="flavor_preferences.healthy_level" 
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
                  name="flavor_preferences.sweet_preference" 
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
                      :name="`meat_preferences.${meat.value}`"
                    >
                    <div class="meat-item">
                      <span class="meat-icon">{{ meat.icon }}</span>
                      <span>{{ meat.label }}</span>
                    </div>
                  </label>
                </div>
              </div>
  
              <div class="preferences-section">
                <h3>Cooking Styles</h3>
                <div class="cooking-grid">
                  <label v-for="style in cookingStyles" :key="style.value" class="cooking-option">
                    <input 
                      type="checkbox" 
                      v-model="formData.cookingStyles[style.value]"
                      :name="`cooking_styles.${style.value}`"
                    >
                    <div class="cooking-item">
                      <span class="cooking-icon">{{ style.icon }}</span>
                      <span>{{ style.label }}</span>
                    </div>
                  </label>
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
                      :name="`breakfast_preferences.${item.value}`"
                    >
                    <div class="meal-item">
                      <span class="meal-icon">{{ item.icon }}</span>
                      <span>{{ item.label }}</span>
                    </div>
                  </label>
                </div>
              </div>
  
              <div v-if="activeMealTab === 'lunch'" class="meal-options">
                <div class="options-grid">
                  <label v-for="item in lunchItems" :key="item.value" class="meal-option">
                    <input 
                      type="checkbox" 
                      v-model="formData.lunchPreferences[item.value]"
                      :name="`lunch_preferences.${item.value}`"
                    >
                    <div class="meal-item">
                      <span class="meal-icon">{{ item.icon }}</span>
                      <span>{{ item.label }}</span>
                    </div>
                  </label>
                </div>
              </div>
  
              <div v-if="activeMealTab === 'juice'" class="meal-options">
                <div class="options-grid">
                  <label v-for="item in juiceItems" :key="item.value" class="meal-option">
                    <input 
                      type="checkbox" 
                      v-model="formData.juicePreferences[item.value]"
                      :name="`juice_preferences.${item.value}`"
                    >
                    <div class="meal-item">
                      <span class="meal-icon">{{ item.icon }}</span>
                      <span>{{ item.label }}</span>
                    </div>
                  </label>
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
                      name="budget"
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
                      :name="`order_times[${time.id}].selected`"
                    >
                    <div class="time-item">
                      <span class="time-icon">{{ time.icon }}</span>
                      <span class="time-label">{{ time.name }}</span>
                      <span class="time-desc">{{ time.time }}</span>
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

    // Form state using consistent pattern from login script
    const currentStep = ref(1);
    const activeMealTab = ref('breakfast');
    const currentFoodIndex = ref(0);
    const isSubmitting = ref(false);
    const message = ref('');
    const errors = ref([]);
    const csrf_token = ref('');  // Changed from let to const

    // Form data - using reactive object like login script
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
        { id: 7, name: 'Halal', icon: '☪️', selected: false, priority: false },
        { id: 8, name: 'No Restrictions', icon: '🍽️', selected: true, priority: false }
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
    
    // Meal preferences
    breakfastPreferences: {},
    lunchPreferences: {},
    juicePreferences: {},
    
    // Budget and order times
    budget: 'medium',
    orderTimes: []
    });

    // Food swipe data - made reactive
    const foodTypes = reactive([
    { id: 1, name: 'Ackee & Saltfish', liked: false, style: '', image: null },
    { id: 2, name: 'Jerk Chicken', liked: false, style: '', image: null },
    { id: 3, name: 'Curry Goat', liked: false, style: '', image: null },
    { id: 4, name: 'Callaloo', liked: false, style: '', image: null },
    { id: 5, name: 'Fried Plantain', liked: false, style: '', image: null },
    { id: 6, name: 'Rice and Peas', liked: false, style: '', image: null },
    { id: 7, name: 'Festival', liked: false, style: '', image: null },
    { id: 8, name: 'Steamed Fish', liked: false, style: '', image: null }
    ]);

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

    const breakfastItems = [
    { value: 'ackee_saltfish', label: 'Ackee & Saltfish', icon: '🐟' },
    { value: 'callaloo', label: 'Callaloo', icon: '🥬' },
    { value: 'porridge', label: 'Porridge', icon: '🥣' },
    { value: 'fried_plantain', label: 'Fried Plantain', icon: '🍌' },
    { value: 'scrambled_eggs', label: 'Scrambled Eggs', icon: '🍳' },
    { value: 'pancakes', label: 'Pancakes', icon: '🥞' },
    { value: 'festival', label: 'Festival', icon: '🌽' },
    { value: 'dumplings', label: 'Dumplings', icon: '🥟' }
    ];

    const lunchItems = [
    { value: 'fry_chicken', label: 'Fried Chicken', icon: '🍗' },
    { value: 'curry_goat', label: 'Curry Goat', icon: '🍛' },
    { value: 'steamed_fish', label: 'Steamed Fish', icon: '🐟' },
    { value: 'pasta', label: 'Pasta', icon: '🍝' },
    { value: 'patty', label: 'Patty', icon: '🥧' },
    { value: 'soups', label: 'Soups', icon: '🍲' },
    { value: 'sandwiches', label: 'Sandwiches', icon: '🥪' }
    ];

    const juiceItems = [
    { value: 'pine_ginger', label: 'Pine & Ginger', icon: '🍍' },
    { value: 'callallo', label: 'Callaloo Juice', icon: '🥬' },
    { value: 'june_plum', label: 'June Plum', icon: '🟠' },
    { value: 'guava_pine', label: 'Guava-Pineapple', icon: '🍊' },
    { value: 'beet_root', label: 'Beet Root', icon: '🟤' },
    { value: 'orange', label: 'Orange', icon: '🍊' }
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

    // Initialize form defaults
    onMounted(() => {
    // Get CSRF token first
    getCsrfToken();
    
    // Initialize empty objects for meal preferences
    breakfastItems.forEach(item => {
        formData.breakfastPreferences[item.value] = false;
    });
    
    lunchItems.forEach(item => {
        formData.lunchPreferences[item.value] = false;
    });
    
    juiceItems.forEach(item => {
        formData.juicePreferences[item.value] = false;
    });
    
    // Set up event listeners for form inputs (following login pattern)
    const form = document.querySelector('.form-wrapper');
    if (form) {
        form.addEventListener('input', (event) => {
        const target = event.target;
        
        if (target.name && target.type === 'checkbox') {
            // Handle checkboxes (preferences)
            const nameParts = target.name.split('.');
            if (nameParts.length === 2) {
            formData[nameParts[0]][nameParts[1]] = target.checked;
            }
        } else if (target.name && target.type === 'range') {
            // Handle range sliders
            const nameParts = target.name.split('.');
            if (nameParts[0] === 'flavor_preferences') {
            formData.flavorPreferences[nameParts[1]] = parseInt(target.value);
            }
        } else if (target.name === 'budget') {
            // Handle budget radio
            formData.budget = target.value;
        }
        });
    }
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
    formData.likedFoods.push(currentFood.name);
    
    setTimeout(() => {
        nextFood();
    }, 300);
    }

    function nextFood() {
    currentFoodIndex.value++;
    if (currentFoodIndex.value >= foodTypes.length) {
        currentFoodIndex.value = 0;
        // Reset all foods for another round if needed
        foodTypes.forEach(food => {
        food.style = '';
        });
    }
    }

    function toggleRestriction(restriction) {
    if (restriction.name === 'No Restrictions') {
        // If selecting "No Restrictions", deselect all others
        formData.dietaryRestrictions.forEach(r => {
        if (r.id !== restriction.id) {
            r.selected = false;
            r.priority = false;
        }
        });
        restriction.selected = true;
        restriction.priority = false;
    } else {
        // If selecting any other restriction, deselect "No Restrictions"
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
    
    // Add validation logic for each step if needed
    switch(currentStep.value) {
        case 1:
        // Food swipe validation - already handled in swipe functions
        break;
        case 2:
        // Dietary restrictions - optional, no validation needed
        break;
        case 3:
        // Flavor preferences - already have default values
        break;
        case 4:
        // Meat and cooking - optional
        break;
        case 5:
        // Meal preferences - optional
        break;
        case 6:
        // Budget and times - budget has default, times are optional
        break;
    }
    
    return errors.value.length === 0;
    }

    // Submit function using the same pattern as login
    function submitForm() {
    // Clear previous messages
    message.value = "";
    
    // First, validate the form
    if (!validateStep()) {
        return;
    }
    
    isSubmitting.value = true;
    
    // Prepare the data to match your forms.py structure
    const submissionData = {
        food_preferences: {
        liked_foods: formData.likedFoods,
        dietary_restrictions: formData.dietaryRestrictions.filter(r => r.selected),
        flavor_preferences: formData.flavorPreferences,
        meat_preferences: formData.meatPreferences,
        cooking_styles: formData.cookingStyles,
        breakfast_preferences: formData.breakfastPreferences,
        lunch_preferences: formData.lunchPreferences,
        juice_preferences: formData.juicePreferences,
        budget: formData.budget,
        order_times: orderTimes.filter(t => t.selected)
        }
    };
    
    // Convert to FormData like login script
    const form_data = new FormData();
    
    // Add the JSON data as a string
    form_data.append('preferences', JSON.stringify(submissionData));
    
    fetch('/gen/onboarding', {
        method: 'POST',
        body: form_data,
        headers: {
        'X-CSRFToken': csrf_token.value
        }
    })
    .then(function (response) { 
        return response.json().then(data => {
        if (!response.ok) {
            // For error responses, throw the error with the server message
            throw new Error(data.error || 'Failed to save preferences');
        }
        return data;
        });
    }) 
    .then(function (data) {
        console.log(data);
        
        // Set success message
        message.value = data.message || 'Your preferences have been saved!';
        
        // Redirect based on response
        if (data.redirect) {
        // Allow the success message to be seen briefly before redirecting
        setTimeout(() => {
            router.push(data.redirect);
        }, 1500);
        } else {
        router.push('/dashboard');
        }
    })
    .catch(function (error) {
        console.error('Submission error:', error);
        errors.value.push(error.message);
    })
    .finally(() => {
        isSubmitting.value = false;
    });

    }
    
</script>  

  
  
  
  
<style scoped>
  /* Base Variables */
  :root {
    --primary-orange: #FF8C00;
    --primary-orange-light: #FFB347;
    --primary-orange-dark: #CC7000;
    --secondary-bg: #F8F9FA;
    --text-dark: #333333;
    --text-light: #666666;
    --border-light: #E8E8E8;
    --success-green: #28A745;
    --error-red: #DC3545;
    --white: #FFFFFF;
    --shadow-sm: 0 2px 4px rgba(0,0,0,0.05);
    --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
    --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
    --border-radius: 12px;
    --transition: all 0.3s ease;
  }
  
  /* Reset & Base Styles */
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
  
  /* Main Container */
  .main-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
  }
  
  /* Background Image */
  .background-image {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, rgba(255, 140, 0, 0.1) 0%, rgba(255, 179, 71, 0.05) 100%);
    z-index: 1;
  }
  
  /* Content Container */
  .content-container {
    position: relative;
    z-index: 2;
    max-width: 800px;
    width: 100%;
    margin: 40px auto;
    padding: 0 20px;
    flex: 1;
  }
  
  /* Form Wrapper */
  .form-wrapper {
    background: var(--white);
    padding: 40px;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow-lg);
    animation: fadeIn 0.6s ease-out;
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
  
  /* Logo */
  .logo-container {
    text-align: center;
    margin-bottom: 30px;
  }
  
  .logo {
    max-width: 120px;
    height: auto;
    transition: var(--transition);
  }
  
  .logo:hover {
    transform: scale(1.05);
  }
  
  /* Headers */
  h1 {
    text-align: center;
    color: var(--primary-orange);
    font-size: 2rem;
    margin-bottom: 30px;
    font-weight: 600;
  }
  
  h2 {
    color: var(--text-dark);
    font-size: 1.5rem;
    margin-bottom: 10px;
    font-weight: 600;
  }
  
  h3 {
    color: var(--text-dark);
    font-size: 1.2rem;
    margin-bottom: 15px;
    font-weight: 500;
  }
  
  /* Progress Bar */
  .progress-container {
    margin-bottom: 40px;
  }
  
  .progress-bar {
    width: 100%;
    height: 8px;
    background-color: var(--border-light);
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 10px;
  }
  
  .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--primary-orange) 0%, var(--primary-orange-light) 100%);
    border-radius: 4px;
    transition: width 0.5s ease;
  }
  
  .progress-text {
    text-align: center;
    color: var(--text-light);
    font-size: 0.9rem;
    display: block;
  }
  
  /* Alert Messages */
  .alert {
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 20px;
    animation: slideIn 0.3s ease-out;
  }
  
  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateX(-20px);
    }
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }
  
  .alert-success {
    background-color: rgba(40, 167, 69, 0.1);
    color: var(--success-green);
    border: 1px solid rgba(40, 167, 69, 0.2);
  }
  
  .alert-danger {
    background-color: rgba(220, 53, 69, 0.1);
    color: var(--error-red);
    border: 1px solid rgba(220, 53, 69, 0.2);
  }
  
  /* Step Container */
  .step-container {
    min-height: 500px;
    margin-bottom: 30px;
  }
  
  .step-content {
    animation: stepTransition 0.4s ease-out;
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
  
  .step-description {
    text-align: center;
    color: var(--text-light);
    margin-bottom: 30px;
    font-size: 1rem;
  }
  
  /* Food Swipe Section */
  .swipe-container {
    width: 100%;
    height: 400px;
    position: relative;
    margin: 40px auto;
    perspective: 1000px;
  }
  
  .swipe-card {
    position: absolute;
    width: 300px;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    background: var(--white);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow-md);
    overflow: hidden;
    transition: var(--transition);
    cursor: pointer;
  }
  
  .swipe-card:not(.top-card) {
    transform: translate(-50%, -50%) scale(0.95);
    opacity: 0.7;
    z-index: 1;
  }
  
  .swipe-card.top-card {
    z-index: 10;
  }
  
  .food-image {
    height: 250px;
    overflow: hidden;
    position: relative;
  }
  
  .food-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .food-info {
    padding: 20px;
    text-align: center;
    background: linear-gradient(to bottom, var(--white) 0%, rgba(255, 240, 230, 0.5) 100%);
  }
  
  .food-info h3 {
    color: var(--text-dark);
    margin: 0;
    font-size: 1.1rem;
  }
  
  .swipe-actions {
    text-align: center;
    margin-top: 30px;
    display: flex;
    justify-content: center;
    gap: 40px;
  }
  
  .swipe-btn {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    border: none;
    font-size: 24px;
    cursor: pointer;
    transition: var(--transition);
    box-shadow: var(--shadow-md);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .like-btn {
    background: linear-gradient(135deg, var(--primary-orange) 0%, var(--primary-orange-light) 100%);
    color: var(--white);
  }
  
  .dislike-btn {
    background: var(--white);
    color: var(--error-red);
    border: 2px solid var(--error-red);
  }
  
  .swipe-btn:hover {
    transform: scale(1.1);
  }
  
  .like-btn:hover {
    background: linear-gradient(135deg, var(--primary-orange-dark) 0%, var(--primary-orange) 100%);
  }
  
  .dislike-btn:hover {
    background: var(--error-red);
    color: var(--white);
  }
  
  /* Dietary Restrictions Grid */
  .restrictions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-top: 20px;
  }
  
  .restriction-item {
    background: var(--white);
    border: 2px solid var(--border-light);
    border-radius: var(--border-radius);
    padding: 20px;
    text-align: center;
    cursor: pointer;
    transition: var(--transition);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
  }
  
  .restriction-item:hover {
    border-color: var(--primary-orange-light);
    transform: translateY(-2px);
  }
  
  .restriction-item.selected {
    border-color: var(--primary-orange);
    background: rgba(255, 140, 0, 0.05);
  }
  
  .restriction-item.priority {
    background: linear-gradient(135deg, rgba(255, 140, 0, 0.1) 0%, rgba(255, 179, 71, 0.05) 100%);
    border-color: var(--primary-orange);
    box-shadow: 0 0 0 3px rgba(255, 140, 0, 0.2);
  }
  
  .restriction-icon {
    font-size: 32px;
    margin-bottom: 5px;
  }
  
  .restriction-text {
    color: var(--text-dark);
    font-weight: 500;
  }
  
  /* Flavor Preferences */
  .flavor-section {
    margin-bottom: 40px;
  }
  
  .flavor-section label {
    display: block;
    color: var(--text-dark);
    font-weight: 500;
    margin-bottom: 15px;
    font-size: 1.1rem;
  }
  
  .flavor-slider {
    width: 100%;
    height: 8px;
    -webkit-appearance: none;
    appearance: none;
    background: var(--border-light);
    border-radius: 4px;
    outline: none;
    margin-bottom: 10px;
  }
  
  .flavor-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 24px;
    height: 24px;
    background: var(--primary-orange);
    border-radius: 50%;
    cursor: pointer;
    box-shadow: var(--shadow-sm);
    transition: var(--transition);
  }
  
  .flavor-slider::-webkit-slider-thumb:hover {
    background: var(--primary-orange-dark);
    transform: scale(1.1);
  }
  
  .flavor-slider::-moz-range-thumb {
    width: 24px;
    height: 24px;
    background: var(--primary-orange);
    border-radius: 50%;
    cursor: pointer;
    border: none;
    box-shadow: var(--shadow-sm);
    transition: var(--transition);
  }
  
  .slider-labels {
    display: flex;
    justify-content: space-between;
    color: var(--text-light);
    font-size: 0.9rem;
  }
  
  .slider-labels span:nth-child(2) {
    color: var(--primary-orange);
    font-weight: 600;
  }
  
  /* Meat and Cooking Preferences */
  .preferences-section {
    margin-bottom: 40px;
  }
  
  .meat-grid,
  .cooking-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 15px;
    margin-top: 20px;
  }
  
  .meat-option,
  .cooking-option {
    display: block;
    cursor: pointer;
  }
  
  .meat-option input,
  .cooking-option input {
    display: none;
  }
  
  .meat-item,
  .cooking-item {
    background: var(--white);
    border: 2px solid var(--border-light);
    border-radius: var(--border-radius);
    padding: 15px;
    text-align: center;
    transition: var(--transition);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
  }
  
  .meat-option:hover .meat-item,
  .cooking-option:hover .cooking-item {
    border-color: var(--primary-orange-light);
    transform: translateY(-2px);
  }
  
  .meat-option input:checked ~ .meat-item,
  .cooking-option input:checked ~ .cooking-item {
    border-color: var(--primary-orange);
    background: rgba(255, 140, 0, 0.05);
  }
  
  .meat-icon,
  .cooking-icon {
    font-size: 24px;
  }
  
  /* Meal Preferences */
  .meal-tabs {
    display: flex;
    gap: 10px;
    margin-bottom: 30px;
    border-bottom: 2px solid var(--border-light);
  }
  
  .meal-tab {
    padding: 12px 24px;
    border: none;
    background: none;
    color: var(--text-light);
    font-size: 1rem;
    cursor: pointer;
    border-bottom: 3px solid transparent;
    margin-bottom: -2px;
    transition: var(--transition);
  }
  
  .meal-tab:hover {
    color: var(--primary-orange);
  }
  
  .meal-tab.active {
    color: var(--primary-orange);
    border-bottom-color: var(--primary-orange);
    font-weight: 600;
  }
  
  .options-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 20px;
    margin-top: 20px;
  }
  
  .meal-option {
    display: block;
    cursor: pointer;
  }
  
  .meal-option input {
    display: none;
  }
  
  .meal-item {
    background: var(--white);
    border: 2px solid var(--border-light);
    border-radius: var(--border-radius);
    padding: 20px;
    text-align: center;
    transition: var(--transition);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    min-height: 100px;
  }
  
  .meal-option:hover .meal-item {
    border-color: var(--primary-orange-light);
    transform: translateY(-2px);
  }
  
  .meal-option input:checked ~ .meal-item {
    border-color: var(--primary-orange);
    background: rgba(255, 140, 0, 0.05);
  }
  
  .meal-icon {
    font-size: 28px;
  }
  
  /* Budget and Order Times */
  .budget-section,
  .time-section {
    margin-bottom: 40px;
  }
  
  .budget-options {
    display: flex;
    gap: 20px;
    justify-content: center;
    margin-top: 20px;
  }
  
  .budget-option {
    flex: 1;
    cursor: pointer;
  }
  
  .budget-option input {
    display: none;
  }
  
  .budget-item {
    background: var(--white);
    border: 2px solid var(--border-light);
    border-radius: var(--border-radius);
    padding: 20px;
    text-align: center;
    transition: var(--transition);
  }
  
  .budget-option:hover .budget-item {
    border-color: var(--primary-orange-light);
    transform: translateY(-2px);
  }
  
  .budget-option input:checked ~ .budget-item {
    border-color: var(--primary-orange);
    background: rgba(255, 140, 0, 0.05);
  }
  
  .budget-icon {
    font-size: 24px;
    display: block;
    margin-bottom: 5px;
  }
  
  .budget-label {
    font-size: 18px;
    font-weight: 600;
    color: var(--primary-orange);
    display: block;
    margin-bottom: 5px;
  }
  
  .budget-desc {
    color: var(--text-light);
    font-size: 0.9rem;
  }
  
  .time-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 15px;
    margin-top: 20px;
  }
  
  .time-option {
    display: block;
    cursor: pointer;
  }
  
  .time-option input {
    display: none;
  }
  
  .time-item {
    background: var(--white);
    border: 2px solid var(--border-light);
    border-radius: var(--border-radius);
    padding: 15px;
    text-align: center;
    transition: var(--transition);
  }
  
  .time-option:hover .time-item {
    border-color: var(--primary-orange-light);
    transform: translateY(-2px);
  }
  
  .time-option input:checked ~ .time-item {
    border-color: var(--primary-orange);
    background: rgba(255, 140, 0, 0.05);
  }
  
  .time-icon {
    font-size: 24px;
    display: block;
    margin-bottom: 5px;
  }
  
  .time-label {
    font-weight: 500;
    color: var(--text-dark);
    display: block;
    margin-bottom: 2px;
  }
  
  .time-desc {
    color: var(--text-light);
    font-size: 0.85rem;
  }
  
  /* Navigation */
  .navigation {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 40px;
  }
  
  .nav-btn {
    padding: 12px 32px;
    border-radius: var(--border-radius);
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: var(--transition);
    display: inline-flex;
    align-items: center;
    gap: 8px;
  }
  
  .nav-btn.primary {
    background: linear-gradient(135deg, var(--primary-orange) 0%, var(--primary-orange-light) 100%);
    color: var(--white);
    border: none;
    box-shadow: var(--shadow-sm);
  }
  
  .nav-btn.primary:hover {
    background: linear-gradient(135deg, var(--primary-orange-dark) 0%, var(--primary-orange) 100%);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
  
  .nav-btn.primary:disabled {
    background: var(--text-light);
    transform: none;
    box-shadow: none;
    cursor: not-allowed;
  }
  
  .nav-btn.secondary {
    background: var(--white);
    color: var(--text-dark);
    border: 2px solid var(--border-light);
  }
  
  .nav-btn.secondary:hover {
    border-color: var(--primary-orange);
    color: var(--primary-orange);
    transform: translateY(-2px);
  }
  
  /* Footer */
  .login-footer {
    background: var(--white);
    padding: 20px;
    text-align: center;
    border-top: 1px solid var(--border-light);
    margin-top: auto;
    position: relative;
    z-index: 2;
  }
  
  .login-footer p {
    color: var(--text-light);
    font-size: 0.9rem;
    margin: 0;
  }
  
  /* Responsive Design */
  @media (max-width: 768px) {
    .form-wrapper {
      padding: 30px 20px;
    }
    
    h1 {
      font-size: 1.5rem;
    }
    
    .swipe-card {
      width: 100%;
      max-width: 280px;
    }
    
    .restrictions-grid,
    .meat-grid,
    .cooking-grid,
    .options-grid {
      grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    }
    
    .meal-tabs {
      overflow-x: auto;
      flex-wrap: nowrap;
      padding-bottom: 5px;
    }
    
    .budget-options {
      flex-direction: column;
    }
    
    .navigation {
      flex-direction: column;
      gap: 15px;
    }
    
    .nav-btn {
      width: 100%;
      justify-content: center;
    }
  }
  
  @media (max-width: 480px) {
    .content-container {
      margin: 20px auto;
      padding: 0 15px;
    }
    
    .form-wrapper {
      padding: 20px 15px;
    }
    
    .swipe-card {
      max-width: 240px;
    }
    
    .food-image {
      height: 200px;
    }
    
    .restrictions-grid,
    .meat-grid,
    .cooking-grid,
    .options-grid,
    .time-grid {
      grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
      gap: 10px;
    }
  }
  
  /* Custom Scrollbar */
  ::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }
  
  ::-webkit-scrollbar-track {
    background: var(--secondary-bg);
  }
  
  ::-webkit-scrollbar-thumb {
    background: var(--primary-orange-light);
    border-radius: 4px;
  }
  
  ::-webkit-scrollbar-thumb:hover {
    background: var(--primary-orange);
  }
  
  /* Focus States for Accessibility */
  *:focus {
    outline: 2px solid var(--primary-orange);
    outline-offset: 2px;
  }
  
</style>
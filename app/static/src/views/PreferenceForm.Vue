<!-- Food Preference Quiz App.vue -->
<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-orange-50 to-amber-100 p-4">
    <div v-if="!quizCompleted" class="w-full max-w-md bg-white rounded-xl shadow-lg p-6">
      <!-- Progress indicator -->
      <div class="mb-6">
        <div class="flex justify-between mb-1 text-xs text-gray-500">
          <span>Your Food Profile</span>
          <span>{{ currentStep }}/5</span>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2">
          <div class="bg-amber-500 h-2 rounded-full" :style="`width: ${(currentStep/5)*100}%`"></div>
        </div>
      </div>

      <!-- Step 1: Food Swipe Cards -->
      <div v-if="currentStep === 1" class="transition-all duration-300">
        <h2 class="text-xl font-bold text-center mb-6">Swipe on Foods You Like</h2>
        <div class="relative h-64">
          <div 
            v-for="(food, index) in foodType" 
            :key="food.id"
            class="absolute w-full h-64 rounded-lg shadow-md overflow-hidden transition-all duration-300"
            :class="{'z-10': index === 0}"
            :style="`transform: translateX(${food.offset}px) rotate(${food.rotation}deg); opacity: ${1 - (index * 0.2)}`"
          >
            <img :src="`/api/placeholder/400/320`" :alt="food.name" class="w-full h-full object-cover" />
            <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-4">
              <span class="text-white font-bold">{{ food.name }}</span>
            </div>
          </div>
        </div>
        
        <div class="flex justify-center space-x-6 mt-6">
          <button @click="swipeLeft" class="bg-red-500 hover:bg-red-600 text-white rounded-full w-14 h-14 flex items-center justify-center text-xl">✕</button>
          <button @click="swipeRight" class="bg-green-500 hover:bg-green-600 text-white rounded-full w-14 h-14 flex items-center justify-center text-xl">✓</button>
        </div>
        
        <div class="text-center mt-6">
          <button @click="nextStep" class="text-amber-600 text-sm font-medium">
            Skip this step →
          </button>
        </div>
      </div>

      <!-- Step 2: Dietary Restrictions -->
      <div v-if="currentStep === 2" class="transition-all duration-300">
        <h2 class="text-xl font-bold text-center mb-6">Any Food Restrictions?</h2>
        <div class="grid grid-cols-3 gap-3">
          <div 
            v-for="restriction in dietaryRestrictions" 
            :key="restriction.id"
            @click="toggleRestriction(restriction.id)"
            class="flex flex-col items-center justify-center p-3 rounded-lg cursor-pointer transition-all duration-200"
            :class="[
              restriction.selected ? 'bg-amber-100 border-2 border-amber-500' : 'bg-gray-100 border-2 border-transparent',
              restriction.priority ? 'ring-2 ring-red-500' : ''
            ]"
          >
            <div class="text-2xl mb-1">{{ restriction.icon }}</div>
            <div class="text-xs text-center">{{ restriction.name }}</div>
          </div>
        </div>
        
        <div class="text-center mt-6 text-sm text-gray-600">
          <p>Tap once to select, twice for high priority</p>
        </div>
        
        <div class="flex justify-between mt-6">
          <button @click="prevStep" class="px-4 py-2 text-amber-600 font-medium">← Back</button>
          <button @click="nextStep" class="px-6 py-2 bg-amber-500 text-white rounded-lg font-medium">Next</button>
        </div>
      </div>

      <!-- Step 3: Flavor Profiles -->
      <div v-if="currentStep === 3" class="transition-all duration-300">
        <h2 class="text-xl font-bold text-center mb-6">Your Flavor Profile</h2>
        
        <div class="mb-8">
          <div class="flex justify-between mb-1">
            <span>🌶️ Mild</span>
            <span>Spicy 🔥</span>
          </div>
          <input type="range" v-model="preferences.spiceLevel" min="1" max="5" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-amber-500">
          <div class="flex justify-between text-xs text-gray-500 mt-1">
            <span>No spice for me</span>
            <span v-if="preferences.spiceLevel >= 4">Bring the heat!</span>
            <span v-else>Just right</span>
          </div>
        </div>
        
        <div class="mb-6">
          <div class="flex justify-between mb-1">
            <span>🥗 Healthy</span>
            <span>Indulgent 🍔</span>
          </div>
          <input type="range" v-model="preferences.healthyLevel" min="1" max="5" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-amber-500">
          <div class="flex justify-between text-xs text-gray-500 mt-1">
            <span>Nutrition focused</span>
            <span v-if="preferences.healthyLevel >= 4">Treat myself</span>
            <span v-else>Balance</span>
          </div>
        </div>
        
        <div class="flex justify-between mt-8">
          <button @click="prevStep" class="px-4 py-2 text-amber-600 font-medium">← Back</button>
          <button @click="nextStep" class="px-6 py-2 bg-amber-500 text-white rounded-lg font-medium">Next</button>
        </div>
      </div>

      <!-- Step 4: Budget Bubbles -->
      <div v-if="currentStep === 4" class="transition-all duration-300">
        <h2 class="text-xl font-bold text-center mb-6">Your Budget Preference</h2>
        
        <div class="flex justify-center space-x-4 mb-8">
          <div 
            v-for="option in budgetOptions" 
            :key="option.value"
            @click="selectBudget(option.value)"
            class="flex items-center justify-center rounded-full transition-all duration-200 cursor-pointer"
            :class="[
              preferences.budget === option.value ? 'bg-amber-500 text-white border-2 border-amber-600' : 'bg-gray-100 text-gray-700 border-2 border-transparent',
              option.size
            ]"
          >
            <div class="font-bold">{{ option.label }}</div>
          </div>
        </div>
        
        <div class="text-center text-sm text-gray-600 mb-6">
          <p>Tap a bubble based on your usual budget per meal</p>
        </div>
        
        <div class="flex justify-between mt-6">
          <button @click="prevStep" class="px-4 py-2 text-amber-600 font-medium">← Back</button>
          <button @click="nextStep" class="px-6 py-2 bg-amber-500 text-white rounded-lg font-medium">Next</button>
        </div>
      </div>

      <!-- Step 5: Order Times -->
      <div v-if="currentStep === 5" class="transition-all duration-300">
        <h2 class="text-xl font-bold text-center mb-6">When Do You Usually Order?</h2>
        
        <div class="grid grid-cols-3 gap-3 mb-6">
          <div 
            v-for="timeBlock in orderTimes" 
            :key="timeBlock.id"
            @click="toggleOrderTime(timeBlock.id)"
            class="p-3 rounded-lg text-center cursor-pointer transition-all duration-200"
            :class="timeBlock.selected ? 'bg-amber-100 border-2 border-amber-500' : 'bg-gray-100 border-2 border-transparent'"
          >
            <div class="text-xl mb-1">{{ timeBlock.icon }}</div>
            <div class="text-xs">{{ timeBlock.name }}</div>
          </div>
        </div>
        
        <div class="flex justify-between mt-8">
          <button @click="prevStep" class="px-4 py-2 text-amber-600 font-medium">← Back</button>
          <button @click="completeQuiz" class="px-6 py-2 bg-amber-500 text-white rounded-lg font-medium">Finish</button>
        </div>
      </div>
    </div>

    <!-- Completion Screen -->
    <div v-if="quizCompleted" class="w-full max-w-md bg-white rounded-xl shadow-lg p-6 text-center">
      <div class="mb-6 text-6xl">🎉</div>
      <h2 class="text-2xl font-bold mb-4">Your Taste Profile Is Ready!</h2>
      <p class="text-gray-600 mb-6">We've created personalized recommendations just for you. Get ready to discover meals you'll love!</p>
      <button @click="goToApp" class="w-full px-6 py-3 bg-amber-500 text-white rounded-lg font-medium">Start Exploring</button>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        currentStep: 1,
        quizCompleted: false,
        foodType: [
          { id: 1, name: 'Pizza', offset: 0, rotation: 0, liked: false },
          { id: 2, name: 'Chicken', offset: 0, rotation: 0, liked: false },
          { id: 3, name: 'Beef', offset: 0, rotation: 0, liked: false },
          { id: 4, name: 'Vegan Bowl', offset: 0, rotation: 0, liked: false },
          { id: 5, name: 'Fish meal', offset: 0, rotation: 0, liked: false },
          { id: 6, name: 'Soup', offset: 0, rotation: 0, liked: false }
        ],
        dietaryRestrictions: [
          { id: 1, name: 'Vegetarian', icon: '🥗', selected: false, priority: false },
          { id: 2, name: 'Vegan', icon: '🌱', selected: false, priority: false },
          { id: 3, name: 'Gluten-Free', icon: '🌾', selected: false, priority: false },
          { id: 4, name: 'Dairy-Free', icon: '🥛', selected: false, priority: false },
          { id: 5, name: 'Nut-Free', icon: '🥜', selected: false, priority: false },
          { id: 6, name: 'No Seafood', icon: '🐟', selected: false, priority: false },
          { id: 7, name: 'No Restrictions', icon: '🍽️', selected: false, priority: false }
        ],
        preferences: {
          spiceLevel: 3,
          healthyLevel: 3,
          budget: 'medium'
        },
        budgetOptions: [
          { value: 'low', label: '$', size: 'w-16 h-16' },
          { value: 'medium', label: '$$', size: 'w-20 h-20' },
          { value: 'high', label: '$$$', size: 'w-24 h-24' }
        ],
        orderTimes: [
          { id: 'morning', name: 'Morning', icon: '🌅', selected: false, time: '6am-11am' },
          { id: 'midday', name: 'Midday', icon: '☀️', selected: false, time: '11am-3pm' },
          { id: 'evening', name: 'Evening', icon: '🌆', selected: false, time: '3pm-8pm' },
          { id: 'night', name: 'Night', icon: '🌙', selected: false, time: '8pm-12am' },
          { id: 'latenight', name: 'Late Night', icon: '🌚', selected: false, time: '12am-6am' },
          { id: 'weekends', name: 'Weekends', icon: '📅', selected: false }
        ]
      }
    },
    methods: {
      swipeLeft() {
        if (this.foodType.length > 0) {
          const currentFood = this.foodType[0];
          currentFood.offset = -300;
          currentFood.rotation = -15;
          currentFood.liked = false;
          
          // Move to the back after animation
          setTimeout(() => {
            this.foodType.push(this.foodType.shift());
            this.resetTopCard();
          }, 300);
        }
      },
      swipeRight() {
        if (this.foodType.length > 0) {
          const currentFood = this.foodType[0];
          currentFood.offset = 300;
          currentFood.rotation = 15;
          currentFood.liked = true;
          
          // Move to the back after animation
          setTimeout(() => {
            this.foodType.push(this.foodType.shift());
            this.resetTopCard();
          }, 300);
        }
      },
      resetTopCard() {
        if (this.foodType.length > 0) {
          this.foodType[0].offset = 0;
          this.foodType[0].rotation = 0;
        }
      },
      toggleRestriction(id) {
        const restriction = this.dietaryRestrictions.find(r => r.id === id);
        if (restriction.selected) {
          // If already selected, toggle priority
          restriction.priority = !restriction.priority;
          if (!restriction.priority) {
            // If removing priority, also remove selection
            restriction.selected = false;
          }
        } else {
          // First tap, just select it
          restriction.selected = true;
          restriction.priority = false;
        }
      },
      toggleOrderTime(id) {
        const timeBlock = this.orderTimes.find(t => t.id === id);
        timeBlock.selected = !timeBlock.selected;
      },
      selectBudget(value) {
        this.preferences.budget = value;
      },
      nextStep() {
        if (this.currentStep < 5) {
          this.currentStep++;
        }
      },
      prevStep() {
        if (this.currentStep > 1) {
          this.currentStep--;
        }
      },
      completeQuiz() {
        // Prepare data to send to backend
        const preferencesData = {
          likedFoods: this.foodType.filter(food => food.liked).map(food => food.name),
          dietaryRestrictions: this.dietaryRestrictions.filter(r => r.selected).map(r => ({
            name: r.name,
            priority: r.priority
          })),
          flavorPreferences: {
            spiceLevel: this.preferences.spiceLevel,
            healthyLevel: this.preferences.healthyLevel
          },
          budget: this.preferences.budget,
          orderTimes: this.orderTimes.filter(t => t.selected).map(t => t.id)
        };
        
        // Here you would typically make an API call to save preferences
        console.log('Sending preferences to backend:', preferencesData);
        
        // For demo purposes, just mark as completed
        this.quizCompleted = true;
      },
      goToApp() {
        // Navigate to main app after completing quiz
        console.log('Navigating to main app');
        // In real app: this.$router.push('/dashboard');
      }
    }
  }
</script>
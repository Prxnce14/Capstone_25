<template>
  <div class="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
    <h2 class="text-2xl font-bold mb-6 text-center">Your Food Preferences</h2>
    <form @submit.prevent="submitPreferences">
      <!-- Dietary Preferences -->
      <div class="mb-4">
        <label class="block text-gray-700 font-semibold mb-2">Dietary Preferences</label>
        <div class="space-y-2">
          <label v-for="diet in dietaryOptions" :key="diet" class="flex items-center">
            <input
              type="checkbox"
              v-model="form.dietaryPreferences"
              :value="diet"
              class="mr-2"
            />
            {{ diet }}
          </label>
        </div>
      </div>

      <!-- Favorite Cuisines -->
      <div class="mb-4">
        <label class="block text-gray-700 font-semibold mb-2">Favorite Cuisines</label>
        <div class="space-y-2">
          <label v-for="cuisine in cuisineOptions" :key="cuisine" class="flex items-center">
            <input
              type="checkbox"
              v-model="form.favoriteCuisines"
              :value="cuisine"
              class="mr-2"
            />
            {{ cuisine }}
          </label>
        </div>
      </div>

      <!-- Delivery Time Preference -->
      <div class="mb-6">
        <label class="block text-gray-700 font-semibold mb-2">Preferred Delivery Time</label>
        <select
          v-model="form.deliveryTime"
          class="w-full p-2 border rounded-md"
          required
        >
          <option value="" disabled>Select a time</option>
          <option v-for="time in deliveryTimes" :key="time" :value="time">
            {{ time }}
          </option>
        </select>
      </div>

      <!-- Submit Button -->
      <button
        type="submit"
        class="w-full bg-blue-500 text-white p-2 rounded-md hover:bg-blue-600"
        :disabled="isSubmitting"
      >
        {{ isSubmitting ? 'Submitting...' : 'Save Preferences' }}
      </button>
    </form>
  </div>
</template>
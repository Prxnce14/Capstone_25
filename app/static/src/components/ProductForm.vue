<template>
  <form @submit.prevent="handleSubmit">
    <!-- Basic Product Fields -->
    <input v-model="product.name" placeholder="Name" required />
    <input v-model.number="product.price" type="number" placeholder="Price" required />
    <input v-model.number="product.quantity" type="number" placeholder="Quantity" required />
    <textarea v-model="product.description" placeholder="Description"></textarea>

    <!-- Category Selector -->
    <select v-model="product.category">
      <option disabled value="">Select Category</option>
      <option value="appetizer">Appetizer</option>
      <option value="main_course">Main Course</option>
      <option value="dessert">Dessert</option>
      <option value="beverage">Beverage</option>
      <option value="side">Side Dish</option>
      <option value="special">Daily Special</option>
    </select>

    <!-- Toggles -->
    <label><input type="checkbox" v-model="product.is_vegetarian" /> Vegetarian</label>
    <label><input type="checkbox" v-model="product.is_vegan" /> Vegan</label>
    <label><input type="checkbox" v-model="product.is_gluten_free" /> Gluten-Free</label>
    <label><input type="checkbox" v-model="product.is_featured" /> Featured</label>

    <!-- Discount -->
    <input v-model.number="product.discount_percentage" type="number" placeholder="Discount %" min="0" max="100" />

    <!-- Minimum stock -->
    <input v-model.number="product.minimum_stock" type="number" placeholder="Minimum Stock" min="0" />

    <!-- Image Upload -->
    <input type="file" @change="handleImageUpload" accept="image/*" />
    <img v-if="imagePreview" :src="imagePreview" alt="Preview" class="h-20 mt-2" />
    <span v-if="errors.image" class="text-red-600">{{ errors.image }}</span>

    <!-- Submit -->
    <button type="submit">{{ isEditing ? 'Update' : 'Create' }}</button>
    <button type="button" @click="$emit('cancel')">Cancel</button>
  </form>
</template>

<script>
export default {
  props: {
    product: Object,
    isEditing: Boolean,
    imagePreview: String,
    errors: Object
  },
  emits: ['submit', 'cancel', 'image-upload'],
  methods: {
    handleSubmit() {
      this.$emit('submit');
    },
    handleImageUpload(event) {
      this.$emit('image-upload', event);
    }
  }
};
</script>

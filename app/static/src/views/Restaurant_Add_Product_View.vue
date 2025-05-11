<template>
  <div class="product-form-wrapper">
    <!-- Page Title -->
    <h1 class="page-title">{{ isEditing ? 'Edit Product' : 'Add Product' }}</h1>
    
    <!-- Alert messages for feedback -->
    <div v-if="message || errors.length > 0" 
         :class="{'alert alert-success': message, 'alert alert-danger': errors.length > 0}" 
         role="alert">
      <p v-if="message">{{ message }}</p>
      <ul v-if="errors.length > 0">
        <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
      </ul>
    </div>

    <form @submit.prevent="handleSubmit" enctype="multipart/form-data" class="product-form">
      <div class="form-content">
        <div class="image-section">
          <div class="image-container">
            <div v-if="imagePreview" class="image-preview">
              <img :src="imagePreview" alt="Image preview" />
            </div>
            <div v-else class="placeholder-image">
              <span>No image selected</span>
            </div>
          </div>
        </div>

        <div class="form-section">
          <div class="form-fields">
            <div class="form-row">
              <div class="form-group">
                <label>Product Name</label>
                <input v-model="form.name" type="text" placeholder="Big Deal" required />
              </div>

              <div class="form-group form-group-half">
                <label>Price</label>
                <input v-model.number="form.price" type="number" step="0.01" min="0.01" placeholder="1420" required />
              </div>

              <div class="form-group form-group-half">
                <label>Quantity</label>
                <input v-model.number="form.quantity" type="number" min="0" placeholder="50" required />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Image URL (optional)</label>
                <input v-model="form.image_url" type="url" placeholder="https://images.kfc.com/products/chicken-original.jpg" />
              </div>

              <div class="form-group">
                <label>Upload Image</label>
                <input type="file" @change="handleFileUpload" accept="image/*" />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Description</label>
                <textarea v-model="form.description" maxlength="500" placeholder="- 3 pieces of chicken, 1 regular fries, 1 16oz. drink ."></textarea>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group form-group-half">
                <label>Category</label>
                <select v-model="form.category" required>
                  <option disabled value="">Select category</option>
                  <option value="appetizer">Appetizer</option>
                  <option value="main_course">Main Course</option>
                  <option value="dessert">Dessert</option>
                  <option value="beverage">Beverage</option>
                  <option value="side">Side Dish</option>
                  <option value="special">Daily Special</option>
                </select>
              </div>

              <div class="form-group form-group-half">
                <label>Discount (%)</label>
                <input v-model.number="form.discount_percentage" type="number" min="0" max="100" placeholder="e.g., 10" />
              </div>
            </div>

            <div class="form-row">
              <div class="form-checkboxes">
                <label><input type="checkbox" v-model="form.is_vegetarian" /> Vegetarian</label>
                <label><input type="checkbox" v-model="form.is_vegan" /> Vegan</label>
                <label><input type="checkbox" v-model="form.is_gluten_free" /> Gluten Free</label>
                <label><input type="checkbox" v-model="form.is_featured" /> Feature on Homepage</label>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group form-group-half">
                <label>Minimum Stock Alert</label>
                <input v-model.number="form.minimum_stock" type="number" min="0" placeholder="e.g., 10" />
              </div>
            </div>
          </div>

          <div class="form-actions">
            <button type="button" class="btn-cancel" @click="cancelForm">Cancel</button>
            <button type="submit" class="btn-submit" :disabled="isSubmitting">
              {{ isSubmitting ? 'Saving...' : (isEditing ? 'Update Product' : 'Add Product') }}
            </button>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import api from '@/api';

export default {
  props: {
    product: Object,
    isEditing: Boolean
  },
  emits: ['add-product', 'update-product', 'cancel'],
  data() {
    return {
      form: {
        name: '',
        price: null,
        quantity: null,
        image_url: '',
        description: '',
        category: '',
        is_vegetarian: false,
        is_vegan: false,
        is_gluten_free: false,
        is_featured: false,
        discount_percentage: 0,
        minimum_stock: 0,
      },
      imageFile: null,
      imagePreview: '',
      errors: [],
      message: '',
      isSubmitting: false,
      currentUser: null
    };
  },
  computed: {
    restaurantId() {
      return this.currentUser?.id || null;
    }
  },
  watch: {
    product: {
      handler(newVal) {
        if (newVal) {
          this.form = JSON.parse(JSON.stringify(newVal));
          this.imagePreview = newVal.image_url || '';
        }
      },
      immediate: true,
    },
  },
  async mounted() {
    try {
      await this.fetchCurrentUser();
    } catch (error) {
      console.error('Error during component initialization:', error);
      this.errors.push('Failed to initialize component. Please try again.');
      // Don't redirect here to avoid potential redirect loops
    }
  },
  methods: {
    async fetchCurrentUser() {
      try {
        console.log('Fetching current user...');
        
        // Get CSRF token first
        try {
          const csrfResponse = await api.get('/csrf-token');
          sessionStorage.setItem('csrf_token', csrfResponse.csrf_token);
        } catch (csrfError) {
          console.error('Error fetching CSRF token:', csrfError);
        }
        
        // Now fetch the current user
        const response = await api.get('/current-user');
        console.log('Current user response:', response);
        
        // Check if response and response.user exist
        if (!response || !response.user) {
          console.error('Invalid user response format:', response);
          this.errors.push('Invalid user response from server');
          this.$router.push('/login');
          return;
        }
        
        this.currentUser = response.user;
        
        if (this.currentUser?.user_type !== 'restaurant') {
          this.errors.push('Only restaurant accounts can add products');
          this.$router.push('/login');
        }
      } catch (error) {
        console.error('Error fetching current user:', error);
        this.errors.push('Authentication error. Please log in again.');
        this.$router.push('/login');
      }
    },

    handleFileUpload(e) {
      const file = e.target.files[0];
      if (file) {
        this.imageFile = file;
        this.imagePreview = URL.createObjectURL(file);
      }
    },
    
    createFormData() {
      const formData = new FormData();
      
      if (this.restaurantId) {
        formData.append('restaurant_id', this.restaurantId);
      }
      
      for (const key in this.form) {
        if (this.form[key] !== null && this.form[key] !== undefined) {
          if (typeof this.form[key] === 'boolean') {
            formData.append(key, this.form[key]);
          } else {
            formData.append(key, this.form[key]);
          }
        }
      }
      
      if (this.imageFile) {
        formData.append('image', this.imageFile);
      }
      
      return formData;
    },
    
    validateForm() {
      this.errors = [];
      
      if (!this.currentUser) {
        this.errors.push("You must be logged in as a restaurant to add products");
        return false;
      }
      
      if (this.currentUser?.user_type !== 'restaurant') {
        this.errors.push("Only restaurant accounts can add products");
        return false;
      }
      
      const requiredFields = ['name', 'price', 'quantity', 'category'];
      const missingFields = requiredFields.filter(field => {
        const value = this.form[field];
        return value === null || value === undefined || value === '';
      });
      
      if (missingFields.length > 0) {
        this.errors.push("Please fill in all required fields");
        return false;
      }
      
      if (this.form.price <= 0) {
        this.errors.push("Price must be greater than zero");
        return false;
      }
      
      if (this.form.quantity < 0) {
        this.errors.push("Quantity cannot be negative");
        return false;
      }
      
      if (!this.restaurantId) {
        this.errors.push("Restaurant ID is required");
        return false;
      }
      
      return true;
    },
    
    showMessage(text) {
      this.message = text;
      setTimeout(() => {
        this.message = '';
      }, 5000);
    },
    
    resetForm() {
      this.form = {
        name: '',
        price: null,
        quantity: null,
        image_url: '',
        description: '',
        category: '',
        is_vegetarian: false,
        is_vegan: false,
        is_gluten_free: false,
        is_featured: false,
        discount_percentage: 0,
        minimum_stock: 0,
      };
      this.imageFile = null;
      this.imagePreview = '';
      this.errors = [];
    },
    
    async handleSubmit() {
      try {
        if (!this.validateForm()) {
          return;
        }
        
        this.isSubmitting = true;
        
        const formData = this.createFormData();
        const url = this.isEditing 
          ? `/restaurant/products/${this.form.id}`
          : '/restaurant/products';
        
        console.log('Submitting form to:', url);
        console.log('Form data:', Object.fromEntries(formData.entries()));
        
        const response = await api.post(url, formData, true); // true for FormData
        console.log('Submit response:', response);
        
        const productData = response.product || response;
        
        if (this.isEditing) {
          this.$emit('update-product', productData);
          this.showMessage(`Product updated successfully!`);
        } else {
          this.$emit('add-product', productData);
          this.showMessage(`Product added successfully!`);
          this.resetForm();
        }
      } catch (err) {
        console.error('Error submitting form:', err);
        
        if (err.response) {
          const errorData = err.response.data;
          const errorMessage = errorData?.error || errorData?.message || 
            `Server error: ${err.response.status || 'unknown'}`;
          this.errors.push(errorMessage);
        } else if (err.request) {
          this.errors.push("Network error. Please check your connection and try again.");
        } else {
          this.errors.push("An unexpected error occurred. Please try again.");
        }
      } finally {
        this.isSubmitting = false;
      }
    },
    
    cancelForm() {
      this.$router.push('/restaurant/menu');
    },
  },
};
</script>

<style scoped>
.product-form-wrapper {
  background-color: white;
  padding: 40px;
  border-radius: 10px;
  max-width: 1200px;
  margin: 0 auto;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.page-title {
  color:rgb(19, 16, 13);
  font-size: 30px;
  font-weight: 700;
  margin: 0 0 32px 0;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 1px;
  position: relative;
  padding-bottom: 12px;
}

.product-form {
  background-color:rgb(255, 241, 223);
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.form-content {
  display: flex;
  gap: 40px;
}

.image-section {
  flex: 0 0 35%;
}

.image-container {
  height: 320px;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 2px dashed #fed7aa;
  border-radius: 12px;
  background-color: #fef3f3;
  position: relative;
  overflow: hidden;
}

.image-preview img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 8px;
}

.placeholder-image {
  color: #666;
  text-align: center;
  font-size: 16px;
  padding: 20px;
}

.form-section {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.form-fields {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.form-group {
  flex: 1;
  min-width: 200px;
}

.form-group-half {
  flex: 0 0 calc(50% - 8px);
}

.form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 8px;
  color: #333;
  font-size: 14px;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  font-size: 14px;
  transition: border-color 0.2s ease;
  box-sizing: border-box;
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: #9ca3af;
  font-style: italic;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #f97316;
  box-shadow: 0 0 0 3px rgba(249, 115, 22, 0.1);
}

.form-group textarea {
  height: 80px;
  resize: vertical;
  min-height: 80px;
}

.form-checkboxes {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  width: 100%;
}

.form-checkboxes label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: normal;
  font-size: 14px;
  cursor: pointer;
}

.form-checkboxes input[type="checkbox"] {
  width: auto;
  cursor: pointer;
  accent-color: #f97316;
}

/* Alert styling */
.alert {
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 24px;
  position: relative;
}

.alert-success {
  background-color: #d1fae5;
  color: #065f46;
  border: 1px solid #a7f3d0;
}

.alert-danger {
  background-color: #fee2e2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

.alert ul {
  margin: 8px 0 0 20px;
  padding: 0;
}

.alert li {
  font-size: 14px;
}

/* Form actions */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

.btn-submit,
.btn-cancel {
  padding: 10px 24px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.2s ease;
  min-width: 120px;
}

.btn-submit {
  background-color: #f97316;
  color: white;
}

.btn-submit:hover:not(:disabled) {
  background-color: #ea580c;
  transform: translateY(-1px);
}

.btn-submit:disabled {
  background-color: #d1d5db;
  cursor: not-allowed;
  transform: none;
}

.btn-cancel {
  background-color: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.btn-cancel:hover {
  background-color: #e5e7eb;
  transform: translateY(-1px);
}

/* Responsive design */
@media (max-width: 768px) {
  .product-form-wrapper {
    padding: 20px;
  }
  
  .page-title {
    font-size: 24px;
    margin-bottom: 24px;
  }
  
  .product-form {
    padding: 20px;
  }
  
  .form-content {
    flex-direction: column;
    gap: 24px;
  }
  
  .image-section {
    flex: none;
  }
  
  .form-group-half {
    flex: 1;
    min-width: 140px;
  }
  
  .form-actions {
    justify-content: stretch;
  }
  
  .btn-submit,
  .btn-cancel {
    flex: 1;
  }
}
</style>
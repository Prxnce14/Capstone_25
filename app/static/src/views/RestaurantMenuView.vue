<template>
  <form @submit.prevent="handleSubmit" enctype="multipart/form-data" class="product-form">
    <div class="form-container">
      <div class="image-container">
        <div v-if="imagePreview" class="image-preview">
          <img :src="imagePreview" alt="Image preview" />
        </div>
        <div v-else class="placeholder-image">
          <span>No image selected</span>
        </div>
      </div>

      <div class="form-fields">
        <div class="form-group">
          <label>Product Name</label>
          <input v-model="form.name" type="text" required />
        </div>

        <div class="form-group">
          <label>Price</label>
          <input v-model.number="form.price" type="number" step="0.01" min="0.01" required />
        </div>

        <div class="form-group">
          <label>Quantity</label>
          <input v-model.number="form.quantity" type="number" min="0" required />
        </div>

        <div class="form-group">
          <label>Image URL (optional)</label>
          <input v-model="form.image_url" type="url" placeholder="https://example.com/image.jpg" />
        </div>

        <div class="form-group">
          <label>Upload Image</label>
          <input type="file" @change="handleFileUpload" accept="image/*" />
        </div>

        <div class="form-group">
          <label>Description</label>
          <textarea v-model="form.description" maxlength="500"></textarea>
        </div>

        <div class="form-group">
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

        <div class="form-checkboxes">
          <label><input type="checkbox" v-model="form.is_vegetarian" /> Vegetarian</label>
          <label><input type="checkbox" v-model="form.is_vegan" /> Vegan</label>
          <label><input type="checkbox" v-model="form.is_gluten_free" /> Gluten Free</label>
          <label><input type="checkbox" v-model="form.is_featured" /> Feature on Homepage</label>
        </div>

        <div class="form-group">
          <label>Discount (%)</label>
          <input v-model.number="form.discount_percentage" type="number" min="0" max="100" />
        </div>

        <div class="form-group">
          <label>Minimum Stock Alert</label>
          <input v-model.number="form.minimum_stock" type="number" min="0" />
        </div>

        <button type="submit" class="btn-submit">
          {{ isEditing ? 'Update Product' : 'Add Product' }}
        </button>
        <button type="button" class="btn-cancel" @click="$emit('cancel')">Cancel</button>
      </div>
    </div>
  </form>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    product: Object,
    isEditing: Boolean,
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
        discount_percentage: null,
        minimum_stock: null,
      },
      imageFile: null,
      imagePreview: '',
    };
  },
  watch: {
    product: {
      handler(newVal) {
        if (newVal) {
          this.form = { ...newVal };
          this.imagePreview = newVal.image_url || '';
        }
      },
      immediate: true,
    },
  },
  methods: {
    handleFileUpload(e) {
      const file = e.target.files[0];
      if (file) {
        this.imageFile = file;
        this.imagePreview = URL.createObjectURL(file);
      }
    },
    async handleSubmit() {
      try {
        const formData = new FormData();

        // Append form fields to formData
        for (const key in this.form) {
          if (this.form[key] !== null && this.form[key] !== '') {
            formData.append(key, this.form[key]);
          }
        }

        // Append the image file if available
        if (this.imageFile) {
          formData.append('image', this.imageFile); // Matches the backend field name
        }

        // Send form data via axios
        const response = await axios.post('/api/restaurant/products', formData, {
          headers: {
            'Content-Type': 'multipart/form-data', // Ensure the correct content type for file uploads
          },
        });

        const newProduct = response.data.product;
        if (this.isEditing) {
          this.$emit('update-product', newProduct);
        } else {
          this.$emit('add-product', newProduct);
        }
        alert('Product saved successfully!');
      } catch (err) {
        console.error('Error submitting form:', err);
        alert('Error submitting product.');
      }
    },
  },
};
</script>

<style scoped>
.product-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-container {
  display: flex;
  gap: 30px;
  justify-content: space-between;
}

.image-container {
  flex-basis: 40%;
  max-height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid #fed7aa;
  border-radius: 8px;
  padding: 10px;
  background-color: #fff;
}

.image-preview img {
  max-width: 100%;
  max-height: 200px;
  border-radius: 8px;
}

.placeholder-image {
  font-size: 16px;
  color: #666;
  text-align: center;
  padding: 20px;
  border: 1px dashed #ccc;
  width: 100%;
}

.form-fields {
  flex-basis: 55%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group label {
  font-weight: bold;
  margin-bottom: 5px;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ccc;
  width: 100%;
}

.form-group textarea {
  resize: vertical;
  height: 100px;
}

.form-checkboxes {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.btn-submit,
.btn-cancel {
  margin-top: 10px;
  padding: 12px 16px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
}

.btn-submit {
  background-color: #f97316;  /* Orange color */
  color: white;
}

.btn-cancel {
  background-color: #ef4444; /* Red color */
  color: white;
}

.btn-submit:hover,
.btn-cancel:hover {
  opacity: 0.8;
}
</style>
<template>
  <div class="restaurant-profile">
    <h1>Restaurant Profile</h1>
    
    <div class="profile-container">
      <!-- Profile Header -->
      <div class="profile-header">
        <div class="restaurant-logo">
          <img :src="restaurant.logo || '/api/placeholder/150/150'" alt="Restaurant Logo" class="logo-image">
          <button class="btn btn-sm btn-change-logo" @click="triggerFileUpload">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
              <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
              <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z"/>
            </svg>
            Change Logo
          </button>
          <input type="file" ref="fileInput" @change="handleLogoUpload" accept="image/*" style="display: none">
        </div>
        <div class="restaurant-info">
          <h2>{{ restaurant.name || 'Restaurant Name' }}</h2>
          <p class="restaurant-cuisine">{{ restaurant.cuisine || 'Cuisine Type' }}</p>
          <div class="restaurant-status">
            <span :class="['status-indicator', restaurant.isOpen ? 'open' : 'closed']"></span>
            <span>{{ restaurant.isOpen ? 'Open Now' : 'Closed' }}</span>
            <button class="btn btn-sm btn-toggle-status" @click="toggleRestaurantStatus">
              {{ restaurant.isOpen ? 'Close Restaurant' : 'Open Restaurant' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="profile-tabs">
        <button :class="['tab-button', { active: activeTab === 'basic' }]" @click="activeTab = 'basic'">
          Basic Information
        </button>
        <button :class="['tab-button', { active: activeTab === 'contact' }]" @click="activeTab = 'contact'">
          Contact & Location
        </button>
        <button :class="['tab-button', { active: activeTab === 'hours' }]" @click="activeTab = 'hours'">
          Operating Hours
        </button>
        <button :class="['tab-button', { active: activeTab === 'delivery' }]" @click="activeTab = 'delivery'">
          Delivery Settings
        </button>
      </div>

      <!-- Tab Content -->
      <div class="tab-content">
        <!-- Basic Information Tab -->
        <div v-if="activeTab === 'basic'" class="tab-pane">
          <form @submit.prevent="saveBasicInfo" class="profile-form">
            <div class="form-group">
              <label for="restaurant-name">Restaurant Name</label>
              <input type="text" id="restaurant-name" v-model="editableRestaurant.name" class="form-control" required>
            </div>
            
            <div class="form-group">
              <label for="cuisine-type">Cuisine Type</label>
              <select id="cuisine-type" v-model="editableRestaurant.cuisine" class="form-control" required>
                <option value="">Select Cuisine Type</option>
                <option value="American">American</option>
                <option value="Chinese">Chinese</option>
                <option value="Italian">Italian</option>
                <option value="Mexican">Mexican</option>
                <option value="Indian">Indian</option>
                <option value="Japanese">Japanese</option>
                <option value="Fast Food">Fast Food</option>
                <option value="Other">Other</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="description">Restaurant Description</label>
              <textarea id="description" v-model="editableRestaurant.description" class="form-control" rows="4" 
                placeholder="Tell customers about your restaurant..."></textarea>
            </div>
            
            <div class="form-group">
              <label for="specialties">Specialties</label>
              <input type="text" id="specialties" v-model="editableRestaurant.specialties" class="form-control" 
                placeholder="e.g., Pasta, Pizza, Burgers">
            </div>
            
            <div class="form-actions">
              <button type="submit" class="btn btn-primary">Save Changes</button>
              <button type="button" class="btn btn-secondary" @click="resetForm">Cancel</button>
            </div>
          </form>
        </div>

        <!-- Contact & Location Tab -->
        <div v-if="activeTab === 'contact'" class="tab-pane">
          <form @submit.prevent="saveContactInfo" class="profile-form">
            <div class="form-group">
              <label for="phone">Phone Number</label>
              <input type="tel" id="phone" v-model="editableRestaurant.phone" class="form-control" required>
            </div>
            
            <div class="form-group">
              <label for="email">Email Address</label>
              <input type="email" id="email" v-model="editableRestaurant.email" class="form-control" required>
            </div>
            
            <div class="form-group">
              <label for="address">Restaurant Address</label>
              <input type="text" id="address" v-model="editableRestaurant.address" class="form-control" required>
            </div>
            
            <div class="form-group">
              <label for="website">Website (optional)</label>
              <input type="url" id="website" v-model="editableRestaurant.website" class="form-control" 
                placeholder="https://yourrestaurant.com">
            </div>
            
            <div class="form-group">
              <label for="social-media">Social Media Links</label>
              <div class="social-media-inputs">
                <input type="url" v-model="editableRestaurant.facebook" class="form-control" placeholder="Facebook URL">
                <input type="url" v-model="editableRestaurant.instagram" class="form-control" placeholder="Instagram URL">
                <input type="url" v-model="editableRestaurant.twitter" class="form-control" placeholder="Twitter URL">
              </div>
            </div>
            
            <div class="form-actions">
              <button type="submit" class="btn btn-primary">Save Changes</button>
              <button type="button" class="btn btn-secondary" @click="resetForm">Cancel</button>
            </div>
          </form>
        </div>

        <!-- Operating Hours Tab -->
        <div v-if="activeTab === 'hours'" class="tab-pane">
          <div class="operating-hours">
            <div v-for="day in weekDays" :key="day" class="day-schedule">
              <div class="day-name">{{ day }}</div>
              <div class="day-controls">
                <label class="toggle-switch">
                  <input type="checkbox" v-model="editableRestaurant.hours[day].isOpen">
                  <span class="slider"></span>
                </label>
                <div v-if="editableRestaurant.hours[day].isOpen" class="time-inputs">
                  <input type="time" v-model="editableRestaurant.hours[day].open" class="time-input">
                  <span class="time-separator">to</span>
                  <input type="time" v-model="editableRestaurant.hours[day].close" class="time-input">
                </div>
                <span v-else class="closed-label">Closed</span>
              </div>
            </div>
            
            <div class="form-actions">
              <button @click="saveOperatingHours" class="btn btn-primary">Save Hours</button>
              <button @click="resetForm" class="btn btn-secondary">Cancel</button>
            </div>
          </div>
        </div>

        <!-- Delivery Settings Tab -->
        <div v-if="activeTab === 'delivery'" class="tab-pane">
          <form @submit.prevent="saveDeliverySettings" class="profile-form">
            <div class="form-group">
              <label>
                <input type="checkbox" v-model="editableRestaurant.deliverySettings.offersDelivery">
                Offer Delivery Service
              </label>
            </div>
            
            <div v-if="editableRestaurant.deliverySettings.offersDelivery">
              <div class="form-group">
                <label for="delivery-radius">Delivery Radius (miles)</label>
                <input type="number" id="delivery-radius" v-model.number="editableRestaurant.deliverySettings.deliveryRadius" 
                  class="form-control" min="0" step="0.5">
              </div>
              
              <div class="form-group">
                <label for="delivery-fee">Delivery Fee ($)</label>
                <input type="number" id="delivery-fee" v-model.number="editableRestaurant.deliverySettings.deliveryFee" 
                  class="form-control" min="0" step="0.50">
              </div>
              
              <div class="form-group">
                <label for="min-order">Minimum Order for Delivery ($)</label>
                <input type="number" id="min-order" v-model.number="editableRestaurant.deliverySettings.minimumOrder" 
                  class="form-control" min="0" step="0.50">
              </div>
              
              <div class="form-group">
                <label for="estimated-time">Estimated Delivery Time (minutes)</label>
                <input type="number" id="estimated-time" v-model.number="editableRestaurant.deliverySettings.estimatedTime" 
                  class="form-control" min="5" step="5">
              </div>
            </div>
            
            <div class="form-actions">
              <button type="submit" class="btn btn-primary">Save Settings</button>
              <button type="button" class="btn btn-secondary" @click="resetForm">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const activeTab = ref('basic')
const fileInput = ref(null)

// Sample restaurant data - replace with actual data from backend
const restaurant = reactive({
  id: 1,
  name: 'The Golden Dragon',
  cuisine: 'Chinese',
  description: 'Authentic Chinese cuisine served in a cozy atmosphere',
  logo: '',
  isOpen: true,
  specialties: 'Dim Sum, Kung Pao Chicken, Sweet and Sour Pork',
  phone: '(555) 123-4567',
  email: 'info@goldendragon.com',
  address: '123 Main Street, Kingston, JM',
  website: 'https://goldendragon.com',
  facebook: '',
  instagram: '',
  twitter: '',
  hours: {
    Monday: { isOpen: true, open: '09:00', close: '22:00' },
    Tuesday: { isOpen: true, open: '09:00', close: '22:00' },
    Wednesday: { isOpen: true, open: '09:00', close: '22:00' },
    Thursday: { isOpen: true, open: '09:00', close: '22:00' },
    Friday: { isOpen: true, open: '09:00', close: '23:00' },
    Saturday: { isOpen: true, open: '10:00', close: '23:00' },
    Sunday: { isOpen: false, open: '', close: '' }
  },
  deliverySettings: {
    offersDelivery: true,
    deliveryRadius: 5,
    deliveryFee: 3.50,
    minimumOrder: 15.00,
    estimatedTime: 30
  }
})

// Create a copy for editing
const editableRestaurant = reactive({ ...restaurant })

const weekDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

// Methods
const triggerFileUpload = () => {
  fileInput.value?.click()
}

const handleLogoUpload = async (event) => {
  const file = event.target.files[0]
  if (file) {
    // TODO: Upload file to server and get URL
    // For now, create a local preview
    const reader = new FileReader()
    reader.onload = (e) => {
      restaurant.logo = e.target.result
      editableRestaurant.logo = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const toggleRestaurantStatus = async () => {
  restaurant.isOpen = !restaurant.isOpen
  editableRestaurant.isOpen = restaurant.isOpen
  // TODO: Send update to backend
}

const saveBasicInfo = async () => {
  try {
    // TODO: Send data to backend API
    Object.assign(restaurant, {
      name: editableRestaurant.name,
      cuisine: editableRestaurant.cuisine,
      description: editableRestaurant.description,
      specialties: editableRestaurant.specialties
    })
    alert('Basic information updated successfully!')
  } catch (error) {
    console.error('Error saving basic info:', error)
    alert('Failed to save changes. Please try again.')
  }
}

const saveContactInfo = async () => {
  try {
    // TODO: Send data to backend API
    Object.assign(restaurant, {
      phone: editableRestaurant.phone,
      email: editableRestaurant.email,
      address: editableRestaurant.address,
      website: editableRestaurant.website,
      facebook: editableRestaurant.facebook,
      instagram: editableRestaurant.instagram,
      twitter: editableRestaurant.twitter
    })
    alert('Contact information updated successfully!')
  } catch (error) {
    console.error('Error saving contact info:', error)
    alert('Failed to save changes. Please try again.')
  }
}

const saveOperatingHours = async () => {
  try {
    // TODO: Send data to backend API
    restaurant.hours = { ...editableRestaurant.hours }
    alert('Operating hours updated successfully!')
  } catch (error) {
    console.error('Error saving operating hours:', error)
    alert('Failed to save changes. Please try again.')
  }
}

const saveDeliverySettings = async () => {
  try {
    // TODO: Send data to backend API
    restaurant.deliverySettings = { ...editableRestaurant.deliverySettings }
    alert('Delivery settings updated successfully!')
  } catch (error) {
    console.error('Error saving delivery settings:', error)
    alert('Failed to save changes. Please try again.')
  }
}

const resetForm = () => {
  Object.assign(editableRestaurant, { ...restaurant })
}
</script>

<style scoped>
.restaurant-profile {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.profile-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
}

.profile-header {
  display: flex;
  padding: 30px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 1px solid #dee2e6;
}

.restaurant-logo {
  position: relative;
  margin-right: 30px;
}

.logo-image {
  width: 150px;
  height: 150px;
  border-radius: 8px;
  object-fit: cover;
  border: 3px solid white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.btn-change-logo {
  position: absolute;
  bottom: 0;
  right: 0;
  background: #FF8C00;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
}

.restaurant-info {
  flex: 1;
}

.restaurant-info h2 {
  margin: 0 0 5px 0;
  color: #333;
}

.restaurant-cuisine {
  color: #6c757d;
  margin: 0 0 15px 0;
  font-size: 16px;
}

.restaurant-status {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.status-indicator.open {
  background: #28a745;
}

.status-indicator.closed {
  background: #dc3545;
}

.btn-toggle-status {
  margin-left: 15px;
  padding: 4px 12px;
  background: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
}

.profile-tabs {
  display: flex;
  background: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.tab-button {
  padding: 15px 30px;
  background: none;
  border: none;
  color: #6c757d;
  cursor: pointer;
  transition: all 0.3s;
  border-bottom: 3px solid transparent;
}

.tab-button.active {
  color: #FF8C00;
  border-bottom-color: #FF8C00;
  background: white;
}

.tab-content {
  padding: 30px;
}

.profile-form {
  max-width: 600px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  color: #333;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  transition: border-color 0.3s;
}

.form-control:focus {
  outline: none;
  border-color: #FF8C00;
  box-shadow: 0 0 0 0.2rem rgba(255, 140, 0, 0.25);
}

.social-media-inputs {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.form-actions {
  margin-top: 30px;
  display: flex;
  gap: 10px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background: #FF8C00;
  color: white;
}

.btn-primary:hover {
  background: #e67e00;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 14px;
}

/* Operating Hours Styles */
.operating-hours {
  max-width: 800px;
}

.day-schedule {
  display: flex;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #e9ecef;
}

.day-name {
  width: 100px;
  font-weight: 500;
}

.day-controls {
  display: flex;
  align-items: center;
  gap: 15px;
  flex: 1;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 26px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 34px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #FF8C00;
}

input:checked + .slider:before {
  transform: translateX(24px);
}

.time-inputs {
  display: flex;
  align-items: center;
  gap: 10px;
}

.time-input {
  padding: 6px 8px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  width: 120px;
}

.time-separator {
  color: #6c757d;
}

.closed-label {
  color: #6c757d;
  font-style: italic;
}

/* Responsive Design */
@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    text-align: center;
  }
  
  .restaurant-logo {
    margin: 0 auto 20px;
  }
  
  .profile-tabs {
    overflow-x: auto;
    white-space: nowrap;
  }
  
  .tab-button {
    padding: 12px 20px;
  }
  
  .day-schedule {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .day-controls {
    width: 100%;
    justify-content: space-between;
  }
}
</style>
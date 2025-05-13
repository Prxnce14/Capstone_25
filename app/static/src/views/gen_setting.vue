<template>
  <div class="user-settings">
    <h1>User Settings</h1>
    
    <div class="settings-container">
      <!-- Sidebar Navigation -->
      <div class="settings-sidebar">
        <nav class="settings-nav">
          <a href="#profile" :class="{ active: activeSection === 'profile' }" @click.prevent="setActiveSection('profile')">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
              <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"/>
            </svg>
            Profile
          </a>
          
          <a href="#notifications" :class="{ active: activeSection === 'notifications' }" @click.prevent="setActiveSection('notifications')">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
              <path d="M8 16a2 2 0 0 0 2-2H6a2 2 0 0 0 2 2zm.995-14.901a1 1 0 1 0-1.99 0A5.002 5.002 0 0 0 3 6c0 1.098-.5 6-2 7h14c-1.5-1-2-5.902-2-7 0-2.42-1.72-4.44-4.005-4.901z"/>
            </svg>
            Notifications
          </a>
          
          <a href="#security" :class="{ active: activeSection === 'security' }" @click.prevent="setActiveSection('security')">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
              <path d="M5.338 1.59a61.44 61.44 0 0 0-2.837.856.481.481 0 0 0-.328.39c-.554 4.157.726 7.19 2.253 9.188a10.725 10.725 0 0 0 2.287 2.233c.346.244.652.42.893.533.12.057.218.095.293.118a.55.55 0 0 0 .101.025.615.615 0 0 0 .1-.025c.076-.023.174-.061.294-.118.24-.113.547-.29.893-.533a10.726 10.726 0 0 0 2.287-2.233c1.527-1.997 2.807-5.031 2.253-9.188a.48.48 0 0 0-.328-.39c-.651-.213-1.75-.56-2.837-.855C9.552 1.29 8.531 1.067 8 1.067c-.53 0-1.552.223-2.662.524zM5.072.56C6.157.265 7.31 0 8 0s1.843.265 2.928.56c1.11.3 2.229.655 2.887.87a1.54 1.54 0 0 1 1.044 1.262c.596 4.477-.787 7.795-2.465 9.99a11.775 11.775 0 0 1-2.517 2.453 7.159 7.159 0 0 1-1.048.625c-.28.132-.581.24-.829.24s-.548-.108-.829-.24a7.158 7.158 0 0 1-1.048-.625 11.777 11.777 0 0 1-2.517-2.453C1.928 10.487.545 7.169 1.141 2.692A1.54 1.54 0 0 1 2.185 1.43 62.456 62.456 0 0 1 5.072.56z"/>
              <path d="M10.854 5.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7.5 7.793l2.646-2.647a.5.5 0 0 1 .708 0z"/>
            </svg>
            Security
          </a>
          
          <a href="#payment" :class="{ active: activeSection === 'payment' }" @click.prevent="setActiveSection('payment')">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
              <path d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4zm2-1a1 1 0 0 0-1 1v1h14V4a1 1 0 0 0-1-1H2zm13 4H1v5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V7z"/>
              <path d="M2 10a1 1 0 0 1 1-1h1a1 1 0 0 1 1 1v1a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1v-1z"/>
            </svg>
            Payment Methods
          </a>
          
          <a href="#preferences" :class="{ active: activeSection === 'preferences' }" @click.prevent="setActiveSection('preferences')">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
              <path d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492zM5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0z"/>
              <path d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52l-.094-.319zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.415 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.291c.415.764-.42 1.6-1.185 1.184l-.291-.159a1.873 1.873 0 0 0-2.693 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.291A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.115l.094-.319z"/>
            </svg>
            Preferences
          </a>

          <a href="#addresses" :class="{ active: activeSection === 'addresses' }" @click.prevent="setActiveSection('addresses')">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
              <path d="M12.166 8.94c-.524 1.062-1.234 2.12-1.96 3.07A31.493 31.493 0 0 1 8 14.58a31.481 31.481 0 0 1-2.206-2.57c-.726-.95-1.436-2.008-1.96-3.07C3.304 7.867 3 6.862 3 6a5 5 0 0 1 10 0c0 .862-.305 1.867-.834 2.94zM8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10z"/>
              <path d="M8 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm0 1a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
            </svg>
            Addresses
          </a>
          
          <a href="#privacy" :class="{ active: activeSection === 'privacy' }" @click.prevent="setActiveSection('privacy')">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
              <path d="M6 12.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5zm3.5-1v.5h-3v-.5h3z"/>
              <path fill-rule="evenodd" d="M2 1a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V1zm11 0H3v14h10V1z"/>
              <path d="M6 2h4v6H6zM4 7h8v4H4z"/>
            </svg>
            Privacy & Data
          </a>
        </nav>
      </div>

      <!-- Main Content -->
      <div class="settings-content">
        <!-- Profile Settings -->
        <div v-if="activeSection === 'profile'" class="settings-section">
          <h2>Profile Settings</h2>
          <form @submit.prevent="saveProfileSettings" class="settings-form">
            <div class="form-group">
              <label for="profile-image">Profile Image</label>
              <div class="profile-image-container">
                <img :src="profileImageUrl || '/default-avatar.png'" alt="Profile" class="profile-image">
                <button type="button" @click="uploadProfileImage" class="btn btn-secondary">Change Photo</button>
              </div>
            </div>
            
            <div class="form-group">
              <label for="full-name">Full Name</label>
              <input type="text" id="full-name" v-model="settings.profile.fullName" class="form-control" required>
            </div>
            
            <div class="form-group">
              <label for="email">Email Address</label>
              <input type="email" id="email" v-model="settings.profile.email" class="form-control" required>
            </div>
            
            <div class="form-group">
              <label for="phone">Phone Number</label>
              <input type="tel" id="phone" v-model="settings.profile.phone" class="form-control">
            </div>
            
            <div class="form-group">
              <label for="date-of-birth">Date of Birth</label>
              <input type="date" id="date-of-birth" v-model="settings.profile.dateOfBirth" class="form-control">
            </div>
            
            <div class="form-group">
              <label for="language">Language</label>
              <select id="language" v-model="settings.profile.language" class="form-control">
                <option value="en">English</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
                <option value="de">German</option>
                <option value="zh">Chinese</option>
              </select>
            </div>
            
            <button type="submit" class="btn btn-primary">Save Changes</button>
          </form>
        </div>

        <!-- Notification Settings -->
        <div v-if="activeSection === 'notifications'" class="settings-section">
          <h2>Notification Settings</h2>
          <div class="notification-categories">
            <div class="notification-group">
              <h3>Order Updates</h3>
              <div class="notification-options">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="settings.notifications.orders.email">
                  <span>Email notifications for orders</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="settings.notifications.orders.sms">
                  <span>SMS notifications for orders</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="settings.notifications.orders.push">
                  <span>Push notifications for orders</span>
                </label>
              </div>
            </div>
            
            <div class="notification-group">
              <h3>Account & Security</h3>
              <div class="notification-options">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="settings.notifications.account.securityAlerts">
                  <span>Security alerts</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="settings.notifications.account.accountUpdates">
                  <span>Account updates</span>
                </label>
              </div>
            </div>
            
            <div class="notification-group">
              <h3>Marketing & Promotions</h3>
              <div class="notification-options">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="settings.notifications.marketing.email">
                  <span>Email newsletters</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="settings.notifications.marketing.specialOffers">
                  <span>Special offers and promotions</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="settings.notifications.marketing.events">
                  <span>Events and news</span>
                </label>
              </div>
            </div>
          </div>
          
          <button @click="saveNotificationSettings" class="btn btn-primary">Save Notification Settings</button>
        </div>

        <!-- Security Settings -->
        <div v-if="activeSection === 'security'" class="settings-section">
          <h2>Security Settings</h2>
          
          <div class="security-section">
            <h3>Password</h3>
            <form @submit.prevent="changePassword" class="password-form">
              <div class="form-group">
                <label for="current-password">Current Password</label>
                <input type="password" id="current-password" v-model="passwordForm.current" class="form-control" required>
              </div>
              
              <div class="form-group">
                <label for="new-password">New Password</label>
                <input type="password" id="new-password" v-model="passwordForm.new" class="form-control" required>
              </div>
              
              <div class="form-group">
                <label for="confirm-password">Confirm New Password</label>
                <input type="password" id="confirm-password" v-model="passwordForm.confirm" class="form-control" required>
              </div>
              
              <button type="submit" class="btn btn-primary">Change Password</button>
            </form>
          </div>
          
          <div class="security-section">
            <h3>Two-Factor Authentication</h3>
            <p>{{ settings.security.twoFactorEnabled ? 'Two-factor authentication is enabled' : 'Two-factor authentication is disabled' }}</p>
            <button @click="toggleTwoFactor" class="btn btn-primary">
              {{ settings.security.twoFactorEnabled ? 'Disable' : 'Enable' }} Two-Factor Authentication
            </button>
          </div>
          
          <div class="security-section">
            <h3>Login Sessions</h3>
            <div class="login-sessions">
              <div v-for="(session, index) in settings.security.loginSessions" :key="index" class="session-item">
                <div class="session-info">
                  <div class="device-name">{{ session.device }}</div>
                  <div class="session-details">
                    <span>{{ session.location }}</span>
                    <span>•</span>
                    <span>{{ formatDate(session.date) }}</span>
                  </div>
                </div>
                <button @click="endSession(index)" class="btn btn-sm btn-delete" :disabled="index === 0">
                  {{ index === 0 ? 'Current Session' : 'End Session' }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Payment Methods Settings -->
        <div v-if="activeSection === 'payment'" class="settings-section">
          <h2>Payment Methods</h2>
          
          <div class="add-payment-method">
            <button @click="showAddPaymentModal = true" class="btn btn-primary">Add Payment Method</button>
          </div>
          
          <div class="payment-methods-list">
            <div v-for="(method, index) in settings.payment.methods" :key="index" class="payment-method-item">
              <div class="payment-method-info">
                <div class="payment-card-icon">
                  <span :class="getCardIconClass(method.type)"></span>
                </div>
                <div class="payment-details">
                  <div class="payment-type">{{ method.type }}</div>
                  <div class="payment-number">•••• •••• •••• {{ method.lastFour }}</div>
                  <div class="payment-expiry">Expires {{ method.expiryMonth }}/{{ method.expiryYear }}</div>
                </div>
              </div>
              <div class="payment-actions">
                <span v-if="method.isDefault" class="default-badge">Default</span>
                <button v-else @click="setDefaultPayment(index)" class="btn btn-sm btn-secondary">Set as Default</button>
                <button @click="removePaymentMethod(index)" class="btn btn-sm btn-delete">Remove</button>
              </div>
            </div>
            
            <div v-if="settings.payment.methods.length === 0" class="no-payment-methods">
              <p>You don't have any payment methods added yet.</p>
            </div>
          </div>
          
          <div v-if="showAddPaymentModal" class="modal-overlay">
            <div class="modal">
              <h3>Add Payment Method</h3>
              <form @submit.prevent="addPaymentMethod">
                <div class="form-group">
                  <label for="card-number">Card Number</label>
                  <input type="text" id="card-number" v-model="newPayment.cardNumber" class="form-control" placeholder="1234 5678 9012 3456" required>
                </div>
                
                <div class="form-row">
                  <div class="form-group">
                    <label for="expiry-month">Expiry Month</label>
                    <select id="expiry-month" v-model="newPayment.expiryMonth" class="form-control" required>
                      <option v-for="month in 12" :key="month" :value="month < 10 ? '0' + month : month.toString()">
                        {{ month < 10 ? '0' + month : month }}
                      </option>
                    </select>
                  </div>
                  
                  <div class="form-group">
                    <label for="expiry-year">Expiry Year</label>
                    <select id="expiry-year" v-model="newPayment.expiryYear" class="form-control" required>
                      <option v-for="year in 10" :key="year" :value="(new Date().getFullYear() + year - 1).toString().slice(-2)">
                        {{ new Date().getFullYear() + year - 1 }}
                      </option>
                    </select>
                  </div>
                  
                  <div class="form-group">
                    <label for="cvv">CVV</label>
                    <input type="text" id="cvv" v-model="newPayment.cvv" class="form-control" placeholder="123" maxlength="4" required>
                  </div>
                </div>
                
                <div class="form-group">
                  <label for="card-name">Name on Card</label>
                  <input type="text" id="card-name" v-model="newPayment.cardholderName" class="form-control" required>
                </div>
                
                <label class="checkbox-label">
                  <input type="checkbox" v-model="newPayment.setAsDefault">
                  <span>Set as default payment method</span>
                </label>
                
                <div class="modal-actions">
                  <button type="submit" class="btn btn-primary">Add Payment Method</button>
                  <button type="button" @click="showAddPaymentModal = false" class="btn btn-secondary">Cancel</button>
                </div>
              </form>
            </div>
          </div>
        </div>

        <!-- Preferences Settings -->
        <div v-if="activeSection === 'preferences'" class="settings-section">
          <h2>Preferences</h2>
          
          <div class="preference-group">
            <h3>Appearance</h3>
            <div class="form-group">
              <label for="theme">Theme</label>
              <select id="theme" v-model="settings.preferences.theme" class="form-control">
                <option value="light">Light</option>
                <option value="dark">Dark</option>
                <option value="system">Use System Setting</option>
              </select>
            </div>
          </div>
          
          <div class="preference-group">
            <h3>Regional Settings</h3>
            <div class="form-group">
              <label for="timezone">Timezone</label>
              <select id="timezone" v-model="settings.preferences.timezone" class="form-control">
                <option value="EST">Eastern Time (EST)</option>
                <option value="CST">Central Time (CST)</option>
                <option value="MST">Mountain Time (MST)</option>
                <option value="PST">Pacific Time (PST)</option>
                <option value="UTC">Coordinated Universal Time (UTC)</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="currency">Currency</label>
              <select id="currency" v-model="settings.preferences.currency" class="form-control">
                <option value="USD">US Dollar (USD)</option>
                <option value="EUR">Euro (EUR)</option>
                <option value="GBP">British Pound (GBP)</option>
                <option value="CAD">Canadian Dollar (CAD)</option>
                <option value="AUD">Australian Dollar (AUD)</option>
              </select>
            </div>
          </div>
          
          <div class="preference-group">
            <h3>Accessibility</h3>
            <label class="checkbox-label">
              <input type="checkbox" v-model="settings.preferences.accessibility.reduceMotion">
              <span>Reduce motion</span>
            </label>
            
            <label class="checkbox-label">
              <input type="checkbox" v-model="settings.preferences.accessibility.highContrast">
              <span>High contrast mode</span>
            </label>
            
            <div class="form-group">
              <label for="font-size">Font Size</label>
              <select id="font-size" v-model="settings.preferences.accessibility.fontSize" class="form-control">
                <option value="small">Small</option>
                <option value="medium">Medium</option>
                <option value="large">Large</option>
                <option value="x-large">Extra Large</option>
              </select>
            </div>
          </div>
          
          <button @click="savePreferences" class="btn btn-primary">Save Preferences</button>
        </div>

        <!-- Addresses Settings -->
        <div v-if="activeSection === 'addresses'" class="settings-section">
          <h2>Addresses</h2>
          
          <div class="address-actions">
            <button @click="showAddAddressModal = true" class="btn btn-primary">Add New Address</button>
          </div>
          
          <div class="address-list">
            <div v-for="(address, index) in settings.addresses" :key="index" class="address-item">
              <div class="address-info">
                <div class="address-name">{{ address.nickname || 'Address ' + (index + 1) }}</div>
                <div class="address-details">
                  <div>{{ address.street }}</div>
                  <div>{{ address.city }}, {{ address.state }} {{ address.zipCode }}</div>
                  <div>{{ address.country }}</div>
                </div>
              </div>
              <div class="address-actions">
                <span v-if="address.isDefault" class="default-badge">Default</span>
                <button v-else @click="setDefaultAddress(index)" class="btn btn-sm btn-secondary">Set as Default</button>
                <button @click="editAddress(index)" class="btn btn-sm btn-edit">Edit</button>
                <button @click="removeAddress(index)" class="btn btn-sm btn-delete">Remove</button>
              </div>
            </div>
            
            <div v-if="settings.addresses.length === 0" class="no-addresses">
              <p>You don't have any saved addresses yet.</p>
            </div>
          </div>
          
          <div v-if="showAddAddressModal || showEditAddressModal" class="modal-overlay">
            <div class="modal">
              <h3>{{ showEditAddressModal ? 'Edit Address' : 'Add New Address' }}</h3>
              <form @submit.prevent="showEditAddressModal ? updateAddress() : addAddress()">
                <div class="form-group">
                  <label for="address-nickname">Nickname (optional)</label>
                  <input type="text" id="address-nickname" v-model="addressForm.nickname" class="form-control" placeholder="Home, Work, etc.">
                </div>
                
                <div class="form-group">
                  <label for="address-street">Street Address</label>
                  <input type="text" id="address-street" v-model="addressForm.street" class="form-control" required>
                </div>
                
                <div class="form-group">
                  <label for="address-apt">Apartment/Suite (optional)</label>
                  <input type="text" id="address-apt" v-model="addressForm.apt" class="form-control">
                </div>
                
                <div class="form-row">
                  <div class="form-group">
                    <label for="address-city">City</label>
                    <input type="text" id="address-city" v-model="addressForm.city" class="form-control" required>
                  </div>
                  
                  <div class="form-group">
                    <label for="address-state">State/Province</label>
                    <input type="text" id="address-state" v-model="addressForm.state" class="form-control" required>
                  </div>
                  
                  <div class="form-group">
                    <label for="address-zip">ZIP/Postal Code</label>
                    <input type="text" id="address-zip" v-model="addressForm.zipCode" class="form-control" required>
                  </div>
                </div>
                
                <div class="form-group">
                  <label for="address-country">Country</label>
                  <select id="address-country" v-model="addressForm.country" class="form-control" required>
                    <option value="United States">United States</option>
                    <option value="Canada">Canada</option>
                    <option value="United Kingdom">United Kingdom</option>
                    <option value="Australia">Australia</option>
                    <option value="Germany">Germany</option>
                    <option value="France">France</option>
                    <!-- Add more countries as needed -->
                  </select>
                </div>
                
                <label class="checkbox-label">
                  <input type="checkbox" v-model="addressForm.setAsDefault">
                  <span>Set as default address</span>
                </label>
                
                <div class="modal-actions">
                  <button type="submit" class="btn btn-primary">
                    {{ showEditAddressModal ? 'Update Address' : 'Add Address' }}
                  </button>
                  <button type="button" @click="closeAddressModal" class="btn btn-secondary">Cancel</button>
                </div>
              </form>
            </div>
          </div>
        </div>

        <!-- Privacy & Data Settings -->
        <div v-if="activeSection === 'privacy'" class="settings-section">
          <h2>Privacy & Data</h2>
          
          <div class="privacy-group">
            <h3>Data Usage</h3>
            <p class="privacy-description">Manage how your data is used to improve your experience.</p>
            <div class="privacy-options">
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.privacy.allowPersonalization">
                <span>Allow personalization based on my activity</span>
              </label>
              
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.privacy.sharePurchaseHistory">
                <span>Share my purchase history to receive relevant recommendations</span>
              </label>
              
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.privacy.allowCookies">
                <span>Allow cookies to optimize site experience</span>
              </label>
            </div>
          </div>
          
          <div class="privacy-group">
            <h3>Data Management</h3>
            <div class="data-actions">
              <button @click="downloadUserData" class="btn btn-secondary">Download My Data</button>
              <button @click="showDeleteAccountModal = true" class="btn btn-danger">Delete Account</button>
            </div>
          </div>
          
          <button @click="savePrivacySettings" class="btn btn-primary">Save Privacy Settings</button>
          
          <div v-if="showDeleteAccountModal" class="modal-overlay">
            <div class="modal danger-modal">
              <h3>Delete Account</h3>
              <p class="warning-text">Warning: This action cannot be undone. All your data will be permanently deleted.</p>
              <form @submit.prevent="deleteAccount">
                <div class="form-group">
                  <label for="delete-password">Enter your password to confirm</label>
                  <input type="password" id="delete-password" v-model="deleteAccountPassword" class="form-control" required>
                </div>
                
                <div class="modal-actions">
                  <button type="submit" class="btn btn-danger">Permanently Delete Account</button>
                  <button type="button" @click="showDeleteAccountModal = false" class="btn btn-secondary">Cancel</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';

const activeSection = ref('profile');
const showAddPaymentModal = ref(false);
const showAddAddressModal = ref(false);
const showEditAddressModal = ref(false);
const showDeleteAccountModal = ref(false);
const editingAddressIndex = ref(-1);
const profileImageUrl = ref(null);
const deleteAccountPassword = ref('');

// Form for password change
const passwordForm = reactive({
  current: '',
  new: '',
  confirm: ''
});

// Form for new payment method
const newPayment = reactive({
  cardNumber: '',
  expiryMonth: '',
  expiryYear: '',
  cvv: '',
  cardholderName: '',
  setAsDefault: false
});

// Form for address
const addressForm = reactive({
  nickname: '',
  street: '',
  apt: '',
  city: '',
  state: '',
  zipCode: '',
  country: 'United States',
  setAsDefault: false
});

// Settings data structure
const settings = reactive({
  profile: {
    fullName: 'John Doe',
    email: 'john.doe@example.com',
    phone: '(555) 123-4567',
    dateOfBirth: '1990-01-01',
    language: 'en'
  },
  notifications: {
    orders: {
      email: true,
      sms: true,
      push: true
    },
    account: {
      securityAlerts: true,
      accountUpdates: true
    },
    marketing: {
      email: true,
      specialOffers: true,
      events: false
    }
  },
  security: {
    twoFactorEnabled: false,
    loginSessions: [
      { device: 'Chrome on Windows', location: 'New York, USA', date: new Date() },
      { device: 'Safari on iPhone', location: 'New York, USA', date: new Date(Date.now() - 86400000) }
    ]
  },
  payment: {
    methods: [
      { 
        type: 'Visa', 
        lastFour: '4242', 
        expiryMonth: '06', 
        expiryYear: '24', 
        isDefault: true 
      },
      { 
        type: 'Mastercard', 
        lastFour: '5678', 
        expiryMonth: '09', 
        expiryYear: '25', 
        isDefault: false 
      }
    ]
  },
  preferences: {
    theme: 'light',
    timezone: 'EST',
    currency: 'USD',
    accessibility: {
      reduceMotion: false,
      highContrast: false,
      fontSize: 'medium'
    }
  },
  addresses: [
    {
      nickname: 'Home',
      street: '123 Main St',
      apt: 'Apt 4B',
      city: 'New York',
      state: 'NY',
      zipCode: '10001',
      country: 'United States',
      isDefault: true
    },
    {
      nickname: 'Work',
      street: '456 Business Ave',
      apt: 'Suite 200',
      city: 'New York',
      state: 'NY',
      zipCode: '10002',
      country: 'United States',
      isDefault: false
    }
  ],
  privacy: {
    allowPersonalization: true,
    sharePurchaseHistory: true,
    allowCookies: true
  }
});

// Methods
const setActiveSection = (section) => {
  activeSection.value = section;
};

// Profile methods
const saveProfileSettings = async () => {
  try {
    // TODO: Send to backend
    showSuccessMessage('Profile settings saved successfully!');
  } catch (error) {
    console.error('Error saving profile settings:', error);
    showErrorMessage('Failed to save settings. Please try again.');
  }
};

const uploadProfileImage = () => {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'image/*';
  input.onchange = (event) => {
    const file = event.target.files[0];
    if (file) {
      // TODO: Upload file to backend
      // For now, create a temporary URL
      const reader = new FileReader();
      reader.onload = (e) => {
        profileImageUrl.value = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  };
  input.click();
};

// Notification methods
const saveNotificationSettings = async () => {
  try {
    // TODO: Send to backend
    showSuccessMessage('Notification settings saved successfully!');
  } catch (error) {
    console.error('Error saving notification settings:', error);
    showErrorMessage('Failed to save settings. Please try again.');
  }
};

// Security methods
const changePassword = async () => {
  if (passwordForm.new !== passwordForm.confirm) {
    showErrorMessage('New passwords do not match!');
    return;
  }
  
  try {
    // TODO: Send to backend
    showSuccessMessage('Password changed successfully!');
    passwordForm.current = '';
    passwordForm.new = '';
    passwordForm.confirm = '';
  } catch (error) {
    console.error('Error changing password:', error);
    showErrorMessage('Failed to change password. Please try again.');
  }
};

const toggleTwoFactor = async () => {
  try {
    settings.security.twoFactorEnabled = !settings.security.twoFactorEnabled;
    // TODO: Send to backend
    showSuccessMessage(`Two-factor authentication ${settings.security.twoFactorEnabled ? 'enabled' : 'disabled'} successfully!`);
  } catch (error) {
    console.error('Error toggling two-factor:', error);
    settings.security.twoFactorEnabled = !settings.security.twoFactorEnabled;
    showErrorMessage('Failed to update two-factor authentication. Please try again.');
  }
};

const endSession = async (index) => {
  if (index === 0) return; // Cannot end current session
  
  try {
    // TODO: Send to backend
    settings.security.loginSessions.splice(index, 1);
    showSuccessMessage('Session ended successfully!');
  } catch (error) {
    console.error('Error ending session:', error);
    showErrorMessage('Failed to end session. Please try again.');
  }
};

// Payment methods
const getCardIconClass = (type) => {
  switch (type.toLowerCase()) {
    case 'visa': return 'visa-icon';
    case 'mastercard': return 'mastercard-icon';
    case 'amex': return 'amex-icon';
    case 'discover': return 'discover-icon';
    default: return 'card-icon';
  }
};

const addPaymentMethod = async () => {
  try {
    // In a real application, you would send the card details to a payment processor
    // and only store the tokenized information
    
    // Get last 4 digits of card number
    const lastFour = newPayment.cardNumber.slice(-4);
    
    // Determine card type (simplified)
    let cardType = 'Credit Card';
    const firstDigit = newPayment.cardNumber.charAt(0);
    if (firstDigit === '4') cardType = 'Visa';
    else if (firstDigit === '5') cardType = 'Mastercard';
    else if (firstDigit === '3') cardType = 'Amex';
    else if (firstDigit === '6') cardType = 'Discover';
    
    const newCard = {
      type: cardType,
      lastFour,
      expiryMonth: newPayment.expiryMonth,
      expiryYear: newPayment.expiryYear,
      isDefault: newPayment.setAsDefault
    };
    
    // If new card is default, update other cards
    if (newCard.isDefault) {
      settings.payment.methods.forEach(method => {
        method.isDefault = false;
      });
    }
    
    settings.payment.methods.push(newCard);
    
    // Reset form
    Object.keys(newPayment).forEach(key => {
      newPayment[key] = key === 'setAsDefault' ? false : '';
    });
    
    showAddPaymentModal.value = false;
    showSuccessMessage('Payment method added successfully!');
  } catch (error) {
    console.error('Error adding payment method:', error);
    showErrorMessage('Failed to add payment method. Please try again.');
  }
};

const setDefaultPayment = (index) => {
  settings.payment.methods.forEach((method, i) => {
    method.isDefault = i === index;
  });
  showSuccessMessage('Default payment method updated!');
};

const removePaymentMethod = async (index) => {
  if (confirm('Are you sure you want to remove this payment method?')) {
    try {
      // Check if it's the default card
      const isDefault = settings.payment.methods[index].isDefault;
      
      // Remove the card
      settings.payment.methods.splice(index, 1);
      
      // If it was the default and there are other cards, set the first one as default
      if (isDefault && settings.payment.methods.length > 0) {
        settings.payment.methods[0].isDefault = true;
      }
      
      showSuccessMessage('Payment method removed successfully!');
    } catch (error) {
      console.error('Error removing payment method:', error);
      showErrorMessage('Failed to remove payment method. Please try again.');
    }
  }
};

// Preferences methods
const savePreferences = async () => {
  try {
    // TODO: Send to backend
    showSuccessMessage('Preferences saved successfully!');
  } catch (error) {
    console.error('Error saving preferences:', error);
    showErrorMessage('Failed to save preferences. Please try again.');
  }
};

// Address methods
const addAddress = async () => {
  try {
    const newAddress = {
      nickname: addressForm.nickname,
      street: addressForm.street,
      apt: addressForm.apt,
      city: addressForm.city,
      state: addressForm.state,
      zipCode: addressForm.zipCode,
      country: addressForm.country,
      isDefault: addressForm.setAsDefault
    };
    
    // If new address is default, update other addresses
    if (newAddress.isDefault) {
      settings.addresses.forEach(address => {
        address.isDefault = false;
      });
    }
    
    settings.addresses.push(newAddress);
    resetAddressForm();
    showAddAddressModal.value = false;
    showSuccessMessage('Address added successfully!');
  } catch (error) {
    console.error('Error adding address:', error);
    showErrorMessage('Failed to add address. Please try again.');
  }
};

const editAddress = (index) => {
  const address = settings.addresses[index];
  
  // Populate form with address data
  addressForm.nickname = address.nickname;
  addressForm.street = address.street;
  addressForm.apt = address.apt || '';
  addressForm.city = address.city;
  addressForm.state = address.state;
  addressForm.zipCode = address.zipCode;
  addressForm.country = address.country;
  addressForm.setAsDefault = address.isDefault;
  
  editingAddressIndex.value = index;
  showEditAddressModal.value = true;
};

const updateAddress = async () => {
  try {
    const index = editingAddressIndex.value;
    const updatedAddress = {
      nickname: addressForm.nickname,
      street: addressForm.street,
      apt: addressForm.apt,
      city: addressForm.city,
      state: addressForm.state,
      zipCode: addressForm.zipCode,
      country: addressForm.country,
      isDefault: addressForm.setAsDefault
    };
    
    // If updated address is default, update other addresses
    if (updatedAddress.isDefault && !settings.addresses[index].isDefault) {
      settings.addresses.forEach(address => {
        address.isDefault = false;
      });
    }
    
    settings.addresses[index] = updatedAddress;
    resetAddressForm();
    showEditAddressModal.value = false;
    showSuccessMessage('Address updated successfully!');
  } catch (error) {
    console.error('Error updating address:', error);
    showErrorMessage('Failed to update address. Please try again.');
  }
};

const setDefaultAddress = (index) => {
  settings.addresses.forEach((address, i) => {
    address.isDefault = i === index;
  });
  showSuccessMessage('Default address updated!');
};

const removeAddress = async (index) => {
  if (confirm('Are you sure you want to remove this address?')) {
    try {
      // Check if it's the default address
      const isDefault = settings.addresses[index].isDefault;
      
      // Remove the address
      settings.addresses.splice(index, 1);
      
      // If it was the default and there are other addresses, set the first one as default
      if (isDefault && settings.addresses.length > 0) {
        settings.addresses[0].isDefault = true;
      }
      
      showSuccessMessage('Address removed successfully!');
    } catch (error) {
      console.error('Error removing address:', error);
      showErrorMessage('Failed to remove address. Please try again.');
    }
  }
};

const closeAddressModal = () => {
  showAddAddressModal.value = false;
  showEditAddressModal.value = false;
  resetAddressForm();
};

const resetAddressForm = () => {
  addressForm.nickname = '';
  addressForm.street = '';
  addressForm.apt = '';
  addressForm.city = '';
  addressForm.state = '';
  addressForm.zipCode = '';
  addressForm.country = 'United States';
  addressForm.setAsDefault = false;
  editingAddressIndex.value = -1;
};

// Privacy methods
const savePrivacySettings = async () => {
  try {
    // TODO: Send to backend
    showSuccessMessage('Privacy settings saved successfully!');
  } catch (error) {
    console.error('Error saving privacy settings:', error);
    showErrorMessage('Failed to save settings. Please try again.');
  }
};

const downloadUserData = async () => {
  try {
    // TODO: Implement data download
    showSuccessMessage('Your data is being prepared for download. You will receive an email when it\'s ready.');
  } catch (error) {
    console.error('Error preparing data download:', error);
    showErrorMessage('Failed to prepare data download. Please try again.');
  }
};

const deleteAccount = async () => {
  try {
    // TODO: Implement account deletion
    showSuccessMessage('Your account has been deleted. You will be logged out shortly.');
    showDeleteAccountModal.value = false;
    
    // In a real application, you would redirect to logout page after a delay
    setTimeout(() => {
      window.location.href = '/logout';
    }, 3000);
  } catch (error) {
    console.error('Error deleting account:', error);
    showErrorMessage('Failed to delete account. Please try again.');
  }
};

// Helper functions
const formatDate = (date) => {
  return new Date(date).toLocaleString();
};

const showSuccessMessage = (message) => {
  alert(message); // In a real app, use a toast or notification component
};

const showErrorMessage = (message) => {
  alert(message); // In a real app, use a toast or notification component
};
</script>

<style scoped>
.user-settings {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.settings-container {
  display: flex;
  gap: 30px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  min-height: 600px;
}

.settings-sidebar {
  width: 250px;
  background: #f8f9fa;
  border-right: 1px solid #e9ecef;
  border-top-left-radius: 8px;
  border-bottom-left-radius: 8px;
}

.settings-nav {
  padding: 20px 0;
  position: sticky;
  top: 100px;
}

.settings-nav a {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  color: #495057;
  text-decoration: none;
  transition: all 0.3s;
  border-left: 3px solid transparent;
}

.settings-nav a:hover {
  background: #e9ecef;
  color: #4a6de5;
}

.settings-nav a.active {
  background: #e9ecef;
  color: #4a6de5;
  border-left-color: #4a6de5;
}

.settings-nav svg {
  width: 16px;
  height: 16px;
}

.settings-content {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
}

.settings-section {
  max-width: 700px;
}

.settings-section h2 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 24px;
}

.settings-section h3 {
  margin: 20px 0 15px 0;
  color: #495057;
  font-size: 18px;
}

.settings-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-group label {
  color: #495057;
  font-weight: 500;
}

.form-control {
  padding: 10px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  transition: border-color 0.3s;
  font-size: 14px;
}

.form-control:focus {
  outline: none;
  border-color: #4a6de5;
  box-shadow: 0 0 0 0.2rem rgba(74, 109, 229, 0.25);
}

.form-row {
  display: flex;
  gap: 15px;
}

.form-row .form-group {
  flex: 1;
}

.btn {
  padding: 10px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
  font-weight: 500;
}

.btn-primary {
  background: #4a6de5;
  color: white;
}

.btn-primary:hover {
  background: #3a5bd5;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn-danger:hover {
  background: #c82333;
}

.btn-sm {
  padding: 6px 10px;
  font-size: 12px;
}

.btn-edit {
  background: #0d6efd;
  color: white;
}

.btn-delete {
  background: #dc3545;
  color: white;
}

.btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

/* Profile settings */
.profile-image-container {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 10px;
}

.profile-image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #ced4da;
}

/* Notification Settings */
.notification-categories {
  display: flex;
  flex-direction: column;
  gap: 30px;
  margin-bottom: 30px;
}

.notification-group {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 20px;
}

.notification-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 10px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  cursor: pointer;
}

/* Security Settings */
.password-form {
  margin-bottom: 40px;
}

.security-section {
  margin-bottom: 40px;
  padding-bottom: 30px;
  border-bottom: 1px solid #e9ecef;
}

.login-sessions {
  margin-top: 15px;
}

.session-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 6px;
  margin-bottom: 10px;
}

.device-name {
  font-weight: 500;
  margin-bottom: 5px;
}

.session-details {
  color: #6c757d;
  font-size: 13px;
}

.session-details span {
  margin-right: 5px;
}

/* Payment Methods */
.payment-methods-list {
  margin-top: 20px;
}

.payment-method-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 6px;
  margin-bottom: 10px;
}

.payment-method-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.payment-card-icon {
  font-size: 24px;
  color:rgb(224, 115, 12);
}

.payment-type {
  font-weight: 500;
  margin-bottom: 5px;
}

.payment-number, .payment-expiry {
  color: #6c757d;
  font-size: 13px;
}

.payment-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.default-badge {
  background:rgb(224, 115, 12);
  color: white;
  font-size: 12px;
  padding: 3px 8px;
  border-radius: 4px;
}

.no-payment-methods {
  background: #f8f9fa;
  border-radius: 6px;
  padding: 20px;
  text-align: center;
  color: #6c757d;
}

/* Preferences */
.preference-group {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e9ecef;
}

/* Addresses */
.address-list {
  margin-top: 20px;
}

.address-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 6px;
  margin-bottom: 10px;
}

.address-name {
  font-weight: 500;
  margin-bottom: 5px;
}

.address-details {
  color: #6c757d;
  font-size: 14px;
}

.address-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.no-addresses {
  background: #f8f9fa;
  border-radius: 6px;
  padding: 20px;
  text-align: center;
  color: #6c757d;
}

/* Privacy */
.privacy-group {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e9ecef;
}

.privacy-description {
  color: #6c757d;
  margin-bottom: 15px;
}

.privacy-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.data-actions {
  display: flex;
  gap: 15px;
  margin-top: 15px;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 30px;
  border-radius: 8px;
  width: 500px;
  max-width: 90vw;
  max-height: 90vh;
  overflow-y: auto;
}

.modal h3 {
  margin: 0 0 20px 0;
}

.modal-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.danger-modal {
  border-top: 5px solid #dc3545;
}

.warning-text {
  color: #dc3545;
  font-weight: 500;
  margin-bottom: 20px;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .settings-container {
    flex-direction: column;
  }
  
  .settings-sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #e9ecef;
    border-radius: 8px 8px 0 0;
  }
  
  .settings-nav {
    position: relative;
    top: auto;
    display: flex;
    flex-wrap: wrap;
    padding: 10px;
  }
  
  .settings-nav a {
    flex: 1;
    min-width: 150px;
    justify-content: center;
    border-left: none;
    border-bottom: 3px solid transparent;
  }


  .settings-nav a.active {
    border-left: none;
    border-bottom-color: #FF8C00;
  }
  
  .settings-content {
    padding: 20px;
  }
}

@media (max-width: 768px) {
  .restaurant-settings {
    padding: 10px;
  }

 .modal {
    padding: 20px;
  }
}
</style>
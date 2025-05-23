<template>
  <div class="restaurant-settings">
    <h1>Restaurant Settings</h1>
    
    <div class="settings-container">
      <!-- Sidebar Navigation -->
      <div class="settings-sidebar">
        <nav class="settings-nav">
          <a href="#account" :class="{ active: activeSection === 'account' }" @click.prevent="setActiveSection('account')">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
              <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"/>
            </svg>
            Account Settings
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
            Security & Privacy
          </a>
          
          <a href="#payment" :class="{ active: activeSection === 'payment' }" @click.prevent="setActiveSection('payment')">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
              <path d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4zm2-1a1 1 0 0 0-1 1v1h14V4a1 1 0 0 0-1-1H2zm13 4H1v5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V7z"/>
              <path d="M2 10a1 1 0 0 1 1-1h1a1 1 0 0 1 1 1v1a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1v-1z"/>
            </svg>
            Payment Settings
          </a>
          
          <a href="#ordering" :class="{ active: activeSection === 'ordering' }" @click.prevent="setActiveSection('ordering')">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
              <path d="M0 1.5A.5.5 0 0 1 .5 1H2a.5.5 0 0 1 .485.379L2.89 3H14.5a.5.5 0 0 1 .49.598l-1 5a.5.5 0 0 1-.465.401l-9.397.472L4.415 11H13a.5.5 0 0 1 0 1H4a.5.5 0 0 1-.491-.408L2.01 3.607 1.61 2H.5a.5.5 0 0 1-.5-.5zM3.102 4l.84 4.479 9.144-.459L13.89 4H3.102zM5 12a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm7 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm-7 1a1 1 0 1 1 0 2 1 1 0 0 1 0-2zm7 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
            </svg>
            Ordering Settings
          </a>
          
          <a href="#staff" :class="{ active: activeSection === 'staff' }" @click.prevent="setActiveSection('staff')">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
              <path d="M7 14s-1 0-1-1 1-4 5-4 5 3 5 4-1 1-1 1H7zm4-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
              <path fill-rule="evenodd" d="M5.216 14A2.238 2.238 0 0 1 5 13c0-1.355.68-2.75 1.936-3.72A6.325 6.325 0 0 0 5 9c-4 0-5 3-5 4s1 1 1 1h4.216z"/>
              <path d="M4.5 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z"/>
            </svg>
            Staff & Permissions
          </a>
          
          <a href="#taxes" :class="{ active: activeSection === 'taxes' }" @click.prevent="setActiveSection('taxes')">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
              <path d="M4 10a1 1 0 1 1 0-2 1 1 0 0 1 0 2zm0 3a1 1 0 1 1 0-2 1 1 0 0 1 0 2zm4-3a1 1 0 1 1 0-2 1 1 0 0 1 0 2zm0 3a1 1 0 1 1 0-2 1 1 0 0 1 0 2zm2-3a1 1 0 1 1 0-2 1 1 0 0 1 0 2zm0 3a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/>
              <path fill-rule="evenodd" d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4zm15 0a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4z"/>
            </svg>
            Tax Settings
          </a>
          
          <a href="#advanced" :class="{ active: activeSection === 'advanced' }" @click.prevent="setActiveSection('advanced')">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
              <path d="M6 12.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5zm3.5-1v.5h-3v-.5h3z"/>
              <path fill-rule="evenodd" d="M2 1a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V1zm11 0H3v14h10V1z"/>
              <path d="M6 2h4v6H6zM4 7h8v4H4z"/>
            </svg>
            Advanced Settings
          </a>
        </nav>
      </div>

      <!-- Main Content -->
      <div class="settings-content">
        <!-- Account Settings -->
        <div v-if="activeSection === 'account'" class="settings-section">
          <h2>Account Settings</h2>
          <form @submit.prevent="saveAccountSettings" class="settings-form">
            <div class="form-group">
              <label for="restaurant-name">Restaurant Name</label>
              <input type="text" id="restaurant-name" v-model="settings.restaurant.name" class="form-control" required>
            </div>
            
            <div class="form-group">
              <label for="restaurant-email">Restaurant Email</label>
              <input type="email" id="restaurant-email" v-model="settings.restaurant.email" class="form-control" required>
            </div>
            
            <div class="form-group">
              <label for="admin-email">Administrator Email</label>
              <input type="email" id="admin-email" v-model="settings.account.adminEmail" class="form-control" required>
            </div>
            
            <div class="form-group">
              <label for="language">Language</label>
              <select id="language" v-model="settings.account.language" class="form-control">
                <option value="en">English</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="timezone">Timezone</label>
              <select id="timezone" v-model="settings.account.timezone" class="form-control">
                <option value="EST">Eastern Time (EST)</option>
                <option value="CST">Central Time (CST)</option>
                <option value="MST">Mountain Time (MST)</option>
                <option value="PST">Pacific Time (PST)</option>
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
              <h3>Order Notifications</h3>
              <div class="notification-options">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="settings.notifications.newOrders.email">
                  <span>Email notifications for new orders</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="settings.notifications.newOrders.sms">
                  <span>SMS notifications for new orders</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="settings.notifications.newOrders.app">
                  <span>In-app notifications for new orders</span>
                </label>
              </div>
            </div>
            
            <div class="notification-group">
              <h3>Customer Reviews</h3>
              <div class="notification-options">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="settings.notifications.reviews.email">
                  <span>Email notifications for new reviews</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="settings.notifications.reviews.weekly">
                  <span>Weekly review summary</span>
                </label>
              </div>
            </div>
            
            <div class="notification-group">
              <h3>Payment & Financial</h3>
              <div class="notification-options">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="settings.notifications.financial.dailyReport">
                  <span>Daily sales report</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="settings.notifications.financial.weeklyReport">
                  <span>Weekly sales report</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="settings.notifications.financial.paymentFailed">
                  <span>Payment failure alerts</span>
                </label>
              </div>
            </div>
          </div>
          
          <button @click="saveNotificationSettings" class="btn btn-primary">Save Notification Settings</button>
        </div>

        <!-- Security Settings -->
        <div v-if="activeSection === 'security'" class="settings-section">
          <h2>Security & Privacy Settings</h2>
          
          <div class="security-section">
            <h3>Password Security</h3>
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
            <h3>Login History</h3>
            <table class="login-history-table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>IP Address</th>
                  <th>Device</th>
                  <th>Location</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="login in settings.security.loginHistory" :key="login.id">
                  <td>{{ formatDate(login.date) }}</td>
                  <td>{{ login.ip }}</td>
                  <td>{{ login.device }}</td>
                  <td>{{ login.location }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Payment Settings -->
        <div v-if="activeSection === 'payment'" class="settings-section">
          <h2>Payment Settings</h2>
          
          <div class="payment-methods">
            <h3>Accepted Payment Methods</h3>
            <div class="payment-options">
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.payment.methods.cash">
                <span>Cash</span>
              </label>
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.payment.methods.card">
                <span>Credit/Debit Card</span>
              </label>
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.payment.methods.digitalWallet">
                <span>Digital Wallet (Apple Pay, Google Pay)</span>
              </label>
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.payment.methods.bitcoin">
                <span>Bitcoin/Cryptocurrency</span>
              </label>
            </div>
          </div>
          
          <div class="bank-details">
            <h3>Bank Account Details</h3>
            <form @submit.prevent="saveBankDetails" class="bank-form">
              <div class="form-group">
                <label for="bank-name">Bank Name</label>
                <input type="text" id="bank-name" v-model="settings.payment.bankDetails.bankName" class="form-control" required>
              </div>
              
              <div class="form-group">
                <label for="account-name">Account Name</label>
                <input type="text" id="account-name" v-model="settings.payment.bankDetails.accountName" class="form-control" required>
              </div>
              
              <div class="form-group">
                <label for="account-number">Account Number</label>
                <input type="text" id="account-number" v-model="settings.payment.bankDetails.accountNumber" class="form-control" required>
              </div>
              
              <div class="form-group">
                <label for="routing-number">Routing Number</label>
                <input type="text" id="routing-number" v-model="settings.payment.bankDetails.routingNumber" class="form-control" required>
              </div>
              
              <button type="submit" class="btn btn-primary">Save Bank Details</button>
            </form>
          </div>
          
          <button @click="savePaymentSettings" class="btn btn-primary">Save Payment Settings</button>
        </div>

        <!-- Ordering Settings -->
        <div v-if="activeSection === 'ordering'" class="settings-section">
          <h2>Ordering Settings</h2>
          
          <div class="ordering-options">
            <h3>Order Types</h3>
            <label class="checkbox-label">
              <input type="checkbox" v-model="settings.ordering.allowPickup">
              <span>Allow pickup orders</span>
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="settings.ordering.allowDelivery">
              <span>Allow delivery orders</span>
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="settings.ordering.allowDineIn">
              <span>Allow dine-in orders (table service)</span>
            </label>
          </div>
          
          <div class="order-limits">
            <h3>Order Limits</h3>
            <div class="form-group">
              <label for="max-items">Maximum items per order</label>
              <input type="number" id="max-items" v-model.number="settings.ordering.maxItemsPerOrder" class="form-control" min="1">
            </div>
            
            <div class="form-group">
              <label for="min-order-value">Minimum order value ($)</label>
              <input type="number" id="min-order-value" v-model.number="settings.ordering.minimumOrderValue" class="form-control" min="0" step="0.01">
            </div>
            
            <div class="form-group">
              <label for="prep-time">Average preparation time (minutes)</label>
              <input type="number" id="prep-time" v-model.number="settings.ordering.averagePreparationTime" class="form-control" min="5" step="5">
            </div>
          </div>
          
          <button @click="saveOrderingSettings" class="btn btn-primary">Save Ordering Settings</button>
        </div>

        <!-- Staff & Permissions -->
        <div v-if="activeSection === 'staff'" class="settings-section">
          <h2>Staff & Permissions</h2>
          
          <div class="staff-actions">
            <button @click="showAddStaffModal = true" class="btn btn-primary">Add New Staff Member</button>
          </div>
          
          <div class="staff-list">
            <table class="staff-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Role</th>
                  <th>Email</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="staff in settings.staff.members" :key="staff.id">
                  <td>{{ staff.name }}</td>
                  <td>{{ staff.role }}</td>
                  <td>{{ staff.email }}</td>
                  <td>
                    <span :class="['status-badge', staff.status.toLowerCase()]">
                      {{ staff.status }}
                    </span>
                  </td>
                  <td>
                    <button @click="editStaff(staff)" class="btn btn-sm btn-edit">Edit</button>
                    <button @click="removeStaff(staff.id)" class="btn btn-sm btn-delete">Remove</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div v-if="showAddStaffModal" class="modal-overlay">
            <div class="modal">
              <h3>Add New Staff Member</h3>
              <form @submit.prevent="addStaffMember">
                <div class="form-group">
                  <label for="staff-name">Name</label>
                  <input type="text" id="staff-name" v-model="newStaff.name" class="form-control" required>
                </div>
                
                <div class="form-group">
                  <label for="staff-email">Email</label>
                  <input type="email" id="staff-email" v-model="newStaff.email" class="form-control" required>
                </div>
                
                <div class="form-group">
                  <label for="staff-role">Role</label>
                  <select id="staff-role" v-model="newStaff.role" class="form-control" required>
                    <option value="">Select Role</option>
                    <option value="manager">Manager</option>
                    <option value="chef">Chef</option>
                    <option value="server">Server</option>
                    <option value="cashier">Cashier</option>
                  </select>
                </div>
                
                <div class="modal-actions">
                  <button type="submit" class="btn btn-primary">Add Staff</button>
                  <button type="button" @click="showAddStaffModal = false" class="btn btn-secondary">Cancel</button>
                </div>
              </form>
            </div>
          </div>
        </div>

        <!-- Tax Settings -->
        <div v-if="activeSection === 'taxes'" class="settings-section">
          <h2>Tax Settings</h2>
          
          <div class="tax-settings">
            <div class="form-group">
              <label for="default-tax-rate">Default Tax Rate (%)</label>
              <input type="number" id="default-tax-rate" v-model.number="settings.taxes.defaultRate" class="form-control" min="0" max="100" step="0.01">
            </div>
            
            <div class="form-group">
              <label for="tax-name">Tax Display Name</label>
              <input type="text" id="tax-name" v-model="settings.taxes.displayName" class="form-control" placeholder="e.g., Sales Tax, VAT">
            </div>
            
            <label class="checkbox-label">
              <input type="checkbox" v-model="settings.taxes.includeInPrice">
              <span>Include tax in displayed prices</span>
            </label>
            
            <label class="checkbox-label">
              <input type="checkbox" v-model="settings.taxes.taxDeliveryFee">
              <span>Apply tax to delivery fees</span>
            </label>
          </div>
          
          <div class="tax-exemptions">
            <h3>Tax Exemptions</h3>
            <div class="exemption-list">
              <button @click="addTaxExemption" class="btn btn-primary">Add Exemption</button>
              <div v-if="settings.taxes.exemptions.length > 0" class="exemption-items">
                <div v-for="(exemption, index) in settings.taxes.exemptions" :key="index" class="exemption-item">
                  <span>{{ exemption.name }} ({{ exemption.type }})</span>
                  <button @click="removeTaxExemption(index)" class="btn btn-sm btn-delete">Remove</button>
                </div>
              </div>
            </div>
          </div>
          
          <button @click="saveTaxSettings" class="btn btn-primary">Save Tax Settings</button>
        </div>

        <!-- Advanced Settings -->
        <div v-if="activeSection === 'advanced'" class="settings-section">
          <h2>Advanced Settings</h2>
          
          <div class="advanced-options">
            <div class="advanced-group">
              <h3>Data Management</h3>
              <button @click="exportData" class="btn btn-secondary">Export Restaurant Data</button>
              <button @click="importData" class="btn btn-secondary">Import Restaurant Data</button>
              <button @click="backupData" class="btn btn-secondary">Create Backup</button>
            </div>
            
            <div class="advanced-group">
              <h3>API Configuration</h3>
              <div class="form-group">
                <label for="api-key">API Key</label>
                <div class="api-key-container">
                  <input type="text" id="api-key" :value="settings.advanced.apiKey" class="form-control" readonly>
                  <button @click="regenerateApiKey" class="btn btn-primary">Regenerate</button>
                </div>
              </div>
              
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.advanced.apiEnabled">
                <span>Enable API access</span>
              </label>
            </div>
            
            <div class="advanced-group">
              <h3>System Settings</h3>
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.advanced.allowTestOrders">
                <span>Allow test orders</span>
              </label>
              
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.advanced.enableDebugMode">
                <span>Enable debug mode</span>
              </label>
              
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.advanced.autoBackup">
                <span>Enable automatic daily backup</span>
              </label>
            </div>
          </div>
          
          <button @click="saveAdvancedSettings" class="btn btn-primary">Save Advanced Settings</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const activeSection = ref('account')
const showAddStaffModal = ref(false)

// Form for password change
const passwordForm = reactive({
  current: '',
  new: '',
  confirm: ''
})

// Form for new staff member
const newStaff = reactive({
  name: '',
  email: '',
  role: ''
})

// Settings data structure
const settings = reactive({
  restaurant: {
    name: 'The Golden Dragon',
    email: 'contact@goldendragon.com'
  },
  account: {
    adminEmail: 'admin@goldendragon.com',
    language: 'en',
    timezone: 'EST'
  },
  notifications: {
    newOrders: {
      email: true,
      sms: true,
      app: true
    },
    reviews: {
      email: true,
      weekly: true
    },
    financial: {
      dailyReport: true,
      weeklyReport: true,
      paymentFailed: true
    }
  },
  security: {
    twoFactorEnabled: false,
    loginHistory: [
      { id: 1, date: new Date(), ip: '192.168.1.1', device: 'Chrome on Windows', location: 'New York, USA' },
      { id: 2, date: new Date(Date.now() - 86400000), ip: '192.168.1.2', device: 'Safari on iPhone', location: 'New York, USA' }
    ]
  },
  payment: {
    methods: {
      cash: true,
      card: true,
      digitalWallet: true,
      bitcoin: false
    },
    bankDetails: {
      bankName: '',
      accountName: '',
      accountNumber: '',
      routingNumber: ''
    }
  },
  ordering: {
    allowPickup: true,
    allowDelivery: true,
    allowDineIn: true,
    maxItemsPerOrder: 10,
    minimumOrderValue: 10.00,
    averagePreparationTime: 30
  },
  staff: {
    members: [
      { id: 1, name: 'John Doe', role: 'Manager', email: 'john@goldendragon.com', status: 'Active' },
      { id: 2, name: 'Jane Smith', role: 'Chef', email: 'jane@goldendragon.com', status: 'Active' },
      { id: 3, name: 'Mike Johnson', role: 'Server', email: 'mike@goldendragon.com', status: 'Inactive' }
    ]
  },
  taxes: {
    defaultRate: 8.5,
    displayName: 'Sales Tax',
    includeInPrice: false,
    taxDeliveryFee: true,
    exemptions: []
  },
  advanced: {
    apiKey: 'sk_live_123456789abcdef',
    apiEnabled: true,
    allowTestOrders: false,
    enableDebugMode: false,
    autoBackup: true
  }
})

// Methods
const setActiveSection = (section) => {
  activeSection.value = section
}

const saveAccountSettings = async () => {
  try {
    // TODO: Send to backend
    alert('Account settings saved successfully!')
  } catch (error) {
    console.error('Error saving account settings:', error)
    alert('Failed to save settings. Please try again.')
  }
}

const saveNotificationSettings = async () => {
  try {
    // TODO: Send to backend
    alert('Notification settings saved successfully!')
  } catch (error) {
    console.error('Error saving notification settings:', error)
    alert('Failed to save settings. Please try again.')
  }
}

const changePassword = async () => {
  if (passwordForm.new !== passwordForm.confirm) {
    alert('New passwords do not match!')
    return
  }
  
  try {
    // TODO: Send to backend
    alert('Password changed successfully!')
    passwordForm.current = ''
    passwordForm.new = ''
    passwordForm.confirm = ''
  } catch (error) {
    console.error('Error changing password:', error)
    alert('Failed to change password. Please try again.')
  }
}

const toggleTwoFactor = async () => {
  try {
    settings.security.twoFactorEnabled = !settings.security.twoFactorEnabled
    // TODO: Send to backend
    alert(`Two-factor authentication ${settings.security.twoFactorEnabled ? 'enabled' : 'disabled'} successfully!`)
  } catch (error) {
    console.error('Error toggling two-factor:', error)
    settings.security.twoFactorEnabled = !settings.security.twoFactorEnabled
    alert('Failed to update two-factor authentication. Please try again.')
  }
}

const savePaymentSettings = async () => {
  try {
    // TODO: Send to backend
    alert('Payment settings saved successfully!')
  } catch (error) {
    console.error('Error saving payment settings:', error)
    alert('Failed to save settings. Please try again.')
  }
}

const saveBankDetails = async () => {
  try {
    // TODO: Send to backend
    alert('Bank details saved successfully!')
  } catch (error) {
    console.error('Error saving bank details:', error)
    alert('Failed to save bank details. Please try again.')
  }
}

const saveOrderingSettings = async () => {
  try {
    // TODO: Send to backend
    alert('Ordering settings saved successfully!')
  } catch (error) {
    console.error('Error saving ordering settings:', error)
    alert('Failed to save settings. Please try again.')
  }
}

const addStaffMember = async () => {
  try {
    const staffMember = {
      id: Date.now(),
      name: newStaff.name,
      email: newStaff.email,
      role: newStaff.role,
      status: 'Active'
    }
    
    settings.staff.members.push(staffMember)
    
    // Reset form
    newStaff.name = ''
    newStaff.email = ''
    newStaff.role = ''
    showAddStaffModal.value = false
    
    // TODO: Send to backend
    alert('Staff member added successfully!')
  } catch (error) {
    console.error('Error adding staff member:', error)
    alert('Failed to add staff member. Please try again.')
  }
}

const editStaff = (staff) => {
  // TODO: Implement edit functionality
  console.log('Edit staff:', staff)
}

const removeStaff = async (staffId) => {
  if (confirm('Are you sure you want to remove this staff member?')) {
    try {
      const index = settings.staff.members.findIndex(member => member.id === staffId)
      if (index > -1) {
        settings.staff.members.splice(index, 1)
        // TODO: Send to backend
        alert('Staff member removed successfully!')
      }
    } catch (error) {
      console.error('Error removing staff member:', error)
      alert('Failed to remove staff member. Please try again.')
    }
  }
}

const saveTaxSettings = async () => {
  try {
    // TODO: Send to backend
    alert('Tax settings saved successfully!')
  } catch (error) {
    console.error('Error saving tax settings:', error)
    alert('Failed to save settings. Please try again.')
  }
}

const addTaxExemption = () => {
  const exemptionName = prompt('Enter exemption name:')
  const exemptionType = prompt('Enter exemption type (e.g., Category, Item):')
  
  if (exemptionName && exemptionType) {
    settings.taxes.exemptions.push({
      name: exemptionName,
      type: exemptionType
    })
  }
}

const removeTaxExemption = (index) => {
  settings.taxes.exemptions.splice(index, 1)
}

const saveAdvancedSettings = async () => {
  try {
    // TODO: Send to backend
    alert('Advanced settings saved successfully!')
  } catch (error) {
    console.error('Error saving advanced settings:', error)
    alert('Failed to save settings. Please try again.')
  }
}

const exportData = () => {
  // TODO: Implement data export
  console.log('Exporting restaurant data...')
  alert('Data export initiated. You will receive an email when complete.')
}

const importData = () => {
  // TODO: Implement data import
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = '.json,.csv'
  input.onchange = (event) => {
    const file = event.target.files[0]
    if (file) {
      console.log('Importing data from:', file.name)
      alert('Data import initiated. This may take a few moments.')
    }
  }
  input.click()
}

const backupData = async () => {
  try {
    // TODO: Implement backup
    alert('Backup created successfully!')
  } catch (error) {
    console.error('Error creating backup:', error)
    alert('Failed to create backup. Please try again.')
  }
}

const regenerateApiKey = async () => {
  if (confirm('Are you sure you want to regenerate your API key? This will invalidate the current key.')) {
    try {
      settings.advanced.apiKey = 'sk_live_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15)
      // TODO: Send to backend
      alert('API key regenerated successfully!')
    } catch (error) {
      console.error('Error regenerating API key:', error)
      alert('Failed to regenerate API key. Please try again.')
    }
  }
}

const formatDate = (date) => {
  return new Date(date).toLocaleString()
}
</script>

<style scoped>
.restaurant-settings {
  padding: 20px;
  max-width: 1400px;
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
  color: #FF8C00;
}

.settings-nav a.active {
  background: #fff3e0;
  color: #FF8C00;
  border-left-color: #FF8C00;
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
  max-width: 800px;
}

.settings-section h2 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 24px;
}

.settings-section h3 {
  margin: 0 0 15px 0;
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

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
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
  padding: 4px 8px;
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

/* Notification Settings */
.notification-categories {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.notification-group {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 20px;
}

.notification-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
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
  padding-bottom: 20px;
  border-bottom: 1px solid #e9ecef;
}

.login-history-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
}

.login-history-table th,
.login-history-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #e9ecef;
}

.login-history-table th {
  background: #f8f9fa;
  font-weight: 600;
  color: #495057;
}

/* Payment Settings */
.payment-methods {
  margin-bottom: 40px;
}

.payment-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
}

.bank-details {
  padding-top: 20px;
  border-top: 1px solid #e9ecef;
}

/* Staff Management */
.staff-actions {
  margin-bottom: 20px;
}

.staff-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
}

.staff-table th,
.staff-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #e9ecef;
}

.staff-table th {
  background: #f8f9fa;
  font-weight: 600;
  color: #495057;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  text-transform: capitalize;
}

.status-badge.active {
  background: #d4edda;
  color: #155724;
}

.status-badge.inactive {
  background: #f8d7da;
  color: #721c24;
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
}

.modal h3 {
  margin: 0 0 20px 0;
}

.modal-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

/* Tax Settings */
.tax-settings {
  margin-bottom: 40px;
}

.tax-exemptions {
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid #e9ecef;
}

.exemption-items {
  margin-top: 15px;
}

.exemption-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 4px;
  margin-bottom: 10px;
}

/* Advanced Settings */
.advanced-options {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.advanced-group {
  padding-bottom: 20px;
  border-bottom: 1px solid #e9ecef;
}

.api-key-container {
  display: flex;
  gap: 10px;
}

.api-key-container .form-control {
  flex: 1;
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
  
  .staff-table,
  .login-history-table {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
  }
  
  .modal {
    padding: 20px;
  }
}
</style>
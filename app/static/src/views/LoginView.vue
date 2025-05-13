<template>
    <div class="main-container">

        <div class="background-image"></div>
        
        <!-- Main content area -->
        <div class="content-container">
            <!-- Form area -->
            <div class="form-wrapper">
                <!-- Logo -->
                <div class="logo-container">
                    <img src="/uploads/pelican.png" alt="Pelican Eats" class="logo">
                </div>
                
                <h1>Welcome Back - Log In</h1>
                
                <!-- Login form -->
                <form @submit.prevent="login" id="loginform" class="login-form">
                    <!-- Alert messages -->
                    <div v-if="message || errors.length > 0" :class="{'alert alert-success': message, 'alert alert-danger': errors.length > 0}" role="alert">
                        <p v-if="message">{{ message }}</p>
                        <ul v-if="errors.length > 0">
                            <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
                        </ul>
                    </div>
                    
                    <div class="form-fields">
                        <div class="form-group">
                            <label for="username">Username</label>
                            <input 
                                type="text" 
                                id="username" 
                                name="username" 
                                class="form-control" 
                                placeholder="Your username" 
                                v-model="formData.username"
                                required
                            />
                        </div>

                        <div class="form-group">
                            <label for="password">Password</label>
                            <input 
                                type="password" 
                                name="password" 
                                class="form-control" 
                                placeholder="Your password" 
                                v-model="formData.password"
                                required 
                            />
                        </div>

                        <div class="form-group remember-group">
                            <input type="checkbox" id="remember" v-model="formData.remember" name="remember">
                            <label for="remember" class="remember-label">
                                Remember me
                            </label>
                        </div>

                        <div class="button-container">
                            <button type="submit" class="login-button" :disabled="isSubmitting">
                                {{ isSubmitting ? 'Logging in...' : 'Log In' }}
                            </button>
                        </div>
                        
                        <div class="forgot-password">
                            <a href="/forgot-password">Forgot your password?</a>
                        </div>
                        
                        <div class="signup-link">
                            Don't have an account? <a href="/register/personal">Sign up</a>
                        </div>
                    </div>
                </form>
            </div>
        </div>
        <div class="login-footer">
            <p>Copyright © {{ new Date().getFullYear() }} Pelican Eats, Inc All rights reserved.</p>
        </div>

    </div>
</template>

<script setup>
    import { ref, onMounted, reactive } from "vue";
    import { useRouter } from 'vue-router';
    import api from '@/api';

    const router = useRouter();

    // Reactive form state
    const formData = reactive({
        username: '',
        password: '',
        remember: false
    });

    let csrf_token = ref("");
    let message = ref("");
    let errors = ref([]);
    let isSubmitting = ref(false);
    
    async function getCsrfToken() {
        try {
            console.log('Fetching CSRF token...');
            const data = await api.get('/csrf-token');
            console.log('CSRF token received:', data);
            csrf_token.value = data.csrf_token;
            // Store CSRF token for future requests
            sessionStorage.setItem('csrf_token', data.csrf_token);
        } catch (error) {
            console.error("Failed to fetch CSRF token:", error);
            errors.value.push("Server connection issue. Please try again later.");
        }
    }

    onMounted(() => {
        getCsrfToken();
        
        // Clear any existing tokens on login page
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_type');
        localStorage.removeItem('user_id');
    });

    // Function to validate the form
    function validateForm() {
        errors.value = [];
        
        // Check required fields
        if (!formData.username.trim()) {
            errors.value.push("Username is required");
            return false;
        }
        
        if (!formData.password) {
            errors.value.push("Password is required");
            return false;
        }
        
        return true;
    }

    // Function to login a user
    async function login() {
        // Clear previous messages
        message.value = "";
        
        // First, validate the form
        if (!validateForm()) {
            return;
        }

        isSubmitting.value = true;

        try {
            // Create FormData 
            let form = document.querySelector("#loginform");
            let form_data = new FormData(form);

            console.log('Sending login request...');
            console.log('CSRF Token being sent:', csrf_token.value);

            const response = await fetch("/api/login", {
                method: 'POST',
                body: form_data,
                headers: {
                    'X-CSRFToken': csrf_token.value
                },
                credentials: 'include'
            });

            const data = await response.json();
            console.log('Login response:', data);
            
            if (!response.ok) {
                throw new Error(data.error || 'Login failed');
            }
            
            // Set success message
            message.value = data.message || "You have successfully logged in!";
            
            // Store tokens and user info using our API helper
            if (data.access_token) {
                console.log('Access token received, storing...');
                api.setAuthTokens(data.access_token, csrf_token.value);
                localStorage.setItem('user_id', data.id);
                localStorage.setItem('user_type', data.user_type);
                
                // Verify tokens are stored
                console.log('Stored tokens:');
                console.log('- access_token:', localStorage.getItem('access_token') ? 'Present' : 'Missing');
                console.log('- user_type:', localStorage.getItem('user_type'));
                console.log('- csrf_token:', sessionStorage.getItem('csrf_token') ? 'Present' : 'Missing');
            }
            
            // Redirect based on user type
            if (data.redirect) {
                console.log('Redirecting to:', data.redirect);
                // Allow the success message to be seen briefly before redirecting
                setTimeout(() => {
                    router.push(data.redirect);
                }, 1000);
            }
        } catch (error) {
            console.error('Login error:', error);
            // Display specific error message
            errors.value.push(error.message);
        } finally {
            isSubmitting.value = false;
        }
    }
</script>

<style>
/* Global styles */
.main-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    width: 100%;
    margin: 0;
    padding: 0;
    position: relative;
    overflow-x: hidden;
}

.background-image {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url('/uploads/background.png');
    background-size: cover;
    background-position: center;
    z-index: -1;
}

/* Header styles */
.site-header {
    background-color: #FF8C00;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.8rem 2rem;
}

.logo-text {
    font-size: 1.2rem;
    font-weight: bold;
}

.main-nav a {
    color: white;
    text-decoration: none;
    margin-left: 1.5rem;
    font-size: 0.9rem;
}

.content-container {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 3rem;
    position: relative;
    z-index: 1;
    transform: translateX(-10%);
}

/* Form wrapper */
.form-wrapper {
    width: 450px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    padding: 2rem;
    text-align: center;
}

.logo-container {
    margin-bottom: 1.5rem;
}

.logo {
    height: 80px;
}

h1 {
    font-size: 1.5rem;
    color: #333;
    margin-bottom: 1.5rem;
}

/* Form fields */
.form-fields {
    background-color: #FFF3E0;
    padding: 1.5rem;
    border-radius: 8px;
}

.form-group {
    margin-bottom: 1rem;
    text-align: left;
}

.form-group label {
    display: block;
    color: #555;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}

.form-control {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 0.9rem;
}

/* Remember me checkbox */
.remember-group {
    display: flex;
    align-items: center;
    margin-top: 0.5rem;
}

.remember-group input[type="checkbox"] {
    margin-right: 0.5rem;
}

.remember-label {
    font-size: 0.8rem;
    color: #666;
}

/* Login button */
.button-container {
    text-align: center;
    margin: 1.5rem 0 1rem;
}

.login-button {
    background-color: #FF8C00;
    color: white;
    border: none;
    border-radius: 25px;
    padding: 0.75rem 2rem;
    font-size: 0.9rem;
    cursor: pointer;
    transition: background-color 0.2s;
    width: 80%;
}

.login-button:hover {
    background-color: #e67e00;
}

.login-button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
}

.forgot-password {
    font-size: 0.8rem;
    margin-bottom: 1rem;
}

.signup-link {
    font-size: 0.8rem;
    color: #666;
    margin-top: 1rem;
}

.forgot-password a, .signup-link a {
    color: #FF8C00;
    text-decoration: none;
}

/* Alert styles */
.alert {
    padding: 0.75rem;
    border-radius: 4px;
    margin-bottom: 1rem;
    text-align: left;
}

.alert-success {
    background-color: #f5b75a8b;
    color: #555;
    border: 1px solid #FFF3E0;
}

.alert-danger {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

/* For larger screens */
@media (min-width: 769px) {
  .login-footer {
    position: absolute;
    bottom: 0;
    transform: translateX(-10%);
  }
  
  .main-container {
    position: relative;
    min-height: 100vh;
    padding-bottom: 2rem;
  }
}

/* For smaller screens */
@media (max-width: 768px) {
    .content-container {
        padding: 1rem;
        transform: translateX(0);
    }
    
    .form-wrapper {
        width: 100%;
        max-width: 450px;
    }
}

/* href link styles */
a {
    color: #FF8C00;
    text-decoration: none;
}

/* Custom footer just for this page */
.login-footer {
  color: white;
  text-align: center;
  margin-top: 0.5rem;
  padding: 0.5rem;
  position: relative;
  z-index: 100;
  width: 100%;
  left: 0;
  right: 0;
}

/* Hide the regular footer on this page only */
footer {
  display: none;
}
</style>
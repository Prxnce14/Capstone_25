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
                
                <h1>Driver Account - Sign Up</h1>
                
                <!-- Registration form -->
                <form @submit.prevent="register_driver" id="driverform" class="signup-form">
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
                                placeholder="Choose a unique username" 
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
                                placeholder="Password" 
                                v-model="formData.password"
                                @input="clearPasswordRelatedErrors"
                                required 
                            />
                        </div>

                        <div class="form-group">
                            <label for="confirmPassword">Confirm Password</label>
                            <input 
                                type="password" 
                                id="confirmPassword" 
                                name="confirmPassword" 
                                class="form-control" 
                                placeholder="Password"
                                v-model="formData.confirmPassword"
                                @input="clearPasswordRelatedErrors"
                                required
                            />
                        </div>

                        <div class="form-group">
                            <label for="firstname">Firstname</label>
                            <input 
                                type="text" 
                                name="firstname" 
                                class="form-control" 
                                placeholder="Mark" 
                                v-model="formData.firstname"
                                @input="validateFieldOnChange('firstname')"
                                required 
                            />
                        </div>

                        <div class="form-group">
                            <label for="lastname">Lastname</label>
                            <input 
                                type="text" 
                                name="lastname" 
                                class="form-control" 
                                placeholder="Black" 
                                v-model="formData.lastname"
                                @input="validateFieldOnChange('lastname')"
                                required 
                            />
                        </div>

                        <div class="form-group">
                            <label for="email">Email</label>
                            <input 
                                type="email" 
                                name="email" 
                                class="form-control" 
                                placeholder="markblack@gmail.com" 
                                v-model="formData.email"
                                @input="validateFieldOnChange('email')"
                                required 
                            />
                        </div>

                        <div class="form-group">
                            <label for="phone_number">Phone number</label>
                            <input 
                                type="text" 
                                name="phone_number" 
                                class="form-control" 
                                placeholder="876-237-2799" 
                                v-model="formData.phone_number"
                                @input="validateFieldOnChange('phone_number')"
                                required 
                            />
                        </div>

                        <div class="form-group terms-group">
                            <input type="checkbox" id="terms" required>
                            <label for="terms" class="terms-label">
                                By signing up, you agree to our <a href="#">Terms of Service and Privacy Policy</a>.
                            </label>
                        </div>

                        <div class="button-container">
                            <button type="submit" class="signup-button" :disabled="isSubmitting">
                                {{ isSubmitting ? 'Submitting...' : 'Sign Up' }}
                            </button>
                        </div>
                        
                        <div class="login-link">
                            Already have an account? <a href="/login">Log in</a>
                        </div>
                    </div>
                </form>
            </div>
        </div>
        <div class="register-footer">
            <p>Copyright © {{ new Date().getFullYear() }} Pelican Eats, Inc All rights reserved.</p>
        </div>

    </div>
</template>

<script setup>
    import {ref, onMounted, reactive, watch} from "vue";

    // Reactive form state
    const formData = reactive({
        username: '',
        password: '',
        confirmPassword: '',
        firstname: '',
        lastname: '',
        email: '',
        phone_number: ''
    });

    let csrf_token = ref("");
    let message = ref("");
    let errors = ref([]);
    let isSubmitting = ref(false);
    
    // Track which fields have been validated to prevent premature error clearing
    const fieldValidationState = reactive({
        firstname: false,
        lastname: false,
        email: false,
        phone_number: false,
        password: false,
        confirmPassword: false
    });

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

    onMounted(() => {
        getCsrfToken();
        
        // Set up event listeners to sync form data with the input fields
        const form = document.getElementById('driverform');
        if (form) {
            form.addEventListener('input', (event) => {
                if (event.target.name && event.target.name in formData) {
                    formData[event.target.name] = event.target.value;
                }
            });
        }
    });

    // Function to validate email format
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(String(email).toLowerCase());
    }

    // Function to validate names (letters, spaces, hyphens, apostrophes)
    function validateName(name) {
        // Allow letters, spaces, hyphens, and apostrophes (common in names)
        const nameRegex = /^[A-Za-z\s\-']+$/;
        return nameRegex.test(name);
    }

    // Function to validate phone number
    function validatePhone(phone) {
        // Clear any non-numeric characters for validation
        const digitsOnly = phone.replace(/\D/g, '');
        
        // Check if the input after stripping non-digits has 7-10 digits
        if (digitsOnly.length < 7 || digitsOnly.length > 10) {
            return false;
        }
        
        // For display validation, ensure it matches expected formats
        const phoneRegex = /^(?:\(\d{3}\)\s?\d{3}-\d{4}|\d{3}-\d{3}-\d{4}|\d{3}-\d{4}|\d{7,10})$/;
        return phoneRegex.test(phone);
    }

    // Function to validate password strength
    function validatePasswordStrength(password) {
        // At least 8 characters, with at least one uppercase, one lowercase, and one number
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
        return passwordRegex.test(password);
    }
    
    // Function to clear errors when field values change
    function validateFieldOnChange(fieldName) {
        // Mark this field as having been validated
        fieldValidationState[fieldName] = true;
        
        // Only validate fields that have been previously validated (had errors)
        if (!fieldValidationState[fieldName]) return;
        
        let isValid = true;
        
        switch (fieldName) {
            case 'firstname':
            case 'lastname':
                isValid = validateName(formData[fieldName]);
                if (!isValid) {
                    return; // Don't clear errors if still invalid
                }
                removeErrorForField(`${fieldName} should only contain letters, spaces, hyphens, or apostrophes`);
                break;
                
            case 'email':
                isValid = validateEmail(formData.email);
                if (!isValid) {
                    return; // Don't clear errors if still invalid
                }
                removeErrorForField("Please enter a valid email address");
                break;
                
            case 'phone_number':
                isValid = validatePhone(formData.phone_number);
                if (!isValid) {
                    return; // Don't clear errors if still invalid
                }
                removeErrorForField("Please enter a valid phone number (7-10 digits, with or without formatting)");
                break;
        }
    }
    
    // Function to clear password-related errors when either password field changes
    function clearPasswordRelatedErrors() {
        fieldValidationState.password = true;
        fieldValidationState.confirmPassword = true;
        
        // Check if passwords match now
        if (formData.password && formData.confirmPassword && 
            formData.password === formData.confirmPassword) {
            removeErrorForField("Passwords do not match");
        }
        
        // Check if password meets strength requirements
        if (formData.password && validatePasswordStrength(formData.password)) {
            removeErrorForField("Password must be at least 8 characters and include uppercase, lowercase, and numbers");
        }
    }
    
    // Helper function to remove a specific error from the errors array
    function removeErrorForField(errorText) {
        const errorIndex = errors.value.findIndex(error => error === errorText);
        if (errorIndex !== -1) {
            errors.value.splice(errorIndex, 1);
        }
    }

    // Function to validate the complete form
    function validateForm() {
        errors.value = [];
        
        // Check required fields
        const requiredFields = ['username', 'password', 'confirmPassword', 'firstname', 'lastname', 'email', 'phone_number'];
        const missingFields = requiredFields.filter(field => !formData[field]);
        
        if (missingFields.length > 0) {
            errors.value.push("Please fill in all required fields");
            return false;
        }
        
        // Name validation
        if (!validateName(formData.firstname)) {
            errors.value.push("First name should only contain letters, spaces, hyphens, or apostrophes");
            fieldValidationState.firstname = true;
            return false;
        }
        
        if (!validateName(formData.lastname)) {
            errors.value.push("Last name should only contain letters, spaces, hyphens, or apostrophes");
            fieldValidationState.lastname = true;
            return false;
        }
        
        // Password validation
        if (formData.password !== formData.confirmPassword) {
            errors.value.push("Passwords do not match");
            fieldValidationState.password = true;
            fieldValidationState.confirmPassword = true;
            return false;
        }
        
        // Password strength check
        if (!validatePasswordStrength(formData.password)) {
            errors.value.push("Password must be at least 8 characters and include uppercase, lowercase, and numbers");
            fieldValidationState.password = true;
            return false;
        }
        
        // Email validation
        if (!validateEmail(formData.email)) {
            errors.value.push("Please enter a valid email address");
            fieldValidationState.email = true;
            return false;
        }

        // Phone validation
        if (!validatePhone(formData.phone_number)) {
            errors.value.push("Please enter a valid phone number (7-10 digits, with or without formatting)");
            fieldValidationState.phone_number = true;
            return false;
        }
        
        return errors.value.length === 0;
    }

    // Function to register a new driver
    function register_driver() {
        // Clear previous messages
        message.value = "";
        
        // First, validate the form
        if (!validateForm()) {
            // If validation fails, stop the submission
            return;
        }

        isSubmitting.value = true;

        let reg_form = document.querySelector("#driverform");
        let form_data = new FormData(reg_form);

        // Extract username to use in success message
        const username = form_data.get('username');

        fetch("/api/driver/register", {
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
                    throw new Error(data.error || 'Registration failed');
                }
                return data;
            });
        }) 
        .then(function (data) {
            console.log(data);
            
            // Immediately set success message using the correct username
            message.value = `${data.username || username}, you're successfully registered!`;
            
            // Clear the message after 10 seconds
            setTimeout(() => {
                message.value = "";
            }, 10000);
            
            // Reset form after success
            reg_form.reset();
            
            // Reset form data object
            Object.keys(formData).forEach(key => {
                formData[key] = '';
            });
            
            // Reset validation states
            Object.keys(fieldValidationState).forEach(key => {
                fieldValidationState[key] = false;
            });
        })
        .catch(function (error) {
            console.log(error);
            // Display specific error message
            errors.value.push(error.message);
        })
        .finally(() => {
            isSubmitting.value = false;
        });
    }
</script>



<style >
/* Global styles */

.main-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    width: 100%;
    margin: 0;
    padding: 0;
    position: relative; /* Add this */
    overflow-x: hidden; /* Add this to prevent horizontal scrolling */
}


.background-image {
    position: fixed; /* Fixed position covers entire viewport */
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url('/uploads/background.png'); /* Replace with your image path */
    background-size: cover;
    background-position: center;
    z-index: -1; /* Place behind content */
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
    position: relative; /* Add this */
    z-index: 1; /* Place above background */
    transform: translateX(-10%);
}



/* Form wrapper */
.form-wrapper {
    width: 600px;
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

/* Terms & conditions */
.terms-group {
    display: flex;
    align-items: flex-start;
}

.terms-group input[type="checkbox"] {
    margin-top: 0.25rem;
    margin-right: 0.5rem;
}

.terms-label {
    font-size: 0.8rem;
    color: #666;
}

/* Sign up button */
.button-container {
    text-align: center;
    margin: 1.5rem 0;
}

.signup-button {
    background-color: #FF8C00;
    color: white;
    border: none;
    border-radius: 25px;
    padding: 0.75rem 2rem;
    font-size: 0.9rem;
    cursor: pointer;
    transition: background-color 0.2s;
}

.signup-button:hover {
    background-color: #e67e00;
}

.signup-button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
}

.login-link {
    font-size: 0.8rem;
    color: #666;
}

.login-link a {
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


/* For larger screens - add this to ensure footer stays centered */
@media (min-width: 769px) {
  .register-footer {
    position: absolute; /* Position at the bottom */
    bottom: 0; /* Align to bottom */
    transform: translateX(-10%);
  }
  
  /* Ensure the main container has proper positioning for the absolute footer */
  .main-container {
    position: relative;
    min-height: 100vh;
    padding-bottom: 2rem; /* Add padding to prevent content from being hidden by footer */
  }
}

/* For smaller screens */
@media (max-width: 768px) {
    .content-container {
        padding: 1rem;
        transform: translateX(0); /* Reset translation for smaller screens */
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

/* Override footer styles for this page only */

/* Custom footer just for this page */
.register-footer {
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
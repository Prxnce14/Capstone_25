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
                
                <h1>Personal Account - Sign Up</h1>
                
                <!-- Registration form -->
                <form @submit.prevent="register_general" id="registerform" class="signup-form">
                    <!-- Alert messages -->
                    <div v-if="message || errors.length > 0" :class="{'alert alert-success': message, 'alert alert-danger': errors.length > 0}" role="alert">
                        <p v-if="message">{{ message }}</p>
                        <ul v-if="errors">
                            <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
                        </ul>
                    </div>
                    
                    <div class="form-fields">
                        <div class="form-group">
                            <label for="username">Username</label>
                            <input type="text" id="username" name="username" class="form-control" placeholder="Choose a unique username" required/>
                        </div>

                        <div class="form-group">
                            <label for="password">Password</label>
                            <input type="password" name="password" class="form-control" placeholder="Password" required />
                        </div>

                        <div class="form-group">
                            <label for="confirmPassword">Confirm Password</label>
                            <input type="password" id="confirmPassword" name="confirmPassword" class="form-control" placeholder="Password" required/>
                        </div>

                        <div class="form-group">
                            <label for="firstname">Firstname</label>
                            <input type="text" name="firstname" class="form-control" placeholder="John" required />
                        </div>

                        <div class="form-group">
                            <label for="lastname">Lastname</label>
                            <input type="text" name="lastname" class="form-control" placeholder="Brown" required />
                        </div>

                        <div class="form-group">
                            <label for="email">Email</label>
                            <input type="email" name="email" class="form-control" placeholder="johnbrown@hotmail.com" required />
                        </div>

                        <div class="form-group">
                            <label for="phone_number">Phone number</label>
                            <input type="text" name="phone_number" class="form-control" placeholder="658-123-4567" required />
                        </div>

                        <div class="form-group terms-group">
                            <input type="checkbox" id="terms" required>
                            <label for="terms" class="terms-label">
                                By signing up, you agree to our <a href="#">Terms of Service and Privacy Policy</a>.
                            </label>
                        </div>

                        <div class="button-container">
                            <button type="submit" class="signup-button">Sign Up</button>
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

    import {ref, onMounted} from "vue";
    let csrf_token = ref("");
    let message = ref("");
    let errors = ref([]);


    function getCsrfToken() {
        fetch('/api/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            csrf_token.value = data.csrf_token;
        })
    }

    onMounted(() => {
    getCsrfToken();
    });


    // Fucntion to validate email format
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(String(email).toLowerCase());
    }


    // Function to validate password and confirm password match
    function validateForm() {
        errors.value = [];
        const form = document.querySelector("#registerform");
        const password = form.querySelector('input[name="password"]').value;
        const confirmPassword = form.querySelector('input[name="confirmPassword"]').value;
        const email = form.querySelector('input[name="email"]').value;
        const phoneNumber = form.querySelector('input[name="phone_number"]').value;
        
        // Check required fields (add more as needed)
        if (!password || !confirmPassword || !email) {
            errors.value.push("Please fill in all required fields");
            return false;
        }
        
        // Password validation
        if (password !== confirmPassword) {
            errors.value.push("Passwords do not match");
            return false;
        }
        
        // Email validation
        if (!validateEmail(email)) {
            errors.value.push("Please enter a valid email address");
            return false;
        }

        // Updated phone regex to accept 7-10 digits with or without formatting
        // Will accept formats like: 1234567, 123-4567, 1234567890, 123-456-7890
        // - Parentheses format with area code (876)654-1234

        const phoneRegex = /^(?:\(\d{3}\)\d{3}-\d{4}|\d{3}-\d{3}-\d{4}|\d{3}-\d{4}|\d{7,10})$/;
        if (!phoneRegex.test(phoneNumber)) {
            errors.value.push("Please enter a valid phone number (7-10 digits, with or without dashes)");
            return false;
        }
    
        return errors.value.length === 0;
    }

    // Function to register a new user
    function register_general() {
        // Clear previous messages
        message.value = "";
        errors.value = [];
        
        // First, validate the form
        if (!validateForm()) {
            // If validation fails, stop the submission
            return;
        }

        let reg_form = document.querySelector("#registerform");
        let form_data = new FormData(reg_form);

        // Extract username to use in success message
        const username = form_data.get('username');

        fetch("/api/gen/register", {
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
            // We use the username from the form data as a fallback
            message.value = `${data.username || username} you're successfully registered!`;
            
            // Clear the message after 10 seconds
            setTimeout(() => {
                message.value = "";
            }, 10000);
            
            // Reset form only after success
            reg_form.reset();
        })
        .catch(function (error) {
            console.log(error);
            // Display specific error message
            errors.value.push(error.message);
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






















































































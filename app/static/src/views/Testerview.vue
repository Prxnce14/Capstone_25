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



    function register_general() {
        // First, validate the form
        if (!validateForm()) {
            // If validation fails, stop the submission
            return;
        }

        let reg_form = document.querySelector("#registerform");
        let form_data = new FormData(reg_form);

        fetch("/api/gen/register", {
                method: 'POST',
                body: form_data,
                headers: {
                    'X-CSRFToken': csrf_token.value
                }
        })
        .then(function (response) { 
            // Check if the response is successful
            if (!response.ok) {
                return response.json().then(data => {
                    // Pass the error information to the catch block
                    throw new Error(data.error || 'Network response was not ok');
                });
            }
            return response.json(); 
        }) 
        .then(function (data) {
            console.log(data);
            
            // Display the success message immediately with the correct username
            message.value = `${data.username} you're Successfully registered!`;
            
            // Clear the message after 10 seconds
            setTimeout(() => {
                message.value = "";
            }, 10000);
            
            // Reset the form after success
            reg_form.reset();
        })
        .catch(function (error) {
            console.log(error);
            // Display specific error to user
            errors.value = [];
            errors.value.push(error.message || "Registration failed. Please try again.");
        });
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

        // Phone number validation (basic check, can be improved)
       
        // Add more validations as needed (password strength, etc.)
        
    
        return errors.value.length === 0;
    }

    // Fucntion to validate email format
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(String(email).toLowerCase());
    }
        
</script>
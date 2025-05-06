<template>
    <div class="home-container">
        <h1> Welcome to Pelican Eats</h1>
        <p class="lead">Your favorite food delivery service at UWI Mona Campus</p>
        
        <div class="features">
            <div class="feature-card">
                <h3>Fast Delivery</h3>
                <p>Get your food delivered quickly across campus</p>
            </div>
        
            <div class="feature-card">
                <h3>Local Restaurants</h3>
                <p>Choose from a variety of campus and nearby restaurants</p>
            </div>
        
            <div class="feature-card">
                <h3>Easy Ordering</h3>
                <p>Simple interface to place and track your orders</p>
            </div>
        </div>
        <div class="cta-section">
            <h2>Hungry? Order now!</h2>
            <button class="order-btn">Browse Restaurants</button>
        </div>
    </div>
</template>
  
<script setup>
// You can add component logic here if needed
</script>
  
<style scoped>
    .home-container {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
    }

    h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color: #333;
    }

    .lead {
    font-size: 1.25rem;
    margin-bottom: 2rem;
    color: #555;
    }

    .features {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin: 40px 0;
    }

    .feature-card {
    flex: 1;
    min-width: 250px;
    padding: 20px;
    background-color: #f8f9fa;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .feature-card h3 {
    color: #FF8C00; /* Changed from blue to orange */
    margin-bottom: 10px;
    }

    .cta-section {
    text-align: center;
    margin: 40px 0;
    padding: 30px;
    background-color: #FFF3E0; /* Changed from light blue to light orange */
    border-radius: 8px;
    }

    .order-btn {
    background-color: #FF8C00; /* Changed from blue to orange */
    color: white;
    border: none;
    padding: 10px 20px;
    font-size: 1rem;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 15px;
    transition: background-color 0.3s;
    }

    .order-btn:hover {
    background-color: #E67300; /* Changed from darker blue to darker orange */
    }
</style>
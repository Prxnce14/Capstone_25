<template>
    <div class="about-container">
      <h1 class="about-title">About Pelican Eats</h1>
      <div class="title-underline"></div>
      
      <p class="about-text">
        Founded in 2024 by a team of university seniors, Pelican Eats was born from a passion to serve both locals and tourists in Jamaica with authentic culinary experiences.
      </p>
      
      <p class="about-text">
        Our young, energetic team combines fresh perspectives with a deep appreciation for Jamaican cuisine and culture. We bridge the gap between traditional flavors and modern dining expectations.
      </p>
      
      <h2 class="commitment-title">What sets us apart is our commitment to:</h2>
      
      <ul class="commitment-list">
        <li>Support local food establishments</li>
        <li>Provide AI recommendations for personalized food choices</li>
        <li>Ensuring fast and reliable delivery across the UWI Mona Campus</li>
      </ul>
      
      <p class="about-text closing">
        Whether you're a local looking for comfort food or a visitor eager to explore authentic Jamaican flavors, Pelican Eats welcomes you to our table.
      </p>
    </div>
  </template>
  
  <style scoped>
  .about-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 2rem;
    background-color: white;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    border-radius: 4px;
    color: #333;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  }
  
  .about-title {
    color: #333;
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    font-weight: 500;
  }
  
  .title-underline {
    height: 2px;
    background-color: #f9a826;
    margin-bottom: 2rem;
  }
  
  .about-text {
    font-size: 1.1rem;
    line-height: 1.6;
    margin-bottom: a1.5rem;
    color: #333;
  }
  
  .commitment-title {
    color: #333;
    font-size: 1.5rem;
    margin-top: 2rem;
    margin-bottom: 1rem;
    font-weight: 500;
  }
  
  .commitment-list {
    padding-left: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .commitment-list li {
    margin-bottom: 0.7rem;
    position: relative;
    color: #333;
  }
  
  .commitment-list li::marker {
    color: #f9a826;
  }
  
  .closing {
    font-style: italic;
    border-top: 1px solid #eee;
    padding-top: 1.5rem;
    margin-top: 2rem;
  }
  </style>
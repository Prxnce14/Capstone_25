import axios from 'axios';

/**
 * Service for interacting with the product API endpoints
 */
class ProductService {
  /**
   * Get all products for a specific restaurant
   * @param {number} restaurantId - The restaurant ID
   * @returns {Promise} - Promise resolving to an array of products
   */
  async getRestaurantProducts(restaurantId) {
    try {
      const response = await axios.get(`/api/restaurant/${restaurantId}/products`);
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  /**
   * Get a single product by ID
   * @param {number} productId - The product ID
   * @returns {Promise} - Promise resolving to the product object
   */
  async getProduct(productId) {
    try {
      const response = await axios.get(`/api/products/${productId}`);
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  /**
   * Create a new product
   * @param {FormData} formData - The product data as FormData (for file uploads)
   * @param {number} restaurantId - The restaurant ID
   * @returns {Promise} - Promise resolving to the created product
   */
  async createProduct(formData, restaurantId) {
    try {
      const response = await axios.post(
        `/api/restaurant/${restaurantId}/products`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      );
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  /**
   * Update an existing product
   * @param {number} productId - The product ID
   * @param {FormData} formData - The updated product data as FormData
   * @returns {Promise} - Promise resolving to the updated product
   */
  async updateProduct(productId, formData) {
    try {
      const response = await axios.put(
        `/api/products/${productId}`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      );
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  /**
   * Delete a product
   * @param {number} productId - The product ID
   * @returns {Promise} - Promise resolving to the delete response
   */
  async deleteProduct(productId) {
    try {
      const response = await axios.delete(`/api/products/${productId}`);
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  /**
   * Handle API errors consistently
   * @param {Error} error - The error object
   * @private
   */
  handleError(error) {
    // Log error for debugging
    console.error('API Error:', error);
    
    // You could add more sophisticated error handling here
    // For example, dispatch to a store action to show notifications
    
    // Return meaningful errors based on status codes
    if (error.response) {
      // Server responded with error status
      const { status } = error.response;
      
      if (status === 401 || status === 403) {
        // Handle authentication/authorization errors
        console.error('Authentication error. Please login again.');
        // Could trigger logout or redirect to login
      } else if (status === 422 || status === 400) {
        // Validation errors - already handled in components
        return;
      } else if (status === 500) {
        // Server errors
        console.error('Server error. Please try again later.');
      }
    } else if (error.request) {
      // No response received
      console.error('Network error. Please check your connection.');
    }
  }
}

// Create a singleton instance
const productService = new ProductService();

export default productService;
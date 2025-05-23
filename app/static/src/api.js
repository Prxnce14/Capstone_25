class API {
  constructor() {
    this.baseURL = '/api';
  }

  // Helper method to create fetch options with auth
  getFetchOptions(method = 'GET', body = null, isFormData = false) {
    const token = localStorage.getItem('access_token');
    const csrfToken = sessionStorage.getItem('csrf_token');
    
    console.log('API Call - Token present:', !!token); // Debug
    console.log('API Call - Method:', method); // Debug
    
    const headers = {};
    
    // Add JWT token for authentication
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    
    // Add CSRF token for non-GET requests
    if (method !== 'GET' && csrfToken) {
      headers['X-CSRFToken'] = csrfToken;
    }
    
    // Add Content-Type for JSON requests (not for FormData)
    if (!isFormData && method !== 'GET') {
      headers['Content-Type'] = 'application/json';
    }
    
    const options = {
      method,
      headers,
      credentials: 'include' // Important for CORS
    };
    
    if (body) {
      if (isFormData) {
        options.body = body;
      } else if (typeof body === 'string') {
        options.body = body;
      } else {
        options.body = JSON.stringify(body);
      }
    }
    
    console.log('Fetch options:', {
      method: options.method,
      headers: options.headers,
      hasBody: !!options.body
    }); // Debug
    
    return options;
  }

  // Generic request handler
  async request(url, options) {
    try {
      const fullUrl = `${this.baseURL}${url}`;
      console.log('Making request to:', fullUrl); // Debug
      
      const response = await fetch(fullUrl, options);
      console.log('Response status:', response.status); // Debug
      
      // Handle 401 (Unauthorized) - token expired or invalid
      if (response.status === 401) {
        console.log('Unauthorized - clearing tokens and redirecting'); // Debug
        this.handleUnauthorized();
        throw new Error('Unauthorized - Session expired');
      }
      
      // Try to parse JSON response
      let data;
      try {
        data = await response.json();
        console.log('Response data:', data); // Debug
      } catch (e) {
        console.error('Failed to parse JSON response:', e);
        throw new Error('Invalid server response');
      }
      
      if (!response.ok) {
        throw new Error(data.error || `HTTP error! status: ${response.status}`);
      }
      
      return data;
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  // Handle unauthorized access
  handleUnauthorized() {
    // Clear all stored auth data
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_type');
    localStorage.removeItem('user_id');
    sessionStorage.removeItem('csrf_token');
    
    // Redirect to login
    // Use window.location for a hard redirect to avoid Vue Router issues
    window.location.href = '/login';
  }

  // HTTP Methods
  async get(url) {
    return this.request(url, this.getFetchOptions('GET'));
  }

  async post(url, body = null, isFormData = false) {
    return this.request(url, this.getFetchOptions('POST', body, isFormData));
  }

  async put(url, body = null, isFormData = false) {
    return this.request(url, this.getFetchOptions('PUT', body, isFormData));
  }

  async delete(url) {
    return this.request(url, this.getFetchOptions('DELETE'));
  }

  // Utility methods
  setAuthTokens(accessToken, csrfToken) {
    console.log('Setting tokens:', { 
      hasAccessToken: !!accessToken, 
      hasCsrfToken: !!csrfToken 
    }); // Debug
    
    localStorage.setItem('access_token', accessToken);
    if (csrfToken) {
      sessionStorage.setItem('csrf_token', csrfToken);
    }
  }

  clearAuthTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_type');
    localStorage.removeItem('user_id');
    sessionStorage.removeItem('csrf_token');
  }

  isAuthenticated() {
    return !!localStorage.getItem('access_token');
  }

  getUserType() {
    return localStorage.getItem('user_type');
  }
}

// Create and export a singleton instance
const api = new API();

export default api;
<template>
  <div class="delivery-container">
    <h1 class="delivery-title">Track Delivery</h1>
    
    <div class="delivery-content">
      <!-- Form Section -->
      <div class="form-section">
        <form @submit.prevent="handleRouteSubmit" class="route-form">
          <div class="input-group">
            <label for="origin">Origin Address</label>
            <input 
              id="origin" 
              ref="originInput"
              v-model="originAddress" 
              placeholder="Enter pickup location" 
              required
            />
          </div>
          
          <div class="input-group">
            <label for="destination">Destination Address</label>
            <input 
              id="destination" 
              ref="destinationInput"
              v-model="destinationAddress" 
              placeholder="Enter delivery location" 
              required
            />
          </div>
          
          <button type="submit" class="route-button">Get Routes</button>
        </form>

        <!-- Route Details (will show after authentication) -->
        <div v-if="isAuthenticated && showRouteDetails" class="route-details">
          <div class="route-option">
            <h3>Default Route</h3>
            <p>Distance: {{ defaultRoute.distance || 'Calculating...' }}</p>
            <p>Duration: {{ defaultRoute.duration || 'Calculating...' }}</p>
            <button @click="selectRoute('default')" class="select-button">Select</button>
          </div>
          
          <div class="route-option">
            <h3>Alternate Route</h3>
            <p>Distance: {{ alternateRoute.distance || 'Calculating...' }}</p>
            <p>Duration: {{ alternateRoute.duration || 'Calculating...' }}</p>
            <button @click="selectRoute('alternate')" class="select-button">Select</button>
          </div>
        </div>
      </div>
      
      <!-- Map/Image Section -->
      <div class="visual-section">
        <!-- Show placeholder image if not authenticated -->
        <img 
          v-if="!isAuthenticated" 
          src="/uploads/aerial_jamaica.jpg" 
          alt="Aerial view of Jamaica" 
          class="placeholder-image"
        />
        
        <!-- Show map if authenticated -->
        <div v-else id="my_map" ref="mapDiv" class="map-view"></div>
      </div>
    </div>
    
    <!-- Login Modal -->
    <div v-if="showLoginModal" class="login-modal">
      <div class="modal-content">
        <h2>Login Required</h2>
        <p>Please login to view route details</p>
        <div class="login-buttons">
          <button @click="login" class="login-button">Login</button>
          <button @click="closeLoginModal" class="cancel-button">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DeliveryView',
  data() {
    return {
      map: null,
      markers: [],
      apiKey: '',
      mapId: '',
      originAddress: '',
      destinationAddress: '',
      isAuthenticated: false,
      showRouteDetails: false,
      defaultRoute: {
        distance: null,
        duration: null,
        path: []
      },
      alternateRoute: {
        distance: null,
        duration: null,
        path: []
      },
      selectedRoute: null,
      directionsService: null,
      directionsRenderer: null,
      autocompleteOrigin: null,
      autocompleteDestination: null,
      locations: [
        {
          coords: { lat: 18.0059, lng: -76.7468 },
          title: "UWI Mona"
        },
        {
          coords: { lat: 18.0179, lng: -76.8099 },
          title: "Kingston"
        }
      ]
    }
  },
  mounted() {
    // Fetch API key and map ID from backend
    this.fetchMapConfig()
      .then(() => {
        // Only load Google Maps API for autocomplete initially
        this.loadGoogleMapsApi(true);
      })
      .catch(error => {
        console.error('Error initializing configuration:', error);
      });
      
    // Check if user is already authenticated
    this.checkAuthentication();
    
    // Check for pending route requests
    this.checkPendingRoute();
  },
  methods: {
    async fetchMapConfig() {
      try {
        const response = await fetch('/api/map-config');
        const data = await response.json();
        this.apiKey = data.api_key;
        this.mapId = data.map_id;
      } catch (error) {
        console.error('Error fetching map configuration:', error);
        throw error;
      }
    },
    
    loadGoogleMapsApi(autocompleteOnly = false) {
      // Create the script element
      const script = document.createElement('script');
      
      // Define libraries to load
      const libraries = autocompleteOnly ? 'places' : 'places,marker';
      
      // Define callback function
      const callback = autocompleteOnly ? 'initAutocomplete' : 'initMap';
      
      script.src = `https://maps.googleapis.com/maps/api/js?key=${this.apiKey}&libraries=${libraries}&callback=${callback}`;
      script.async = true;
      script.defer = true;
      
      // Define the global callback function that Google Maps will call
      window.initAutocomplete = this.initAutocomplete;
      window.initMap = this.initMap;
      
      // Append the script to the document
      document.head.appendChild(script);
    },
    
    initAutocomplete() {
      // Set the autocomplete options to restrict to Jamaica
      const options = {
        componentRestrictions: { country: 'jm' },
        fields: ['address_components', 'geometry', 'name']
      };
      
      // Initialize autocomplete for origin and destination fields
      if (this.$refs.originInput) {
        this.autocompleteOrigin = new google.maps.places.Autocomplete(
          this.$refs.originInput,
          options
        );
      }
      
      if (this.$refs.destinationInput) {
        this.autocompleteDestination = new google.maps.places.Autocomplete(
          this.$refs.destinationInput,
          options
        );
      }
    },
    
    async initMap() {
      try {
        // Import required Google Maps libraries
        const { Map } = await google.maps.importLibrary('maps');
        const { AdvancedMarkerElement } = await google.maps.importLibrary('marker');
        
        // Configure map options
        const options = {
          center: { lat: 18.0179, lng: -76.8099 }, // Kingston, Jamaica
          zoom: 14,
          mapId: this.mapId
        };
        
        // Create the map
        this.map = new Map(this.$refs.mapDiv, options);
        console.log('Google Map initialized');
        
        // Initialize directions service and renderer
        this.directionsService = new google.maps.DirectionsService();
        this.directionsRenderer = new google.maps.DirectionsRenderer({
          map: this.map,
          suppressMarkers: false,
          polylineOptions: {
            strokeColor: '#4285F4',
            strokeWeight: 5
          }
        });
        
        // If we have origin and destination addresses, calculate routes
        if (this.originAddress && this.destinationAddress) {
          this.calculateRoutes();
        } else {
          // Add default markers if no routes to display
          this.locations.forEach(location => {
            this.addMarker(location, AdvancedMarkerElement);
          });
        }
      } catch (error) {
        console.error('Error initializing Google Maps:', error);
      }
    },
    
    addMarker(props, AdvancedMarkerElement) {
      const markerOptions = {
        position: props.coords,
        map: this.map,
        title: props.title
      };
      
      const marker = new AdvancedMarkerElement(markerOptions);
      this.markers.push(marker);
      
      return marker;
    },
    
    handleRouteSubmit() {
      if (!this.originAddress || !this.destinationAddress) {
        alert('Please enter both origin and destination addresses');
        return;
      }
      
      if (!this.isAuthenticated) {
        // Store the origin and destination in localStorage or Vuex to retrieve after login
        localStorage.setItem('pendingOrigin', this.originAddress);
        localStorage.setItem('pendingDestination', this.destinationAddress);
        
        // Redirect to the login page
        this.$router.push('/login');
      } else {
        // If already authenticated, calculate and show routes
        this.initializeMapAndCalculateRoutes();
      }
    },
    
    checkAuthentication() {
      // Check if user is already logged in
      // Replace with your actual authentication check
      // For example, checking a token in localStorage or using your auth service
      const token = localStorage.getItem('authToken');
      this.isAuthenticated = !!token;
    },
    
    checkPendingRoute() {
      // Check if there's a pending route calculation from before login
      const pendingOrigin = localStorage.getItem('pendingOrigin');
      const pendingDestination = localStorage.getItem('pendingDestination');
      
      if (this.isAuthenticated && pendingOrigin && pendingDestination) {
        // Set the addresses
        this.originAddress = pendingOrigin;
        this.destinationAddress = pendingDestination;
        
        // Clear the pending data
        localStorage.removeItem('pendingOrigin');
        localStorage.removeItem('pendingDestination');
        
        // Initialize map and calculate routes
        this.initializeMapAndCalculateRoutes();
      }
    },
    
    initializeMapAndCalculateRoutes() {
      // Load full map if not already loaded
      if (!this.map) {
        this.loadGoogleMapsApi(false);
      } else {
        // If map is already loaded, just calculate routes
        this.calculateRoutes();
      }
    },
    
    calculateRoutes() {
      if (!this.directionsService) {
        console.error('Directions service not initialized');
        return;
      }
      
      // Clear existing markers
      this.markers.forEach(marker => marker.map = null);
      this.markers = [];
      
      // Request for default route
      const requestDefault = {
        origin: this.originAddress,
        destination: this.destinationAddress,
        travelMode: google.maps.TravelMode.DRIVING,
        provideRouteAlternatives: false
      };
      
      // Request for alternate route
      const requestAlternate = {
        origin: this.originAddress,
        destination: this.destinationAddress,
        travelMode: google.maps.TravelMode.DRIVING,
        provideRouteAlternatives: true,
        optimizeWaypoints: true
      };
      
      // Get default route
      this.directionsService.route(requestDefault, (result, status) => {
        if (status === google.maps.DirectionsStatus.OK) {
          // Store default route
          const route = result.routes[0];
          this.defaultRoute = {
            distance: route.legs[0].distance.text,
            duration: route.legs[0].duration.text,
            path: route.overview_path
          };
          
          // If this is the selected route or no route is selected, display it
          if (!this.selectedRoute || this.selectedRoute === 'default') {
            this.directionsRenderer.setDirections(result);
            this.selectedRoute = 'default';
          }
          
          // Show route details panel
          this.showRouteDetails = true;
        } else {
          console.error('Error fetching default route:', status);
        }
      });
      
      // Get alternate route
      this.directionsService.route(requestAlternate, (result, status) => {
        if (status === google.maps.DirectionsStatus.OK && result.routes.length > 1) {
          // Use the second route as the alternate
          const route = result.routes[1];
          this.alternateRoute = {
            distance: route.legs[0].distance.text,
            duration: route.legs[0].duration.text,
            path: route.overview_path
          };
        } else {
          console.log('No alternate route available or error:', status);
          // Create a simple alternate route if none found
          this.alternateRoute = {
            distance: 'Not available',
            duration: 'Not available',
            path: []
          };
        }
      });
    },
    
    selectRoute(routeType) {
      this.selectedRoute = routeType;
      
      // Create a directions request based on the selected route
      const request = {
        origin: this.originAddress,
        destination: this.destinationAddress,
        travelMode: google.maps.TravelMode.DRIVING
      };
      
      // Get directions and set the appropriate route
      this.directionsService.route(request, (result, status) => {
        if (status === google.maps.DirectionsStatus.OK) {
          if (routeType === 'default' || result.routes.length <= 1) {
            // Display the first (default) route
            this.directionsRenderer.setRouteIndex(0);
            this.directionsRenderer.setDirections(result);
          } else {
            // Display the second (alternate) route
            this.directionsRenderer.setRouteIndex(1);
            this.directionsRenderer.setDirections(result);
          }
        }
      });
    }
  }
}
</script>

<style scoped>
.delivery-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.delivery-title {
  color: #333;
  font-weight: bold;
  text-align: center;
  margin-bottom: 30px;
}

.delivery-content {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 30px;
}

@media (max-width: 768px) {
  .delivery-content {
    flex-direction: column;
  }
}

.form-section {
  flex: 1;
  min-width: 300px;
}

.visual-section {
  flex: 1.5;
  min-height: 500px;
  border-radius: 8px;
  overflow: hidden;
}

.route-form {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.input-group {
  margin-bottom: 15px;
}

.input-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.input-group input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.route-button {
  width: 100%;
  padding: 12px;
  background-color: #4285F4;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.route-button:hover {
  background-color: #3367d6;
}

.placeholder-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  min-height: 500px;
  border-radius: 8px;
}

.map-view {
  width: 100%;
  height: 500px;
  border-radius: 8px;
}

.route-details {
  margin-top: 20px;
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.route-option {
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
}

.route-option h3 {
  margin-top: 0;
  color: #4285F4;
}

.select-button {
  padding: 8px 12px;
  background-color: #34A853;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.select-button:hover {
  background-color: #2d9144;
}

/* Login Modal Styles */
.login-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.login-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 20px;
}

.login-button {
  padding: 10px 20px;
  background-color: #4285F4;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.cancel-button {
  padding: 10px 20px;
  background-color: #f1f1f1;
  color: #333;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
<template>
    <div class="map-container">
      <h1 class="delivery-link">Track Delivery</h1>
      
      <!-- The div element for the map -->
      <div id="my_map" ref="mapDiv"></div>
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
          // Load Google Maps API dynamically
          this.loadGoogleMapsApi();
        })
        .catch(error => {
          console.error('Error initializing map:', error);
        });
    },
    methods: {
      async fetchMapConfig() {
        try {
          const response = await fetch('http://localhost:7000/api/map-config');
          const data = await response.json();
          this.apiKey = data.api_key;
          this.mapId = data.map_id;
        } catch (error) {
          console.error('Error fetching map configuration:', error);
          throw error;
        }
      },
      
      loadGoogleMapsApi() {
        // Create the script element
        const script = document.createElement('script');
        script.src = `https://maps.googleapis.com/maps/api/js?key=${this.apiKey}&libraries=marker&callback=initMap`;
        script.async = true;
        script.defer = true;
        
        // Define the global callback function that Google Maps will call
        window.initMap = this.initMap;
        
        // Append the script to the document
        document.head.appendChild(script);
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
          
          // Add markers
          this.locations.forEach(location => {
            this.addMarker(location, AdvancedMarkerElement);
          });
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
        
        // You could add click listener for info windows here if needed
        // marker.addListener('click', () => {
        //   // Handle marker click
        // });
        
        return marker;
      }
    }
  }
</script>
  
<style scoped>

    .delivery-link {
    color: #333;
    font-weight: bold;
    cursor: pointer;
    text-decoration: none;
    padding: 8px 16px;
    border-radius: 4px;
    background-color: #f5f5f5;
    transition: background-color 0.3s;
    display: inline-block;
    margin: 10px 0;
    }

    .delivery-link:hover {
    background-color: #e0e0e0;
    }

  .map-container {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  #my_map {
    height: 500px;
    width: 100%;
    margin-top: 20px;
  }
</style>
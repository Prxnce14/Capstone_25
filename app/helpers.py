# Add these imports at the top of the file
from math import radians, cos, sin, asin, sqrt
import requests
import json
import time
from datetime import datetime
import geojson
import os

def get_node_from_location(location_str):
    """Convert location string to node format with coordinates"""
    # Use Google Maps Geocoding API to convert address to coordinates
    # Replace with your actual API key
    api_key = os.environ.get('API_KEY')
    
    # Handle case where location is already in coordinate format
    if isinstance(location_str, dict) and 'lat' in location_str and 'lng' in location_str:
        return {
            'latitude': location_str['lat'],
            'longitude': location_str['lng'],
            'address': location_str.get('address', '')
        }
    
    # Otherwise geocode the address
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location_str}&key={api_key}"
    response = requests.get(geocode_url)
    
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK' and len(data['results']) > 0:
            location = data['results'][0]['geometry']['location']
            return {
                'latitude': location['lat'],
                'longitude': location['lng'],
                'address': data['results'][0]['formatted_address']
            }
    
    # Return default if geocoding fails
    return None

def haversine(coord1, coord2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

def current_time():
    """Get current time for traffic calculations"""
    return datetime.now()

def get_traffic_factor(node, current_time):
    """
    Return traffic multiplier based on location and time
    - Higher values mean more traffic
    - Default implementation uses time of day as a simple proxy
    """
    hour = current_time.hour
    
    # Rush hour: 7-9 AM and 4-6 PM
    if (7 <= hour <= 9) or (16 <= hour <= 18):
        return 1.5
    # Late night: 11 PM - 5 AM
    elif hour >= 23 or hour <= 5:
        return 0.8
    # Default: normal traffic
    else:
        return 1.0

def get_nearby_intersections(lat, lng, radius=500):
    """
    Get nearby road intersections
    Using Google Maps Roads API
    """
    api_key = os.environ.get('API_KEY')
    
    # In a real implementation, you would use the Roads API
    # For simplicity, we'll simulate this with some nearby points
    # This is where you'd make the actual API call
    
    # Sample code for actual implementation:
    # roads_url = f"https://roads.googleapis.com/v1/nearestRoads?points={lat},{lng}&key={api_key}"
    # response = requests.get(roads_url)
    # data = response.json()
    
    # For now, simulate with points in cardinal directions
    # In a real implementation, replace this with actual API data
    nearby = []
    # Create points around 100m in each direction
    for i in range(4):
        angle = i * 90  # 0, 90, 180, 270 degrees
        # Simple approximation (not accurate for large distances)
        lat_offset = 0.0009 * cos(radians(angle))  # ~100m
        lng_offset = 0.0011 * sin(radians(angle))  # ~100m
        
        nearby.append({
            'latitude': lat + lat_offset,
            'longitude': lng + lng_offset,
            'address': f"Intersection {i}"
        })
    
    return nearby

def get_route_segment(start, end):
    """
    Get route info between two points
    Using Google Maps Directions API
    """
    api_key = os.environ.get('API_KEY')
    
    # Construct the URL for the Directions API
    directions_url = (
        f"https://maps.googleapis.com/maps/api/directions/json?"
        f"origin={start['latitude']},{start['longitude']}&"
        f"destination={end['latitude']},{end['longitude']}&"
        f"key={api_key}"
    )
    
    # Make the request
    response = requests.get(directions_url)
    
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK' and len(data['routes']) > 0:
            route = data['routes'][0]['legs'][0]
            return {
                'duration': route['duration']['value'],  # in seconds
                'distance': route['distance']['value'],  # in meters
                'start_location': route['start_location'],
                'end_location': route['end_location'],
                'steps': route['steps']
            }
    
    # If API call fails or no routes, estimate using haversine
    distance = haversine(
        (start['longitude'], start['latitude']),
        (end['longitude'], end['latitude'])
    ) * 1000  # Convert km to meters
    
    # Estimate duration assuming 30 km/h average speed
    duration = distance / 30 * 3.6  # Convert to seconds
    
    return {
        'duration': duration,
        'distance': distance,
        'start_location': {'lat': start['latitude'], 'lng': start['longitude']},
        'end_location': {'lat': end['latitude'], 'lng': end['longitude']},
        'steps': []
    }

def convert_to_geojson(path):
    """Convert path to GeoJSON format for map rendering"""
    if not path:
        return None
        
    # Create a LineString feature
    coordinates = [(node['longitude'], node['latitude']) for node in path]
    
    line = geojson.LineString(coordinates)
    feature = geojson.Feature(geometry=line, properties={})
    feature_collection = geojson.FeatureCollection([feature])
    
    return feature_collection
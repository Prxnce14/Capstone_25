let map;
let marker;


async function initMap() 
{

    // Create the map div dynamically
    const mapDiv = document.createElement('div');
    mapDiv.id = 'my_map';
    document.body.appendChild(mapDiv);
    

    // This is  the call to the google maps library
    const { Map } = await google.maps.importLibrary('maps');
    // another call to the google maps library
    const { AdvancedMarkerElement } = await google.maps.importLibrary('marker');
    
    var options = 
    {   
        // The center of the map is set to the coordinates of Kingston, Jamaica
        center: { lat: 18.0179, lng: -76.8099 },
        // The center of the map is set to the coordinates of the Papine Area in Kingston, Jamaica
        //center: { lat: 18.0192, lng: -76.7409 },
        zoom: 14,
        mapId: window.map_id,   
    };

    //The map object is created here.
    /* Thhis map obeject takes in two parameters, the first is the element that the map will be rendered in, 
    and the second is an object that contains the center and zoom level of the map. */
    map = new Map(document.getElementById("my_map"), options);
    console.log("Hello World");

    //Listen for a click on the map.  This accepts three parameters, 1st - map object, 2nd - click event, 3rd - function executed when the event is triggered.
    // google.maps.event.addListener(map, 'click', function(event)
    // {
    //     // Add marker
    //     addMarker({coords:event.latLng});
    // });



    // Add marker function

    function addMarker(props)
    {   

        var markerOptions =
        {
            position: props.coords,
            map: map,
            title: props.title
        };
        
        marker = new AdvancedMarkerElement(markerOptions);

        
        // // Addinf infowwindow to each marker that is clicked.
        // marker.addListener("click", () => {
        //     // Set content based on this marker's info
        //     infoWindow.setContent(props.content);
        //     // Open info window at this marker's position
        //     infoWindow.open({
        //         anchor: marker,
        //         map: map
        //     });
        // });
        
        // // Store marker in array if needed for later reference
        // marker.push(marker);
    };


    //Array of markers.  // Here we can add one marker object that contains the coordinates and title of said marker.
    var my_marker = [
    {
        coords: { lat: 18.0059, lng: -76.7468 },
        title: "UWI Mona"
    },
    {
        coords: { lat: 18.0179, lng: -76.8099 },
        title: "Kingston"
    }
    
    ];


    // Loop through markers.  This is a more efficient way to add  and call multiple markers to the map.
    for (var x =0; x < my_marker.length; x++)
    {
        addMarker(my_marker[x]);
    }

    

}


// Ensure the script runs after the page is fully loaded
window.addEventListener('load', initMap);
//initMap();


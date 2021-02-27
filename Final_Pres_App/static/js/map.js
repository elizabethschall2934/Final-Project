// * * *
// Map.js builds the map displayed by index.html. 
// 
// *
// Declares a function to loop through photo data for each pet to check that at least one photo is available and insert that photo into an array.
// If no photo is available, a paw icon is inserted as a place-holder that will appear in the map pop-up.
function buildPhotoArray(dataTest) {
  var photos = []
  // Extract photos property of each object and store as array
  var photosToCheck = dataTest.map(x => x.photos);

  for (var i = 0; i < photosToCheck.length; i++) {
    // Check if a small photo exists.
    if (photosToCheck[i][0] != undefined && photosToCheck[i][0].medium != undefined) {
      photos.push(photosToCheck[i][0].medium);
    }
    // If no small photo is available, show the paw icon.
    else {
      photos.push("../static/assets/pet_icons/pawIcon.png");
    }
  } // close for loop
  return photos;

} // close function declaration

// Declares function to select marker icon based on pet type
function getIcon(animalType) {
  return animalType == "Cat" ? "../static/assets/pet_icons/catIcon.png" :
         animalType == "Dog" ? "../static/assets/pet_icons/dogIcon.png" :
         animalType == "Horse" ? "../static/assets/pet_icons/horseIcon.png" :
         animalType == "Rabbit" ? "../static/assets/pet_icons/rabbitIcon.png" :
         animalType == "Bird" ? "../static/assets/pet_icons/birdIcon.png" :
         animalType == "Small & Furry" ? "../static/assets/pet_icons/smallFurryIcon.png" :
         animalType == "Scales, Fins & Other" ? "../static/assets/pet_icons/fishIcon.png" :
                       "../static/assets/pet_icons/pawIcon.png"; // default return value
}

// Reads in coordinate look-up table
d3.json("/lookUpLocation").then(function(lookupTable) {

  // Reads in data and parses arrays of interest for markers
  d3.json("/getPetData").then(function(data) {
    // Parse arrays of interest from json
    var street = data.map(x => x.contact.address.address1)
    var city = data.map(x => x.contact.address.city)
    var state = data.map(x => x.contact.address.state)
    var types = data.map(x => x.type);
    var names = data.map(x => x.name);
    var photos = buildPhotoArray(data);
    var urls = data.map(x => x.url);

    // Loops through street, city, and state arrays to concatenate and format address components into one array of addresses
    var addresses = [];
    for (i = 0; i < state.length; i++) {
      var address = `${street[i]}, ${city[i]}, ${state[i]}`;
      addresses.push(address);
    } // closes for loop

    // Passes address array to getCoordinates function to retrieve corresponding lat/longs and build locations array
    var coordinates = [];
    for (i = 0; i < addresses.length; i++) {
      try {
        var lat = lookupTable[addresses[i]][0];
        var lon = lookupTable[addresses[i]][1];
        //Appends lat and long to coordinates array
        var coordinatePair = [lat, lon];
        coordinates.push(coordinatePair);
      }
      catch (err) { }
    }

    createMarkers();

    // Function to create markers and assign design and pop-up from data
    function createMarkers() {
      // Creates marker cluster group to aggregate markers neatly when map user zooms out
      var markerClusters = L.markerClusterGroup();

      // Loops through data arrays
      for (var i = 0; i < coordinates.length; i++) {
        // Declares string variable to hold icon URLs
        var iconURL = "";
        // Extracts attributes needed to define markers
        var lat = coordinates[i][1];
        console.log(lat)
        var lon = coordinates[i][0];
        var type = types[i];
        var name = names[i];
        var photo = photos[i];
        var url = urls[i];
        // Calls getIcon() to select icon based on pet type
        iconURL = getIcon(type);
        // Creates pawIcon object
        var pawIcon = L.icon({
          iconUrl: iconURL,
          iconSize: [60, 50]
        });

        // Adds a new marker to the cluster group and binds a pop-up
        markerClusters.addLayer(L.marker([lat, lon], { icon: pawIcon })
          .bindPopup(`<img src=${photo} width="300" height="250"<br><br><br><center><strong><a style="font-size: 20px" href=${url} target="_blank">Meet ${name}</a></strong></center>`));
      } // close for loop

      // Calls createMap function, passing in the marker layer group.
      createMap(markerClusters);
    }
  }); // Closes d3.json to read in pet data
}); // Closes d3.json to read in look-up table

function createMap(markerClusters) {
  // Uses Stadia Maps base map (available at https://leaflet-extras.github.io/leaflet-providers/preview/)
  var basemap = L.tileLayer("https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}{r}.png", {
    attribution: "&copy; <a>Stadia Maps</a>, &copy; <a>OpenMapTiles</a> &copy; <a>OpenStreetMap</a> contributors",
    maxZoom: 15
  });

  // Creates an object to hold the basemap. This will be passed to the layer control.
  var baseMapChoices = {
    "Base map": basemap
  };

  // Creates an object to hold the layer group. This will be passed to the layer control.
  var overlayChoices = {
    "Markers": markerClusters
  };

  // Creates the map object, centered over California on page load
  L.map("map", {
    center: [37.5, -120],
    zoom: 6,
    layers: [basemap, markerClusters]
  })
}; // Close createMap()
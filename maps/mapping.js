//var map;

var colors = {
    pos : "green",
    neg : "red",
    neutral : "blue"
}

var fillColors = {
    pos : "#2ecc71",
    neg : "#f03",
    neutral : "#2980b9"
}

var regionLocations = {
    "Manhattan, NY" : [40.7903, -73.9597],
    "Bronx, NY" : [40.8373, -73.8860],
    "Queens, NY" : [40.7500, -73.8667],
    "Brooklyn, NY" : [40.6928, -73.9903 ]  
};



function setLocationRegion(region){
    console.log("Setting region: " + region);
    setLocationView(regionLocations[region]);
    displayRegionSentiment(region);
}
        
function setLocationView(coords){
    map.setView(coords, 13);
}



function displayRegionSentiment(region){
    var regionData = yaks.filter(function(yak){
        return (yak.region === region);
    });
    
    regionData.forEach(function(yak) {
        var position = [yak.latitude, yak.longitude];
    
        L.circle(position, 180, {
            color : colors[yak.sentiment],
            fillColor : fillColors[yak.sentiment],
            fillOpacity : 0.9 
        }).addTo(map).bindPopup(yak.message);
    });
}

function initializeMap(){
    map = L.map('map').setView([51.505, -0.09], 13);

    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
}
var map = L.map('map').setView([55.61121, 12.99351], 16);
L.tileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
        'tiles Courtesy of <a href="http://www.mapquest.com/" target="_blank">MapQuest</a>',
    subdomains: '1234',
}).addTo(map);

var marker = L.marker(map.getCenter()).addTo(map);
marker.bindPopup("Hello World!").openPopup();

if(typeof MainWindow != 'undefined') {
    var onMapMove = function() { MainWindow.onMapMove(map.getCenter().lat, map.getCenter().lng) };
    map.on('move', onMapMove);
    onMapMove();
}
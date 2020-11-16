let map;
let marker;
const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

window.onload = () => {
    'Se dispara cuando el html termine de cargar'
    initializeMap('myMap');
};

const initializeMap = () => {
    map = L.map('myMap').setView([-34.9187,-57.956], 13);
    L.tileLayer(tileUrl).addTo(map);
    
    map.on('click', mapClickHandler);
    /*addSearchControl(); llamado al buscador. todavia no*/
};

const mapClickHandler = (e) => {
    addMarker(e.latlng);
};

const addMarker = ({ lat, lng }) => {
    if (marker) marker.remove();
    marker = L.marker([lat, lng]).addTo(map);
}; 

const submitHandler = (event) => {
    if(!marker) {
        event.preventDefault();
        alert('Debe seleccionar la ubicacion en el mapa');
    }
    else { 
        latlng = marker.getLatLng();
        document.getElementById('lat').setAttribute('value', latlng.lat.toString());
        document.getElementById('lng').setAttribute('value', latlng.lng.toString());
    }
};

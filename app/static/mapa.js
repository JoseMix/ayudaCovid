
let map;
let marker;
const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

window.onload = () => {
    'Se dispara cuando el html termine de cargar'
    initializeMap('myMap');
};

const initializeMap = (selector) => {
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
    alert("HOOOLA")
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

/*const addSearchControl = () => {
    L.control.scale().addTo(map);
    let addSearchControl = L.ersi.Controls.Geoseach().addTo(map);
    let results = new L.LayerGroup().addTo(map);*/


    /*searchControl.on('results', (data) => {
        results.clearLayers();

        if (data.results.length > 0){
            addMarker(data.results[0].latlng);
        };        
    });
};*/
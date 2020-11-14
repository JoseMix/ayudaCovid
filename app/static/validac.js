function confirmation() 
{
    if(confirm("Esta seguro que desea eliminar Usuario?"))
    {
      return true;
    }
    else
    {
      return false;
    }
}

function activar() 
{
    if(confirm("Esta seguro que desea activar Usuario?"))
    {
      return true;
    }
    else
    {
      return false;
    }
}

function eliminarCentro() 
{
    if(confirm("Esta seguro que desea eliminar el Centro?"))
    {
      return true;
    }
    else
    {
      return false;
    }
}
let map;
let marker;

const mapClickHandler = (e) => {
    addMarker(e.latlng);
};

const addMarker = ({ lat, lng }) => {
    if (marker) marker.remove();

    marker = L.marker([lat, lng]).addTo(map);
};

const initializeMap = (selector) => {
    mpa = L.map(selector).setView([-34.9187,-57.956], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

    addSearchControl();

    map.on('click', mapClickHandler);
};
 
const addSearchControl = () => {
    L.control.scale().addTo(map);
    let addSearchControl = L.ersi.Controls.Geoseach().addTo(map);

    let results = new L.LayerGroup().addTo(map);

    searchControl.on('results', (data) => {
        results.clearLayers();

        if (data.results.length > 0){
            addMarker(data.results[0].latlng);
        };        
    });
};

const submitHandler = (event) => {
    if(!maker) {
        event.preventDefault();
        alert('Debe seleccionar la ubicacion en el mapa');
    }
    else { 
        latlng = market.getLatLng();
        document.getElementById('lat').setAttribute('value', latlng.lat);
        document.getElementById('lng').setAttribute('value', latlng.lng);
    }
};

window.onload = () => {
    initializeMap('mapid');
};
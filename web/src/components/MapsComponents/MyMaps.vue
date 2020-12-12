<template>
  <div class="mapa">
    <l-map :zoom="zoom" :center="center">
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <l-marker
        v-for="(marker, index) in markers"
        :key="index"
        ref="markersRef"
        :lat-lng="{ lat: marker.latitud, lng: marker.longitud }"
      >
        <l-popup>
          <strong>{{ marker.nombre }}</strong>
          <p>
            Dirección:
            {{ marker.direccion }} <br />
            Horario:
            {{ marker.apertura + "-" + marker.cierre }}<br />
            Teléfono:
            {{ marker.telefono }}
          </p>
          <!-- llamamos componente  -->
          <FormFecha />
          <br /><button style="margin:5%;" @click="addStops(marker)">
            Solicitar turno
          </button>
        </l-popup>
      </l-marker>
    </l-map>
  </div>
</template>

<script>
//   LTooltip,
import { LMap, LTileLayer, LMarker, LPopup } from "vue2-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import axios from "axios";
import FormFecha from "../components/CentroComponents/FormFecha.vue";

L.Icon.Default.imagePath = "https://unpkg.com/leaflet@1.3.4/dist/images/";

export default {
  name: "MyMap",
  components: {
    "l-map": LMap,
    "l-tile-layer": LTileLayer,
    "l-marker": LMarker,
    // "l-tooltip": LTooltip,
    "l-popup": LPopup,
    FormFecha,
  },
  data() {
    return {
      zoom: 14,
      center: { lat: -34.9187, lng: -57.956 },
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      markers: [],
      markerObjects: null,
    };
  },
  mounted: function() {
    axios.get("http://127.0.0.1:5000/api/centros-all/").then((response) => {
      this.markers = response.data[0].centros[0];
    });
  },
  // mounted: function() {
  //   L.Icon.Default.imagePath = "https://unpkg.com/leaflet@1.3.4/dist/images/";
  //   this.$nextTick(() => {
  //     this.markerObjects = this.$refs.markersRef.map((ref) => ref.mapObject);
  //   });
  // },

  // methods: {
  //   displayTooltip(selectedIndex) {
  //     for (let markerObject of this.markerObjects) {
  //       markerObject.closeTooltip();
  //     }
  //     this.markerObjects[selectedIndex].toggleTooltip();
  //   },
  // },

  // axios
  //     .get("http://127.0.0.1:5000/api/centros/").catch((e) => {
  //       if (e=="Error: Network Error"){
  //           alert("En este momento no se puede visualizar los centros, intente mas tarde.");
  //       }
  //       })
  //     .then((response) => (this.centros = response.data[0].centros[0]) );
  // },
};
</script>

<style>
li {
  cursor: pointer;
}
.mapa {
  height: 60%;

  margin: 10px;
}
</style>

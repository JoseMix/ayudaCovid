<template>
  <div class="container">
    <l-map :zoom="zoom" :center="center">
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <l-marker
        v-for="(marker, index) in markers"
        :key="index"
        ref="markersRef"
        :lat-lng="marker.position"
      >
        <!-- en la siguiente linea ponemos info para ver cuando nos posicionamos en el punto -->
        <l-tooltip :content="marker.name.nombre + marker.name.horario" />
        <!-- l-popup :content="marker.name"/ -->
      </l-marker>
    </l-map>
  </div>
</template>

<script>
// , LPopup }
import { LMap, LTileLayer, LMarker, LTooltip } from "vue2-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

L.Icon.Default.imagePath = "https://unpkg.com/leaflet@1.3.4/dist/images/";

export default {
  name: "MyMap",
  components: {
    "l-map": LMap,
    "l-tile-layer": LTileLayer,
    "l-marker": LMarker,
    "l-tooltip": LTooltip,
    // "l-popup": LPopup,
  },
  data() {
    return {
      zoom: 14,
      center: { lat: -34.9187, lng: -57.956 },
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      markers: [
        /* aca se muestran todos los puntos */
        {
          Id: 1,
          name: { nombre: "Centro 1", tipo: "comedor", horario: "12hs a 22hs" },
          position: { lat: -34.9135, lng: -57.9651 },
        },
        {
          Id: 2,
          name: { nombre: "Centro 1", tipo: "comedor", horario: "12hs a 22hs" },
          position: { lat: -34.9248, lng: -57.967 },
        },
        {
          Id: 3,
          name: { nombre: "Centro 1", tipo: "comedor", horario: "12hs a 22hs" },
          position: { lat: -34.9158, lng: -57.9725 },
        },
        {
          Id: 4,
          name: { nombre: "Centro 1", tipo: "comedor", horario: "12hs a 22hs" },
          position: { lat: -34.9177, lng: -57.9587 },
        },
        {
          Id: 5,
          name: { nombre: "Centro 1", tipo: "comedor", horario: "12hs a 22hs" },
          position: { lat: -34.9231, lng: -57.9637 },
        },
      ],
      markerObjects: null,
    };
  },
  mounted: function() {
    L.Icon.Default.imagePath = "https://unpkg.com/leaflet@1.3.4/dist/images/";
    this.$nextTick(() => {
      this.markerObjects = this.$refs.markersRef.map((ref) => ref.mapObject);
    });
  },

  methods: {
    displayTooltip(selectedIndex) {
      for (let markerObject of this.markerObjects) {
        markerObject.closeTooltip();
      }
      this.markerObjects[selectedIndex].toggleTooltip();
    },
  },
};
</script>

<style>
li {
  cursor: pointer;
}
</style>

<template>
  <v-container>
    <h1>Página de centros</h1>
    <router-link to="/turnos" class="btn btn-primary">Turnos</router-link>
    <router-link to="/" class="btn btn-primary">Volver </router-link>
    <my-map />
    <ListaCentros />
  </v-container>
</template>

<script>
import MyMap from "../components/MapsComponents/MyMaps.vue";
import ListaCentros from "../components/CentroComponents/ListaCentros.vue";
export default {
  name: "Centros",
  components: {
    MyMap,
    ListaCentros,
  },
};
</script>

<style>
html,
body,
#app,
div.container {
  height: 100%;
  margin: 0;
}
</style>

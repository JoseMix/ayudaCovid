<template>
  <v-container>
    <h1>Página de Centros</h1>
          <v-btn
          class="red darken-1 display-1 font-weight-thin"
          elevation="2"
          large
          accent-2
          outlined
          rounded
          @click="$router.go(-1)"
          >Volver</v-btn>        
         <MyMap />
  </v-container>
</template>

<script>
import MyMap from "../components/MapsComponents/MyMaps.vue";

export default {
  name: "Centros",
  components: {
    MyMap,
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

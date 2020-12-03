<template>
  <v-container>
    <my-map />
    <div class="Centros">
      <h1>Página de centros</h1>
      <p>
        Acá consumimos la api de Centros, mostramos el mapa con un punto por
        cada centro. Al hacer click en uno, se muestra la info de contacto.
      </p>
      <router-link to="/turnos" class="btn btn-primary">Turnos</router-link>
      <p>
        Dado un centro de ayuda seleccionado, se debe brindar la posibilidad de
        solicitar un turno. El usuario debe especificar primero para que fecha
        espera el turno. La aplicación debe mostrarles los turnos disponibles
        para ese día y al seleccionar uno y completar su datos de contacto
        (Nombre, apellido, email y teléfono) puede realizar la solicitud.
      </p>
      <br />
      <router-link to="/" class="btn btn-primary">Volver </router-link>
    </div>
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

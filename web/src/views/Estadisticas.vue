<template>
  <div class="Estadisticas">
    <h1 class="display-1 font-weight-thin" style="text-align:center">
      Estadisticas
    </h1>

    <Stats></Stats>
  </div>
</template>

<script>
// @ is an alias to /src
import Stats from "../components/EstadisticasComponents/Inicio.vue";

export default {
  name: "Estadisticas",
  components: {
    Stats,
  },
};
</script>

<template>
  <div class="Estadisticas">
    <h1>Estadisticas</h1>
    <PieChart></PieChart>
    <VeWaterfall></VeWaterfall>

    <router-link to="/" class="btn btn-primary">Volver </router-link>
  </div>
</template>

<script>
// @ is an alias to /src
import PieChart from "../components/EstadisticasComponents/PieChart.vue";
import VeWaterfall from "../components/EstadisticasComponents/LineChart.vue";

export default {
  name: "Estadisticas",
  components: {
    PieChart,
    VeWaterfall,
  },
};
</script>

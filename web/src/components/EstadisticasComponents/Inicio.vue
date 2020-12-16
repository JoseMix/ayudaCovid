<template>
  <v-container fluid ma-0 px-6 fill-height>
    <v-row>
      <v-col align="center" justify="center">
        <PieChart></PieChart>
      </v-col>
      <v-col align="center" justify="center">
        <LineChart></LineChart>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import LineChart from "./LineChart.vue";
import PieChart from "./PieChart.vue";
export default {
  name: "Estadisticas",
  components: {
    PieChart,
    LineChart,
  },
  data: () => ({}),
};
</script>

<style></style>

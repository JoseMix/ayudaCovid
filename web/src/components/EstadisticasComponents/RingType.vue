<template>
  <v-container fluid ma-0 px-6 fill-height>
    <v-row>
      <v-col>
        <h4>CANTIDAD DE CENTROS POR TIPO</h4>
        <ve-ring :data="chartData" :settings="chartSettings"></ve-ring>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import VeRing from "v-charts/lib/ring.common";
import axios from "axios";

export default {
  components: { VeRing },
  data() {
    this.chartSettings = {
      radius: [30, 100],
      offsetY: 200,
    };
    return {
      chartData: {
        columns: ["tipo_centro", "cantidad"],
        rows: [],
      },
    };
  },
  created() {
    axios
      .get(
        "https://admin-grupo13.proyecto2020.linti.unlp.edu.ar/api/centros/tipos/"
      )
      .then((response) => {
        this.chartData.rows = response.data[0].centros[0];
      });
  },
};
</script>

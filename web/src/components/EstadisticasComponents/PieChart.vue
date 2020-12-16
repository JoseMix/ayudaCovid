<template>
  <v-container fluid ma-0 px-6 fill-height>
    <v-row>
      <v-col align="center" justify="center">
        <ve-pie :data="chartData"></ve-pie>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import VePie from "v-charts/lib/pie.common";
import axios from "axios";

export default {
  components: { VePie },
  data() {
    return {
      chartData: {
        columns: ["Municipio", "Cantidad"],
        rows: [],
      },
    };
  },
  methods: {},

  created() {
    axios
      .all([
        axios.get("http://localhost:5000/api/municipios/top/5", {}),
        axios.get(
          "https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?page=1&per_page=140",
          {}
        ),
      ])
      .then((result) => {
        this.turnos = result[0].data[0].centros[0];
        this.municipios = result[1].data.data.Town;
        this.municipios = Object.values(this.municipios);

        let arr = [];
        this.turnos.forEach((element) => {
          arr.push({
            Municipio: this.municipios[element.id].name,
            Cantidad: element.cantidad,
          });
        });
        this.chartData.rows = arr;
      });
  },
};
</script>

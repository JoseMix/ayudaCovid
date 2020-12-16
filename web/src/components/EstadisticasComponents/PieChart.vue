<template>
  <v-container fluid ma-0 px-6 fill-height>
    <v-row>
      <v-col align="center" justify="center">
        <ve-pie :data="chartData"></ve-pie>
        <v-select
          v-model="e1"
          @change="onChange(e1)"
          :items="items"
          label="Seleccione cantidad"
        ></v-select>
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
      e1: "5",
      items: ["1", "2", "3", "4", "5"],
      chartData: {
        columns: ["Municipio", "Cantidad"],
        rows: [],
      },
    };
  },
  methods: {
    onChange(event) {
      axios
        .all([
          axios.get("http://localhost:5000/api/municipios/top/" + event, {}),
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
          console.log(arr);
          this.chartData.rows = arr;
        });
    },
  },

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

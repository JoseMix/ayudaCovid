<template>
  <v-container fluid ma-0 px-6 fill-height>
    <v-row>
      <v-col>
        <h3>CANTIDAD DE TURNOS POR TIPO DE CENTRO</h3>
        <v-date-picker v-model="dates" range></v-date-picker>

        <v-text-field
          v-model="dateRangeText"
          label="Fechas seleccionadas:"
          prepend-icon="mdi-calendar"
          readonly
        ></v-text-field>
      </v-col>
      <v-col v-if="tiene_datos">
        <ve-histogram
          :data="chartData"
          :settings="chartSettings"
        ></ve-histogram>
      </v-col>
      <v-col v-if="!tiene_datos" style="text-align:center; margin-top:15%">
        <h3>{{ vacio }}</h3>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import VeHistogram from "v-charts/lib/histogram.common";
import axios from "axios";
import moment from "moment";
export default {
  components: { VeHistogram },
  data() {
    return {
      dates: [],
      dates_vista: [],
      vacio: "SIN RESULTADOS",
      tiene_datos: false,
      chartSettings: {
        yAxisName: ["Turnos"],
      },
      chartData: {
        columns: ["tipo_centro", "cantidad"],
        rows: [],
      },
    };
  },
  created() {
    //   inicia con rango de fechas por defecto ( hoy a 5 días)
    this.dates[0] = moment().format("YYYY[-]M[-]D");
    this.dates[1] = moment(this.dates[0] + " 00:00:00")
      .add(5, "days")
      .format("YYYY[-]M[-]D");

    this.dates_vista[0] = moment(this.dates[0]).format("D[-]M[-]YYYY");
    this.dates_vista[1] = moment(this.dates[1]).format("D[-]M[-]YYYY");
    this.llamadoApi();
  },
  updated() {
    this.llamadoApi();
  },
  methods: {
    llamadoApi() {
      axios
        .get(
          "http://127.0.0.1:5000/api/turnosPorTipo/fecha_inicio=" +
            this.dates[0] +
            ",fecha_fin=" +
            this.dates[1]
        )
        .then((response) => {
          if (response.data[0].centros[0].length != 0) {
            this.tiene_datos = true;
            this.chartData.rows = response.data[0].centros[0];
          } else {
            this.tiene_datos = false;
          }
        });
    },
    update() {
      this.dates_vista[1] = "";
      this.dates_vista[0] = moment(this.dates[0]).format("D[-]M[-]YYYY");
      this.dates_vista[1] = moment(this.dates[1]).format("D[-]M[-]YYYY");
    },
  },
  computed: {
    dateRangeText() {
      this.update();
      return this.dates_vista.join(" hasta ");
    },
  },
};
</script>

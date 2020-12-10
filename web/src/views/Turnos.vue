<template>
  <div class="Turnos">
    <h1>Página de Turnos</h1>

    <h3>{{ rutasApi($route.params.id, $route.params.fecha) }}</h3>

    <router-link to="/centros" class="btn btn-primary">Volver </router-link>
    <v-form class="pa-15" >
      <v-text-field v-model="email" label="Email"></v-text-field>
      <v-text-field v-model="nombre" label="Nombre"></v-text-field>
      <v-text-field v-model="apellido" label="Apellido"></v-text-field>
      <v-text-field v-model="telefono" label="Telefono"></v-text-field>
      <v-select
        v-model="hora_inicio"
        :items="options"
        label="Horario"
        data-vv-name="select"
        required
      ></v-select>
      <v-btn class="mr-4" @click="reservarTurno">
      submit
      </v-btn>
    </v-form>
    <h1>{{this.error}}</h1>
  </div>
</template>
<script>
import axios from "axios";
import moment from "moment"; 
export default {
  name: "Turnos",
  components: {},
  data: () => ({
    email: "",
    nombre: "",
    apellido: "",
    telefono: "",
    hora_inicio: "",
    hora_fin:"",
    options: [],
    fecha: null,
    apiHorarios: null,
    apiReservarTurno: null,
    error:null,
  }),
  methods: {
    rutasApi(id, fecha) {
      this.fecha = fecha
        .split("-")
        .reverse()
        .join("-");
      this.apiHorarios =
        "http://127.0.0.1:5000/api/centros/" +
        id +
        "/turnos_disponibles/?fecha=" +
        this.fecha;
      this.apiReservarTurno =
        "http://127.0.0.1:5000/api/centros/" + id + "/reserva/";
    },
    reservarTurno() {
      this.hora_fin = moment("2016-03-12 "+this.hora_inicio+":00").add(30, 'minutes').format('HH:mm');
      axios({
        method: "POST",
        url: this.apiReservarTurno,
        data: {
          email: this.email,
          nombre: this.nombre,
          apellido: this.apellido,
          telefono: this.telefono,
          hora_inicio: this.hora_inicio,
          hora_fin: this.hora_fin,
          fecha: this.fecha,
        },
      })
      .catch((e) => {this.error =e.response.data.message});
    },
  },
  mounted: function() {
    axios.get(this.apiHorarios).then((response) => {
      for (let i = 0; i < response.data[0].turno.length; i++) {
        this.options.push(response.data[0].turno[i].hora_inicio);
      }
    });
  },
};
</script>

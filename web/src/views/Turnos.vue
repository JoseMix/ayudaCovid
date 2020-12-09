<template>
  <div class="Turnos">
    <h1>Página de Turnos</h1>

    <h3>{{ rutasApi($route.params.id, $route.params.fecha) }}</h3>

    <router-link to="/centros" class="btn btn-primary">Volver </router-link>
    <v-form class="pa-15">
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
    </v-form>
    <h1>
      {{ this.email }}{{ this.nombre }} {{ this.apellido }} {{ this.telefono }}
    </h1>
  </div>
</template>
<script>
import axios from "axios";
export default {
  name: "Turnos",
  components: {},
  data: () => ({
    email: "",
    nombre: "",
    apellido: "",
    telefono: "",
    hora_inicio: "",
    options: [],
    fecha: null,
    apiHorarios: null,
    apiReservarTurno: null,
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
      alert("holita");
      axios({
        method: "POST",
        url: this.apiReservarTurno,
        data: {
          email: "cata@gmail.com",
          nombre: "Cata",
          apellido: "Lina",
          telefono: "221-3330941",
          hora_inicio: "14:00",
          hora_fin: "14:30",
          fecha: "10-12-2020",
        },
      })
        .then((res) => console.log(res.data))
        .catch((err) => console.log(err));
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

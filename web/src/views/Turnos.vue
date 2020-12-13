<template>
  <div class="Turnos">
    <h1>Página de Turnos</h1>

    <h3>{{ rutasApi($route.params.id, $route.params.fecha) }}</h3>

    <router-link to="/centros" class="btn btn-primary">Volver </router-link>
    <v-form class="pa-15">
      <v-text-field
        v-model="email"
        :error-messages="emailErrors"
        label="Email"
        required
        @input="$v.email.$touch()"
        @blur="$v.email.$touch()"
      ></v-text-field>
      <v-text-field
        v-model="nombre"
        :error-messages="nameErrors"
        label="Nombre"
        required
        @input="$v.nombre.$touch()"
        @blur="$v.nombre.$touch()"
      ></v-text-field>
      <v-text-field
        v-model="ape"
        :error-messages="apeErrors"
        label="Apellido"
        required
        @input="$v.ape.$touch()"
        @blur="$v.ape.$touch()"
      ></v-text-field>
      <v-text-field
        v-model="telefono"
        :error-messages="telefonoErrors"
        label="Telefono"
        type="number"
        required
        @input="$v.telefono.$touch()"
        @blur="$v.telefono.$touch()"
      ></v-text-field>
      <v-select
        v-model="hora_inicio"
        :error-messages="selectErrors"
        :items="options"
        label="Horario"
        data-vv-name="select"
        required
        @change="$v.hora_inicio.$touch()"
        @blur="$v.hora_inicio.$touch()"
      ></v-select>
      <v-btn class="mr-4" @click="reservarTurno">
        submit
      </v-btn>
    </v-form>
  </div>
</template>
<script>
import axios from "axios";
import moment from "moment";
import { validationMixin } from "vuelidate";
import { required, email, maxLength } from "vuelidate/lib/validators";

export default {
  mixins: [validationMixin],
  validations: {
    nombre: { required, maxLength: maxLength(15) },
    email: { required, email },
    ape: { required, maxLength: maxLength(15) },
    telefono: { required, maxLength: maxLength(15) },
    hora_inicio: { required },
  },
  name: "Turnos",
  components: {},
  data: () => ({
    email: "",
    nombre: "",
    ape: "",
    telefono: "",
    hora_inicio: null,
    hora_fin: "",
    options: [],
    fecha: null,
    apiHorarios: null,
    apiReservarTurno: null,
  }),
  computed: {
    nameErrors() {
      const errors = [];
      if (!this.$v.nombre.$dirty) return errors;
      !this.$v.nombre.maxLength &&
        errors.push("Nombre debe tener como maximo 15 caracteres");
      !this.$v.nombre.required && errors.push("Campo obligatorio");
      return errors;
    },
    emailErrors() {
      const errors = [];
      if (!this.$v.email.$dirty) return errors;
      !this.$v.email.email && errors.push("Debe ser un email valido");
      !this.$v.email.required && errors.push("Campo obligatorio");
      return errors;
    },
    apeErrors() {
      const errors = [];
      if (!this.$v.ape.$dirty) return errors;
      !this.$v.ape.maxLength &&
        errors.push("Apellido debe tener como maximo 15 caracteres");
      !this.$v.ape.required && errors.push("Campo obligatorio");
      return errors;
    },
    telefonoErrors() {
      const errors = [];
      if (!this.$v.telefono.$dirty) return errors;
      !this.$v.telefono.maxLength &&
        errors.push("Telefono debe tener como maximo 15 caracteres");
      !this.$v.telefono.required && errors.push("Campo obligatorio");
      return errors;
    },
    selectErrors() {
      const errors = [];
      if (!this.$v.hora_inicio.$dirty) return errors;
      !this.$v.hora_inicio.required && errors.push("Campo obligatorio");
      return errors;
    },
  },
  methods: {
    submit() {
      this.$v.$touch();
    },
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
      this.hora_fin = moment("2016-03-12 " + this.hora_inicio + ":00")
        .add(30, "minutes")
        .format("HH:mm");
      axios({
        method: "POST",
        url: this.apiReservarTurno,
        data: {
          email: this.email,
          nombre: this.nombre,
          apellido: this.ape,
          telefono: this.telefono,
          hora_inicio: this.hora_inicio,
          hora_fin: this.hora_fin,
          fecha: this.fecha,
        },
      })
        .then((response) => {
          response.data[1] == 201;
          alert("Se registro el turno con exito");
        })
        .catch((e) => {
          alert(e.response.data.message);
        });
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

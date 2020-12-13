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
      <v-btn class="mr-4" @click="validaciones">
        submit
      </v-btn>
    </v-form>
  </div>
</template>
<script>
import axios from "axios";
import moment from "moment";
import { validationMixin } from "vuelidate";
import { required, email } from "vuelidate/lib/validators";

export default {
  mixins: [validationMixin],
  validations: {
    nombre: { required },
    email: { required, email },
    ape: { required },
    telefono: { required },
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
      !this.$v.ape.required && errors.push("Campo obligatorio");
      return errors;
    },
    telefonoErrors() {
      const errors = [];
      if (!this.$v.telefono.$dirty) return errors;
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
    validaciones() {
        if ((this.email=="")){
          alert("El campo email no puede estar vacío");
          return false;
        }
        let emailRegex = /^[-\w.%+]{1,64}@(?:[A-Z0-9-]{1,63}\.){1,125}[A-Z]{2,63}$/i;
        if (!emailRegex.test(this.email)) {
          alert("Debe ingresar un email valido");
            return false;
        }  
        if ((this.nombre=="")){
          alert("El campo nombre no puede estar vacío");
          return false;
        }
        if ((this.ape=="" ) ){ 
          alert("El campo apellido no puede estar vacío");
          return false;
        }
        if ((this.telefono=="" ) ){ 
          alert("El campo telefono no puede estar vacío");
          return false;
        }
        if ((this.hora_inicio=="" ) ){ 
          alert("El campo hora no puede estar vacío");
          return false;
        }
      this.reservarTurno()
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
          window.location.href = 'javascript:history.go(-1)';
        })
        .catch((e) => {

          if (e == "Error: Request failed with status code 422"){
            alert('Debe completar todos los campos.')
          }
          else { 
          if(e == "Error: Network Error"){
            alert("En este momento no se puede registrar su turno, intente mas tarde.");
            window.location.href = 'javascript:history.go(-1)';
          }else{
            alert(e.response.data.message);
          }
          }
          });
    },
  },
  mounted: function() {
    axios.get(this.apiHorarios)
    .then((response) => {
      for (let i = 0; i < response.data[0].turno.length; i++) {
        this.options.push(response.data[0].turno[i].hora_inicio);
      }
    })
    .catch((e) => {
      if (e == "Error: Network Error") {
          alert("En este momento no se puede visualizar los horarios para este centro, intente mas tarde.");
          window.location.href = 'javascript:history.go(-1)';
      }else{
        alert(e.response.data.message);
        window.location.href = 'javascript:history.go(-1)';
        }});
  },
};
</script>

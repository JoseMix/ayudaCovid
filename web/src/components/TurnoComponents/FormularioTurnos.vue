<template>
  <div class="formTurnos">
   
   
    <h3>{{ rutasApi($route.params.id, $route.params.fecha) }}</h3>
    <v-container>
      <h1>Página de Turnos</h1>       
      <v-btn
          class="red darken-1 display-1 font-weight-thin"
          elevation="2"
          large
          accent-2
          outlined
          rounded
          @click="$router.go(-1)"
          >Volver</v-btn>
        <v-row align="center" justify="center">
        
          <v-col cols="6"> 
                      
            <v-form class="pa-15">
               <h2>{{$route.params.nombre}}</h2>
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
              <v-btn class="v-btn green darken-1 v-btn--depressed v-btn--flat v-btn--outlined v-btn--rounded v-btn--router theme--light elevation-2 v-size--large display-1 font-weight-thin " @click="validaciones">
                Reservar
              </v-btn>
            </v-form>
          </v-col>
        </v-row>
    </v-container>
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
  name: "FormularioTurnos",
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
        "https://admin-grupo13.proyecto2020.linti.unlp.edu.ar/api/centros/" +
        id +
        "/turnos_disponibles/?fecha=" +
        this.fecha;
      this.apiReservarTurno =
        "https://admin-grupo13.proyecto2020.linti.unlp.edu.ar/api/centros/" + id + "/reserva/";
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
          this.$router.push({name:'Centros'});
        })
        .catch((e) => {

          if (e == "Error: Request failed with status code 422"){
            alert('Debe completar todos los campos.')
          }
          else { 
          if(e == "Error: Network Error"){
            alert("En este momento no se puede registrar su turno, intente mas tarde.");
            this.$router.push({name:'Home'});
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
      }else{
        alert(e.response.data.message);
        }
      this.$router.push({name:'Home'});
      });
  },
};
</script>

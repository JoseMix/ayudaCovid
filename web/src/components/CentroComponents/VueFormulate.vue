<template>
  <v-container>
    <FormulateForm
      v-model="formValues"
      @submit="handleSubmit"
      v-if="creado == ''"
    >
      <v-container fluid ma-0 px-6 fill-height>
        <v-row>
          <v-col align="center" justify="center">
            <FormulateInput
              name="nombre"
              label="Nombre del centro *"
              placeholder="Ingrese un nombre"
              validation="required"
              :validation-messages="{
                required: 'El nombre es requerido.',
              }"
            />

            <FormulateInput
              name="apertura"
              label="Horario de apertura *"
              type="time"
              validation="required"
              :validation-messages="{
                required: 'La hora de apertura es requerida.',
              }"
            />
            <FormulateInput
              name="cierre"
              label="Horario de cierre *"
              type="time"
              validation="required"
              :validation-messages="{
                required: 'La hora de cierre es requerida.',
              }"
            />
            <span
              style="color: #960505;
            font-size: 0.8em;
            font-weight: 300;
            line-height: 1.5;
            margin-bottom: 0.25em;"
            >
              {{ errorDate }}
            </span>

            <FormulateInput
              name="email"
              label="Email"
              type="email"
              placeholder="Ingrese un email"
            />
            <FormulateInput
              name="telefono"
              label="Teléfono *"
              type="text"
              placeholder="Ingrese un teléfono"
              validation="required|number"
              :validation-messages="{
                required: 'El telefono es requerido.',
                number: 'Introduzca un telefono valido',
              }"
            />
            <FormulateInput
              name="tipo_centro"
              label="Tipo de centro"
              placeholder="Seleccione un tipo de centro"
              type="select"
              :options="{ Ropa: 'ropa', Plasma: 'plasma', Comida: 'comida' }"
              validation="required"
              :validation-messages="{
                required: 'Tipo de centro requerido.',
              }"
            />
            <FormulateInput
              name="web"
              label="Web"
              type="url"
              placeholder="Ingrese sitio web"
            />

            <FormulateInput
              name="latitud"
              type="hidden"
              v-model="lat"
              validation="required"
            />
            <FormulateInput
              name="longitud"
              type="hidden"
              v-model="lng"
              validation="required"
              :validation-messages="{
                required: 'La ubicación es requerida.',
              }"
            />
            <FormulateInput
              type="select"
              name="id_municipio"
              label="Municipio *"
              :options="municipios"
              validation="required"
              placeholder="Seleccione un municipio"
              :validation-messages="{
                required: 'El municipio es requerido.',
              }"
            />
          </v-col>
          <v-col align="center" justify="center">
            <FormulateInput
              name="direccion"
              label="Direccion del centro *"
              placeholder="Ingrese una dirección"
              validation="required"
              :validation-messages="{
                required: 'La direccion es requerida.',
              }"
            />

            <strong>Ubicación *</strong>
            <MapComponent @latitud="lat = $event" @longitud="lng = $event" />
            <br />
            <vue-recaptcha
              sitekey="6LeaMgUaAAAAAMO68Dyq8L61D8UDRHM-aY0luK8v"
              :loadRecaptchaScript="true"
              @verify="captchaVerificado"
              @expired="captchaExpired"
            ></vue-recaptcha>
            <span
              style="color: #960505;
            font-size: 0.8em;
            font-weight: 300;
            line-height: 1.5;
            margin-bottom: 0.25em;"
            >
              {{ errorCaptcha }}
            </span>
            <br />
            <br />
            <FormulateInput
              type="submit"
              label="CREAR SOLICITUD DE CENTRO"
              ouner-class="success"
            />
          </v-col>
        </v-row>
      </v-container>
    </FormulateForm>
    <v-row v-if="creado != ''" style=" margin-left:13%">
      <v-col>
        <v-alert type="success" style="text-align:center">
          {{ creado }}
        </v-alert>
      </v-col>
    </v-row>
    <v-row v-if="errorCreacion != ''" style=" margin-left:13%">
      <v-col>
        <v-alert type="alert" color="red" style="text-align:center">
          {{ errorCreacion }}
        </v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script src="https://www.google.com/recaptcha/api.js" async defer></script>
<script
  src="https://www.google.com/recaptcha/api.js?onload=vueRecaptchaApiLoaded&render=explicit"
  async
  defer
></script>
<script src="https://unpkg.com/vue-recaptcha@latest/dist/vue-recaptcha.min.js%22%3E"></script>

<script>
import axios from "axios";
import VueRecaptcha from "vue-recaptcha";
import MapComponent from "./MapComponent.vue";

export default {
  name: "CrearCentro",
  components: {
    VueRecaptcha,
    MapComponent,
  },
  data: () => {
    return {
      captchaFlag: false,
      items: ["Comida", "Ropa", "Plasma"],
      formValues: {},
      municipios: {},
      nombre: "",
      direccion: "",
      email: "",
      errors: "",
      phoneNumber: "",
      apertura: "",
      cierre: "",
      errorDate: "",
      errorCaptcha: "",
      lat: 0,
      lng: 0,
      creado: "",
      errorCreacion: "",
    };
  },
  methods: {
    handleSubmit() {
      if (this.captchaFlag) {
        if (this.formValues.apertura < this.formValues.cierre) {
          axios
            .post(
              "https://admin-grupo13.proyecto2020.linti.unlp.edu.ar/api/centros/",
              // "http://127.0.0.1:5000/api/centros/",
              this.formValues,
              {
                headers: {},
              }
            )
            .then((result) => {
              if (result.data[1] == 201) {
                this.errorCreacion = "";
                this.creado = "¡Solicitud de creación de centro exitosa!";
              }
            })
            .catch((e) => {
              if (e == "Error: Network Error") {
                this.errorCreacion =
                  "En este momento no se puede registrar el centro, intente mas tarde.";
              } else {
                this.errorCreacion = e.response.data.message;
              }
            });
        } else {
          this.errorDate =
            "La hora de cierre debe ser posterior a la de apertura";
        }
      } else {
        this.errorCaptcha = "Por favor verificar Captcha";
      }
    },
    captchaVerificado() {
      this.captchaFlag = true;
      this.errorCaptcha = "";
    },
    captchaExpired() {
      this.captchaFlag = false;
    },
  },

  created() {
    axios
      .get(
        "https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?page=1&per_page=140",
        {}
      )
      .then((result) => {
        this.municipios = result.data.data.Town;
        this.municipios = Object.values(this.municipios);

        let arr = [];
        this.municipios.forEach((element) => {
          arr.push({ label: element.name, value: `${element.id}` });
        });
        this.municipios = arr;
      });
  },
};
</script>

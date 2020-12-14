<template>
  <FormulateForm v-model="formValues" @submit="handleSubmit">
    <v-container>
      <v-row>
        <v-col>
          <FormulateInput
            name="nombre"
            label="Nombre del centro"
            validation="required"
            :validation-messages="{
              required: 'El nombre es requerido.',
            }"
          />
          <FormulateInput
            name="direccion"
            label="Direccion del centro"
            validation="required"
            :validation-messages="{
              required: 'La direccion es requerida.',
            }"
          />
          <FormulateInput
            name="apertura"
            label="Horario de apertura"
            type="time"
            validation="required"
            :validation-messages="{
              required: 'La hora de apertura es requerida.',
            }"
          />
          <FormulateInput
            name="cierre"
            label="Horario de cierre"
            type="time"
            validation="required"
            :validation-messages="{
              required: 'La hora de apertura es requerida.',
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

          <FormulateInput name="email" label="Email" type="email" />
        </v-col>

        <v-col>
          <strong>Ubicación:</strong>
          <MapComponent @latitud="lat = $event" @longitud="lng = $event" />
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
            name="telefono"
            label="Teléfono"
            type="text"
            validation="required|number"
            :validation-messages="{
              required: 'El telefono es requerido.',
              number: 'Introduzca un telefono valido',
            }"
          />
          <FormulateInput
            name="tipo_centro"
            label="Tipo de centro"
            type="select"
            :options="{ Ropa: 'ropa', Plasma: 'plasma', Comida: 'comida' }"
            validation="required"
          />
          <FormulateInput
            name="web"
            label="Web"
            type="url"
            validation="required"
            :validation-messages="{
              required: 'La web es requerida.',
            }"
          />
          <FormulateInput
            type="select"
            name="id_municipio"
            label="Municipio"
            :options="municipios"
            validation="required"
            placeholder="Seleccione un municipio"
            :validation-messages="{
              required: 'El municipio es requerido.',
            }"
          />

          <FormulateInput type="submit" label="Enviar" />
        </v-col>
      </v-row>
      <v-row> </v-row>
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
    </v-container>
  </FormulateForm>
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
    };
  },
  methods: {
    handleSubmit() {
      if (this.captchaFlag) {
        if (this.formValues.apertura < this.formValues.cierre) {
          axios
            .post(
              "https://admin-grupo13.proyecto2020.linti.unlp.edu.ar/api/centros/",
              this.formValues,
              {
                headers: {},
              }
            )
            .then((result) => {
              this.$router.push({ name: "Home" });
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

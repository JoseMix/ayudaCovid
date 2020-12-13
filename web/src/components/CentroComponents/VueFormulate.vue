<template>
  <FormulateForm v-model="formValues" @submit="handleSubmit">
    <v-container>
      <v-row>
        <v-col>
          <FormulateInput
            name="nombre"
            label="Nombre del centro"
            validation="required|alpha:latin"
            :validation-messages="{
              required: 'El nombre es requerido.',
              alpha: 'El nombre solo puede contener letras',
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
            error-behavior="live"
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
          <FormulateInput name="latitud" type="hidden" />
          <FormulateInput name="longitud" type="hidden" />
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
          <FormulateInput name="web" label="Web" type="url" />
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
    </v-container>

    <h5>{{ formValues }}</h5>
  </FormulateForm>
</template>

<script>
import axios from "axios";
export default {
  data: () => {
    return {
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
    };
  },
  methods: {
    handleSubmit() {
      if (this.formValues.apertura < this.formValues.cierre) {
        axios
          .post("http://127.0.0.1:5000/api/centros/", this.formValues, {
            headers: {},
          })
          .then((result) => {
            console.log(typeof result);
          });
      } else {
        this.errorDate =
          "La hora de cierre debe ser posterior a la de apertura";
      }
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

<template>
  <FormulateForm v-model="formValues" @submit="handleSubmit">
    <v-container>
      <v-row>
        <v-col>
          <h2>Formulario centros</h2>

          <FormulateInput name="nombre" label="nombre" validation="required" />
          <FormulateInput
            name="direccion"
            label="direccion"
            validation="required"
          />
          <FormulateInput
            name="apertura"
            label="apertura"
            type="time"
            validation="required"
          />
          <FormulateInput
            name="cierre"
            label="cierre"
            type="time"
            validation="required"
          />

          <FormulateInput
            name="email"
            label="email"
            type="email"
            validation="required"
          />
        </v-col>
        <v-col>
          <FormulateInput name="latitud" label="latitud" />
          <FormulateInput name="longitud" label="longitud" />
          <FormulateInput
            name="telefono"
            label="telefono"
            type="number"
            validation="required"
          />
          <FormulateInput
            name="tipo_centro"
            label="tipo de centro"
            type="select"
            :options="{ Ropa: 'ropa', Plasma: 'plasma', Comida: 'comida' }"
            validation="required"
          />
          <FormulateInput
            name="web"
            label="web"
            type="url"
            validation="required"
          />
          <FormulateInput
            type="select"
            name="Municipio"
            :options="municipios"
          />

          <FormulateInput type="submit" label="Enviar" />
        </v-col>
      </v-row>
    </v-container>

    <h3>{{ formValues }}</h3>
    <h3>{{ municipios }}</h3>
  </FormulateForm>
</template>

<!--
<template>
  <v-form v-model="valid">
    <v-container>
      <v-row>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="nombre"
            :rules="nameRules"
            label="Nombre del centro"
            required
          ></v-text-field>
        </v-col>

        <v-col cols="12" md="6">
          <v-text-field
            v-model="direccion"
            :rules="nameRules"
            label="Direccion"
            required
          ></v-text-field>
        </v-col>

        <v-col cols="12" md="6">
          <v-text-field
            v-model="email"
            :rules="emailRules"
            label="E-mail"
            required
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="6">
          <v-text-field
            v-model="phoneNumber"
            :counter="7"
            :error-messages="errors"
            label="Numero de telefono"
            required
          ></v-text-field>
        </v-col>

        <v-col class="d-flex" cols="12" sm="6">
          <v-select :items="items" label="Tipo de centro"></v-select>
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="direccion"
            :rules="nameRules"
            label="Direccion"
            required
          ></v-text-field>
        </v-col>
        <v-col class="d-flex" cols="12" sm="6">
          <v-select
            :items="municipios"
            :item-text="municipios.name"
            name="Municipio"
            v-validate="'required'"
            menu-props="auto"
            hide-details
            label="Select"
            single-line
          />
        </v-col>
      </v-row>
      <h3>{{ municipios }}</h3>
    </v-container>
  </v-form>
</template>
-->
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
    };
  },
  methods: {
    handleSubmit() {
      axios
        .post("http://127.0.0.1:5000/api/centros/", this.formValues, {
          headers: {},
        })
        .then((result) => {
          console.log(result);
        });
    },
  },
  created() {
    axios
      .get(
        "https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?page=1&per_page=140",
        {}
      )
      .then((result) => {
        console.log(result);
        this.municipios = result.data.data.Town;
        //this.municipios = Object.values(this.municipios);
        // this.municipios.forEach((elemento) => {

        //this.nuevinsky[elemento.id] = elemento.name;
        //this.nuevinsky.push({ value: elemento.id, label: elemento.name });

        //this.municipios = this.municipios.map((item) => {
        //  return {
        //    value: item.id,
        //    label: item.name,
        //  };
        //});
      });

    //});
  },

  nameRules() {
    return true;
  },
  emailRules() {
    return true;
  },
};
</script>

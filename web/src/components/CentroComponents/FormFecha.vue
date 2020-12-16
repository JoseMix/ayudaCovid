<template>
  <v-container>
    {{ horarios() }}
    <FormulateForm v-model="formValues">
      <FormulateInput
        name="fecha"
        label="Fecha"
        type="date"
        validation="required"
        :min="fecha_ini"
        :max="fecha_fin"
      />
    </FormulateForm>
    <router-link
      :to="{
        name: 'Turnos',
        params: { id: centro_id, fecha: formValues.fecha },
      }"
    >
      <v-btn depressed color="primary">Sacar Turno</v-btn></router-link
    >
  </v-container>
</template>

<script>
import moment from "moment";
export default {
  data: () => ({
    formValues: {},
    fecha_fin: null,
    fecha_ini: null,
  }),
  props: ["centro_id"],
  methods: {
    horarios() {
      this.fecha_ini = moment().format("YYYY[-]M[-]D");
      console.log( this.fecha_ini);
      this.fecha_fin = moment(this.fecha_ini + " 00:00:00")
        .add(2, "days")
        .format("YYYY[-]M[-]D");
      console.log('fecha fin',this.fecha_fin)  
    },
  },
};
</script>

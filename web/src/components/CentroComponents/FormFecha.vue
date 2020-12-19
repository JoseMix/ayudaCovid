<template>
  <v-container>
    {{ horarios() }}
    <FormulateForm v-model="formValues" @submit="sacarTurno">
      <FormulateInput
        name="fecha"
        label="Fecha"
        type="date"
        validation="required"
        :min="fecha_ini"
        :max="fecha_fin"
      />
    <FormulateInput
      type="submit"
      label="Register"
      /> 
    </FormulateForm>

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
  props: ["centro_id","nombre_centro"],
  methods: {
    sacarTurno() {
        this.$router.push({ name: "Turnos" , params: { id: this.centro_id, fecha: this.formValues.fecha, nombre: this.nombre_centro }});
    },
    horarios() {
      this.fecha_ini = moment().format("YYYY[-]M[-]D");
      this.fecha_fin = moment(this.fecha_ini + " 00:00:00")
        .add(2, "days")
        .format("YYYY[-]M[-]D");
    },

  },
};
</script>

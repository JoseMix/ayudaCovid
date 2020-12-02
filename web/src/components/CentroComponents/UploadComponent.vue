<template>
  <div>
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group
        id="input-group-2"
        label="Nombre del centro:"
        label-for="input-2"
      >
        <b-form-input
          id="input-2"
          v-model="form.nombre"
          required
          placeholder="Introduzca nombre del centro"
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="input-group-1"
        label="Direccion de email:"
        label-for="input-1"
        description="Tu email no se compartirá con terceros"
      >
        <b-form-input
          id="input-1"
          v-model="form.email"
          type="email"
          required
          placeholder="Introduzca email"
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-3" label="Telefono:" label-for="input-2">
        <b-form-input
          id="input-2"
          v-model="form.telefono"
          required
          placeholder="Introduzca numero de telefono"
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="input-group-4"
        label="Tipo de centro:"
        label-for="input-3"
      >
        <b-form-select
          id="input-3"
          v-model="form.tipo"
          :options="tipos"
          required
        ></b-form-select>
      </b-form-group>

      <b-form-group id="input-group-4">
        <b-form-checkbox-group v-model="form.checked" id="checkboxes-4">
          <b-form-checkbox value="me">Check me out</b-form-checkbox>
          <b-form-checkbox value="that">Check that out</b-form-checkbox>
        </b-form-checkbox-group>
      </b-form-group>

      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
    <b-card class="mt-3" header="Form Data Result">
      <pre class="m-0">{{ form }}</pre>
    </b-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        email: "",
        name: "",
        food: null,
        checked: [],
      },
      tipos: [
        { text: "Seleccione uno", value: null },
        "Ropa",
        "Plasma",
        "Sangre",
        "Comida",
      ],
      show: true,
    };
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      alert(JSON.stringify(this.form));
    },
    onReset(evt) {
      evt.preventDefault();
      // Reset our form values
      this.form.email = "";
      this.form.name = "";
      this.form.food = null;
      this.form.checked = [];
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
  },
};
</script>

<template>
  <div>
    <FormulateForm v-model="formValues" @submit="llamarAlOtroCOmponente">
      <v-container>
        <v-row>
          <v-col>
            <h2>Formulario Turnos</h2>
            <FormulateInput
              name="hora"
              label="Hora"
              type="time"
              validation="required"
            />
            <FormulateInput
              name="email"
              label="Email"
              type="text"
              validation="required"
            />
            <FormulateInput
              name="telefono"
              label="Telefono"
              type="text"
              validation="required"
            />
            <FormulateInput type="submit" label="Enviar" />
          </v-col>
        </v-row>
      </v-container>
      <h3>{{ formValues }}</h3>
    </FormulateForm>
  </div>
</template>
<script></script>

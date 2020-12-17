<template>
  <v-container fluid ma-0 px-6 fill-height>
    <v-row>
      <v-col align="center" justify="center"><br>
        <PieChart></PieChart>
      </v-col>
      <v-col align="center" justify="center">
          <RingType/>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6" align="center" justify="center"> 
        <Bar/>        
      </v-col>
    </v-row>  
    <v-row>
      <v-col cols="6" align="center" justify="center"> 
        <LineChart></LineChart>        
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6" align="center" justify="center"> 
        <Bar/>        
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import LineChart from "./LineChart.vue";
import PieChart from "./PieChart.vue";
import RingType from "./RingType.vue";
import Bar from "./Bar"

export default {
  name: "Estadisticas",
  components: {
    PieChart,
    LineChart,
    RingType,
    Bar,
  },
  data: () => ({}),
};
</script>

<style></style>

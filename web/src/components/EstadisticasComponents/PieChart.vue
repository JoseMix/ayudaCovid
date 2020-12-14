<template>
  <div>
    <ve-pie :data="chartData"></ve-pie>
  </div>
</template>

<script>
import VePie from "v-charts/lib/pie.common";
export default {
  components: { VePie },
  data() {
    return {
      chartData: {
        columns: ["date", "cost", "profit"],
        rows: [
          { date: "01/01", cost: 123, profit: 3 },
          { date: "01/02", cost: 1223, profit: 6 },
          { date: "01/03", cost: 2123, profit: 90 },
          { date: "01/04", cost: 4123, profit: 12 },
          { date: "01/05", cost: 3123, profit: 15 },
          { date: "01/06", cost: 7123, profit: 20 },
        ],
      },
    };
  },
};
</script>

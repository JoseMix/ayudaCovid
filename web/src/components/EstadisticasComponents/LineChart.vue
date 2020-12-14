<template>
  <div>
    <ve-waterfall :data="chartData"></ve-waterfall>
  </div>
</template>

<script>
import VeWaterfall from "v-charts/lib/waterfall.common";
export default {
  components: { VeWaterfall },
  data() {
    return {
      chartData: {
        columns: ["action", "time"],
        rows: [
          { action: "eat", time: 4 },
          { action: "sleep", time: 10 },
          { action: "learn", time: 5 },
        ],
      },
    };
  },
};
</script>

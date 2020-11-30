import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
//import Centros from "../views/Centro.vue";
//import Turnos from "../views/Turno.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  } /*,
  {
    path: "/centros",
    name: "Centros",
    component: Centros,
  },
  {
    path: "/turnos",
    name: "Turnos",
    component: Turnos,
  },*/
];

const router = new VueRouter({
  routes
});

export default router;

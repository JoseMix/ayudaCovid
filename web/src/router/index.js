import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Centros from "../views/Centros.vue";
import Turnos from "../views/Turnos.vue";
import Carga_centro from "../views/Carga_centro.vue";
import About from "../views/About.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/centros",
    name: "Centros",
    component: Centros,
  },
  {
    path: "/turnos/:id/:fecha",
    name: "Turnos",
    component: Turnos,
  },
  {
    path: "/carga-centro",
    name: "Carga-centro",
    component: Carga_centro,
  },
  {
    path: "/about",
    name: "About",
    component: About,
  },
];
const router = new VueRouter({
  mode: "history",
  routes,
});

export default router;

import { LMap, LPolyline, LTileLayer, LCircle } from '@vue-leaflet/vue-leaflet';
import { defineNuxtPlugin } from '#app';

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.component('LMap', LMap);
  nuxtApp.vueApp.component('LPolyline', LPolyline);
  nuxtApp.vueApp.component('LTileLayer', LTileLayer);
  nuxtApp.vueApp.component('LCircle', LCircle);
});

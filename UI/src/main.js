import { createApp } from 'vue';
import App from './App.vue';
import router from './router/index.ts'; // Importa el router

createApp(App)
  .use(router) // Usa el router
  .mount('#app');

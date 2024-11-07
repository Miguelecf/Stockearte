import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '../components/MainPage.vue';
import UserManagement from '../components/UserManagement.vue';
import StoreManagement from '../components/StoreManagement.vue';
import UserLogin from '../components/UserLogin.vue';

const routes = [
  {
    path: '/',
    name: 'UserLogin',
    component: UserLogin,
  },
  {
    path: '/main',
    name: 'MainPage',
    component: MainPage,
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('auth_token'); // Verifica si existe el token
      if (!token) {
        next('/'); // Si no hay token, redirige al login
      } else {
        next(); // Si hay token, permite el acceso
      }
    }
  },
  {
    path: '/user-management',
    name: 'UserManagement',
    component: UserManagement,
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        next('/'); // Redirige al login si no hay token
      } else {
        next();
      }
    }
  },
  {
    path: '/store-management',
    name: 'StoreManagement',
    component: StoreManagement,
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        next('/'); // Redirige al login si no hay token
      } else {
        next();
      }
    }
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Verificación global antes de cada navegación
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('auth_token');
  if (to.name !== 'UserLogin' && !token) {
    next('/'); // Si no está autenticado, redirige al login
  } else {
    next();
  }
});

export default router;

// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '../components/MainPage.vue';
import UserManagement from '../components/UserManagement.vue';
import StoreManagement from '../components/StoreManagement.vue';
import UserLogin from '../components/UserLogin.vue';

const routes = [

  {
    path:'/',
    name:'UserLogin',
    component: UserLogin,
  },

  {
    path: '/main',
    name: 'MainPage',
    component: MainPage,
  },
  {
    path: '/user-management',
    name: 'UserManagement',
    component: UserManagement,
  },
  {
    path: '/store-management',
    name: 'StoreManagement',
    component: StoreManagement,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

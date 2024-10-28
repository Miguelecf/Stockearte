// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '../components/MainPage.vue';
import UserManagement from '../components/UserManagement.vue';
import StoreManagement from '../components/StoreManagement.vue';

const routes = [
  {
    path: '/',
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

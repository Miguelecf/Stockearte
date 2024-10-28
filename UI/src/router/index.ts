// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '../components/MainPage.vue';
import UserManagement from '../components/UserManagement.vue';

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
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

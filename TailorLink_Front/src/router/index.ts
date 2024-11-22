import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import LoginView from '../views/Login.vue';
import JoinView from '../views/Join.vue'; // Join.vue 임포트

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/join', name: 'join', component: JoinView }, // 회원가입 경로 추가
  { path: '/how-to', name: 'how-to', component: () => import('../views/HowToView.vue') },
  { path: '/experience', name: 'experience', component: () => import('../views/ExperienceView.vue') },
  { path: '/support', name: 'support', component: () => import('../views/SupportView.vue') },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;

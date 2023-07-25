import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ChatView from '../views/ChatView.vue'
import isLoggedIn from '../services/auth.service';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: false }
    },
    {
      path: '/document/:docId/chat/:chatId',
      props: true,
      name: 'chat',
      component: ChatView,
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  
  if (requiresAuth) {
    const { is_authenticated, user } = await isLoggedIn.isLoggedIn();
    if (!is_authenticated) {
      next('/');
    } else {
      next();
    }
  } else {
    next();
  }
});


export default router

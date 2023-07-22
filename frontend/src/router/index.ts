import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
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
      path: '/about',
      name: 'about',
      meta: { requiresAuth: true },
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
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

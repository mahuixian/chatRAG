import Vue from 'vue';
import Router from 'vue-router';
import Login from '@/views/MainLogin.vue';
import MainLayout from '@/views/MainLayout.vue';

Vue.use(Router);

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/',
      component: MainLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'Main',
          component: () => import('@/components/AppContent.vue')
        }
      ]
    },
    {
      path: '/',
      redirect: '/login' //默认跳转到登录页面
    }
  ]
});

// 合并守卫
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token'); // 检查 token 是否存在

  console.log(`Navigating to: ${to.path}, Authenticated: ${isAuthenticated}`);
  console.log(`username: ${localStorage.getItem('username')}`);

  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next({ name: 'Login' }); // 如果需要认证并且未登录，跳转到登录页面
  } else {
    next(); // 否则，继续
  }
});

export default router;



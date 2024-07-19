

// import Vue from 'vue';
// import Router from 'vue-router';
// import Login from '@/views/Login.vue';
// import App from '@/views/App.vue';

// Vue.use(Router);

// const router = new Router({
//   mode: 'history',
//   routes: [
//     {
//       path: '/login',
//       name: 'Login',
//       component: Login
//     },
//     {
//       path: '/',
//       name: 'App',
//       component: App,
//       meta: { requiresAuth: true }
//     }
//   ]
// });

// // 合并守卫
// router.beforeEach((to, from, next) => {

//   console.log("111111111111111111111111111111111");
//   const isAuthenticated = !!localStorage.getItem('token');
//   console.log('Navigating to:', to.path);  // 记录当前路径
//   console.log('isAuthenticated:', isAuthenticated);  // 记录认证状态

//   if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
//     console.log('Redirecting to login');  // 记录重定向
//     next({ name: 'Login' });
//   } else {
//     next();
//   }
// });

// export default router;


import Vue from 'vue';
import Router from 'vue-router';
import Login from '@/views/Login.vue';
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
          name: 'Content',
          component: () => import('@/components/Content.vue')
        }
      ]
    }
  ]
});

// 合并守卫
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token');
  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

export default router;



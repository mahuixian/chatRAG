import Vue from 'vue';
import ElementUI from 'element-ui';
import App from './views/App.vue';
import 'element-ui/lib/theme-chalk/index.css';
import "./assets/css/style.css";
import { EventBus } from './bus';
import router from './router/router';

Vue.config.productionTip = false;

Vue.prototype.$bus = EventBus;

Vue.use(ElementUI);

new Vue({
  router,
  render: h => h(App)
}).$mount('#app');


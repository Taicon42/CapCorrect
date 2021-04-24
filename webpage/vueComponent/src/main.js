import { createApp } from 'vue'
import App from './Prototype.vue'
import store from './store'
import router from './router'

createApp(App).use(router).use(store).mount('#app')

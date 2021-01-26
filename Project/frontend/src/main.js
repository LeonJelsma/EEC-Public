import Vue from 'vue'
import App from './App.vue'
import Vuex from 'vuex'
import Buefy from 'buefy'
import 'buefy/dist/buefy.css'

Vue.config.productionTip = false

Vue.use(Vuex)
Vue.use(Buefy)

const store = {
    state: {
    },
    methods: {
    }
}

new Vue({
    render: h => h(App),
    store: store
}).$mount('#app')

import Vue from 'vue';
import store from './../../store';

export default () => {
  if (store.state.auth.authenticated) {
    Vue.$http.post('/account/logout/');

    store.dispatch('auth/logout');
    Vue.router.push({
      name: 'login.index',
    });
  }
};

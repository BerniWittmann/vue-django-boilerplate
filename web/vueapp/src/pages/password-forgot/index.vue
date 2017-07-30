<template>
  <v-layout>
    <v-panel contextual-style="primary">
      <h1 class="panel-title" slot="heading">
        Forgot Password?
      </h1>
      <div slot="body">
        <form @submit.prevent="requestPassword(user)">
          <div class="form-group">
            <div class="input-group">
              <div class="input-group-addon">
                <i class="fa fa-envelope fa-fw"></i>
              </div>
              <input
                v-model="user.email"
                type="email"
                placeholder="Email"
                class="form-control"
              >
            </div>
          </div>
          <div class="form-group">
            <button class="btn btn-primary">
              Reset Password
            </button>
          </div>
        </form>
      </div>
      <div slot="footer">
        No account?
        <router-link :to="{ name: 'register.index' }">Register</router-link>
      </div>
    </v-panel>
  </v-layout>
</template>

<script>
  /* ============
   * Password forgot Index Page
   * ============
   *
   * Page where the user can request a new Password.
   */
  import authService from '@/services/auth';

  export default {
    data() {
      return {
        user: {
          email: null,
        },
      };
    },

    methods: {
      requestPassword(user) {
        authService.requestPassword(user);
      },
    },

    components: {
      VLayout: require('@/layouts/minimal.vue'),
      VPanel: require('@/components/panel.vue'),
    },
  };
</script>

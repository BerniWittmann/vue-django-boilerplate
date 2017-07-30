<template>
  <v-layout>
    <v-panel contextual-style="primary">
      <h1 class="panel-title" slot="heading">
        Reset Password
      </h1>
      <div slot="body">
        <form @submit.prevent="resetPassword(user)">
          <div class="form-group">
            <div class="input-group">
              <div class="input-group-addon">
                <i class="fa fa-lock fa-fw"></i>
              </div>
              <input
                v-model="user.password"
                type="password"
                placeholder="Password"
                class="form-control"
              >
            </div>
          </div>
          <div class="form-group">
            <div class="input-group">
              <div class="input-group-addon">
                <i class="fa fa-lock fa-fw"></i>
              </div>
              <input
                      v-model="user.passwordConfirm"
                      type="password"
                      placeholder="Confirm Password"
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
   * Login Index Page
   * ============
   *
   * Page where the user can login.
   */
  import authService from '@/services/auth';

  export default {
    data() {
      return {
        user: {
          code: null,
          password: null,
          passwordConfirm: null,
        },
      };
    },

    beforeMount() {
      authService.checkResetPasswordCode(this.$route.query.code);
      this.user.code = this.$route.query.code;
    },

    methods: {
      resetPassword(user) {
        authService.resetPassword(user);
      },
    },

    components: {
      VLayout: require('@/layouts/minimal.vue'),
      VPanel: require('@/components/panel.vue'),
    },
  };
</script>

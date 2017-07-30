<template>
    <v-layout>
        <v-panel contextual-style="primary">
            <h1 class="panel-title" slot="heading">
                Verify E-Mail
            </h1>
            <div slot="body">
                We are currently verifying your e-mail address
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
 * Email Verify Index Page
 * ============
 *
 * Page where the user can verify the email.
 */
import authService from '@/services/auth';

export default {
  beforeMount() {
    authService.verifyEmail(this.$route.query.code);
  },

  components: {
    VLayout: require('@/layouts/minimal.vue'),
    VPanel: require('@/components/panel.vue'),
  },
};
</script>

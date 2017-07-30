import Vue from 'vue';

// When the request succeeds
const success = () => {
  Vue.router.push({
    name: 'login.index',
  });
};

// When the request fails
const failed = () => {
};

export default (user) => {
  /*
   * Normally you would perform an AJAX-request.
   * But to get the example working, the data is hardcoded.
   *
   * With the include REST-client Axios, you can do something like this:
   * Vue.$http.post('/auth/login', user)
   *   .then((response) => {
   *     success(response);
   *   })
   *   .catch((error) => {
   *     failed(error);
   *   });
   */
  Vue.$http.post('/account/password/reset/verified/', user)
      .then(() => {
        success();
      }).catch((error) => {
        failed(error);
      });
};

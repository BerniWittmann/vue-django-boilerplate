import Vue from 'vue';

// When the request succeeds
const success = () => {
};

// When the request fails
const failed = () => {
  Vue.router.push({
    name: 'register.index',
  });
};

export default (code) => {
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
  Vue.$http.get('account/password/reset/verify/', { params: { code } })
      .then(success)
      .catch(failed);
};

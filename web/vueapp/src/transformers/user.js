/* ============
 * User Transformer
 * ============
 *
 * The transformer for the User.
 */

import Transformer from './transformer';

export default class UserTransformer extends Transformer {
  /**
   * Method used to transform a fetched user
   *
   * @param user The fetched user
   *
   * @returns {Object} The transformed user
   */
  static fetch(user) {
    return user;
  }

  /**
   * Method used to transform a send user
   *
   * @param user The user to be send
   *
   * @returns {Object} The transformed user
   */
  static send(user) {
    return {
      email: user.email,
      first_name: user.firstName,
      last_name: user.lastName,
      password: user.password,
    };
  }
}

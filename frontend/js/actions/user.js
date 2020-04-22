import axios from 'axios';

import { GET_USER_DATA } from '.';

// action creators
export function getUserData() {
  console.log('inside getUserData');
  const url = window.Urls['api:userAuthenticated']();
  const user = axios
    .get(url)
    .then((res) => res.data)
    .catch((err) => {
      return new Error(err);
    });
  // since I'm using the middleware, it waits until "battle" gets the data to dispatch the action
  return {
    type: GET_USER_DATA,
    payload: user,
  };
}

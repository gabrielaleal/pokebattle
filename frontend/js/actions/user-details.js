import axios from 'axios';

import { GET_USER_DATA } from '.';

const getUserDataSuccess = (user) => ({
  type: GET_USER_DATA,
  payload: user,
});

// action creators
const getUserData = () => {
  return (dispatch) => {
    const url = window.Urls['api:userAuthenticated']();
    axios
      .get(url)
      .then((res) => {
        return dispatch(getUserDataSuccess(res.data));
      })
      .catch((err) => {
        throw new Error(err);
      });
  };
};

export default getUserData;

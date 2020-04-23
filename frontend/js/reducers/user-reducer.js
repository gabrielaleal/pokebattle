import { GET_USER_DATA } from '../actions';

const defaultState = {
  user: {},
};

const user = (state = defaultState, action) => {
  switch (action.type) {
    case GET_USER_DATA:
      return {
        ...state,
        data: action.payload,
      };
    default:
      return state;
  }
};

export default user;

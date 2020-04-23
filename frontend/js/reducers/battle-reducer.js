import { GET_BATTLE_DETAILS } from '../actions';

const defaultState = {
  battle: {},
  isLoading: true,
};

const battle = (state = defaultState, action) => {
  // take the actual state and update it based on the action
  switch (action.type) {
    case GET_BATTLE_DETAILS:
      return {
        ...state,
        battle: action.payload,
        isLoading: false,
      };
    default:
      return state;
  }
};

export default battle;

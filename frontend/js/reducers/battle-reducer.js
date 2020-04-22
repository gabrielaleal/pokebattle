/* eslint-disable sonarjs/no-small-switch */
import { GET_BATTLE_DETAILS } from '../actions';

const defaultState = {
  battle: {},
  isLoading: true,
};

const battle = (action, state = defaultState) => {
  // take the actual state and update it based on the action
  switch (action.type) {
    case GET_BATTLE_DETAILS:
      return {
        ...state,
        battle: action.payload.results,
        isLoading: false,
      };
    default:
      return state;
  }
};

export default battle;

import { GET_BATTLE_DETAILS, GET_SETTLED_BATTLES_LIST, GET_ONGOING_BATTLES_LIST } from '../actions';

const defaultState = {
  battle: {},
  settledBattlesList: {},
  ongoingBattlesList: {},
  isLoading: true,
};

const battle = (state = defaultState, action) => {
  switch (action.type) {
    case GET_BATTLE_DETAILS:
      return {
        ...state,
        battle: action.payload,
        isLoading: false,
      };
    case GET_SETTLED_BATTLES_LIST:
      return {
        ...state,
        settledBattlesList: action.payload,
        isLoading: false,
      };
    case GET_ONGOING_BATTLES_LIST:
      return {
        ...state,
        ongoingBattlesList: action.payload,
        isLoading: false,
      };
    default:
      return state;
  }
};

export default battle;

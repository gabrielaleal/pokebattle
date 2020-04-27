import { GET_BATTLE_DETAILS, GET_SETTLED_BATTLES_LIST, GET_ONGOING_BATTLES_LIST } from '../actions';

const defaultState = {
  battle: {},
  settledBattlesList: [],
  ongoingBattlesList: [],
  loading: {
    list: true,
    details: true,
  },
};

const battle = (state = defaultState, action) => {
  switch (action.type) {
    case GET_BATTLE_DETAILS:
      return {
        ...state,
        battle: action.payload,
        loading: toggleLoading(state.loading, 'details'),
      };
    case GET_SETTLED_BATTLES_LIST:
      return {
        ...state,
        settledBattlesList: action.payload,
        loading: toggleLoading(state.loading, 'list'),
      };
    case GET_ONGOING_BATTLES_LIST:
      return {
        ...state,
        ongoingBattlesList: action.payload,
        loading: toggleLoading(state.loading, 'list'),
      };
    default:
      return state;
  }
};

const toggleLoading = (loading, section) => ({
  ...loading,
  [section]: !loading.section,
});

export default battle;

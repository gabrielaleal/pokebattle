import { GET_BATTLE_DETAILS } from '../actions';

const defaultState = {
  battle: {},
  loading: {
    list: true,
    details: true,
  },
};

const battle = (state = defaultState, action) => {
  // take the actual state and update it based on the action
  switch (action.type) {
    case GET_BATTLE_DETAILS:
      return {
        ...state,
        battle: action.payload,
        loading: toggleLoading(state.loading, 'details'),
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

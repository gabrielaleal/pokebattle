import axios from 'axios';

import { GET_SETTLED_BATTLES_LIST, GET_ONGOING_BATTLES_LIST } from '.';

const getSettledBattlesSuccess = (battles) => ({
  type: GET_SETTLED_BATTLES_LIST,
  payload: battles,
});

const getOngoingBattlesSuccess = (battles) => ({
  type: GET_ONGOING_BATTLES_LIST,
  payload: battles,
});

// action creators
const getSettledBattlesList = () => {
  return (dispatch) => {
    const url = window.Urls['api:settledBattlesList']();
    axios
      .get(url)
      .then((res) => {
        return dispatch(getSettledBattlesSuccess(res.data));
      })
      .catch((err) => {
        throw new Error(err);
      });
  };
};

const getOngoingBattlesList = () => {
  return (dispatch) => {
    const url = window.Urls['api:ongoingBattlesList']();
    axios
      .get(url)
      .then((res) => {
        return dispatch(getOngoingBattlesSuccess(res.data));
      })
      .catch((err) => {
        throw new Error(err);
      });
  };
};

export { getSettledBattlesList, getOngoingBattlesList };

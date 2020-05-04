import axios from 'axios';
import { normalize } from 'normalizr';

import { battleListSchema } from '../utils/schema';

import { GET_SETTLED_BATTLES_LIST, GET_ONGOING_BATTLES_LIST } from '.';

const getSettledBattlesSuccess = (battles, entities) => ({
  type: GET_SETTLED_BATTLES_LIST,
  battles,
  entities,
});

const getOngoingBattlesSuccess = (battles, entities) => ({
  type: GET_ONGOING_BATTLES_LIST,
  battles,
  entities,
});

// action creators
const getSettledBattlesList = () => {
  return (dispatch) => {
    const url = window.Urls['api:settledBattlesList']();
    axios
      .get(url)
      .then((res) => {
        const normalizedList = normalize(res.data, battleListSchema);
        const { users, pokemon, battle } = normalizedList.entities;
        const battles = normalizedList.result;
        return dispatch(getSettledBattlesSuccess(battles, { users, pokemon, battle }));
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
        const normalizedList = normalize(res.data, battleListSchema);
        const { users, battle } = normalizedList.entities;
        const battles = normalizedList.result;
        return dispatch(getOngoingBattlesSuccess(battles, { users, battle }));
      })
      .catch((err) => {
        throw new Error(err);
      });
  };
};

export { getSettledBattlesList, getOngoingBattlesList };

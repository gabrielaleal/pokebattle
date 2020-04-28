import axios from 'axios';
import { normalize } from 'normalizr';

import { battle as battleSchema } from '../utils/schema';

import { GET_BATTLE_DETAILS } from '.';

const getBattleDetailsSuccess = (battle, entities) => ({
  type: GET_BATTLE_DETAILS,
  battle,
  entities,
});

// action creators
const getBattleDetails = (battlePk) => {
  return (dispatch) => {
    const url = window.Urls['api:battleDetail'](battlePk);
    axios
      .get(url)
      .then((res) => {
        const normalizedBattle = normalize(res.data, battleSchema);
        const { pokemon, users } = normalizedBattle.entities;
        const battle = normalizedBattle.entities.battle[normalizedBattle.result];
        return dispatch(getBattleDetailsSuccess(battle, { pokemon, users }));
      })
      .catch((err) => {
        throw new Error(err);
      });
  };
};

export default getBattleDetails;

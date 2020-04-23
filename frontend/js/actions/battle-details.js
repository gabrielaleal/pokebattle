import axios from 'axios';

import { GET_BATTLE_DETAILS } from '.';

// action creators
export function getBattleDetails(battlePk) {
  const url = window.Urls['api:battleDetail'](battlePk);
  const battle = axios
    .get(url)
    .then((res) => res.data)
    .catch((err) => new Error(err));
  // since I'm using the middleware, it waits until "battle" gets the data to dispatch the action
  return {
    type: GET_BATTLE_DETAILS,
    payload: battle,
  };
}

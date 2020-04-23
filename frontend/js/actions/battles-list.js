import axios from 'axios';

import { GET_SETTLED_BATTLES_LIST, GET_ONGOING_BATTLES_LIST } from '.';

// action creators
export function getSettledBattlesList() {
  const url = window.Urls['api:settledBattlesList']();
  const settledBattles = axios
    .get(url)
    .then((res) => res.data)
    .catch((err) => new Error(err));
  // since I'm using the middleware, it waits until "battle" gets the data to dispatch the action
  return {
    type: GET_SETTLED_BATTLES_LIST,
    payload: settledBattles,
  };
}

export function getOngoingBattlesList() {
  const url = window.Urls['api:ongoingBattlesList']();
  const ongoingBattles = axios
    .get(url)
    .then((res) => res.data)
    .catch((err) => new Error(err));
  // since I'm using the middleware, it waits until "battle" gets the data to dispatch the action
  return {
    type: GET_ONGOING_BATTLES_LIST,
    payload: ongoingBattles,
  };
}

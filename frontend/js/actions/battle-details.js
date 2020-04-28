import axios from 'axios';
// import { normalize } from 'normalizr';

// import { battle as battleSchema } from '../utils/schema';

import { GET_BATTLE_DETAILS } from '.';

const getBattleDetailsSuccess = (battle) => ({
  type: GET_BATTLE_DETAILS,
  payload: battle,
});

// action creators
const getBattleDetails = (battlePk) => {
  return (dispatch) => {
    const url = window.Urls['api:battleDetail'](battlePk);
    axios
      .get(url)
      .then((res) => {
        // const normalizedBattle = normalize(res.data, battleSchema);
        // console.log('-> normalizedBattle', normalizedBattle);
        return dispatch(getBattleDetailsSuccess(res.data));
      })
      .catch((err) => {
        throw new Error(err);
      });
  };
};

export default getBattleDetails;

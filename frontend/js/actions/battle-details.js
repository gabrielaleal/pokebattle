import axios from 'axios';

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
        return dispatch(getBattleDetailsSuccess(res.data));
      })
      .catch((err) => {
        throw new Error(err);
      });
  };
};

export default getBattleDetails;

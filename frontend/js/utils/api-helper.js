import axios from 'axios';

const getOpponentsFromAPI = () => {
  const url = window.Urls['api:opponentsList']();
  return axios.get(url).then((res) => {
    return res.data;
  });
};

export default getOpponentsFromAPI;

import axios from 'axios';

const getOpponentsFromAPI = () => {
  const url = window.Urls['api:opponentsList']();
  return axios.get(url).then((res) => {
    return res.data;
  });
};

const getPokemonFromAPI = () => {
  const url = window.Urls['api:pokemonList']();
  return axios.get(url).then((res) => {
    return res.data;
  });
};

const postOnAPI = (url, data) => {
  const headers = {
    'X-CSRFToken': getCookie('csrftoken'),
  };
  console.log('inside post on api');
  return axios.post(url, data, { headers });
};

const getCookie = (cname) => {
  const name = `${cname}=`;
  const decodedCookie = decodeURIComponent(document.cookie);
  const ca = decodedCookie.split(';');
  for (let c of ca) {
    while (c.charAt(0) === ' ') {
      c = c.slice(1);
    }
    if (c.indexOf(name) === 0) {
      return c.slice(name.length, c.length);
    }
  }
  return '';
};

export { getOpponentsFromAPI, getPokemonFromAPI, postOnAPI, getCookie };

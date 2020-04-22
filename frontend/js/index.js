import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import promiseMiddleware from 'redux-promise';

import App from './App';
import reducers from './reducers';

import './bootstrap-includes';
import '../sass/style.scss';

// this returns a high-order function
const store = applyMiddleware(promiseMiddleware)(createStore);

ReactDOM.render(
  <Provider store={store(reducers)}>
    <App />
  </Provider>,
  document.getElementById('PokeBattleContainer')
);

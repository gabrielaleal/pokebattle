import React from 'react';
import { hot } from 'react-hot-loader/root';
import { BrowserRouter, Switch } from 'react-router-dom';

import Navbar from './components/navbar';
import BattleDetails from './pages/battle-details';

const App = () => (
  <BrowserRouter>
    <div>
      <Navbar />
      <Switch>
        <BattleDetails path="/battles/:pk/" />
      </Switch>
    </div>
  </BrowserRouter>
);

export default hot(App);

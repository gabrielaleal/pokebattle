import React from 'react';
import { hot } from 'react-hot-loader/root';
import { BrowserRouter, Switch } from 'react-router-dom';

import Navbar from './components/navbar';
import BattleDetails from './pages/battle-details';

const App = () => (
  <BrowserRouter>
    <div>
      <Navbar />
      <div className="block-body">
        <Switch>
          <BattleDetails path="/battles/:pk/" />
        </Switch>
      </div>
    </div>
  </BrowserRouter>
);

export default hot(App);

import axios from 'axios';
import React from 'react';
import { hot } from 'react-hot-loader/root';
import { BrowserRouter, Switch } from 'react-router-dom';

import Navbar from './components/navbar';
import BattleDetails from './pages/battle-details';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      user: {},
    };
  }

  componentDidMount() {
    const url = window.Urls['api:userAuthenticated']();
    axios.get(url).then((res) => {
      this.setState({ user: res.data });
      return res.data;
    });
  }

  render() {
    const { user } = this.state;

    return (
      <BrowserRouter>
        <div>
          <Navbar user={user} />
          <div className="block-body">
            <Switch>
              <BattleDetails path="/battles/:pk/" user={user} />
            </Switch>
          </div>
        </div>
      </BrowserRouter>
    );
  }
}

export default hot(App);

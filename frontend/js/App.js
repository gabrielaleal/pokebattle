import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import { BrowserRouter, Switch } from 'react-router-dom';

import getUserData from './actions/user-details';
import Loading from './components/Loading';
import Navbar from './components/Navbar';
import BattleDetails from './pages/BattleDetails';
import CreateBattle from './pages/CreateBattle';
import OngoingBattlesList from './pages/OngoingBattlesList';
import SelectOpponentTeam from './pages/SelectOpponentTeam';
import SettledBattlesList from './pages/SettledBattlesList';

class App extends React.Component {
  componentDidMount() {
    const { getUserData } = this.props;
    getUserData();
  }

  render() {
    const { user } = this.props;

    if (!user) {
      return <Loading />;
    }

    return (
      <BrowserRouter>
        <div>
          <Navbar user={user} />
          <div className="block-body">
            <Switch>
              <CreateBattle path="/battles/create/" />
              <SettledBattlesList path="/battles/settled/" />
              <OngoingBattlesList path="/battles/ongoing/" />
              <SelectOpponentTeam path="/battles/select-team/:pk/" />
              <BattleDetails path="/battles/:pk/" />
            </Switch>
          </div>
        </div>
      </BrowserRouter>
    );
  }
}

App.propTypes = {
  getUserData: PropTypes.func.isRequired,
  user: PropTypes.object.isRequired,
};

const mapStateToProps = (state) => ({
  user: state.user.data,
});

const mapDispatchToProps = {
  getUserData,
};

export default connect(mapStateToProps, mapDispatchToProps)(App);

import moment from 'moment';
import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

import { getOngoingBattlesList } from '../actions/battles-list';
import Loading from '../components/loading';
import PageTitle from '../components/title';

function BattleWaitingForMeItem({ battle }) {
  return (
    <Link to={window.Urls['battles:battleDetail'](battle.id)}>
      <div className="list-item">
        <div>
          <h6 className="pokemon-font">Battle #{battle.id}</h6>
          <div>
            <span className="list-attribute">{battle.creator.email}</span> challenged you on{' '}
            {moment(battle.timestamp).format('L')} at {moment(battle.timestamp).format('LT')}. Fight
            back!
          </div>
        </div>
      </div>
    </Link>
  );
}

function BattleWaitingForMyOpponentItem({ battle }) {
  return (
    <Link to={window.Urls['battles:battleDetail'](battle.id)}>
      <div className="list-item">
        <div>
          <h6 className="pokemon-font">Battle #{battle.id}</h6>
          <div>
            <span className="list-attribute">Players</span> {battle.creator.email} VS{' '}
            {battle.opponent.email}
          </div>
          <div>
            <span className="list-attribute">Battle created on</span>{' '}
            {moment(battle.timestamp).format('L')} at {moment(battle.timestamp).format('LT')}
          </div>
        </div>
      </div>
    </Link>
  );
}

class OngoingBattlesList extends React.Component {
  componentDidMount() {
    const { getOngoingBattlesList } = this.props;
    getOngoingBattlesList();
  }

  render() {
    const { battles, user } = this.props;

    const battlesWaitingForMe = battles.filter((battle) => battle.opponent.email === user.email);
    const battlesWaitingForOpponent = battles.filter(
      (battle) => battle.creator.email === user.email
    );

    if (!battles) {
      return <Loading />;
    }

    return (
      <div className="pk-container ongoing-battles">
        <PageTitle title="Ongoing Battles" />
        <div className="content">
          <div className="battle-list">
            <h4>Battles waiting for me</h4>
            {battlesWaitingForMe.length === 0 ? (
              <div className="no-battles">
                <div>Ops, there are no battles yet!</div>
              </div>
            ) : (
              <div />
            )}
            {Object.keys(battlesWaitingForMe).map((key) => (
              <BattleWaitingForMeItem
                key={battlesWaitingForMe[key].id}
                battle={battlesWaitingForMe[key]}
              />
            ))}
          </div>
          <div className="battle-list">
            <h4>Battles waiting for my opponent</h4>
            {battlesWaitingForOpponent.length === 0 ? (
              <div className="no-battles">
                <div>Ops, there are no battles yet!</div>
              </div>
            ) : (
              <div />
            )}
            {Object.keys(battlesWaitingForOpponent).map((key) => (
              <BattleWaitingForMyOpponentItem
                key={battlesWaitingForOpponent[key].id}
                battle={battlesWaitingForOpponent[key]}
              />
            ))}
          </div>
        </div>
      </div>
    );
  }
}

OngoingBattlesList.propTypes = {
  user: PropTypes.object.isRequired,
  battles: PropTypes.array,
  getOngoingBattlesList: PropTypes.func,
};

BattleWaitingForMeItem.propTypes = {
  battle: PropTypes.object,
};

BattleWaitingForMyOpponentItem.propTypes = {
  battle: PropTypes.object,
};

const mapStateToProps = (state) => ({
  battles: state.battle.ongoingBattlesList,
  user: state.user.data,
});

const mapDispatchToProps = {
  getOngoingBattlesList,
};

export default connect(mapStateToProps, mapDispatchToProps)(OngoingBattlesList);

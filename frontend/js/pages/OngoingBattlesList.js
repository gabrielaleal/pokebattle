import moment from 'moment';
import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';

import { getOngoingBattlesList } from '../actions/battles-list';
import Loading from '../components/Loading';
import PageTitle from '../components/Title';

function BattleWaitingForMeItem({ battle }) {
  const { id: battleId, creator, timestamp } = battle;
  const formattedDate = moment(timestamp).format('L');
  const formattedTime = moment(timestamp).format('LT');

  return (
    <a href={window.Urls['battles:battleDetail'](battleId)}>
      <div className="list-item">
        <h6 className="pokemon-font">Battle #{battleId}</h6>
        <div>
          <span className="list-attribute">{creator.email}</span> challenged you on {formattedDate}{' '}
          at {formattedTime}. Fight back!
        </div>
      </div>
    </a>
  );
}

function BattleWaitingForMyOpponentItem({ battle }) {
  const { id: battleId, creator, opponent, timestamp } = battle;

  return (
    <a href={window.Urls['battles:battleDetail'](battleId)}>
      <div className="list-item">
        <h6 className="pokemon-font">Battle #{battleId}</h6>
        <div>
          <span className="list-attribute">Players</span> {creator.email} VS {opponent.email}
        </div>
        <div>
          <span className="list-attribute">Battle created on</span> {moment(timestamp).format('L')}{' '}
          at {moment(timestamp).format('LT')}
        </div>
      </div>
    </a>
  );
}

function NoBattlesMessage() {
  return <div className="no-battles">Ops, there are no battles yet!</div>;
}

class OngoingBattlesList extends React.Component {
  componentDidMount() {
    const { getOngoingBattlesList } = this.props;
    getOngoingBattlesList();
  }

  render() {
    const { battles, user, isLoading } = this.props;

    if (isLoading) {
      return <Loading />;
    }

    const battlesWaitingForMe = battles.filter((battle) => battle.opponent.email === user.email);
    const battlesWaitingForOpponent = battles.filter(
      (battle) => battle.creator.email === user.email
    );

    return (
      <div className="pk-container ongoing-battles">
        <PageTitle title="Ongoing Battles" />
        <div className="content">
          <div className="battle-list">
            <h4>Battles waiting for me</h4>
            {battlesWaitingForMe.length === 0 && <NoBattlesMessage />}
            {battlesWaitingForMe.map((battle) => (
              <BattleWaitingForMeItem key={battle.id} battle={battle} />
            ))}
          </div>
          <div className="battle-list">
            <h4>Battles waiting for my opponent</h4>
            {battlesWaitingForOpponent.length === 0 && <NoBattlesMessage />}
            {battlesWaitingForOpponent.map((battle) => (
              <BattleWaitingForMyOpponentItem key={battle.id} battle={battle} />
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
  isLoading: PropTypes.bool,
  getOngoingBattlesList: PropTypes.func,
};

BattleWaitingForMeItem.propTypes = {
  battle: PropTypes.object,
};

BattleWaitingForMyOpponentItem.propTypes = {
  battle: PropTypes.object,
};

const mapStateToProps = ({ battle, user }) => ({
  battles: battle.ongoingBattlesList,
  user: user.data,
  isLoading: battle.loading.list,
});

const mapDispatchToProps = {
  getOngoingBattlesList,
};

export default connect(mapStateToProps, mapDispatchToProps)(OngoingBattlesList);

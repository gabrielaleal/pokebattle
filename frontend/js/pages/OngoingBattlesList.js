import { get, isEqual } from 'lodash';
import moment from 'moment';
import { denormalize } from 'normalizr';
import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

import { getOngoingBattlesList } from '../actions/battles-list';
import Loading from '../components/Loading';
import PageTitle from '../components/PageTitle';
import { battleListSchema } from '../utils/schema';

const BattleWaitingForMeItem = ({ battle }) => {
  const { id: battleId, creator, timestamp } = battle;
  const formattedTimestamp = moment(timestamp).format('L [at] LT');

  return (
    <Link to={{ pathname: `/battles/${battleId}/`, state: { battle, isLoading: false } }}>
      <div className="list-item">
        <h6 className="pokemon-font">Battle #{battleId}</h6>
        <div>
          <span className="list-attribute">{creator.email}</span> challenged you on{' '}
          {formattedTimestamp}. Fight back!
        </div>
      </div>
    </Link>
  );
};

const BattleWaitingForMyOpponentItem = ({ battle }) => {
  const { id: battleId, creator, opponent, timestamp } = battle;
  const formattedTimestamp = moment(timestamp).format('L [at] LT');

  return (
    <Link to={window.Urls['battles:battleDetail'](battleId)}>
      <div className="list-item">
        <h6 className="pokemon-font">Battle #{battleId}</h6>
        <div>
          <span className="list-attribute">Players</span> {creator.email} VS {opponent.email}
        </div>
        <div>
          <span className="list-attribute">Battle created on</span> {formattedTimestamp}
        </div>
      </div>
    </Link>
  );
};

const NoBattlesMessage = () => {
  return <div className="no-battles">Ops, there are no battles yet!</div>;
};

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

    const battlesWaitingForMe = battles.filter((battle) =>
      isEqual(get(battle.opponent, 'email'), user.email)
    );
    const battlesWaitingForOpponent = battles.filter((battle) =>
      isEqual(get(battle.creator, 'email'), user.email)
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

const mapStateToProps = (state) => {
  const { battles } = state;
  const denormalizedData = denormalize(
    battles.ongoingBattlesList,
    battleListSchema,
    battles.entities
  );

  return {
    isLoading: battles.loading.list,
    battles: denormalizedData,
    user: state.user.data,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    getOngoingBattlesList: () => dispatch(getOngoingBattlesList()),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(OngoingBattlesList);

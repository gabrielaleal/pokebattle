import get from 'lodash/get';
import moment from 'moment';
import { denormalize } from 'normalizr';
import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

import { getOngoingBattlesList } from '../actions/battles-list';
import Loading from '../components/loading';
import PageTitle from '../components/title';
import { battleListSchema } from '../utils/schema';

function BattleWaitingForMeItem({ battle }) {
  return (
    <Link to={{ pathname: `/battles/${battle.id}/`, state: { battle } }}>
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
    <Link to={{ pathname: `/battles/${battle.id}/`, state: { battle } }}>
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
    const { battles, user, isLoading } = this.props;
    console.log(battles);
    if (isLoading) {
      return <Loading />;
    }

    const battlesWaitingForMe = battles.filter(
      (battle) => get(battle.opponent, 'email') === user.email
    );
    const battlesWaitingForOpponent = battles.filter(
      (battle) => get(battle.creator, 'email') === user.email
    );

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

const mapDispatchToProps = {
  getOngoingBattlesList,
};

export default connect(mapStateToProps, mapDispatchToProps)(OngoingBattlesList);

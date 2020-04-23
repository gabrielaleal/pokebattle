import moment from 'moment';
import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';

import { getOngoingBattlesList } from '../actions/battles-list';
import Loading from '../components/loading';
import PageTitle from '../components/title';

function BattleWaitingForMeItem({ battle, userEmail }) {
  if (battle.creator.email === userEmail) {
    return <div />;
  }
  return (
    <a href={window.Urls['battles:battleDetail'](battle.id)}>
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
    </a>
  );
}

function BattleWaitingForMyOpponentItem({ battle, userEmail }) {
  if (battle.opponent.email === userEmail) {
    return <div />;
  }
  return (
    <a href={window.Urls['battles:battleDetail'](battle.id)}>
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
    </a>
  );
}

class OngoingBattlesList extends React.Component {
  componentDidMount() {
    const { getOngoingBattlesList } = this.props;
    getOngoingBattlesList();
  }

  render() {
    const { battles, user } = this.props;

    console.log(battles);

    if (!battles) {
      return <Loading />;
    }

    return (
      <div className="pk-container ongoing-battles">
        <PageTitle title="Ongoing Battles" />
        <div className="content">
          <div className="battle-list">
            <h4>Battles waiting for me</h4>
            {Object.keys(battles).map((key) => (
              <BattleWaitingForMeItem
                key={battles[key].id}
                battle={battles[key]}
                userEmail={user.email}
              />
            ))}
          </div>
          <div className="battle-list">
            <h4>Battles waiting for my opponent</h4>
            {Object.keys(battles).map((key) => (
              <BattleWaitingForMyOpponentItem
                key={battles[key].id}
                battle={battles[key]}
                userEmail={user.email}
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
  battles: PropTypes.oneOfType([PropTypes.array, PropTypes.object]),
  getOngoingBattlesList: PropTypes.func,
};

BattleWaitingForMeItem.propTypes = {
  battle: PropTypes.object,
  userEmail: PropTypes.string.isRequired,
};

BattleWaitingForMyOpponentItem.propTypes = {
  battle: PropTypes.object,
  userEmail: PropTypes.string.isRequired,
};

const mapStateToProps = (state) => ({
  battles: state.battle.ongoingBattlesList,
  user: state.user.data,
});

const mapDispatchToProps = {
  getOngoingBattlesList,
};

export default connect(mapStateToProps, mapDispatchToProps)(OngoingBattlesList);

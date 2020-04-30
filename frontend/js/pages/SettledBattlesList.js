import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';

import { getSettledBattlesList } from '../actions/battles-list';
import Loading from '../components/Loading';
import PageTitle from '../components/Title';

function SettledBattleItem({ battle }) {
  const { id: battleId, creator, opponent, winner } = battle;

  return (
    <a href={window.Urls['battles:battleDetail'](battleId)}>
      <div className="list-item settled-battle-item">
        <h6 className="pokemon-font">Battle #{battleId}</h6>
        <div>
          <span className="list-attribute">Players</span> {creator.email} VS {opponent.email}
        </div>
        <div>
          <span className="list-attribute">Winner</span> {winner.email}
        </div>
      </div>
    </a>
  );
}

class SettledBattlesList extends React.Component {
  componentDidMount() {
    const { getSettledBattlesList } = this.props;
    getSettledBattlesList();
  }

  render() {
    const { battles, isLoading } = this.props;

    if (isLoading) {
      return <Loading />;
    }

    return (
      <div className="pk-container battle-detail">
        <PageTitle title="Settled Battles" />
        <div className="content">
          {battles.length === 0 && (
            <div className="no-battles">
              <h4>Ops, there are no battles yet!</h4>
            </div>
          )}
          <div className="battle-list">
            {Object.keys(battles).map((key) => (
              <SettledBattleItem key={battles[key].id} battle={battles[key]} />
            ))}
          </div>
        </div>
      </div>
    );
  }
}

SettledBattlesList.propTypes = {
  battles: PropTypes.array,
  isLoading: PropTypes.bool,
  getSettledBattlesList: PropTypes.func,
};

SettledBattleItem.propTypes = {
  battle: PropTypes.object,
};

const mapStateToProps = ({ battle }) => ({
  battles: battle.settledBattlesList,
  isLoading: battle.loading.list,
});

const mapDispatchToProps = {
  getSettledBattlesList,
};

export default connect(mapStateToProps, mapDispatchToProps)(SettledBattlesList);

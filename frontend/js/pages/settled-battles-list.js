import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

import { getSettledBattlesList } from '../actions/battles-list';
import Loading from '../components/loading';
import PageTitle from '../components/title';

function SettledBattleItem({ battle }) {
  return (
    <Link to={window.Urls['battles:battleDetail'](battle.id)}>
      <div className="list-item settled-battle-item">
        <div>
          <h6 className="pokemon-font">Battle #{battle.id}</h6>
          <div>
            <span className="list-attribute">Players</span> {battle.creator.email} VS{' '}
            {battle.opponent.email}
          </div>
          <div>
            <span className="list-attribute">Winner</span> {battle.winner.email}
          </div>
        </div>
      </div>
    </Link>
  );
}

class SettledBattlesList extends React.Component {
  componentDidMount() {
    const { getSettledBattlesList } = this.props;
    getSettledBattlesList();
  }

  render() {
    const { battles } = this.props;

    if (!battles) {
      return <Loading />;
    }

    return (
      <div className="pk-container battle-detail">
        <PageTitle title="Settled Battles" />
        <div className="content">
          {battles.length === 0 ? (
            <div className="no-battles">
              <h4>Ops, there are no battles yet!</h4>
            </div>
          ) : (
            <div />
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
  getSettledBattlesList: PropTypes.func,
};

SettledBattleItem.propTypes = {
  battle: PropTypes.object,
};

const mapStateToProps = (state) => ({
  battles: state.battle.settledBattlesList,
});

const mapDispatchToProps = {
  getSettledBattlesList,
};

export default connect(mapStateToProps, mapDispatchToProps)(SettledBattlesList);

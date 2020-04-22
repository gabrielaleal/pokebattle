import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';

import { getBattleDetails } from '../actions/battle-details';
import BattleInfoDetails from '../components/battle-details/battle-info-details';
import BattleInformation from '../components/battle-details/battle-information';
import PageTitle from '../components/title';

class BattleDetails extends React.Component {
  componentDidMount() {
    const { computedMatch, loadBattle } = this.props;
    const battlePk = computedMatch.params.pk;
    loadBattle(battlePk);
  }

  render() {
    const { isLoading, battle } = this.state;
    const { user } = this.props;

    return (
      <div className="pk-container battle-detail">
        <PageTitle title="Battle Details" />
        {isLoading ? (
          <div>Loading...</div>
        ) : (
          <>
            <BattleInformation battle={battle} user={user} />
            <BattleInfoDetails battle={battle} user={user} />
          </>
        )}
      </div>
    );
  }
}

BattleDetails.propTypes = {
  loadBattle: PropTypes.func.isRequired,
  computedMatch: PropTypes.object,
  user: PropTypes.object,
};

const mapStateToProps = (state) => {
  return state.battle;
};

const mapDispatchToProps = (dispatch) => ({
  loadBattle: (battlePk) => dispatch(getBattleDetails(battlePk)),
});

export default connect(mapStateToProps, mapDispatchToProps)(BattleDetails);

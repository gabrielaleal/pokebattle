import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';

import { getBattleDetails } from '../actions/battle-details';
import BattleInfoDetails from '../components/battle-details/battle-info-details';
import BattleInformation from '../components/battle-details/battle-information';
import PageTitle from '../components/title';

class BattleDetails extends React.Component {
  componentDidMount() {
    const { computedMatch, getBattleDetails } = this.props;
    const battlePk = computedMatch.params.pk;
    getBattleDetails(battlePk);
  }

  render() {
    const { store, user } = this.props;
    const { isLoading, battle } = store;

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
  computedMatch: PropTypes.object,
  getBattleDetails: PropTypes.func.isRequired,
  user: PropTypes.object.isRequired,
  store: PropTypes.object.isRequired,
};

const mapStateToProps = (state) => ({
  store: state.battle,
  user: state.user.data,
});

const mapDispatchToProps = {
  getBattleDetails,
};

export default connect(mapStateToProps, mapDispatchToProps)(BattleDetails);

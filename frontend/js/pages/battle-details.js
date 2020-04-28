import isEmpty from 'lodash/isEmpty';
import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';

import { getBattleDetails } from '../actions/battle-details';
import BattleInfoDetails from '../components/battle-details/battle-info-details';
import BattleInformation from '../components/battle-details/battle-information';
import Loading from '../components/loading';
import PageTitle from '../components/title';

class BattleDetails extends React.Component {
  componentDidMount() {
    const { computedMatch, getBattle } = this.props;
    const battlePk = computedMatch.params.pk;
    getBattle(battlePk);
  }

  render() {
    const { isLoading, battle, user } = this.props;

    return (
      <div className="pk-container battle-detail">
        <PageTitle title="Battle Details" />
        {isLoading && isEmpty(user) ? (
          <Loading />
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
  getBattle: PropTypes.func.isRequired,
  user: PropTypes.object.isRequired,
  battle: PropTypes.object.isRequired,
  isLoading: PropTypes.bool,
};

const mapStateToProps = (state) => ({
  isLoading: state.battle.loading.details,
  battle: state.battle.battle,
  user: state.user.data,
});

const mapDispatchToProps = (dispatch) => ({
  getBattle: (battlePk) => dispatch(getBattleDetails(battlePk)),
});

export default connect(mapStateToProps, mapDispatchToProps)(BattleDetails);

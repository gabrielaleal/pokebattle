import isEmpty from 'lodash/isEmpty';
import { denormalize } from 'normalizr';
import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';

import getBattleDetails from '../actions/battle-details';
import BattleInfoDetails from '../components/battle-details/BattleInfoDetails';
import BattleInformation from '../components/battle-details/BattleInformation';
import Loading from '../components/Loading';
import PageTitle from '../components/Title';
import { battleSchema } from '../utils/schema';

class BattleDetails extends React.Component {
  componentDidMount() {
    const { computedMatch, getBattleDetails } = this.props;
    const battlePk = computedMatch.params.pk;
    getBattleDetails(battlePk);
  }

  // try componentWillReceiveProps

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
  getBattleDetails: PropTypes.func.isRequired,
  user: PropTypes.object.isRequired,
  battle: PropTypes.object.isRequired,
  isLoading: PropTypes.bool,
};

const mapStateToProps = (state) => {
  const { battles } = state;
  const denormalizedData = denormalize(battles.battle, battleSchema, battles.entities);

  return {
    user: state.user.data,
    isLoading: battles.loading.details,
    battle: denormalizedData,
  };
};

// const mapDispatchToProps = {
//   getBattleDetails,
// };

const mapDispatchToProps = (dispatch) => {
  return {
    getBattleDetails: (battlePk) => dispatch(getBattleDetails(battlePk)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(BattleDetails);

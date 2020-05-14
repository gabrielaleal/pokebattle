import { get, isEmpty } from 'lodash';
import { denormalize } from 'normalizr';
import PropTypes from 'prop-types';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';

import getBattleDetails from '../actions/battle-details';
import BattleInfoDetails from '../components/battle-details/BattleInfoDetails';
import BattleInformation from '../components/battle-details/BattleInformation';
import Loading from '../components/Loading';
import PageTitle from '../components/PageTitle';
import { battleSchema } from '../utils/schema';

const BattleDetails = ({ computedMatch, location, getBattleDetails, battle, isLoading, user }) => {
  useEffect(() => {
    if (isEmpty(battle) || get(location.state, 'update')) {
      const battlePk = computedMatch.params.pk;
      getBattleDetails(battlePk);
    }
  });

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
};

BattleDetails.propTypes = {
  computedMatch: PropTypes.object,
  location: PropTypes.object,
  getBattleDetails: PropTypes.func.isRequired,
  battle: PropTypes.object.isRequired,
  isLoading: PropTypes.bool,
  user: PropTypes.object.isRequired,
};

const mapStateToProps = (state, { location }) => {
  const { battles } = state;
  const battle = get(location, 'state.battle');
  const denormalizedData = denormalize(battles.battle, battleSchema, battles.entities);

  return {
    user: state.user.data,
    isLoading: battles.loading.details,
    battle: !isEmpty(battle) ? battle : denormalizedData,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    getBattleDetails: (battlePk) => dispatch(getBattleDetails(battlePk)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(BattleDetails);

import { get, isEmpty } from 'lodash';
import { denormalize } from 'normalizr';
import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';

import getBattleDetails from '../actions/battle-details';
import BattleInfoDetails from '../components/battle-details/BattleInfoDetails';
import BattleInformation from '../components/battle-details/BattleInformation';
import Loading from '../components/Loading';
import PageTitle from '../components/PageTitle';
import { battleSchema } from '../utils/schema';

class BattleDetails extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoading: isEmpty(props.battle),
    };
  }

  componentDidMount() {
    const { computedMatch, location, battle, getBattleDetails } = this.props;
    if (isEmpty(battle) || get(location.state, 'update')) {
      const battlePk = computedMatch.params.pk;
      getBattleDetails(battlePk).then((res) => {
        const { isLoading } = this.props;
        this.setState({ isLoading });
        return res;
      });
    }
  }

  render() {
    const { battle, user } = this.props;
    const { isLoading } = this.state;

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
  location: PropTypes.object,
  getBattleDetails: PropTypes.func.isRequired,
  user: PropTypes.object.isRequired,
  battle: PropTypes.object.isRequired,
  isLoading: PropTypes.bool,
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

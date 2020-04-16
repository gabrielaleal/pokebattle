import axios from 'axios';
import PropTypes from 'prop-types';
import React from 'react';

import PageTitle from '../components/title';

class BattleDetails extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      battle: {},
      isLoading: true,
    };
  }

  componentDidMount() {
    const { computedMatch } = this.props;
    const battlePk = computedMatch.params.pk;
    const url = window.Urls['api:battleDetail'](battlePk);
    axios.get(url).then((res) => {
      this.setState({ battle: res.data, isLoading: false });
      return res.data;
    });
  }

  render() {
    const { isLoading, battle } = this.state;

    return (
      <div className="pk-container battle-detail">
        <PageTitle title="Battle Details" />
        {isLoading ? <div>Loading...</div> : <pre>{JSON.stringify(battle, null, 2)}</pre>}
      </div>
    );
  }
}

BattleDetails.propTypes = {
  computedMatch: PropTypes.object,
};

export default BattleDetails;

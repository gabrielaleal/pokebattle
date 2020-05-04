/* eslint-disable class-methods-use-this */
/* eslint-disable react/prefer-stateless-function */
import React from 'react';

import PageTitle from '../components/Title';

class CreateBattle extends React.Component {
  render() {
    return (
      <div className="pk-container create-battle">
        <PageTitle title="Create Battle" />
        {/* errors */}
        <div className="content">
          <div className="messages">{/* message */}</div>
          {/* form */}
        </div>
      </div>
    );
  }
}

export default CreateBattle;

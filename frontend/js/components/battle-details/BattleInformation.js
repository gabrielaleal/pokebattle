import { get, isEqual } from 'lodash';
import PropTypes from 'prop-types';
import React from 'react';

import LargeButton from '../LargeButton';

const BattleStatus = ({ status }) => {
  return (
    <div className="battle-info-container">
      <h5 className="pokemon-font">Status</h5>
      <div className="subtitle pokemon-font">{status}!</div>
    </div>
  );
};

const BattlePlayers = ({ creatorEmail, opponentEmail }) => {
  return (
    <div className="battle-info-container">
      <h5 className="pokemon-font">Players</h5>
      <div className="subtitle">
        <span>{creatorEmail}</span> challenged <span>{opponentEmail}</span> on this battle!
      </div>
    </div>
  );
};

const BattleWinner = ({ winnerEmail }) => {
  if (!winnerEmail) {
    return <div />;
  }
  return (
    <div className="battle-info-container">
      <h5 className="pokemon-font">Winner</h5>
      <div className="subtitle">
        This battle winner is <span>{winnerEmail}</span>.
      </div>
    </div>
  );
};

const BattleInformation = ({ battle, user }) => {
  // main component
  const { creator, opponent, winner } = battle;
  const fightBackURL = window.Urls['battles:selectTeam'](battle.id);

  return (
    <div className="content">
      <h4>Battle #{battle.id} Information</h4>
      <BattleStatus status={battle.status} />
      <BattlePlayers creatorEmail={get(creator, 'email')} opponentEmail={get(opponent, 'email')} />
      <BattleWinner winnerEmail={get(winner, 'email')} />
      {isEqual(get(user, 'email'), get(opponent, 'email')) && !winner ? (
        <LargeButton text="Fight Back!" url={fightBackURL} />
      ) : (
        <div />
      )}
    </div>
  );
};

BattleWinner.propTypes = {
  winnerEmail: PropTypes.string,
};

BattleStatus.propTypes = {
  status: PropTypes.string,
};

BattlePlayers.propTypes = {
  creatorEmail: PropTypes.string,
  opponentEmail: PropTypes.string,
};

BattleInformation.propTypes = {
  battle: PropTypes.object,
  user: PropTypes.object,
};

export default BattleInformation;

import get from 'lodash/get';
import PropTypes from 'prop-types';
import React from 'react';

function BattleStatus({ status }) {
  return (
    <div className="battle-info-container">
      <h5 className="pokemon-font">Status</h5>
      <div className="subtitle pokemon-font">{status}!</div>
    </div>
  );
}

function BattlePlayers({ creatorEmail, opponentEmail }) {
  return (
    <div className="battle-info-container">
      <h5 className="pokemon-font">Players</h5>
      <div className="subtitle">
        <span>{creatorEmail}</span> challenged <span>{opponentEmail}</span> on this battle!
      </div>
    </div>
  );
}

function FightBackButton({ battle, userEmail }) {
  if (userEmail !== battle.opponent.email || battle.winner) {
    return <div />;
  }
  return (
    <div className="battle-team-container">
      <a href={window.Urls['battles:selectTeam'](battle.id)}>
        <div className="pk-btn">Fight back!</div>
      </a>
    </div>
  );
}

function BattleWinner({ winnerEmail }) {
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
}

function BattleInformation({ battle, user }) {
  // main component
  const { creator, opponent, winner } = battle;
  return (
    <div className="content">
      <h4>Battle #{battle.id} Information</h4>
      <BattleStatus status={battle.status} />
      <BattlePlayers creatorEmail={creator.email} opponentEmail={opponent.email} />
      <BattleWinner winnerEmail={get(winner, 'email')} />
      <FightBackButton battle={battle} userEmail={user.email} />
    </div>
  );
}

BattleWinner.propTypes = {
  winnerEmail: PropTypes.string,
};

BattleStatus.propTypes = {
  status: PropTypes.string,
};

BattlePlayers.propTypes = {
  creatorEmail: PropTypes.string.isRequired,
  opponentEmail: PropTypes.string.isRequired,
};

FightBackButton.propTypes = {
  battle: PropTypes.object,
  userEmail: PropTypes.string,
};

BattleInformation.propTypes = {
  battle: PropTypes.object.isRequired,
  user: PropTypes.object.isRequired,
};

export default BattleInformation;

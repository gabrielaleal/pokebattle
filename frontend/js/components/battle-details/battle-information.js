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

function BattlePlayers({ creator, opponent }) {
  return (
    <div className="battle-info-container">
      <h5 className="pokemon-font">Players</h5>
      <div className="subtitle">
        <span>{creator}</span> challenged <span>{opponent}</span> on this battle!
      </div>
    </div>
  );
}

// user == battle.opponent and battle.winner is None
function FightBackButton({ battlePk }) {
  return (
    <div className="battle-team-container">
      <a href={window.Urls['battles:SelectTeam'](battlePk)}>
        <div className="pk-btn">Fight back!</div>
      </a>
    </div>
  );
}

// if battle winner is not null
function BattleWinner({ winner }) {
  return (
    <div className="battle-info-container">
      <h5 className="pokemon-font">Winner</h5>
      <div className="subtitle">
        This battle winner is <span>{winner}</span>.
      </div>
    </div>
  );
}

function BattleInformation({ battle }) {
  // main component
  // const { creator, opponent } = battle;
  return (
    <div className="content">
      <h4>Battle #{battle.id} Information</h4>
      <BattleStatus status={battle.status} />
      {/* <BattlePlayers creator={creator.email} opponent={opponent.email} /> */}
    </div>
  );
}

BattleWinner.propTypes = {
  winner: PropTypes.string,
};

BattleStatus.propTypes = {
  status: PropTypes.string,
};

BattlePlayers.propTypes = {
  creator: PropTypes.string.isRequired,
  opponent: PropTypes.string.isRequired,
};

FightBackButton.propTypes = {
  battlePk: PropTypes.number,
};

BattleInformation.propTypes = {
  battle: PropTypes.object.isRequired,
};

export default BattleInformation;

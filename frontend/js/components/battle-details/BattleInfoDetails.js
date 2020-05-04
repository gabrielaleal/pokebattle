/* eslint-disable babel/camelcase */
import get from 'lodash/get';
import PropTypes from 'prop-types';
import React from 'react';

import PokemonCard from './PokemonCard';

const PokemonFromTeam = ({ pokemon }) => {
  return (
    <div className="pokemon-info-container">
      <div className="pokemon-icon">
        <img alt="pokemon img" height="90px" src={get(pokemon, 'img_url')} />
      </div>
      <div className="pokemon-name">{get(pokemon, 'name')}</div>
    </div>
  );
};

const BattlePlayerTeam = ({ player, playerTeam }) => {
  return (
    <div className="battle-info-container">
      <div className="pokemon-font">{player.email} team</div>
      <div className="battle-team-container">
        {Object.keys(playerTeam).map((pokemon) => (
          <PokemonFromTeam key={get(playerTeam[pokemon], 'name')} pokemon={playerTeam[pokemon]} />
        ))}
      </div>
    </div>
  );
};

const BattleMatchesInformation = ({ creatorTeam, opponentTeam, winners }) => {
  return (
    <div className="battle-info-container">
      <h5 className="pokemon-font">Matches</h5>
      <div className="match">
        {Object.keys(creatorTeam).map((key, index) => (
          <div key={get(creatorTeam[key], 'id')}>
            <h6 className="pokemon-font">Round #{index + 1}</h6>
            <div className="round-info-container">
              <PokemonCard pokemon={creatorTeam[key]} winner={winners[index]} />
              <div className="vs pokemon-font">VS</div>
              <PokemonCard pokemon={opponentTeam[key]} winner={winners[index]} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

const BattleInfoDetails = ({ battle, user }) => {
  const { creator, opponent, winner, creator_team, opponent_team, matches_winners } = battle;

  if (!creator_team || !opponent_team) return null;

  return (
    <div className="content">
      {get(user, 'email') === get(creator, 'email') || winner ? (
        <>
          <h4>Battle #{battle.id} Details</h4>
          <BattlePlayerTeam player={creator} playerTeam={creator_team} />
        </>
      ) : (
        <div />
      )}
      {winner ? (
        <>
          <BattlePlayerTeam player={opponent} playerTeam={opponent_team} />
          <BattleMatchesInformation
            creatorTeam={creator_team}
            opponentTeam={opponent_team}
            winners={matches_winners}
          />
        </>
      ) : (
        <div />
      )}
    </div>
  );
};

PokemonFromTeam.propTypes = {
  pokemon: PropTypes.object,
};

BattlePlayerTeam.propTypes = {
  player: PropTypes.object,
  playerTeam: PropTypes.array,
};

BattleMatchesInformation.propTypes = {
  creatorTeam: PropTypes.array,
  opponentTeam: PropTypes.array,
  winners: PropTypes.array,
};

BattleInfoDetails.propTypes = {
  battle: PropTypes.object,
  user: PropTypes.object,
};

export default BattleInfoDetails;

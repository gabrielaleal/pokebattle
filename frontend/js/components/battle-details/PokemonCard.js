import get from 'lodash/get';
import PropTypes from 'prop-types';
import React from 'react';

function PokemonCard({ pokemon, winner }) {
  return (
    <div className="card pokemon-font">
      {get(pokemon, 'name') === get(winner, 'name') ? (
        <div className="winner">
          <img alt="crown" height="56px" src="/static/img/icons/pixel-crown.png" />
        </div>
      ) : (
        <div />
      )}
      <div className="title">
        <div>{get(pokemon, 'name')}</div>
        <div>
          <span>HP</span>
          {get(pokemon, 'hp')}
        </div>
      </div>
      <div className="pokemon-icon">
        <img alt="pokemon" height="96px" src={get(pokemon, 'img_url')} />
      </div>
      <div className="pokemon-info">
        <div>
          <span>ATTACK</span> {get(pokemon, 'attack')}
        </div>
        <div>
          <span>DEFENSE</span> {get(pokemon, 'defense')}
        </div>
      </div>
    </div>
  );
}

PokemonCard.propTypes = {
  pokemon: PropTypes.object,
  winner: PropTypes.object,
};

export default PokemonCard;

import PropTypes from 'prop-types';
import React from 'react';

function PokemonCard({ pokemon, winner }) {
  return (
    <div className="card pokemon-font">
      {pokemon.name === winner.name ? (
        <div className="winner">
          <img alt="crown" height="56px" src="/static/img/icons/pixel-crown.png" />
        </div>
      ) : (
        <div />
      )}
      <div className="title">
        <div>{pokemon.name}</div>
        <div>
          <span>HP</span>
          {pokemon.hp}
        </div>
      </div>
      <div className="pokemon-icon">
        <img alt="pokemon" height="96px" src={pokemon.img_url} />
      </div>
      <div className="pokemon-info">
        <div>
          <span>ATTACK</span> {pokemon.attack}
        </div>
        <div>
          <span>DEFENSE</span> {pokemon.defense}
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

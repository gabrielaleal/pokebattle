import arrayMove from 'array-move';
import PropTypes from 'prop-types';
import React from 'react';
import { SortableContainer, SortableElement } from 'react-sortable-hoc';

import { getPokemonFromAPI } from '../utils/api-helper';

const SelectPokemonField = SortableElement(({ pokemon }) => (
  /* autocomplete field goes here */ <h3>Pika, {pokemon.name}</h3>
));

const SortablePokemonList = SortableContainer(({ pokemon }) => {
  return (
    <div>
      {pokemon.map((value, index) => (
        <SelectPokemonField key={value.id} index={index} value={value} />
      ))}
    </div>
  );
});

class SelectPokemon extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      pokemon: [],
    };
  }

  componentDidMount() {
    getPokemonFromAPI().then((res) => {
      console.log('-> pokemon:', res);
      this.setState({
        pokemon: res,
      });
      return res;
    });
  }

  onSortEnd = ({ oldIndex, newIndex }) => {
    this.setState(({ pokemon }) => ({
      pokemon: arrayMove(pokemon, oldIndex, newIndex),
    }));
  };

  render() {
    const { pokemon } = this.state;
    return <SortablePokemonList items={pokemon} onSortEnd={this.onSortEnd} />;
  }
}

SelectPokemon.propTypes = {
  // eslint-disable-next-line react/no-unused-prop-types
  formikBag: PropTypes.object,
};

export default SelectPokemon;

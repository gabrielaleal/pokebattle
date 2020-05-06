import arrayMove from 'array-move';
import PropTypes from 'prop-types';
import React from 'react';
import Autocomplete from 'react-autocomplete';
import { SortableContainer, SortableElement } from 'react-sortable-hoc';

import { getPokemonFromAPI } from '../utils/api-helper';

const shouldItemRender = (item, value) => {
  if (value === '') {
    return false;
  }

  return item.name.startsWith(value);
};

const SelectPokemonField = SortableElement(
  ({ pokemonList, pokemonValue, valueName, setFieldValue }) => {
    return (
      <div className="pk-autocomplete">
        <Autocomplete
          getItemValue={(item) => item.name}
          items={pokemonList}
          renderItem={(item, isHighlighted) => (
            <div key={item.id} style={{ background: isHighlighted ? 'lightgray' : 'white' }}>
              {item.name}
            </div>
          )}
          shouldItemRender={(item, value) => shouldItemRender(item, value)}
          value={pokemonValue}
          onChange={(e) => setFieldValue(valueName, e.target.value)}
          onSelect={(val) => setFieldValue(valueName, val)}
        />
      </div>
    );
  }
);

const SortablePokemonList = SortableContainer(({ pokemonList, items, formikBag }) => {
  const { setFieldValue } = formikBag;
  return (
    <div>
      {items.map((item, index) => (
        <div key={item.name} className="pk-select">
          <SelectPokemonField
            index={index}
            pokemonList={pokemonList}
            pokemonValue={item.values}
            setFieldValue={setFieldValue}
            valueName={item.name}
          />
          {item.errors && item.touched && <div className="field-error">{item.errors}</div>}
        </div>
      ))}
    </div>
  );
});

class SelectPokemonTeam extends React.Component {
  constructor(props) {
    super(props);
    const { formikBag } = this.props;
    const { values, errors, touched } = formikBag;
    this.state = {
      pokemonList: [],
      pokemonTeam: [
        {
          name: 'pokemon1',
          values: values.pokemon1,
          errors: errors.pokemon1,
          touched: touched.pokemon1,
        },
        {
          name: 'pokemon2',
          values: values.pokemon2,
          errors: errors.pokemon2,
          touched: touched.pokemon2,
        },
        {
          name: 'pokemon3',
          values: values.pokemon3,
          errors: errors.pokemon3,
          touched: touched.pokemon3,
        },
      ],
    };
  }

  componentDidMount() {
    getPokemonFromAPI().then((res) => {
      this.setState({
        pokemonList: res,
      });
      return res;
    });
  }

  onSortEnd = ({ oldIndex, newIndex }) => {
    this.setState(({ pokemonTeam }) => ({
      pokemonTeam: arrayMove(pokemonTeam, oldIndex, newIndex),
    }));
  };

  render() {
    const { pokemonList, pokemonTeam } = this.state;
    const { formikBag } = this.props;
    const { setFieldValue } = formikBag;
    return (
      <div>
        Choose your team:
        <div className="pk-hint">
          Once you do, you can drag and drop them to the position they&apos;ll play.
        </div>
        <SortablePokemonList
          formikBag={{ setFieldValue }}
          items={pokemonTeam}
          pokemonList={pokemonList}
          onSortEnd={this.onSortEnd}
        />
      </div>
    );
  }
}

SelectPokemonTeam.propTypes = {
  formikBag: PropTypes.object,
};

export default SelectPokemonTeam;

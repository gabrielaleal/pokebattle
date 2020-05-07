import arrayMove from 'array-move';
import PropTypes from 'prop-types';
import React from 'react';
import Autocomplete from 'react-autocomplete';
import { SortableContainer, SortableElement, SortableHandle } from 'react-sortable-hoc';

import { getPokemonFromAPI } from '../utils/api-helper';

const shouldItemRender = (item, value) => {
  if (value === '') {
    return false;
  }
  return item.name.startsWith(value);
};

const SortHandler = SortableHandle(() => {
  return <div className="pk-sort-handler">☰</div>;
});

const SelectPokemonField = SortableElement(({ pokemonList, name, value, setFieldValue }) => {
  const queryName = `${name}Query`;
  return (
    <div className="pk-autocomplete">
      <SortHandler />
      <Autocomplete
        getItemValue={(item) => item.name}
        items={pokemonList}
        renderItem={(item, isHighlighted) => (
          <div key={item.id} style={{ background: isHighlighted ? 'lightgray' : 'white' }}>
            <img alt="Pokemon icon" height="60px" src={item.img_url} />
            {item.name}
          </div>
        )}
        shouldItemRender={shouldItemRender}
        value={value}
        onChange={({ target: { value } }) => {
          setFieldValue(queryName, value);
        }}
        onSelect={(value, item) => {
          setFieldValue(name, item.id);
          setFieldValue(queryName, value);
        }}
      />
    </div>
  );
});

const SortablePokemonList = SortableContainer(({ pokemonList, items, formikBag }) => {
  const { values, errors, touched, setFieldValue } = formikBag;
  return (
    <div>
      {items.map((item, index) => (
        <div key={item} className="pk-select">
          <SelectPokemonField
            index={index}
            name={item}
            pokemonList={pokemonList}
            setFieldValue={setFieldValue}
            value={values[`${item}Query`]}
          />
          {errors[item] && touched[item] && <div className="field-error">{errors[item]}</div>}
        </div>
      ))}
    </div>
  );
});

class SelectPokemonTeam extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      pokemonList: [],
      pokemonTeam: ['pokemon1', 'pokemon2', 'pokemon3'],
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
    this.setState(({ pokemonTeam }) => {
      const newPokemonOrder = arrayMove(pokemonTeam, oldIndex, newIndex);
      const { formikBag } = this.props;
      const { setFieldValue } = formikBag;
      setFieldValue('ordering', newPokemonOrder);
      return {
        pokemonTeam: newPokemonOrder,
      };
    });
  };

  render() {
    const { pokemonList, pokemonTeam } = this.state;
    const { formikBag } = this.props;
    const { values, errors, touched, setFieldValue } = formikBag;

    return (
      <div>
        Choose your team:
        <div className="pk-hint">
          Once you do, you can drag and drop them to the position they&apos;ll play.
        </div>
        <SortablePokemonList
          formikBag={{ values, errors, touched, setFieldValue }}
          items={pokemonTeam}
          pokemonList={pokemonList}
          useDragHandle
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

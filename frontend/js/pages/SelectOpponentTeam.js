/* eslint-disable babel/camelcase */
import { withFormik } from 'formik';
import { get } from 'lodash';
import PropTypes from 'prop-types';
import React from 'react';
import { Redirect } from 'react-router-dom';

import PageTitle from '../components/PageTitle';
import SelectPokemonTeam from '../components/SelectPokemon';
import { postOnAPI } from '../utils/api-helper';

const SelectBattleTeamForm = (props) => {
  const {
    values,
    touched,
    errors,
    status,
    handleChange,
    handleBlur,
    handleSubmit,
    setFieldValue,
  } = props;

  return (
    <div>
      {errors.general && <div className="error">{errors.general}</div>}
      {get(status, 'success') && (
        <Redirect
          push
          to={{
            pathname: `/battles/${status.battle}/`,
            state: { update: true },
          }}
        />
      )}
      <form onSubmit={handleSubmit}>
        <div className="battle-form-field">
          <SelectPokemonTeam
            formikBag={{ values, touched, errors, handleChange, handleBlur, setFieldValue }}
          />
        </div>
        <div className="btn-container">
          <button className="pk-btn" type="submit">
            Submit
          </button>
        </div>
      </form>
    </div>
  );
};

const SelectBattleTeamEnhancedForm = withFormik({
  mapPropsToValues: () => ({
    pokemon1: null,
    pokemon1Query: '',
    pokemon2: null,
    pokemon2Query: '',
    pokemon3: null,
    pokemon3Query: '',
    ordering: ['pokemon1', 'pokemon2', 'pokemon3'],
  }),
  // Custom sync validation
  validate: (values) => {
    const errors = {};

    if (!values.pokemon1) {
      errors.pokemon1 = 'Required';
    }

    if (!values.pokemon2) {
      errors.pokemon2 = 'Required';
    }

    if (!values.pokemon3) {
      errors.pokemon3 = 'Required';
    }

    return errors;
  },
  handleSubmit: (values, { props, setFieldError, resetForm, setStatus }) => {
    const { battlePk } = props;
    const url = window.Urls['api:selectTeam'](battlePk);
    const data = {
      pokemon_1: values.pokemon1,
      pokemon_1_position: values.ordering.indexOf('pokemon1') + 1,
      pokemon_2: values.pokemon2,
      pokemon_2_position: values.ordering.indexOf('pokemon2') + 1,
      pokemon_3: values.pokemon3,
      pokemon_3_position: values.ordering.indexOf('pokemon3') + 1,
    };
    postOnAPI(url, data)
      .then((res) => {
        resetForm();
        setStatus({
          success: true,
          battle: battlePk,
        });
        return res;
      })
      .catch((err) => {
        if (err.response.status === 400) {
          setFieldError('general', err.response.data.non_field_errors[0]);
        }
        throw err;
      });
  },
  displayName: 'SelectBattleTeamForm',
})(SelectBattleTeamForm);

class SelectOpponentTeam extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      battlePk: '',
    };
  }

  componentDidMount() {
    const { computedMatch } = this.props;
    this.setState({
      battlePk: computedMatch.params.pk,
    });
  }

  render() {
    const { battlePk } = this.state;

    return (
      <div className="pk-container create-battle">
        <PageTitle title="Select Team" />
        <div className="content">
          <SelectBattleTeamEnhancedForm battlePk={battlePk} />
        </div>
      </div>
    );
  }
}

SelectBattleTeamForm.propTypes = {
  values: PropTypes.object,
  touched: PropTypes.object,
  errors: PropTypes.object,
  status: PropTypes.object,
  setFieldValue: PropTypes.func,
  handleChange: PropTypes.func,
  handleBlur: PropTypes.func,
  handleSubmit: PropTypes.func,
};

SelectOpponentTeam.propTypes = {
  computedMatch: PropTypes.object,
};

export default SelectOpponentTeam;

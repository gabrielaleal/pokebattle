/* eslint-disable babel/camelcase */
import { withFormik } from 'formik';
import { get } from 'lodash';
import PropTypes from 'prop-types';
import React from 'react';
import { Link } from 'react-router-dom';

import SelectPokemonTeam from '../components/SelectPokemon';
import PageTitle from '../components/Title';
import { getOpponentsFromAPI, postOnAPI } from '../utils/api-helper';

class SelectOpponentField extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      opponents: [],
    };
  }

  componentDidMount() {
    const { opponents } = this.state;
    getOpponentsFromAPI().then((res) => {
      this.setState({
        opponents: res,
      });
      return opponents;
    });
  }

  render() {
    const { opponents } = this.state;
    const { formikBag } = this.props;
    const { values, handleChange, handleBlur, errors, touched } = formikBag;

    return (
      <div style={{ display: 'grid' }}>
        <label htmlFor="opponentSelect">Opponent:</label>
        <select
          id="opponentSelect"
          name="opponent"
          value={values.opponent}
          onBlur={handleBlur}
          onChange={handleChange}
        >
          <option label="Select your opponent" value="" />
          {opponents.map((opponent) => (
            <option key={opponent.id} label={opponent.email} value={opponent.id} />
          ))}
        </select>
        {errors.opponent && touched.opponent && (
          <div className="field-error">{errors.opponent}</div>
        )}
      </div>
    );
  }
}

const CreateBattleForm = (props) => {
  const {
    values,
    touched,
    status,
    errors,
    handleChange,
    handleBlur,
    handleSubmit,
    setFieldValue,
  } = props;

  return (
    <div>
      {errors.general && <div className="error">{errors.general}</div>}
      {get(status, 'success') && (
        <div className="messages">
          Battle #{status.success} created! Click{' '}
          <Link className="link" to={`/battles/${status.success}`}>
            here
          </Link>{' '}
          to check the battle page while you wait for your opponent to fight back.
        </div>
      )}
      <form onSubmit={handleSubmit}>
        <div className="battle-form-field">
          <SelectOpponentField formikBag={{ values, touched, errors, handleChange, handleBlur }} />
        </div>
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

const CreateBattleEnhancedForm = withFormik({
  mapPropsToValues: () => ({
    opponent: '',
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

    if (!values.opponent) {
      errors.opponent = 'Required';
    }

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
  handleSubmit: (values, { setStatus, setFieldError, resetForm }) => {
    const url = window.Urls['api:createBattle']();
    const data = {
      opponent_id: values.opponent,
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
          success: res.data.battle_id,
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
  displayName: 'BattleForm',
})(CreateBattleForm);

const CreateBattle = () => {
  return (
    <div className="pk-container create-battle">
      <PageTitle title="Create Battle" />
      <div className="content">
        <CreateBattleEnhancedForm />
      </div>
    </div>
  );
};

CreateBattleForm.propTypes = {
  values: PropTypes.object,
  touched: PropTypes.object,
  errors: PropTypes.object,
  status: PropTypes.object,
  setFieldValue: PropTypes.func,
  handleChange: PropTypes.func,
  handleBlur: PropTypes.func,
  handleSubmit: PropTypes.func,
};

SelectOpponentField.propTypes = {
  formikBag: PropTypes.object,
};

export default CreateBattle;

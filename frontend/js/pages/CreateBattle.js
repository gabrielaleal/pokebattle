import { withFormik } from 'formik';
import PropTypes from 'prop-types';
import React from 'react';

import SelectPokemon from '../components/SelectPokemon';
import PageTitle from '../components/Title';
import { getOpponentsFromAPI } from '../utils/api-helper';

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
        {errors.opponent && touched.opponent && <div id="feedback">{errors.opponent}</div>}
      </div>
    );
  }
}

const CreateBattleForm = (props) => {
  const { values, touched, errors, handleChange, handleBlur, handleSubmit } = props;

  return (
    <form onSubmit={handleSubmit}>
      <SelectOpponentField formikBag={{ values, touched, errors, handleChange, handleBlur }} />
      <SelectPokemon formikBag={{ values, touched, errors, handleChange, handleBlur }} />
      <div className="btn-container">
        <button className="pk-btn" type="submit">
          Submit
        </button>
      </div>
    </form>
  );
};

const CreateBattleEnhancedForm = withFormik({
  mapPropsToValues: () => ({ opponent: {} }),
  // Custom sync validation
  validate: (values) => {
    const errors = {};

    if (!values.opponent) {
      errors.opponent = 'Required';
    }

    return errors;
  },
  handleSubmit: (values, { setSubmitting }) => {
    setTimeout(() => {
      console.log(values);
      setSubmitting(false);
    }, 1000);
  },
  displayName: 'BattleForm',
})(CreateBattleForm);

const CreateBattle = () => {
  return (
    <div className="pk-container create-battle">
      <PageTitle title="Create Battle" />
      {/* errors */}
      <div className="content">
        {/* <div className="messages"></div> */}
        <CreateBattleEnhancedForm />
      </div>
    </div>
  );
};

CreateBattleForm.propTypes = {
  values: PropTypes.object,
  touched: PropTypes.object,
  errors: PropTypes.object,
  handleChange: PropTypes.func,
  handleBlur: PropTypes.func,
  handleSubmit: PropTypes.func,
};

SelectOpponentField.propTypes = {
  formikBag: PropTypes.object,
};

export default CreateBattle;

/* eslint-disable class-methods-use-this */
/* eslint-disable react/prefer-stateless-function */
import { Formik } from 'formik';
import React from 'react';
// import Yup from 'yup';

import PageTitle from '../components/Title';
import getOpponentsFromAPI from '../utils/api-helper';

const SelectOpponentField = (formik) => {
  let opponents = [];
  let loading = true;
  const { values, handleBlur, handleChange } = formik;
  getOpponentsFromAPI().then((res) => {
    opponents = res;
    loading = false;
    return opponents;
  });

  if (loading) return <div />;

  return (
    <div>
      {/* eslint-disable-next-line jsx-a11y/label-has-associated-control */}
      <label htmlFor="email" style={{ display: 'block' }}>
        Opponent
      </label>
      <select
        name="opponent"
        style={{ display: 'block' }}
        value={values.opponent}
        onBlur={handleBlur}
        onChange={handleChange}
      >
        <option label="Select your opponent" value="" />
        {opponents.map((opponent) => (
          <option key={opponent.id} label={opponent.email} value={opponent} />
        ))}
      </select>
    </div>
  );
};

const CreateBattleForm = () => {
  console.log('create battle form');
  const formik = Formik({
    mapPropsToValues: () => ({
      opponent: '',
    }),
    // validationSchema: Yup.object().shape({
    //   color: Yup.string().required('Color is required!'),
    // }),
    handleSubmit: (values, { setSubmitting }) => {
      setTimeout(() => {
        // eslint-disable-next-line no-alert
        alert(JSON.stringify(values, null, 2));
        setSubmitting(false);
      }, 1000);
    },
  });

  return (
    <form onSubmit={formik.handleSubmit}>
      <SelectOpponentField formik={formik} />
    </form>
  );
};

class CreateBattle extends React.Component {
  render() {
    return (
      <div className="pk-container create-battle">
        <PageTitle title="Create Battle" />
        {/* errors */}
        <div className="content">
          <div className="messages">{/* message */}</div>
          <CreateBattleForm />
        </div>
      </div>
    );
  }
}

export default CreateBattle;

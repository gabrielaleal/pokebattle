import PropTypes from 'prop-types';
import React from 'react';

const PageTitle = ({ title }) => (
  <div className="pk-comp-title">
    <div className="pk-title">{title}</div>
    <a href={window.Urls['home']()}>
      <div className="go-home-btn">Go home</div>
    </a>
  </div>
);

PageTitle.propTypes = {
  title: PropTypes.string,
};

export default PageTitle;

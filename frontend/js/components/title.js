import PropTypes from 'prop-types';
import React from 'react';

const PageTitle = ({ title }) => (
  <div className="pk-comp-title">
    <div className="pk-title">{title}</div>
  </div>
);

// {/* <a href="{% url 'home' %}">
//   <div className="go-home-btn">Go home</div>
// </a> */}

PageTitle.propTypes = {
  title: PropTypes.string,
};

export default PageTitle;

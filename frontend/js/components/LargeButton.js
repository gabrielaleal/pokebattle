import PropTypes from 'prop-types';
import React from 'react';
import { Link } from 'react-router-dom';

function LargeButton({ text, url }) {
  return (
    <div className="battle-team-container">
      <Link to={url}>
        <div className="pk-btn">{text}</div>
      </Link>
    </div>
  );
}

LargeButton.propTypes = {
  text: PropTypes.string,
  url: PropTypes.string,
};

export default LargeButton;

import PropTypes from 'prop-types';
import React from 'react';

function LargeButton({ text, url }) {
  return (
    <div className="battle-team-container">
      <a href={url}>
        <div className="pk-btn">{text}</div>
      </a>
    </div>
  );
}

LargeButton.propTypes = {
  text: PropTypes.string,
  url: PropTypes.string,
};

export default LargeButton;

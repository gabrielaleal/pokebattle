import PropTypes from 'prop-types';
import React from 'react';

const Navbar = ({ user }) => (
  <nav>
    <div className="pk-nav">
      <div>
        <a href={window.Urls.home()}>
          <div className="pk-logo" />
        </a>
      </div>
      <div className="btns-container">
        {user.email ? (
          <>
            <span>Welcome, {user.email.split('@')[0]}</span>
            <a href={window.Urls.logout()}>
              <div className="pk-small-btn">Logout</div>
            </a>
          </>
        ) : (
          <>
            <a href={window.Urls.login()}>
              <div className="pk-small-btn">Login</div>
            </a>
            <a href={window.Urls.signup()}>
              <div className="pk-small-btn">SignUp</div>
            </a>
          </>
        )}
      </div>
    </div>
  </nav>
);

Navbar.propTypes = {
  user: PropTypes.shape({
    email: PropTypes.string,
  }),
};

Navbar.defaultProps = {
  user: {},
};
export default Navbar;

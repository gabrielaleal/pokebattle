const path = require('path');

module.exports = {
  root: true,
  extends: ['vinta/recommended'],
  rules: {
    'no-console': 'off',
    'dot-notation': 'warn',
    'default-param-last': 'off',
    'sonarjs/no-small-switch': 'off',
    'jsx-a11y/label-has-associated-control': [ 'error', {
      'required': {
        'some': [ 'nesting', 'id'  ]
      }
    }],
  },
  env: {
    es6: true,
    browser: true,
    jest: true
  },
  settings: {
    'import/resolver': {
      webpack: {
        config: path.join(__dirname, '/webpack.local.config.js'),
        'config-index': 1
      }
    },
    react: {
      "version": "detect"
    },
  }
}

import { combineReducers } from 'redux';

import battle from './battle-reducer';
import user from './user-reducer';

const rootReducer = combineReducers({
  battle,
  user,
});

export default rootReducer;

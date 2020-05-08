import { combineReducers } from 'redux';

import battles from './battle-reducer';
import user from './user-reducer';

const rootReducer = combineReducers({
  battles,
  user,
});

export default rootReducer;

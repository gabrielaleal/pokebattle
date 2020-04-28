/* eslint-disable babel/camelcase */
import { schema } from 'normalizr';

const user = new schema.Entity('users');

const pokemon = new schema.Entity('pokemon');

// using camelcase due to API's response format
const battle = new schema.Entity('battle', {
  creator: user,
  opponent: user,
  winner: user,
  creator_team: [pokemon],
  opponent_team: [pokemon],
});

const battleList = [battle];

export { battle, battleList };

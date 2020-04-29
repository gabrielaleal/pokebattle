/* eslint-disable babel/camelcase */
import { schema } from 'normalizr';

const userSchema = new schema.Entity('users');

const pokemonSchema = new schema.Entity('pokemon');

// using snakecase due to API's response format
const battleSchema = new schema.Entity('battle', {
  creator: userSchema,
  opponent: userSchema,
  winner: userSchema,
  creator_team: [pokemonSchema],
  opponent_team: [pokemonSchema],
  matches_winners: [pokemonSchema],
});

const battleListSchema = new schema.Array(battleSchema);

export { battleSchema, battleListSchema };

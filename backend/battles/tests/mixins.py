from model_mommy import mommy


class MakePokemonMixin:
    def _make_pokemon(self):
        # return a pokemon team with valid points sum
        return (
            mommy.make("pokemon.Pokemon", attack=60, defense=45, hp=50),
            mommy.make("pokemon.Pokemon", attack=60, defense=45, hp=50),
            mommy.make("pokemon.Pokemon", attack=60, defense=45, hp=50),
        )


class CreatorAndOpponentMixin:
    def _make_creator_and_opponent(self):
        return (mommy.make("users.User"), mommy.make("users.User"))

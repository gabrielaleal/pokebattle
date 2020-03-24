from celery.schedules import crontab  # noqa


CELERYBEAT_SCHEDULE = {
    "get_all_pokemon_from_api": {
        "task": "pokemon.tasks.get_all_pokemon_from_api_task",
        "schedule": crontab(minute=10, hour=17, day_of_week="mon-fri"),
    }
}

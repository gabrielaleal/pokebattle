from .local_base import *  # noqa

from dj_database_url import parse as db_url

DATABASES = {
    "default": db_url("postgresql://postgres:postgres@localhost:5432/pokebattle"),
}

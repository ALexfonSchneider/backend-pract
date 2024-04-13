import pytest

from alembic.command import downgrade, upgrade
from alembic.config import Config
from alembic.script import Script, ScriptDirectory
from .conftest import get_revisions, alembic_config, pg_url


@pytest.mark.parametrize("revision", get_revisions())
def test_migrations_stairway(revision: Script):
    config = alembic_config()
    upgrade(config, revision.revision)

    downgrade(config, revision.down_revision or "-1")
    upgrade(config, revision.revision)

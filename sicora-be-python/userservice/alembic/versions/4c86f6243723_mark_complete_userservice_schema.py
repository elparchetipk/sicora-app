"""mark_complete_userservice_schema

Revision ID: 4c86f6243723
Revises: 84dd0011bf4f
Create Date: 2025-06-29 03:19:10.096874

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c86f6243723'
down_revision: Union[str, None] = '84dd0011bf4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

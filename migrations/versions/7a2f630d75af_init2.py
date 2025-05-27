"""init2

Revision ID: 7a2f630d75af
Revises: 81e5517a5b6b
Create Date: 2025-05-14 15:19:22.194259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '7a2f630d75af'
down_revision: Union[str, None] = '81e5517a5b6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Explicitly cast VARCHAR to DATE using PostgreSQL syntax
    op.execute(
        "ALTER TABLE books ALTER COLUMN published_date TYPE DATE USING published_date::date"
    )



def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        "ALTER TABLE books ALTER COLUMN published_date TYPE VARCHAR USING published_date::text"
    )

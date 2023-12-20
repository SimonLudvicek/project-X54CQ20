"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    ${upgrades if upgrades else "pass"}

    # Kód pro vytvoření cizího klíče
    op.create_foreign_key(
        'fk_portfolio_user_id',
        'portfolio',  # Tabulka s cizím klíčem
        'myuser',  # Reference na tabulku s primárním klíčem
        ['user_id'],  # Sloupec s cizím klíčem
        ['id'],  # Sloupec s primárním klíčem
    )


def downgrade():
    ${downgrades if downgrades else "pass"}

    # Kód pro odstranění cizího klíče
    op.drop_constraint('fk_portfolio_user_id', 'portfolio', type_='foreignkey')
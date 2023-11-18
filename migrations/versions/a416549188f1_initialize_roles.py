"""initialize_roles

Revision ID: a416549188f1
Revises: fa22ceb6e3e9
Create Date: 2023-11-16 20:38:58.806098

"""
from datetime import datetime
from uuid import uuid4

from alembic import op

# revision identifiers, used by Alembic.
revision = "a416549188f1"
down_revision = "fa22ceb6e3e9"
branch_labels = None
depends_on = None


def upgrade():
    today = datetime.now().strftime("%Y-%m-%d")
    sql = f"""
    INSERT INTO auth_role (id, name, title, description, created_at) VALUES 
    ('{uuid4()}', 'GUEST', 'Guest', 'Basic permissions', '{today}'),
    ('{uuid4()}', 'ADMINISTRATOR', 'Administrator', 'All permissions', '{today}');
    """
    op.execute(sql)


def downgrade():
    op.execute("TRUNCATE TABLE auth_role RESTART IDENTITY;")

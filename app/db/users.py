import sqlalchemy
from sqlalchemy import Table, Column, ForeignKey, BigInteger, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID

metadata = sqlalchemy.MetaData()

users_table = Table(
    "users",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("email", String(50), unique=True, index=True),
    Column("name", String(100)),
    Column("hashed_password", String()),
    Column("is_active", Boolean(), nullable=False,
           server_default=sqlalchemy.sql.expression.true()),
)

tokens_table = Table(
    "tokens",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("token", UUID(as_uuid=False), unique=True, nullable=False, index=True,
           server_default=sqlalchemy.text("uuid_generate_v4()")),
    Column("expires", DateTime()),
    # Column("user_id", ForeignKey("users.id")),
    Column("user_id", ForeignKey(users_table.c.id)),
)

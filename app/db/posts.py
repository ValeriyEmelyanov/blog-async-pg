import sqlalchemy
from sqlalchemy import Table, Column, ForeignKey, BigInteger, String, DateTime, Text

from .users import users_table

metadata = sqlalchemy.MetaData()

post_table = Table(
    "post",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("user_id", ForeignKey(users_table.c.id)),
    Column("title", String(100)),
    Column("created_at", DateTime()),
    Column("content", Text()),
)

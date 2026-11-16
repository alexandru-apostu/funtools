from typing import Optional, List

from sqlalchemy import (
    MetaData,
    create_engine,
    text,
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    TypedColumns,
    Named,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

metadata_obj = MetaData()

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String, nullable=False),
)

other_meta = MetaData()


class UserCols(TypedColumns):
    id: Named[int] = Column(primary_key=True)
    name: Named[str | None] = Column(String(30))
    full_name: Named[str | None]


typed_user_table = Table("user_account", other_meta, UserCols)


class AddressCols(TypedColumns):
    id: Named[int] = Column(primary_key=True)
    user_id: Named[int] = Column(ForeignKey("user_account.id"))
    email_address: Named[str]
    __row_pos__: tuple[int, int, str]


typed_address_table = Table("address", other_meta, AddressCols)

metadata_obj.create_all(engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    addresses: Mapped[List["Address"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))

    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

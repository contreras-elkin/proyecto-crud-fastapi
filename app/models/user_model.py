from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, Boolean, func, Numeric,  Enum as SQLEnum
from decimal import Decimal
from datetime import datetime, timezone
from app.enums.enums_user import UserRole
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.expense import Expense





class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_name: Mapped[str] = mapped_column(String(100), index=True,nullable= False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole, native_enum=False),default=UserRole.USER, server_default="user",nullable=False)
    phone: Mapped[str] = mapped_column(String(20), unique=True,nullable=False)
    monthly_budget: Mapped[Decimal] = mapped_column(Numeric(10,2), default=Decimal("0.00"), server_default="0.00", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), server_default=func.now(),nullable=False)

    expenses: Mapped[list["Expense"]]=relationship(
        "Expense",
        back_populates="user",
        cascade="all, delete-orphan"
    )
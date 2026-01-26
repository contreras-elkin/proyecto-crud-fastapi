from sqlalchemy import Numeric, String, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date
from app.core.database import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.user_model import User



class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    category: Mapped[str | None] = mapped_column(String(50), nullable=True)
    expense_date: Mapped[date] = mapped_column(
        Date, default=date.today, nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    user: Mapped["User"] = relationship(
        back_populates="expenses"
    )

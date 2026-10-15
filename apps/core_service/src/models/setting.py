"""
Provides the Settings model for the core_service application.
"""

from database_lib.db_classes import TimestampMixin, UUIDPrimaryKeyMixin,  Base

from sqlalchemy import Column, String


class SettingModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "settings"

    category = Column(
        String(50),
        nullable=False,
        index=True
    )
    name = Column(
        String(50),
        nullable=False,
        index=True
    )
    value = Column(
        String(200),
        nullable=False
    )

    def __repr__(self):
        return f"""<
id: {self.id}
name: {self.name}
value: {self.value}
category: {self.category}
date_created: {self.date_created}
date_last_edited: {self.date_last_edited}
>"""

    def __str__(self):
        return f"<Setting - {self.name}: {self.value}>"

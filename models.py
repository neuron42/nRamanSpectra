from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import JSON

from nRamanSpectra import app, db


class Spectra(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    data: Mapped[list] = mapped_column(JSON)  # 使用JSON类型存储结构化数据
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

    @property
    def spectral_data(self):
        """获取标准化光谱数据"""
        return self.data

    def __repr__(self):
        return f"<Spectra {self.name}>"


with app.app_context():
    db.create_all()

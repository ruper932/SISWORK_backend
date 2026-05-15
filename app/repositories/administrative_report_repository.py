from sqlalchemy.orm import Session

from app.models.administrative_report import AdministrativeReport


class AdministrativeReportRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_items(self):
        return self.db.query(AdministrativeReport).order_by(AdministrativeReport.generated_at.desc()).all()

    def get_by_id(self, item_id):
        return self.db.query(AdministrativeReport).filter(AdministrativeReport.id == item_id).first()

    def create(self, item):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def save(self, item):
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item):
        self.db.delete(item)
        self.db.commit()
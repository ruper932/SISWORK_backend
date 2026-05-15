from sqlalchemy.orm import Session

from app.models.administrative_note import AdministrativeNote


class AdministrativeNoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_items(self):
        return self.db.query(AdministrativeNote).order_by(AdministrativeNote.created_at.desc()).all()

    def get_by_id(self, item_id):
        return self.db.query(AdministrativeNote).filter(AdministrativeNote.id == item_id).first()

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
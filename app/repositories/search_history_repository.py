from sqlalchemy.orm import Session

from app.models.search_history import SearchHistory


class SearchHistoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_items(self):
        return self.db.query(SearchHistory).order_by(SearchHistory.searched_at.desc()).all()

    def list_by_user_id(self, user_id):
        return self.db.query(SearchHistory).filter(SearchHistory.user_id == user_id).all()

    def get_by_id(self, item_id):
        return self.db.query(SearchHistory).filter(SearchHistory.id == item_id).first()

    def create(self, item):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item):
        self.db.delete(item)
        self.db.commit()
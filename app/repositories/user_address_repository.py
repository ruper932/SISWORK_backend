from sqlalchemy.orm import Session

from app.models.user_address import UserAddress


class UserAddressRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_items(self):
        return self.db.query(UserAddress).order_by(UserAddress.created_at.desc()).all()

    def list_by_user_id(self, user_id):
        return self.db.query(UserAddress).filter(UserAddress.user_id == user_id).all()

    def get_by_id(self, item_id):
        return self.db.query(UserAddress).filter(UserAddress.id == item_id).first()

    def get_primary_by_user_id(self, user_id):
        return self.db.query(UserAddress).filter(
            UserAddress.user_id == user_id,
            UserAddress.is_primary.is_(True),
        ).first()

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
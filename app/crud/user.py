from bson import ObjectId

from app.core.config import customer_db


def find_user(_id):
    user = customer_db.find_one({'_id': ObjectId(_id)})
    return user

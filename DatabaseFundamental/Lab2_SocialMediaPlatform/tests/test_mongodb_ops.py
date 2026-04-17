def test_mongodb_connection():
    from src.db.mongodb_client import get_mongodb
    
    db = get_mongodb()
    assert db.name == "social_activity"
    
def test_mongodb_insert():
    from src.db.mongodb_client import get_mongodb
    from datetime import datetime
    
    db = get_mongodb()
    result = db.activity_stream.insert_one({
        "user_id": 999,
        "action": "TEST",
        "created_at": datetime.utcnow()
    })
    
    assert result.inserted_id is not None
    db.activity_stream.delete_one({"_id": result.inserted_id})

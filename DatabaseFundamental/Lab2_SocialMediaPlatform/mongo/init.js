db = db.getSiblingDB('social_activity');

db.createCollection('activity_stream');

// Index on user_id to quickly get an individual user's activity stream
db.activity_stream.createIndex({ "user_id": 1, "created_at": -1 });

print("social_activity database initialized with activity_stream collection.");

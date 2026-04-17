// MongoDB initialization script
// Creates collections and indexes for session and behavior tracking

db = db.getSiblingDB('ecommerce_sessions');

// Create sessions collection with index
db.createCollection('sessions');
db.sessions.createIndex({ user_id: 1 }, { unique: false });
db.sessions.createIndex({ created_at: -1 });

// Create shopping_carts collection
db.createCollection('shopping_carts');
db.shopping_carts.createIndex({ user_id: 1 }, { unique: false });
db.shopping_carts.createIndex({ updated_at: -1 });

// Create user_behavior collection
db.createCollection('user_behavior');
db.user_behavior.createIndex({ user_id: 1 });
db.user_behavior.createIndex({ event_type: 1 });
db.user_behavior.createIndex({ timestamp: -1 });
db.user_behavior.createIndex({ user_id: 1, event_type: 1, timestamp: -1 });

// Create sample session document
db.sessions.insertOne({
  user_id: 0,
  data: {
    session_id: "example_session",
    login_time: new Date(),
    pages_visited: ["home", "products"],
    last_activity: new Date()
  },
  created_at: new Date(),
  updated_at: new Date()
});

print("MongoDB collections and indexes created successfully!");


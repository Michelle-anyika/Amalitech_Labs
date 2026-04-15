-- This script inserts a small batch of initial data if needed.
-- It will be heavily supplemented by populate_db.py script for larger volumes.

INSERT INTO users (username, email, full_name, bio) VALUES
('alice', 'alice@example.com', 'Alice Smith', 'Just an alice'),
('bob', 'bob@example.com', 'Bob Jones', 'Builder'),
('charlie', 'charlie@example.com', 'Charlie Brown', 'Good grief');

INSERT INTO posts (user_id, content, metadata) VALUES
(1, 'Hello world, first post!', '{"tags": ["intro", "hello"]}'::jsonb),
(2, 'Building something cool', '{"location": "workshop"}'::jsonb),
(3, 'Where did everyone go?', '{"mood": "confused"}'::jsonb);

-- Let alice and bob follow charlie
INSERT INTO followers (follower_id, following_id) VALUES (1, 3), (2, 3);
UPDATE users SET follower_count = 2 WHERE id = 3;
UPDATE users SET following_count = 1 WHERE id IN (1, 2);

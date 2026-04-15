-- Indexes for foreign keys
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_comments_post_id ON comments(post_id);
CREATE INDEX idx_comments_user_id ON comments(user_id);

-- Composite Index on followers to drastically improve performance for feed generation
-- (follower_id to get who a user follows, following_id to get followers of a user)
CREATE INDEX idx_followers_follower ON followers(follower_id);
CREATE INDEX idx_followers_following ON followers(following_id);

-- GIN Index on JSONB for metadata querying (like finding tags in metadata)
CREATE INDEX idx_posts_metadata ON posts USING GIN (metadata);

-- Index on created_at for fast timeline fetching and pagination
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);

-- Composite index for fast lookup of timeline (posts by users followed)
CREATE INDEX idx_posts_user_created ON posts(user_id, created_at DESC);

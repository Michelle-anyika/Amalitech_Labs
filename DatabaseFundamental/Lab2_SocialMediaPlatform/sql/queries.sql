-- 1. Get user feed (Complex CTE, Join, Window Function)
WITH following_users AS (
    SELECT following_id 
    FROM followers 
    WHERE follower_id = 1
),
ranked_posts AS (
    SELECT 
        p.id as post_id, 
        p.user_id as author_id,
        u.username as author_username,
        p.content, 
        p.metadata, 
        p.created_at,
        ROW_NUMBER() OVER(ORDER BY p.created_at DESC) as rank
    FROM posts p
    JOIN following_users f ON p.user_id = f.following_id
    JOIN users u ON u.id = p.user_id
)
SELECT post_id, author_id, author_username, content, metadata, created_at, rank
FROM ranked_posts
WHERE rank > 0 AND rank <= 20
ORDER BY rank;

-- 2. Find Trending Posts (Aggregation)
SELECT 
    p.id, 
    p.content,
    COUNT(DISTINCT c.id) as comment_count,
    COUNT(DISTINCT pl.user_id) as like_count
FROM posts p
LEFT JOIN comments c ON p.id = c.post_id
LEFT JOIN post_likes pl ON p.id = pl.post_id
GROUP BY p.id
HAVING COUNT(DISTINCT pl.user_id) > 5 OR COUNT(DISTINCT c.id) > 2
ORDER BY like_count DESC, comment_count DESC
LIMIT 10;

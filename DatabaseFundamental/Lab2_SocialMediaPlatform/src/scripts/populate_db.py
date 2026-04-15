import os
import sys
import random
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.models.schemas import User, Post
from src.operations.user_ops import create_user
from src.operations.post_ops import create_post
from src.operations.follow_ops import follow_user

def main():
    print("Populating the database with mock data...")
    users = []
    
    # 1. Create Users
    print("Creating 50 users...")
    for i in range(50):
        u = User(username=f"user_{i}", email=f"user_{i}@example.com", bio=f"Bio for user {i}")
        users.append(create_user(u))
        
    # 2. Create Posts
    print("Creating 500 posts...")
    for i in range(500):
        author = random.choice(users)
        p = Post(
            user_id=author.id, 
            content=f"Post content {i} from {author.username}",
            metadata={"tag": f"tag_{random.randint(1, 10)}"}
        )
        create_post(p)
        
    # 3. Create Follows
    print("Creating random followers...")
    for follower in users:
        # Follow 10 random users
        targets = random.sample(users, 10)
        for target in targets:
            if follower.id != target.id:
                try:
                    follow_user(follower.id, target.id)
                except:
                    pass

    print("Population complete.")

if __name__ == "__main__":
    main()

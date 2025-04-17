"""Redis connection management."""

import redis

from backend.config.config import REDIS_DB, REDIS_HOST, REDIS_PORT


def get_redis():
    """Get Redis connection."""
    try:
        client = redis.Redis(
            host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True
        )
        # Test connection
        client.ping()
        return client
    except redis.ConnectionError as e:
        print(f"Warning: Redis connection failed: {str(e)}")
        return None
    except Exception as e:
        print(f"Error: Redis connection error: {str(e)}")
        return None


def request_write_access(redis_client, username):
    """Request write access for a user."""
    try:
        # Check if user already has write access
        current_lock = redis_client.get("write_lock")
        if current_lock == username:
            # User already has access, extend the lock
            redis_client.expire("write_lock", 10)  # 10 seconds timeout
            return True, "Write access extended"

        # Check if any user has write access
        if current_lock:
            # Add user to queue if not already in it
            if username not in redis_client.lrange("write_queue", 0, -1):
                redis_client.rpush("write_queue", username)
            queue_position = redis_client.llen("write_queue")
            return (
                False,
                f"Write access is currently held by another user. You are #{queue_position} in queue",
            )

        # No one has write access, grant it to this user
        redis_client.set("write_lock", username)
        redis_client.expire("write_lock", 10)  # 10 seconds timeout
        return True, "Write access granted"
    except Exception as e:
        print(f"Error requesting write access: {str(e)}")
        return False, str(e)


def get_next_user_in_queue(redis_client):
    """Get the next user in the write access queue."""
    try:
        return redis_client.lpop("write_queue")
    except Exception as e:
        print(f"Error getting next user in queue: {str(e)}")
        return None


def check_write_access(redis_client, username):
    """Check if user has write access."""
    try:
        current_lock = redis_client.get("write_lock")
        if current_lock == username:
            # Extend the lock
            redis_client.expire("write_lock", 10)  # 10 seconds timeout
            return True, "Write access maintained"
        return False, "You do not have write access"
    except Exception as e:
        print(f"Error checking write access: {str(e)}")
        return False, str(e)


def release_write_access(redis_client, username):
    """Release write access for a user."""
    try:
        current_lock = redis_client.get("write_lock")
        if current_lock == username:
            redis_client.delete("write_lock")
            return True, "Write access released"
        return False, "You do not have write access"
    except Exception as e:
        print(f"Error releasing write access: {str(e)}")
        return False, str(e)


def get_queue_status(redis_client):
    """Get current queue status."""
    if not redis_client:
        return [], []

    current_lock = redis_client.get("write_lock")
    queue = redis_client.lrange("write_queue", 0, -1)

    active_users = [current_lock] if current_lock else []
    queue_users = queue

    return active_users, queue_users

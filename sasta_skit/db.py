import redis

redis_client = redis.Redis(host="localhost", port=6379, db=0)


def send_message(user_id, message):
    """Send a message to a user's chat history.

    :param user_id: The ID of the user.
    :type user_id: int
    :param message: The message to be sent.
    :type message: str
    :return: None
    :raises: None
    """
    chat_key = f'chat:{user_id}'
    redis_client.lpush(chat_key, message)


def get_message_history(user_id):
    """Get the message history of a user.

    :param user_id: The ID of the user.
    :type user_id: int
    :return: list -- The message history of the user.
    :raises: None
    """
    chat_key = f"chat:{user_id}"
    return redis_client.lrange(chat_key, 0, -1)


def reset_database():
    """Reset the database.

    :return: None
    :raises: None
    """
    redis_client.flushdb()
    print("Database reset successful.")


# Example Usage
# if __name__ == "__main__":
#     user_id_1 = 1
#     user_id_2 = 2

#     reset_database()

#     # Sending messages
#     send_message(user_id_1, "Hi, how are you?")
#     send_message(user_id_2, "I'm good! How about you?")
#     send_message(user_id_1, "I'm good too!")
#     send_message(user_id_1, "What are you doing?")

#     # Getting message history
#     history_user_1 = get_message_history(user_id_1)
#     history_user_2 = get_message_history(user_id_2)

#     print("Message history for User 1:")
#     for msg in history_user_1:
#         print(msg.decode("utf-8"))

#     print("Message history for User 2:")
#     for msg in history_user_2:
#         print(msg.decode("utf-8"))

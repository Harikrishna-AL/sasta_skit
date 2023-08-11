import redis
import json
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


def dump_data_to_json(data, file_path):
    """Dump data to json.

    :param data: The data to be dumped.
    :type data: dict
    :param file_path: The path to the file where the data is to be dumped.
    :type file_path: str
    :return: None
    :raises: None
    """
    with open(file_path, "w") as f:
        json.dump(data, f)

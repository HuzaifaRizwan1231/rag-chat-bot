from utils.response_builder import ResponseBuilder
from config.db_config import DatabaseConnection


def insertChat():

    conn = DatabaseConnection().create_connection()
    cursor = conn.cursor()

    try:
        # Insert new chat and return the chatId
        cursor.execute("INSERT INTO chat (chat_id) VALUES (DEFAULT)")
        conn.commit()
        chatId = cursor.lastrowid

        # Retrieve the newly added row's columns other than the ID
        cursor.execute("SELECT * FROM chat WHERE chat_id = %s", (chatId,))
        new_chat = cursor.fetchone()

        chat_data = {
            "id": new_chat[0],
            "chat_title": new_chat[1],
            "created_at": new_chat[2],
        }

        return (
            ResponseBuilder()
            .setData(chat_data)
            .setSuccess(True)
            .setMessage("Chat Inserted Successfully")
            .setStatusCode(200)
            .build()
        )
    except Exception as e:
        response = (
            ResponseBuilder()
            .setSuccess(False)
            .setMessage("An Error Occured")
            .setError(str(e))
            .setStatusCode(500)
            .build()
        )
        # Logging the error
        print(response)
        return response

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def getAllChats():

    conn = DatabaseConnection().create_connection()
    cursor = conn.cursor()

    try:
        # Insert new chat and return the chatId
        cursor.execute("SELECT * FROM chat")
        chats = cursor.fetchall()

        chat_list = [
            {"id": chat[0], "title": chat[1], "created_at": chat[2]} for chat in chats
        ]

        return (
            ResponseBuilder()
            .setData(chat_list)
            .setSuccess(True)
            .setMessage("Chats Fetched Successfully")
            .setStatusCode(200)
            .build()
        )
    except Exception as e:
        response = (
            ResponseBuilder()
            .setSuccess(False)
            .setMessage("An Error Occured")
            .setError(str(e))
            .setStatusCode(500)
            .build()
        )
        # Logging the error
        print(response)
        return response

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def getAllMessagesOfChat(chatId):

    conn = DatabaseConnection().create_connection()
    cursor = conn.cursor()

    try:
        # Insert new chat and return the chatId
        cursor.execute("SELECT * FROM message WHERE chat_id = %s", (chatId,))
        messages = cursor.fetchall()

        message_list = [
            {"id": message[0], "text": message[1], "sender": message[2]}
            for message in messages
        ]

        return (
            ResponseBuilder()
            .setData(message_list)
            .setSuccess(True)
            .setMessage("Chats Fetched Successfully")
            .setStatusCode(200)
            .build()
        )
    except Exception as e:
        response = (
            ResponseBuilder()
            .setSuccess(False)
            .setMessage("An Error Occured")
            .setError(str(e))
            .setStatusCode(500)
            .build()
        )
        # Logging the error
        print(response)
        return response

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def insertMessage(message):

    conn = DatabaseConnection().create_connection()
    cursor = conn.cursor()

    try:
        # Insert new chat and return the chatId
        cursor.execute(
            "INSERT INTO message (content, sender, chat_id) VALUES (%s, %s, %s)",
            (message.text, message.sender, message.chatId),
        )

        conn.commit()

        return (
            ResponseBuilder()
            .setSuccess(True)
            .setMessage("Message Inserted Successfully")
            .setStatusCode(200)
            .build()
        )
    except Exception as e:
        response = (
            ResponseBuilder()
            .setSuccess(False)
            .setMessage("An Error Occured")
            .setError(str(e))
            .setStatusCode(500)
            .build()
        )
        # Logging the error
        print(response)
        return response

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def deleteChatRecord(chatId):

    conn = DatabaseConnection().create_connection()
    cursor = conn.cursor()

    try:
        # Insert new chat and return the chatId
        cursor.execute("DELETE FROM chat WHERE chat_id = %s", (chatId,))
        conn.commit()

        return (
            ResponseBuilder()
            .setSuccess(True)
            .setMessage("Chat Deleted Successfully")
            .setStatusCode(200)
            .build()
        )
    except Exception as e:
        response = (
            ResponseBuilder()
            .setSuccess(False)
            .setMessage("An Error Occured")
            .setError(str(e))
            .setStatusCode(500)
            .build()
        )
        # Logging the error
        print(response)
        return response

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def updateChatRecord(body):

    conn = DatabaseConnection().create_connection()
    cursor = conn.cursor()

    title = body.title
    chatId = body.chatId

    try:
        # Insert new chat and return the chatId
        cursor.execute(
            "UPDATE chat SET chat_title = %s WHERE chat_id = %s",
            (
                title,
                chatId,
            ),
        )
        conn.commit()

        return (
            ResponseBuilder()
            .setSuccess(True)
            .setMessage("Chat Updated Successfully")
            .setStatusCode(200)
            .build()
        )
    except Exception as e:
        response = (
            ResponseBuilder()
            .setSuccess(False)
            .setMessage("An Error Occured")
            .setError(str(e))
            .setStatusCode(500)
            .build()
        )
        # Logging the error
        print(response)
        return response

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

from pyrogram import Client, filters
from src import suzune as app

# Define a command handler to ban a user
@app.on_message(filters.command("ban", prefixes="/"))
def ban_user(client, message):
    # Check if the user is an admin
    if not message.from_user.is_admin:
        message.reply_text("You must be an admin to use this command.")
        return
    
    # Check if a user was replied to
    if message.reply_to_message and message.reply_to_message.from_user:
        # Ban the replied user
        client.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        message.reply_text("User has been banned.")
    else:
        # Check if a username/user ID was given in the command
        if len(message.command) == 2:
            username_or_id = message.command[1]
            try:
                user_id = int(username_or_id)
            except ValueError:
                # If it's not a valid user ID, assume it's a username
                user = client.get_users(username_or_id)
                if user:
                    user_id = user.id
                else:
                    message.reply_text("User not found.")
                    return
            # Ban the user by ID
            client.kick_chat_member(message.chat.id, user_id)
            message.reply_text("User has been banned.")
        else:
            message.reply_text("Please specify a user to ban.")

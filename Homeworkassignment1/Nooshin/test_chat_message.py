from chat_message import ChatMessage

# Create a new message
message = ChatMessage(
    "user",
    "How can I reduce emissions?"
)

# Display message information
print(message.get_role())
print(message.get_content())

# Change message information
message.set_role("assistant")
message.set_content("Use LED lights to save energy.")

# Display updated information
print(message.get_role())
print(message.get_content())
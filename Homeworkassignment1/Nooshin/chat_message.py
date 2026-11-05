class ChatMessage:

    def __init__(self, role, content):
        self.role = role
        self.content = content

    # Getter for role
    def get_role(self):
        return self.role

    # Setter for role
    def set_role(self, role):
        self.role = role

    # Getter for content
    def get_content(self):
        return self.content

    # Setter for content
    def set_content(self, content):
        self.content = content
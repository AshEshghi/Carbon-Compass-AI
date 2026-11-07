
class AssistantPage:
    def __init__(self, question):
        self.question = question
        self.response = "No response yet"

    def get_question(self):
        return self.question

    def set_question(self, question):
        self.question = question

    def get_response(self):
        return self.response

    def set_response(self, response):
        self.response = response

    def submit_question(self):
        return self.question

    def render_response(self):
        return self.response


if __name__ == "__main__":
    assistant = AssistantPage(
        "How can we reduce electricity consumption?"
    )

    print("User question:", assistant.submit_question())
    print("AI response:", assistant.render_response())

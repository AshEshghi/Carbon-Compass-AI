
class AppController:
    def __init__(self, current_page):
        self.current_page = current_page

    def get_current_page(self):
        return self.current_page

    def set_current_page(self, page):
        self.current_page = page

    def route_page(self):
        return self.current_page

    def call_service(self, service, *args):
        return service(*args)


if __name__ == "__main__":
    app = AppController("Dashboard")

    print(app.route_page())

    app.set_current_page("Analytics")
    print(app.route_page())

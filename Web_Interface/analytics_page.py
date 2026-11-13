
class AnalyticsPage:
    def __init__(self, selected_period):
        self.selected_period = selected_period
        self.emissions = []

    def get_selected_period(self):
        return self.selected_period

    def set_selected_period(self, period):
        self.selected_period = period

    def get_emissions(self):
        return self.emissions

    def set_emissions(self, emissions):
        self.emissions = emissions

    def select_period(self):
        return self.selected_period

    def render_charts(self):
        return self.emissions


if __name__ == "__main__":
    analytics = AnalyticsPage("January 2026")
    analytics.set_emissions([12, 15, 10, 18])

    print(analytics.select_period())
    print(analytics.render_charts())

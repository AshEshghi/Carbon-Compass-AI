
class DashboardPage:
    def __init__(self, title, total_kwh, total_co2):
        self.title = title
        self.total_kwh = total_kwh
        self.total_co2 = total_co2

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def get_total_kwh(self):
        return self.total_kwh

    def set_total_kwh(self, value):
        self.total_kwh = value

    def get_total_co2(self):
        return self.total_co2

    def set_total_co2(self, value):
        self.total_co2 = value

    def render_kpis(self):
        print("Total Electricity:", self.total_kwh, "kWh")
        print("Total CO2 Emissions:", self.total_co2, "kg CO2e")

    def render_summary(self):
        print("Dashboard:", self.title)


if __name__ == "__main__":
    dashboard = DashboardPage("Carbon Compass AI", 120, 48)

    dashboard.render_summary()
    dashboard.render_kpis()

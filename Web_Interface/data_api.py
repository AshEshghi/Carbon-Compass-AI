import requests

BASE_URL = "http://127.0.0.1:5050"


def get_records():
    try:
        response = requests.get(
            f"{BASE_URL}/records",
            params={
                "start_date": "2016-01-01",
                "end_date": "2016-09-30"
            },
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException:
        return None
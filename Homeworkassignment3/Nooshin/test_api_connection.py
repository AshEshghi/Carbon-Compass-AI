
from context_provider import ContextProvider

context = ContextProvider()

try:
    records = context.get_api_records()
    print("API connection successful!")
    print("Records:", records)

except Exception as error:
    print("API connection failed:")
    print(error)

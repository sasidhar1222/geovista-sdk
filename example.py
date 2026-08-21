from mycompany import MyCompanyClient
from mycompany.exceptions import AuthenticationError


client = MyCompanyClient(
    api_key="test-api-key",
    base_url="http://127.0.0.1:8000",
    max_retries=0
)

try:

    users = client.users.list()

    print("Request successful:")
    print(users)

except AuthenticationError as error:

    print("Authentication Error:")
    print(error)

finally:

    client.close()
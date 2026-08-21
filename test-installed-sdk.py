from mycompany import MyCompanyClient


client = MyCompanyClient(
    api_key="test-api-key",
    base_url="http://127.0.0.1:8000"
)

try:

    users = client.users.list()

    print("Users:")

    for user in users.items:
        print(
            f"{user.id} - "
            f"{user.name} - "
            f"{user.email}"
        )

finally:

    client.close()
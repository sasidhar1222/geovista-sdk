import asyncio

from mycompany import AsyncMyCompanyClient


async def main():

    client = AsyncMyCompanyClient(
        api_key="test-api-key",
        base_url="http://127.0.0.1:8000"
    )

    try:

        # This is where await is used
        users = await client.users.list()

        print("--- ASYNC USERS ---")

        for user in users.items:
            print(
                f"{user.id} - "
                f"{user.name} - "
                f"{user.email}"
            )

    finally:

        await client.close()


asyncio.run(main())
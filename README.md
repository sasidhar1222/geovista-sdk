# MyCompany SDK

Python SDK for interacting with the MyCompany API.

## Installation

```bash
pip install mycompany-sdk
```

## Basic Usage

```python
from mycompany import MyCompanyClient

client = MyCompanyClient(
    api_key="your-api-key",
    base_url="http://127.0.0.1:8000"
)

users = client.users.list()

for user in users.items:
    print(user.name)

client.close()
```

## Async Usage

```python
import asyncio

from mycompany import AsyncMyCompanyClient


async def main():

    client = AsyncMyCompanyClient(
        api_key="your-api-key",
        base_url="http://127.0.0.1:8000"
    )

    try:

        users = await client.users.list()

        for user in users.items:
            print(user.name)

    finally:

        await client.close()


asyncio.run(main())
```

## Features

- User CRUD
- Pagination
- Filtering
- Query parameters
- API key authentication
- Retry handling
- Custom exceptions
- Logging
- Async support

## Example

### Get Users

```python
from mycompany import MyCompanyClient

client = MyCompanyClient(
    api_key="your-api-key",
    base_url="http://127.0.0.1:8000"
)

response = client.users.list()

for user in response.items:
    print(user.id)
    print(user.name)
    print(user.email)

client.close()
```

### Filtering

```python
from mycompany import MyCompanyClient
from mycompany.models import UserFilter


client = MyCompanyClient(
    api_key="your-api-key",
    base_url="http://127.0.0.1:8000"
)

filters = UserFilter(
    name="Sasi"
)

response = client.users.list(
    page=1,
    page_size=10,
    filters=filters
)

for user in response.items:
    print(user.name)

client.close()
```

### Sorting

```python
from mycompany import MyCompanyClient
from mycompany.models import UserFilter


client = MyCompanyClient(
    api_key="your-api-key",
    base_url="http://127.0.0.1:8000"
)

filters = UserFilter(
    sort_by="name",
    sort_order="asc"
)

response = client.users.list(
    page=1,
    page_size=10,
    filters=filters
)

for user in response.items:
    print(user.name)

client.close()
```

## Error Handling

```python
from mycompany import MyCompanyClient
from mycompany.exceptions import (
    AuthenticationError,
    NotFoundError,
    ValidationError,
    NetworkError
)


client = MyCompanyClient(
    api_key="your-api-key",
    base_url="http://127.0.0.1:8000"
)

try:

    user = client.users.get(99999)

except AuthenticationError as error:

    print("Authentication error:")
    print(error)

except NotFoundError as error:

    print("User not found:")
    print(error)

except ValidationError as error:

    print("Validation error:")
    print(error)

except NetworkError as error:

    print("Network error:")
    print(error)

finally:

    client.close()
```

## Development

Run the test suite:

```bash
pytest -v
```

Build the package:

```bash
python -m build
```
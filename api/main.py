from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel


app = FastAPI(
    title="MyCompany API",
    version="1.0.0"
)


# ==========================================
# API KEY
# ==========================================

VALID_API_KEY = "test-api-key"


# ==========================================
# DATABASE - TEMPORARY IN-MEMORY DATA
# ==========================================

users = [
    {
        "id": 1,
        "name": "Sasi",
        "email": "sasi@example.com"
    },
    {
        "id": 2,
        "name": "John",
        "email": "john@example.com"
    }
]


next_user_id = 3


# ==========================================
# MODELS
# ==========================================

class UserCreate(BaseModel):

    name: str

    email: str


class UserUpdate(BaseModel):

    name: str

    email: str


# ==========================================
# AUTHENTICATION
# ==========================================

def validate_api_key(
    authorization: str | None
):

    if authorization is None:

        raise HTTPException(
            status_code=401,
            detail="Authorization header is missing"
        )

    expected = f"Bearer {VALID_API_KEY}"

    if authorization != expected:

        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )


# ==========================================
# GET USERS
# PAGINATION + FILTERING
# ==========================================

@app.get("/api/users")
def get_users(
    page: int = 1,
    page_size: int = 10,
    search: str | None = None,
    name: str | None = None,
    email: str | None = None,
    authorization: str | None = Header(default=None)
):

    # Authentication
    validate_api_key(authorization)

    # Validate pagination
    if page < 1:

        raise HTTPException(
            status_code=400,
            detail="Page must be greater than 0"
        )

    if page_size < 1:

        raise HTTPException(
            status_code=400,
            detail="Page size must be greater than 0"
        )

    # ======================================
    # FILTER USERS
    # ======================================

    filtered_users = users.copy()

    # Search name OR email
    if search:

        search_value = search.lower()

        filtered_users = [
            user
            for user in filtered_users
            if search_value in user["name"].lower()
            or search_value in user["email"].lower()
        ]

    # Filter by name
    if name:

        name_value = name.lower()

        filtered_users = [
            user
            for user in filtered_users
            if name_value in user["name"].lower()
        ]

    # Filter by email
    if email:

        email_value = email.lower()

        filtered_users = [
            user
            for user in filtered_users
            if email_value in user["email"].lower()
        ]

    # ======================================
    # PAGINATION
    # ======================================

    total = len(filtered_users)

    start = (page - 1) * page_size

    end = start + page_size

    paginated_users = filtered_users[start:end]

    # ======================================
    # RESPONSE
    # ======================================

    return {
        "items": paginated_users,
        "page": page,
        "page_size": page_size,
        "total": total
    }


# ==========================================
# GET ONE USER
# ==========================================

@app.get("/api/users/{user_id}")
def get_user(
    user_id: int,
    authorization: str | None = Header(default=None)
):

    validate_api_key(authorization)

    for user in users:

        if user["id"] == user_id:

            return user

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


# ==========================================
# CREATE USER
# ==========================================

@app.post("/api/users")
def create_user(
    user: UserCreate,
    authorization: str | None = Header(default=None)
):

    global next_user_id

    validate_api_key(authorization)

    new_user = {
        "id": next_user_id,
        "name": user.name,
        "email": user.email
    }

    users.append(new_user)

    next_user_id += 1

    return new_user


# ==========================================
# UPDATE USER
# ==========================================

@app.put("/api/users/{user_id}")
def update_user(
    user_id: int,
    user: UserUpdate,
    authorization: str | None = Header(default=None)
):

    validate_api_key(authorization)

    for existing_user in users:

        if existing_user["id"] == user_id:

            existing_user["name"] = user.name

            existing_user["email"] = user.email

            return existing_user

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


# ==========================================
# DELETE USER
# ==========================================

@app.delete("/api/users/{user_id}")
def delete_user(
    user_id: int,
    authorization: str | None = Header(default=None)
):

    validate_api_key(authorization)

    for index, user in enumerate(users):

        if user["id"] == user_id:

            deleted_user = users.pop(index)

            return {
                "message": "User deleted successfully",
                "user": deleted_user
            }

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

app = FastAPI(
    title="GeoVista API",
    version="1.0.0"
)

VALID_API_KEY = "test-api-key"

# In-memory database for Datasets
datasets = [
    {
        "id": "ds_1",
        "name": "Default Dataset",
        "description": "Initial sample dataset",
        "public": True,
        "category": "computer-vision",
        "metadata": {}
    }
]

next_ds_id = 2


class DatasetCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    category: Optional[str] = None
    public: Optional[bool] = False
    metadata: Optional[Dict[str, Any]] = None


class DatasetUpdate(BaseModel):
    description: Optional[str] = None
    category: Optional[str] = None
    public: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None


def validate_api_key(authorization: Optional[str]):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header is missing")

    expected = f"Bearer {VALID_API_KEY}"
    if authorization != expected:
        raise HTTPException(status_code=401, detail="Invalid API key")


@app.get("/api/datasets")
def get_datasets(
    page: int = 1,
    per_page: int = 10,
    name: Optional[str] = None,
    authorization: Optional[str] = Header(default=None)
):
    validate_api_key(authorization)
    filtered = datasets
    if name:
        filtered = [d for d in filtered if name.lower() in d["name"].lower()]

    start = (page - 1) * per_page
    end = start + per_page

    return {
        "items": filtered[start:end],
        "page": page,
        "per_page": per_page,
        "total": len(filtered)
    }


@app.post("/api/datasets", status_code=201)
def create_dataset(
    dataset: DatasetCreate,
    authorization: Optional[str] = Header(default=None)
):
    global next_ds_id
    validate_api_key(authorization)

    new_ds = {
        "id": f"ds_{next_ds_id}",
        "name": dataset.name,
        "description": dataset.description or "",
        "category": dataset.category,
        "public": dataset.public or False,
        "metadata": dataset.metadata or {}
    }
    datasets.append(new_ds)
    next_ds_id += 1
    return new_ds


@app.get("/api/datasets/{dataset_id}")
def get_dataset(
    dataset_id: str,
    authorization: Optional[str] = Header(default=None)
):
    validate_api_key(authorization)
    for d in datasets:
        if d["id"] == dataset_id:
            return d
    raise HTTPException(status_code=404, detail="Dataset not found")


@app.patch("/api/datasets/{dataset_id}")
def update_dataset(
    dataset_id: str,
    updates: DatasetUpdate,
    authorization: Optional[str] = Header(default=None)
):
    validate_api_key(authorization)
    for d in datasets:
        if d["id"] == dataset_id:
            if updates.description is not None:
                d["description"] = updates.description
            if updates.category is not None:
                d["category"] = updates.category
            if updates.public is not None:
                d["public"] = updates.public
            if updates.metadata is not None:
                d["metadata"] = updates.metadata
            return d
    raise HTTPException(status_code=404, detail="Dataset not found")


@app.delete("/api/datasets/{dataset_id}")
def delete_dataset(
    dataset_id: str,
    authorization: Optional[str] = Header(default=None)
):
    validate_api_key(authorization)
    for i, d in enumerate(datasets):
        if d["id"] == dataset_id:
            deleted = datasets.pop(i)
            return {"message": "Dataset deleted", "dataset": deleted}
    raise HTTPException(status_code=404, detail="Dataset not found")
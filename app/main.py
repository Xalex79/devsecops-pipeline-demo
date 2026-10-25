"""Minimal API used to demonstrate a DevSecOps CI/CD pipeline."""

from fastapi import FastAPI, HTTPException

app = FastAPI(title="DevSecOps Pipeline Demo", version="0.1.0")

ITEMS: dict[int, dict[str, str | int]] = {
    1: {"id": 1, "name": "build"},
    2: {"id": 2, "name": "test"},
    3: {"id": 3, "name": "scan"},
}


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check used by the container healthcheck."""
    return {"status": "ok"}


@app.get("/items")
def list_items() -> list[dict[str, str | int]]:
    return list(ITEMS.values())


@app.get("/items/{item_id}")
def get_item(item_id: int) -> dict[str, str | int]:
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail="Item not found")
    return ITEMS[item_id]


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, Any
import os

# NOTE: boto3 is available in Lambda runtime by default.
try:
    import boto3
    from botocore.exceptions import ClientError
except Exception:  # pragma: no cover
    boto3 = None
    ClientError = Exception  # type: ignore

app = FastAPI(title="MyApp API (Lambda + FastAPI)")

# CORS is also configured at the Lambda Function URL level in SAM template,
# but this app-level CORS helps for local testing with uvicorn.
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if ALLOWED_ORIGINS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "up"}

# Simple DynamoDB table operations (optional)
TABLE_NAME = os.environ.get("DDB_TABLE", "")

def _table():
    if not TABLE_NAME:
        raise RuntimeError("DDB_TABLE env var not set")
    if boto3 is None:
        raise RuntimeError("boto3 is not available")
    ddb = boto3.resource("dynamodb")
    return ddb.Table(TABLE_NAME)

@app.put("/items/{pk}")
def put_item(pk: str, body: Optional[Dict[str, Any]] = None):
    if not TABLE_NAME:
        raise HTTPException(500, "DDB_TABLE not configured")
    item = {"pk": pk, **(body or {})}
    try:
        _table().put_item(Item=item)
        return {"ok": True, "item": item}
    except ClientError as e:  # pragma: no cover
        raise HTTPException(500, f"DynamoDB error: {e}")

@app.get("/items/{pk}")
def get_item(pk: str):
    if not TABLE_NAME:
        raise HTTPException(500, "DDB_TABLE not configured")
    try:
        res = _table().get_item(Key={"pk": pk})
        if "Item" not in res:
            raise HTTPException(404, "Not found")
        return res["Item"]
    except ClientError as e:  # pragma: no cover
        raise HTTPException(500, f"DynamoDB error: {e}")

# Lambda handler via Mangum
try:
    from mangum import Mangum
    handler = Mangum(app)  # SAM Handler points to: app.main.handler
except Exception:
    # Local run without Mangum installed: allow 'uvicorn app.main:app'
    handler = None

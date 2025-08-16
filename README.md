
# MVP: FastAPI on AWS Lambda (Function URL) + DynamoDB (Free Tier)

This is a minimal backend to pair with a Next.js frontend. It uses FastAPI wrapped by Mangum to run on AWS Lambda with a **Function URL** (no API Gateway needed). Data persistence uses **DynamoDB** (free tier).

## Prerequisites
- AWS account + IAM user/role with permissions to deploy.
- **AWS CLI** + **AWS SAM CLI** installed.
- Python 3.12 locally.
- (Optional) Docker, for consistent builds: `sam build --use-container`.

## Deploy (first time)
```bash
# 1) Build (uses SAM to vendor dependencies)
sam build --use-container

# 2) Deploy (guided prompts the first time)
sam deploy --guided
# Stack name: myapp-api
# Region: eu-central-1 (Frankfurt) or your choice
# Confirm changeset: y
```

After deploy, note the **FunctionUrl** output. This is your public API base, e.g.
`https://xxxxx.lambda-url.eu-central-1.on.aws`

## Try it
```bash
curl -s $FUNCTION_URL/health
# -> {"status":"up"}

# Create an item
curl -X PUT "$FUNCTION_URL/items/user_123" -H "Content-Type: application/json" -d '{"name":"Alice"}'

# Fetch it back
curl "$FUNCTION_URL/items/user_123"
```

## Local run (optional)
```bash
pip install -r backend/fastapi_lambda/requirements.txt
uvicorn app.main:app --reload --port 8000 --app-dir backend/fastapi_lambda
```

## Notes
- CORS is permissive for MVP. Lock it down by setting `ALLOWED_ORIGINS` and tightening Function URL CORS.
- DynamoDB table throughput is set to 1 RCU / 1 WCU to stay within the Free Tier.
- For production, consider API Gateway or CloudFront in front of the Function URL, and proper auth (Cognito or signed JWT).

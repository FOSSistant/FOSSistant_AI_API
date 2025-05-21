import time

from fastapi import FastAPI, Request, Depends
from pydantic import BaseModel

from transformers import pipeline

from app.auth import get_api_key


class Issue(BaseModel):
    title: str
    body: str | None = None


class Issues(BaseModel):
    issues: list[Issue]


model = pipeline(
    "text-classification",
    model="models/fossistant-v0.1.0",
)

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.post("/v1/fossistant/difficulty/")
async def predict_difficulty(issues: Issues | Issue, api_key: str = Depends(get_api_key)):
    if isinstance(issues, Issues):
        results = []

        for issue in issues.issues:
            if issue.body:
                text = issue.title.strip() + " " + issue.body.strip()
            else:
                text = issue.title.strip()

            result = model(text, max_length=512, truncation=True)
            results.append(
                {
                    "difficulty": result[0]["label"],
                    "score": result[0]["score"],
                }
            )
    else:
        if issues.body:
            text = issues.title.strip() + " " + issues.body.strip()
        else:
            text = issues.title.strip()

        result = model(text, max_length=512, truncation=True)
        results = {
            "difficulty": result[0]["label"],
            "score": result[0]["score"],
        }

    return results

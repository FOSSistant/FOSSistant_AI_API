import time

from functools import lru_cache

from fastapi import FastAPI, Request
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from transformers import pipeline


class Settings(BaseSettings):
    model: str = "FOSSistant-Difficulty-Prediction-v0.3.0"

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()


class Issue(BaseModel):
    title: str
    body: str | None = None


class Issues(BaseModel):
    model: str = settings.model
    issues: list[Issue]


class Difficulty(BaseModel):
    difficulty: str
    score: float


class Difficulties(BaseModel):
    model: str
    results: list[Difficulty]


model = pipeline(
    "text-classification",
    model=f"models/{settings.model}",
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
async def predict_difficulty(issues: Issues) -> Difficulties:
    INPUT_TEMPLATE = "Title: {title}\nBody: {body}"

    results = []

    for issue in issues.issues:
        text = INPUT_TEMPLATE.format(
            title=issue.title,
            body=issue.body or "",
        )

        result = model(text, max_length=1024, truncation=True)
        results.append(
            Difficulty(
                difficulty=result[0]["label"],
                score=result[0]["score"],
            ),
        )

    response = Difficulties(model=issues.model, results=results)

    return response

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import pandas as pd
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI(
    title="hospital-readmisson-api", 
    description="API for accessing hospital-readmisson dataset",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


df = pd.read_csv("data/diabetic_data.csv", na_values=['?', '[]'], low_memory=False)


@app.get("/")
def home():
    return {
        "message": "Dataset API",
        "total_records": len(df),
        "columns":df.columns.tolist()

    }


@app.get("/data")
def get_data(
    limit: int = Query(1000, description="Records per page"),
    offset: int = Query(0, description="Starting Position")
):
    if limit > 5000:
        limit = 5000

    page_data = df.iloc[offset:offset+limit]

    page_data = page_data.replace([float('inf'), float('-inf')], None)
    page_data = page_data.where(pd.notna(page_data), None)

    return {
        "total_records": len(df),
        "limit": limit,
        "offset": offset,
        "returned_records": len(page_data),
        "has_more": (offset + limit) < len(df),
        "data": page_data.to_dict(orient='records')
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
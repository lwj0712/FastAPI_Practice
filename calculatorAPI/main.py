from fastapi import FastAPI

app = FastAPI()


@app.get("/calculate/add/{a}/{b}")
async def add(a: int, b: int):
    return {"연산 결과": a + b}


@app.get("/calculate/sub/{a}/{b}")
async def subtract(a: int, b: int):
    return {"연산 결과": a - b}


@app.get("/calculate/mul/{a}/{b}")
async def multiply(a: int, b: int):
    return {"연산 결과": a * b}


@app.get("/calculate/div/{a}/{b}")
async def divide(a: int, b: int):
    return {"연산 결과": a / b}

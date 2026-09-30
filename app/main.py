from fastapi import FastAPI

from app.users.router import router as users_router
from app.products.router import router_product, router_category

app = FastAPI()
app.include_router(users_router)
app.include_router(router_product)
app.include_router(router_category)


@app.get('/health')
def health_check():
    return {'status':'all good'}
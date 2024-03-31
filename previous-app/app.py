from fastapi import FastAPI
from api.users import router_users

import uvicorn

app = FastAPI(debug=True)

app.include_router(router=router_users, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
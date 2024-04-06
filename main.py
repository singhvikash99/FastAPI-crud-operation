from fastapi import FastAPI
from fastapi.responses import RedirectResponse, JSONResponse
from routers import student




app = FastAPI(title="Backend Developer Assesment Test",
              version="0.1.1"
    )




@app.get('/', include_in_schema=False)
def index():
    return (RedirectResponse('/docs'))

app.include_router(student.router)

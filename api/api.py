from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from tool.IMEI import real_check_imei
from tool.functions import check_imei, is_valid_token

app = FastAPI()

class CheckImeiRequest(BaseModel):
    imei: str
    token: str

@app.post("/api/check-imei")
async def api_check_imei(request: CheckImeiRequest):
    if is_valid_token(request.token):
        raise HTTPException(status_code=403, detail="Unauthorized token")


    if check_imei(request.imei):
        raise HTTPException(status_code=400, detail="Invalid IMEI format")


    return {"status": "success", "imei": real_check_imei(request.imei)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import httpx
import os
from pydantic import BaseModel

app = FastAPI(title="Yandex IoT Bridge")

# Получаем переменные окружения
YANDEX_TOKEN = os.getenv("YANDEX_TOKEN")
DEVICE_ID = os.getenv("DEVICE_ID", "ca02d1ae-9ee6-4bdb-bba5-aa451bcd241f")

class DeviceCommand(BaseModel):
    action: str  # "on" или "off"

@app.get("/")
async def root():
    return {"status": "ok", "message": "Yandex IoT Bridge is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/control")
async def control_device(command: DeviceCommand):
    """
    Управление розеткой
    POST /control
    Body: {"action": "on"} или {"action": "off"}
    """
    if not YANDEX_TOKEN:
        raise HTTPException(status_code=500, detail="YANDEX_TOKEN not configured")
    
    if command.action not in ["on", "off"]:
        raise HTTPException(status_code=400, detail="Action must be 'on' or 'off'")
    
    # Формируем запрос к Яндекс Smart Home API
    url = f"https://api.yandex.net/smart-home/v1/devices/{DEVICE_ID}/control"
    
    headers = {
        "Authorization": f"OAuth {YANDEX_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "command": "turn_on" if command.action == "on" else "turn_off"
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "action": command.action,
                    "device_id": DEVICE_ID,
                    "response": response.json()
                }
            else:
                return JSONResponse(
                    status_code=response.status_code,
                    content={
                        "status": "error",
                        "message": f"Yandex API error: {response.text}",
                        "status_code": response.status_code
                    }
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")

@app.get("/control/on")
async def turn_on():
    """Простой GET запрос для включения"""
    return await control_device(DeviceCommand(action="on"))

@app.get("/control/off")
async def turn_off():
    """Простой GET запрос для выключения"""
    return await control_device(DeviceCommand(action="off"))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

import os
import logging
from fastapi import FastAPI, Request, HTTPException
import uvicorn

# 初始化 FastAPI
app = FastAPI()
logging.basicConfig(level=logging.INFO)

# 从环境变量读取配置（在你的容器管理后台设置这些变量）
WEBHOOK_PASSPHRASE = os.getenv("WEBHOOK_PASSPHRASE", "my_secret_token")

@app.get("/")
async def root():
    return {"message": "Bot is running"}

@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
    except:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # 1. 验证密钥
    if data.get("passphrase") != WEBHOOK_PASSPHRASE:
        logging.warning("Unauthorized access attempt")
        raise HTTPException(status_code=403, detail="Invalid passphrase")

    # 2. 打印接收到的数据（方便你在日志里排查）
    logging.info(f"Received Signal: {data}")

    # 3. 这里接入你现有的开仓逻辑
    # 示例: 
    # symbol = data.get("symbol")
    # side = data.get("side")
    # your_trading_logic(symbol, side)

    return {"status": "success", "received": data}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

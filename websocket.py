from fastapi import FastAPI, WebSocket
import asyncio
import httpx

app = FastAPI()

# 클라이언트의 WebSocket 객체를 저장하는 딕셔너리
client_connections = {}

# 웹 소켓 연결을 처리하는 핸들러
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # 클라이언트의 WebSocket 객체를 저장
        client_connections[id(websocket)] = websocket

        # 클라이언트로부터 메시지를 수신하는 루프
        while True:
            # 클라이언트로부터 메시지 수신
            data = await websocket.receive_text()

            # 클라이언트로부터 'send' 메시지를 수신했을 때마다 백그라운드 작업 시작
            if data == "send":
                await send_progress_until_done(websocket)
                break  # 작업이 완료되면 루프 종료
    except Exception as e:
        print(e)
    finally:
        # 연결이 종료되면 해당 WebSocket 객체를 딕셔너리에서 제거
        del client_connections[id(websocket)]

# 백그라운드 작업: 클라이언트에게 진행 상황을 보냄
async def send_progress_until_done(websocket: WebSocket):
    while True:
        await asyncio.sleep(10)
        # GPU 서버로부터 진행 상황을 가져와 클라이언트에게 전송
        progress_info = await get_progress_from_gpu_server()
        await websocket.send_text(progress_info)

        # 작업이 완료되었으면 루프 종료
        if progress_info[0] == 100:
            break

        await asyncio.sleep(10)  # 10초마다 한 번씩 반복

# GPU 서버로부터 진행 상황을 가져오는 함수
async def get_progress_from_gpu_server():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://163.180.117.43:9003")
        progress_info = response.json()  # JSON 형식의 응답을 파싱하여 진행 정보 추출
        print(progress_info)
        return progress_info

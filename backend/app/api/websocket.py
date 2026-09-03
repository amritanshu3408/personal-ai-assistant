import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.agents.conversation import ConversationAgent
from app.core.router import classify_intent
from app.utils.logger import logger

router = APIRouter()
agent = ConversationAgent()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket client connected")
    history = []

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                data = {"type": "text", "content": raw}

            msg_type = data.get("type", "text")
            content = data.get("content", "")

            if msg_type == "ping":
                await websocket.send_json({"type": "pong"})
                continue

            if not content:
                continue

            intent = classify_intent(content)
            await websocket.send_json({"type": "intent", "intent": intent})

            async for event in agent.handle(content, context={"history": history}):
                await websocket.send_json(event)
                if event.get("type") == "final":
                    history.append({"role": "user", "content": content})
                    history.append({"role": "assistant", "content": event["content"]})
                    # keep history bounded
                    if len(history) > 40:
                        history = history[-40:]

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.exception("WebSocket error")
        try:
            await websocket.send_json({"type": "error", "message": str(e)})
        except Exception:
            pass

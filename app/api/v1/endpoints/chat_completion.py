from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import JSONResponse
from app.schemas.chat import ChatCompletionRequest, ChatCompletionResponse
from app.core.utils.request_id import get_request_id
from app.core.utils.prompt import extract_last_user_prompt
from app.core.dependencies import get_inference_service
from app.services.inference import InferenceService

router = APIRouter()


@router.post("/completions", response_model=ChatCompletionResponse)
async def chat_completions(
    request: Request,
    body: ChatCompletionRequest,
    inference_service: InferenceService = Depends(get_inference_service)
):
    rid = get_request_id(request)
    messages_dicts = [m.model_dump() for m in body.messages]
    prompt = extract_last_user_prompt(messages_dicts)

    payload = {
        "model": body.model,
        "messages": messages_dicts,
    }

    result = await inference_service.process_inference(
        payload=payload,
        prompt=prompt,
        request_id=rid
    )

    return JSONResponse(
        content=result,
        headers={"X-Request-Id": rid}
    )

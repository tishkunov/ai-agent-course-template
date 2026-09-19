"""Ручки приёма и чтения обращения (M1.4, M1.7, M1.8).

Роуты только валидируют вход схемой и делегируют в сервис — ни доступа к БД,
ни бизнес-логики, ни try/except по месту.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status

from app.api.deps import IntakeServiceDep, ReadServiceDep
from app.core.security import require_api_key, require_operator
from app.schemas.request import RequestCreate, RequestOut

router = APIRouter(tags=["requests"])


@router.post(
    "/requests",
    response_model=RequestOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_api_key)],
)
async def create_request(
    payload: RequestCreate,
    service: IntakeServiceDep,
    response: Response,
) -> RequestOut:
    result = await service.accept(payload)
    response.status_code = status.HTTP_201_CREATED if result.is_new else status.HTTP_200_OK
    return RequestOut.model_validate(result.request)


@router.get(
    "/requests/{request_id}",
    response_model=RequestOut,
    dependencies=[Depends(require_operator)],
)
async def get_request(request_id: str, service: ReadServiceDep) -> RequestOut:
    obj = await service.get(request_id)
    return RequestOut.model_validate(obj)

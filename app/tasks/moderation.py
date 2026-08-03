import asyncio
from app.core.celery_app import celery_app
from app.db.session import AsyncSessionLocal
from app.models.moderation import ModerationRequest, ModerationResult, ModerationStatus
from app.services.moderation import analyze_content


@celery_app.task(bind=True, max_retries=3)
def process_moderation(self, request_id: str):
    """
    Celery задача для обработки запроса на модерацию.
    bind=True даёт доступ к self для retry логики.
    max_retries=3 — попробует 3 раза если OpenAI недоступен.
    """
    asyncio.run(_process_moderation_async(self, request_id))


async def _process_moderation_async(task, request_id: str):
    async with AsyncSessionLocal() as session:
        # Получаем запрос из БД
        request = await session.get(ModerationRequest, request_id)
        if not request:
            return

        # Обновляем статус на PROCESSING
        request.status = ModerationStatus.PROCESSING
        await session.commit()

        try:
            # Вызываем OpenAI
            result_data = await analyze_content(request.content)

            # Сохраняем результат
            result = ModerationResult(
                request_id=request.id,
                is_toxic=result_data["is_toxic"],
                toxicity_score=result_data["toxicity_score"],
                categories=result_data.get("categories", {}),
            )
            session.add(result)

            # Обновляем статус на COMPLETED
            request.status = ModerationStatus.COMPLETED
            await session.commit()

        except Exception as exc:
            request.status = ModerationStatus.FAILED
            await session.commit()
            # Retry через 5 секунд если что-то пошло не так
            raise task.retry(exc=exc, countdown=5)
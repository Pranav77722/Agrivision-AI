import uuid
import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_optional, get_current_user
from app.models.user import User
from app.repositories.diagnosis_repo import DiagnosisRepository
from app.repositories.report_repo import ReportRepository
from app.schemas.report import ReportResponse, ReportListResponse, ReportGenerateRequest
from app.services.report_service import ReportService
from app.services.storage_service import get_storage_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/reports", tags=["PDF Diagnostic Reports"])


@router.post(
    "/generate/{diagnosis_id}",
    response_model=ReportResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate PDF diagnosis report",
    description="Generate a PDF diagnostic report with Agrivision AI+ branding, crop pathology assessment, and treatment table."
)
async def generate_report(
    diagnosis_id: uuid.UUID,
    req: ReportGenerateRequest = ReportGenerateRequest(),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
) -> ReportResponse:
    diag_repo = DiagnosisRepository(db)
    diagnosis = await diag_repo.get(diagnosis_id)
    if not diagnosis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnosis record not found.",
        )

    report_service = ReportService()
    report_url = await report_service.generate_diagnostic_report(
        diagnosis=diagnosis,
        user=current_user,
        language=req.language
    )

    report_repo = ReportRepository(db)
    user_id = current_user.id if current_user else None
    report = await report_repo.create(
        user_id=user_id,
        diagnosis_id=diagnosis_id,
        report_url=report_url,
        language=req.language
    )

    return ReportResponse.model_validate(report)


@router.get(
    "/",
    response_model=ReportListResponse,
    summary="List generated PDF reports",
    description="Retrieve all previously generated diagnostic PDF reports for the authenticated farmer."
)
async def list_reports(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> ReportListResponse:
    repo = ReportRepository(db)
    items, total = await repo.list_for_user(
        user_id=current_user.id,
        page=page,
        page_size=page_size
    )
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1

    return ReportListResponse(
        items=[ReportResponse.model_validate(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get(
    "/{id}/download",
    summary="Download PDF report",
    description="Download the generated PDF report directly or redirect to its storage URL."
)
async def download_report(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    repo = ReportRepository(db)
    report = await repo.get(id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found.",
        )

    storage = get_storage_service()
    local_path = await storage.get_file_path(report.report_url)
    if local_path and local_path.exists():
        return FileResponse(
            path=str(local_path),
            filename=f"Agrivision_Report_{str(id)[:8]}.pdf",
            media_type="application/pdf"
        )

    # If hosted on Supabase or CDN
    return RedirectResponse(url=report.report_url)

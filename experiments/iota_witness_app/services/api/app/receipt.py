from __future__ import annotations

from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from pydantic import BaseModel
from sqlmodel import Session

from app.db import get_session
from app.receipt_generator import generate_receipt

router = APIRouter()


class ReceiptRequest(BaseModel):
    entry_kind: str                        # "season" | "moment"
    eden_text: str
    modal: dict[str, Any]
    attestation: dict[str, Any]
    local_mode: bool = False
    crisis_flag: bool = False
    created_at: datetime
    entry_id: str
    include_original_text: bool = False
    original_text: str | None = None


@router.post("/v1/receipt")
def create_receipt(
    payload: ReceiptRequest,
    session: Session = Depends(get_session),  # noqa: B008
) -> Response:
    pdf_bytes = generate_receipt(
        entry_kind=payload.entry_kind,
        eden_text=payload.eden_text,
        modal=payload.modal,
        attestation=payload.attestation,
        local_mode=payload.local_mode,
        crisis_flag=payload.crisis_flag,
        created_at=payload.created_at,
        entry_id=payload.entry_id,
        include_original_text=payload.include_original_text,
        original_text=payload.original_text,
    )
    filename = f"eden_receipt_{payload.entry_id[:8]}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )

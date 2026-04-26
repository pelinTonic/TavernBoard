import uuid
import os
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from model import NPC
from auth.dependencies import get_current_user

router = APIRouter(prefix="/npcs", tags=["npcs"])

PORTRAIT_DIR = "uploads/portraits"
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]


@router.post("/")
async def create_npc(
    campaign_id: int = Form(...),  
    name: str = Form(...),
    description: str = Form(None),
    portrait: UploadFile = File(None),    
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    portrait_filename = None

    if portrait:
        if portrait.content_type not in ALLOWED_TYPES:
            raise HTTPException(
                status_code=400,
                detail="Only JPEG, PNG and WebP images are allowed"
            )

        extension = portrait.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{extension}"
        file_path = os.path.join(PORTRAIT_DIR, unique_filename)

        with open(file_path, "wb") as f:
            content = await portrait.read()
            f.write(content)

        portrait_filename = unique_filename

    npc = Npc(
        campaign_id=campaign_id,
        name=name,
        description=description,
        portrait_filename=portrait_filename
    )
    db.add(npc)
    db.commit()
    db.refresh(npc)
    return npc
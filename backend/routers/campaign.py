from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from model import Campaign, CampaignMember, User
from schemas import CampaignRead
from auth.dependencies import get_current_user
from enums import UserRole
from typing import List

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


@router.get("/", response_model=List[CampaignRead])
def get_campaigns(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ← requires login
):
    """
    Returns campaigns based on the user's role.
    DM sees all campaigns they created.
    Player sees only campaigns they are a member of.
    """

    # If user is a DM — return all campaigns they own
    if current_user.role == UserRole.DM:
        campaigns = db.query(Campaign).filter(
            Campaign.dm_id == current_user.id
        ).all()

    # If user is a Player — return only campaigns they are a member of
    else:
        campaigns = db.query(Campaign).join(CampaignMember).filter(
            CampaignMember.user_id == current_user.id
        ).all()

    return campaigns
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from model import Campaign, CampaignMember, User
from schemas import CampaignRead, CampaignCreate, CampaignUpdate, CampaignMemberCreate, CampaignMemberUpdate
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
    if current_user.role == UserRole.dm:
        campaigns = db.query(Campaign).filter(
            Campaign.dm_id == current_user.id
        ).all()

    # If user is a Player — return only campaigns they are a member of
    else:
        campaigns = db.query(Campaign).join(CampaignMember).filter(
            CampaignMember.user_id == current_user.id
        ).all()

    return campaigns


@router.post("/")
def create_campaigns(
    body: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    if current_user.role != UserRole.dm:
        raise HTTPException(status_code = 403, detail = "DM only")
    
    campaign = Campaign(
    name = body.name, 
    description = body.description, 
    dm_id = current_user.id)

    db.add(campaign)
    db.flush()

    db.add(CampaignMember(campaign_id = campaign.id, user_id = current_user.id, role = UserRole.dm))
    db.commit()
    db.refresh(campaign)
    
    return campaign

@router.put("/{id}")
def update_campaign(
    campaign_id: int,
    body: CampaignUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    if current_user.role != UserRole.dm:
        raise HTTPException(status_code = 403, detail = "DM only")
    
    if body.name is not None:
        campaign.name = body.name
    if body.description is not None:
        campaign.description = body.description

    db.commit()
    db.refresh(campaign)
    return campaign

@router.delete("/{id}")
def delete_campaign(campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    if current_user.role != UserRole.dm:
        raise HTTPException(status_code = 403, detail = "DM only")
    
    db.delete(campaign)
    db.commit()


@router.post("/{campaign_id}/member")
def add_new_member(
    campaign_id: int,
    body: CampaignMemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    player = db.query(User).filter(User.id == body.user_id).first()

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    if current_user.role != UserRole.dm:
        raise HTTPException(status_code = 403, detail = "DM only")
    
    if not player:
        raise HTTPException(status_code=404, detail="User not found")
    
    already_member = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign_id,
        CampaignMember.user_id == body.user_id
    ).first()
    if already_member:
        raise HTTPException(status_code=409, detail="User is already a member")


    campaign_member = CampaignMember(
        user_id = body.user_id,
        campaign_id = campaign_id,
        role = UserRole.player
    )
    
    db.add(campaign_member)
    db.commit()
    db.refresh(campaign_member)

    return(campaign_member)
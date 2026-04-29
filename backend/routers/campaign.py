from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from model import Campaign, CampaignMember, User, NPC
from schemas import (
    CampaignRead,
    CampaignCreate,
    CampaignUpdate,
    CampaignMemberCreate,
    NPCRead,
    NPCCreate,
    NPCUpdate,
)
from auth.dependencies import get_current_user
from enums import UserRole
from typing import List

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


# ----------------------------
# CAMPAIGNS
# ----------------------------

@router.get("/", response_model=list[CampaignRead])
def get_campaigns(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == UserRole.dm:
        return db.query(Campaign).filter(Campaign.dm_id == current_user.id).all()

    return db.query(Campaign).join(CampaignMember).filter(
        CampaignMember.user_id == current_user.id
    ).all()


@router.get("/{campaign_id}", response_model=CampaignRead)
def get_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    return campaign


@router.post("/", response_model=CampaignRead)
def create_campaigns(
    body: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.dm:
        raise HTTPException(status_code=403, detail="DM only")

    campaign = Campaign(
        name=body.name,
        description=body.description,
        dm_id=current_user.id
    )

    db.add(campaign)
    db.flush()

    # SAFE insert (prevents duplicates on broken DB state)
    existing = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign.id,
        CampaignMember.user_id == current_user.id
    ).first()

    if not existing:
        db.add(
            CampaignMember(
                campaign_id=campaign.id,
                user_id=current_user.id,
                role=UserRole.dm
            )
        )

    db.commit()
    db.refresh(campaign)
    return campaign


@router.put("/{campaign_id}")
def update_campaign(
    campaign_id: int,
    body: CampaignUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    if current_user.role != UserRole.dm:
        raise HTTPException(status_code=403, detail="DM only")

    if body.name is not None:
        campaign.name = body.name

    if body.description is not None:
        campaign.description = body.description

    db.commit()
    db.refresh(campaign)
    return campaign


@router.delete("/{campaign_id}")
def delete_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    if current_user.role != UserRole.dm:
        raise HTTPException(status_code=403, detail="DM only")

    if campaign.dm_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your campaign")

    db.delete(campaign)
    db.commit()

    return {"message": "Campaign deleted"}


# ----------------------------
# MEMBERS
# ----------------------------

@router.post("/{campaign_id}/member")
def add_new_member(
    campaign_id: int,
    body: CampaignMemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    if current_user.role != UserRole.dm:
        raise HTTPException(status_code=403, detail="DM only")

    player = db.query(User).filter(User.id == body.user_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="User not found")

    existing = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign_id,
        CampaignMember.user_id == body.user_id
    ).first()

    if existing:
        return existing  # IMPORTANT: prevents IntegrityError

    member = CampaignMember(
        campaign_id=campaign_id,
        user_id=body.user_id,
        role=UserRole.player
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return member


# ----------------------------
# NPCs
# ----------------------------

@router.get("/{campaign_id}/npc", response_model=List[NPCRead])
def get_npc(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(NPC).filter(NPC.campaign_id == campaign_id).all()


@router.post("/{campaign_id}/npc")
def create_NPC(
    body: NPCCreate,
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.dm:
        raise HTTPException(status_code=403, detail="DM only")

    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    npc = NPC(
        campaign_id=campaign_id,
        name=body.name,
        description=body.description,
        portrait_filename=body.portrait_filename,
    )

    db.add(npc)
    db.commit()
    db.refresh(npc)

    return npc


@router.put("/{campaign_id}/npc/{npc_id}")
def update_NPC(
    campaign_id: int,
    npc_id: int,
    body: NPCUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    if campaign.dm_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your campaign")

    npc = db.query(NPC).filter(
        NPC.id == npc_id,
        NPC.campaign_id == campaign_id
    ).first()

    if not npc:
        raise HTTPException(status_code=404, detail="NPC not found")

    if body.name is not None:
        npc.name = body.name
    if body.description is not None:
        npc.description = body.description
    if body.portrait_filename is not None:
        npc.portrait_filename = body.portrait_filename

    db.commit()
    db.refresh(npc)

    return npc


@router.delete("/{campaign_id}/npc/{npc_id}")
def delete_npc(
    campaign_id: int,
    npc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    if campaign.dm_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your campaign")

    npc = db.query(NPC).filter(
        NPC.id == npc_id,
        NPC.campaign_id == campaign_id
    ).first()

    if not npc:
        raise HTTPException(status_code=404, detail="NPC not found")

    db.delete(npc)
    db.commit()

    return {"message": "NPC deleted"}
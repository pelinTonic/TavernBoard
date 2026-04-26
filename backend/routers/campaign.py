from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from model import Campaign, CampaignMember, User, NPC
from schemas import CampaignRead, CampaignCreate, CampaignUpdate, CampaignMemberCreate, CampaignMemberUpdate, NPCCreate, NPCRead, NPCUpdate
from auth.dependencies import get_current_user
from enums import UserRole
from typing import List

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


@router.get("/", response_model=List[CampaignRead])
def get_campaigns(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns campaigns based on the user's role.
    DM sees all campaigns they created.
    Player sees only campaigns they are a member of.
    """

    if current_user.role == UserRole.dm:
        campaigns = db.query(Campaign).filter(
            Campaign.dm_id == current_user.id
        ).all()

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

    """
    Creates a new campaign.

    Only users with the DM role can create campaigns. The creator is automatically
    assigned as the Dungeon Master (DM) of the campaign and added as a member.

    Returns the created campaign.
    """

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

    """
    Updates an existing campaign.

    Only users with the DM role can update campaigns. Allows partial updates:
    - name (optional)
    - description (optional)

    Returns the updated campaign.

    Raises:
    - 404 if the campaign does not exist
    - 403 if the user is not a DM
    """

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
    
    """
    Deletes a campaign.

    Only users with the DM role can delete campaigns.

    Raises:
    - 404 if the campaign does not exist
    - 403 if the user is not a DM
    """

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

    """
    Returns all NPCs for a given campaign.

    The result may be restricted based on the user's role:
    - DM can see all NPCs in their campaign
    - Players can see NPCs only if they are members of the campaign

    Returns a list of NPCs.

    Raises:
    - 404 if the campaign does not exist
    - 403 if the user does not have access to the campaign
    """

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

@router.get("/{campaign_id}/", response_model=List[NPCRead])
def get_NPC(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    
):
    if current_user.role == UserRole.dm:
        npc = db.query(NPC).filter(NPC.campaign_id).all()

    
    return npc

@router.post("/{campaign_id}/npc")
def create_NPC(
    body: NPCCreate,
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    """
    Creates a new NPC in a campaign.

    Only users with the DM role can create NPCs. The NPC is associated
    with the specified campaign.

    Returns the created NPC.

    Raises:
    - 404 if the campaign does not exist
    - 403 if the user is not a DM
    """
    

    if current_user.role != UserRole.dm:
        raise HTTPException(status_code = 403, detail = "DM only")
    
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    new_NPC = NPC(
        campaign_id = campaign_id,
        name = body.name,
        description = body.description,
        portrait_filename = body.portrait_filename,
    )

    db.add(new_NPC)
    db.commit()
    db.refresh(new_NPC)

    return(new_NPC)

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
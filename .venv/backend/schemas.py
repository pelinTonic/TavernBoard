from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
from enums import UserRole, TokenType


class UserBase(BaseModel):

    username: str
    role: UserRole

class UserCreate(UserBase):

    password: str

class UserUpdate(BaseModel):

    username: Optional[str] = None
    password: Optional[str] = None
    user: Optional[UserRole] = None

class UserRead(UserBase):

    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class CampaignBase(BaseModel):

    name: Optional[List] = None
    description: Optional[List] = None

class CampaignCreate(CampaignBase):

    dm_id: int

class CampaignUpdate(BaseModel):

    name: Optional[List] = None
    description: Optional[List] = None

class CampaignRead(CampaignBase):

    id: int
    dm_id: int
    created_at: Optional[List] = None

    model_config = ConfigDict(from_attributes=True)

class CampaignMemberBase(BaseModel):

    role: UserRole

class CampaignMemberCreate(CampaignMemberBase):

    campaign_id: int
    user_id: int

class CampaignMemberUpdate(BaseModel):

    role: UserRole

class CampaignMemberRead(CampaignMemberBase):

    campaign_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)

class NPCBase(BaseModel):

    name: str
    description: Optional[str] = None
    portrait_filename: Optional[str] = None

class NPCCreate(NPCBase):

    campaign_id: int
    
class NPCUpdate(BaseModel):

    name: Optional[str] = None
    description: Optional[str] = None
    portrait_filename: Optional[str] = None

class NPCRead(NPCBase):

    id: int
    campaign_id: int

    model_config = ConfigDict(from_attributes=True)

class MapBase(BaseModel):

    parent_map_id: Optional[int] = None

class MapCreate(MapBase):

    campaign_id: int

class MapUpdate(BaseModel):

    parent_map_id: Optional[int] = None

class MapRead(MapBase):

    id: int
    campaign_id: int

    model_config = ConfigDict(from_attributes=True)

class CharacterBase(BaseModel):
    """
    Shared fields for Character schemas.
    Contains all the core D&D 5e character fields.
    """
    # Identity
    name: str
    race: Optional[str] = None
    subrace: Optional[str] = None
    char_class: Optional[str] = None
    subclass: Optional[str] = None
    level: int = 1
    background: Optional[str] = None
    alignment: Optional[str] = None
    experience_points: int = 0

    # Ability scores
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10

    # Combat
    max_hp: int = 0
    current_hp: int = 0
    temp_hp: int = 0
    armor_class: int = 10
    initiative: int = 0
    speed: int = 30
    hit_dice: Optional[str] = None
    death_save_successes: int = 0
    death_save_failures: int = 0

    # Saving throw proficiencies
    st_strength: bool = False
    st_dexterity: bool = False
    st_constitution: bool = False
    st_intelligence: bool = False
    st_wisdom: bool = False
    st_charisma: bool = False

    # Skill proficiencies
    prof_acrobatics: bool = False
    prof_animal_handling: bool = False
    prof_arcana: bool = False
    prof_athletics: bool = False
    prof_deception: bool = False
    prof_history: bool = False
    prof_insight: bool = False
    prof_intimidation: bool = False
    prof_investigation: bool = False
    prof_medicine: bool = False
    prof_nature: bool = False
    prof_perception: bool = False
    prof_performance: bool = False
    prof_persuasion: bool = False
    prof_religion: bool = False
    prof_sleight_of_hand: bool = False
    prof_stealth: bool = False
    prof_survival: bool = False

    # Appearance
    age: Optional[int] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    eyes: Optional[str] = None
    skin: Optional[str] = None
    hair: Optional[str] = None
    appearance: Optional[str] = None
    portrait_filename: Optional[str] = None

    # Personality
    personality_traits: Optional[str] = None
    ideals: Optional[str] = None
    bonds: Optional[str] = None
    flaws: Optional[str] = None
    backstory: Optional[str] = None

    # Currency
    copper: int = 0
    silver: int = 0
    electrum: int = 0
    gold: int = 0
    platinum: int = 0

class CharacterCreate(CharacterBase):
    """
    Schema for creating a new character.
    Requires user_id to link the character to its owner.
    campaign_id is optional — a character can exist outside a campaign.
    """
    user_id: int
    campaign_id: Optional[int] = None

class CharacterUpdate(BaseModel):
    """
    Schema for updating a character.
    Every single field is optional so you can update just
    current_hp mid-combat without sending the entire character sheet.
    """
    name: Optional[str] = None
    race: Optional[str] = None
    subrace: Optional[str] = None
    char_class: Optional[str] = None
    subclass: Optional[str] = None
    level: Optional[int] = None
    background: Optional[str] = None
    alignment: Optional[str] = None
    experience_points: Optional[int] = None
    strength: Optional[int] = None
    dexterity: Optional[int] = None
    constitution: Optional[int] = None
    intelligence: Optional[int] = None
    wisdom: Optional[int] = None
    charisma: Optional[int] = None
    max_hp: Optional[int] = None
    current_hp: Optional[int] = None
    temp_hp: Optional[int] = None
    armor_class: Optional[int] = None
    initiative: Optional[int] = None
    speed: Optional[int] = None
    hit_dice: Optional[str] = None
    death_save_successes: Optional[int] = None
    death_save_failures: Optional[int] = None
    st_strength: Optional[bool] = None
    st_dexterity: Optional[bool] = None
    st_constitution: Optional[bool] = None
    st_intelligence: Optional[bool] = None
    st_wisdom: Optional[bool] = None
    st_charisma: Optional[bool] = None
    prof_acrobatics: Optional[bool] = None
    prof_animal_handling: Optional[bool] = None
    prof_arcana: Optional[bool] = None
    prof_athletics: Optional[bool] = None
    prof_deception: Optional[bool] = None
    prof_history: Optional[bool] = None
    prof_insight: Optional[bool] = None
    prof_intimidation: Optional[bool] = None
    prof_investigation: Optional[bool] = None
    prof_medicine: Optional[bool] = None
    prof_nature: Optional[bool] = None
    prof_perception: Optional[bool] = None
    prof_performance: Optional[bool] = None
    prof_persuasion: Optional[bool] = None
    prof_religion: Optional[bool] = None
    prof_sleight_of_hand: Optional[bool] = None
    prof_stealth: Optional[bool] = None
    prof_survival: Optional[bool] = None
    age: Optional[int] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    eyes: Optional[str] = None
    skin: Optional[str] = None
    hair: Optional[str] = None
    appearance: Optional[str] = None
    portrait_filename: Optional[str] = None
    personality_traits: Optional[str] = None
    ideals: Optional[str] = None
    bonds: Optional[str] = None
    flaws: Optional[str] = None
    backstory: Optional[str] = None
    copper: Optional[int] = None
    silver: Optional[int] = None
    electrum: Optional[int] = None
    gold: Optional[int] = None
    platinum: Optional[int] = None
    campaign_id: Optional[int] = None

class CharacterRead(CharacterBase):

    """
    Schema for returning character data in responses.
    Adds database-generated id, user_id, campaign_id, and created_at.
    """
    id: int
    user_id: int
    campaign_id: Optional[int] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class SpellBase(BaseModel):
    name: str
    description: str
    school: str
    components: Optional[str] = None
    level: int = 0
    casting_time: str
    range: str
    duration: str

class SpellCreate(SpellBase):
    character_id: int  

class SpellUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    school: Optional[str] = None
    components: Optional[str] = None
    level: Optional[int] = None
    casting_time: Optional[str] = None
    range: Optional[str] = None
    duration: Optional[str] = None

class SpellRead(SpellBase):
    id: int
    character_id: int

    model_config = ConfigDict(from_attributes=True)

class TokenBase(BaseModel):

    filename: str

class TokenCreate(TokenBase):

    campaign_id: int
    token_type: TokenType
    label: str

class TokenUpdate(BaseModel):

    filename: Optional[str] = None
    label: Optional[str] = None
    token_type: Optional[TokenType] = None

class TokenRead(TokenBase):


    id: int
    campaign_id: int    

    model_config = ConfigDict(from_attributes=True)

class InitiativeCombatantBase(BaseModel):
    """
    Shared fields for InitiativeCombatant schemas.
    These are all fields that can change during combat —
    hp changes as damage is taken, initiative can be rerolled,
    ac can change with spells like Shield of Faith.
    """
    name: str
    initiative: int = 0
    hp: int = 0
    max_hp: int = 0
    ac: int = 10
    description: Optional[str] = None
    stat_block: Optional[str] = None
    is_player: bool = False

class InitiativeCombatantCreate(InitiativeCombatantBase):
    """
    Schema for adding a combatant to an initiative tracker.
    Requires session_id to link to a battle session.
    token_id and user_id are optional —
    enemies won't have a user_id and not every combatant has a token.
    """
    session_id: int
    token_id: Optional[int] = None
    user_id: Optional[int] = None

class InitiativeCombatantUpdate(BaseModel):
    """
    Schema for updating a combatant mid combat.
    Every field is optional — most commonly used to update
    just hp when damage is taken, or initiative at start of round.
    """
    name: Optional[str] = None
    initiative: Optional[int] = None
    hp: Optional[int] = None
    max_hp: Optional[int] = None
    ac: Optional[int] = None
    description: Optional[str] = None
    stat_block: Optional[str] = None
    is_player: Optional[bool] = None
    token_id: Optional[int] = None
    user_id: Optional[int] = None

class InitiativeCombatantRead(InitiativeCombatantBase):
    """
    Schema for returning combatant data in responses.
    Adds database generated id and the foreign keys
    session_id, token_id, user_id.
    """
    id: int
    session_id: int
    token_id: Optional[int] = None
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class BattleMapSessionBase(BaseModel):
    """
    Shared fields for BattleMapSession schemas.
    These are all changeable — the DM might swap the map image,
    or toggle the grid on and off during a session.
    """
    map_image_filename: str
    grid_enabled: bool = False
    grid_size: int = 50

class BattleMapSessionCreate(BattleMapSessionBase):
    """
    Schema for creating a new battle map session.
    Requires campaign_id to link the session to a campaign.
    """
    campaign_id: int

class BattleMapSessionUpdate(BaseModel):
    """
    Schema for updating a battle map session.
    All fields optional — for example the DM may just want
    to toggle the grid without changing the map image.
    """
    map_image_filename: Optional[str] = None
    grid_enabled: Optional[bool] = None
    grid_size: Optional[int] = None

class BattleMapSessionRead(BattleMapSessionBase):
    """
    Schema for returning battle map session data in responses.
    Adds database generated id and campaign_id.
    """
    id: int
    campaign_id: int

    model_config = ConfigDict(from_attributes=True)

class BattleTokenBase(BaseModel):
    """
    Shared fields for BattleToken schemas.
    x_pct and y_pct store position as a percentage (0.0 - 1.0)
    of the map width/height so positions work on any screen size.
    These are in Base because they change every time a token is moved.
    """
    x_pct: float
    y_pct: float

class BattleTokenCreate(BattleTokenBase):
    """
    Schema for placing a token on the battle map.
    Requires session_id and token_id to link the placement.
    owner_user_id is optional — enemy tokens have no owner.
    """
    session_id: int
    token_id: int
    owner_user_id: Optional[int] = None

class BattleTokenUpdate(BaseModel):
    """
    Schema for updating a battle token.
    Most commonly used to update x_pct and y_pct
    when a token is dragged to a new position on the map.
    owner_user_id can also change if token ownership is transferred.
    """
    x_pct: Optional[float] = None
    y_pct: Optional[float] = None
    owner_user_id: Optional[int] = None

class BattleTokenRead(BattleTokenBase):

    """
    Schema for returning battle token data in responses.
    Adds database generated id and all foreign keys.
    owner_user_id is optional since enemy tokens have no owner.
    """
    id: int
    session_id: int
    token_id: int
    owner_user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class TokenPayload(BaseModel):
    """
    Schema representing the payload inside a JWT token.
    
    sub  — subject, usually the user's id
    role — the user's role (DM or PLAYER) for authorization
    exp  — expiration timestamp, generated when token is created
    """
    sub: int          
    role: UserRole     
    exp: datetime      
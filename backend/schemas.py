from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from enums import UserRole, TokenType




class UserBase(BaseModel):
    username: str
    role: UserRole


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel): 
    username: str
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None


class UserRead(UserBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class CampaignBase(BaseModel):
    name: str  
    description: Optional[str] = None

class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(BaseModel):
    name: Optional[str] = None       
    description: Optional[str] = None


class CampaignRead(CampaignBase):
    id: int
    dm_id: int
    created_at: Optional[datetime] = None

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
    pass

class NPCUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    portrait_filename: Optional[str] = None


class NPCRead(NPCBase):
    
    campaign_id: int
    model_config = ConfigDict(from_attributes=True)


# =========================
# MAP
# =========================

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


# =========================
# CHARACTER
# =========================

class CharacterBase(BaseModel):
    name: str
    race: Optional[str] = None
    subrace: Optional[str] = None
    char_class: Optional[str] = None
    subclass: Optional[str] = None
    level: int = 1
    background: Optional[str] = None
    alignment: Optional[str] = None
    experience_points: int = 0

    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10

    max_hp: int = 0
    current_hp: int = 0
    temp_hp: int = 0
    armor_class: int = 10
    initiative: int = 0
    speed: int = 30
    hit_dice: Optional[str] = None
    death_save_successes: int = 0
    death_save_failures: int = 0

    st_strength: bool = False
    st_dexterity: bool = False
    st_constitution: bool = False
    st_intelligence: bool = False
    st_wisdom: bool = False
    st_charisma: bool = False

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

    copper: int = 0
    silver: int = 0
    electrum: int = 0
    gold: int = 0
    platinum: int = 0


class CharacterCreate(CharacterBase):
    user_id: int
    campaign_id: Optional[int] = None


class CharacterUpdate(BaseModel):
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
    id: int
    user_id: int
    campaign_id: Optional[int] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# =========================
# SPELL
# =========================

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
    token_type: TokenType     
    label: str                 

    model_config = ConfigDict(from_attributes=True)


class TokenPayload(BaseModel):
    sub: str              
    role: UserRole
    exp: datetime
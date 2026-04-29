from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from database import Base
from typing import Optional, List
from enums import UserRole, TokenType




class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    hashed_password: Mapped[str] = mapped_column(String)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole))
    createad_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    campaign: Mapped[List["Campaign"]] = relationship(back_populates="dm")

    membership: Mapped[List["CampaignMember"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    characters: Mapped[List["Character"]] = relationship(back_populates="user")
    battle_tokens: Mapped[List["BattleToken"]] = relationship(back_populates="owner")
    combatants: Mapped[List["InitiativeCombatant"]] = relationship(back_populates="user")

class Campaign(Base):
    __tablename__ = "campaign"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[Optional[str]] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(500))
    dm_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    dm: Mapped["User"] = relationship(back_populates="campaign")

    members: Mapped[List["CampaignMember"]] = relationship(
        back_populates="campaign",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    campaign_npc: Mapped[List["NPC"]] = relationship(back_populates="campaign")
    characters: Mapped[List["Character"]] = relationship(back_populates="campaign")
    token: Mapped[List["Token"]] = relationship(back_populates="campaign")
    battle_sessions: Mapped[List["BattleMapSession"]] = relationship(back_populates="campaign")
    maps: Mapped[List["Map"]] = relationship(back_populates="campaign")

class CampaignMember(Base):
    __tablename__ = "campaign_members"

    campaign_id: Mapped[int] = mapped_column(
        ForeignKey("campaign.id", ondelete="CASCADE"),
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )

    role: Mapped[UserRole] = mapped_column(Enum(UserRole))

    campaign: Mapped["Campaign"] = relationship(
        back_populates="members",
        passive_deletes=True
    )

    user: Mapped["User"] = relationship(
        back_populates="membership",
        passive_deletes=True
    )

class NPC(Base):

    """
    SQLAlchemy model representing a non-player character (NPC).

    This model stores NPCs that belong to a specific campaign, including
    basic descriptive information and an optional portrait.

    Attributes:
        id (int): Primary key identifier for the NPC.
        campaign_id (int): Foreign key referencing the associated campaign.
        name (str): Name of the NPC (max 100 characters).
        description (Optional[str]): Description of the NPC (max 500 characters).
        portrait_filename (Optional[str]): Filename of the NPC's portrait image.
        campaign (Campaign): The campaign this NPC belongs to.
    """

    __tablename__="NPCmodel"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaign.id"))
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(500))
    portrait_filename: Mapped[Optional[str]] = mapped_column(String)

    campaign: Mapped["Campaign"] = relationship(back_populates = "campaign_npc")

class Map(Base):

    """
    SQLAlchemy model representing a map within a campaign.

    Supports hierarchical maps through a self-referential relationship,
    allowing maps to have parent and child maps.

    Attributes:
        id (int): Primary key identifier for the map.
        campaign_id (int): Foreign key referencing the associated campaign.
        parent_map_id (Optional[int]): Foreign key referencing the parent map.
        parent (Optional[Map]): Parent map in the hierarchy.
        children (List[Map]): List of child maps.
    """

    __tablename__ = "maps"

    id: Mapped[int] = mapped_column(primary_key = True, index = True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaign.id"))
    parent_map_id: Mapped[Optional[int]] = mapped_column(ForeignKey("maps.id"))

    parent: Mapped[Optional["Map"]] = relationship(back_populates = "children", remote_side="Map.id")
    children: Mapped[List["Map"]] = relationship(back_populates = "parent")
    campaign: Mapped["Campaign"] = relationship(back_populates="maps")

class Character(Base):

    """
    SQLAlchemy model representing a player character.

    This model stores all relevant character data including stats,
    abilities, progression, appearance, and relationships to users
    and campaigns.

    Attributes:
        id (int): Primary key identifier for the character.
        name (str): Character name.
        race (Optional[str]): Character race.
        subrace (Optional[str]): Character subrace.
        char_class (Optional[str]): Character class.
        subclass (Optional[str]): Character subclass.
        level (int): Character level.
        background (Optional[str]): Background story type.
        alignment (Optional[str]): Alignment (e.g., Lawful Good).
        experience_points (int): Total experience points.

        user_id (int): Foreign key referencing the owning user.
        campaign_id (Optional[int]): Foreign key referencing the campaign.

        strength (int): Strength ability score.
        dexterity (int): Dexterity ability score.
        constitution (int): Constitution ability score.
        intelligence (int): Intelligence ability score.
        wisdom (int): Wisdom ability score.
        charisma (int): Charisma ability score.

        max_hp (int): Maximum hit points.
        current_hp (int): Current hit points.
        temp_hp (int): Temporary hit points.
        armor_class (int): Armor class value.
        initiative (int): Initiative bonus.
        speed (int): Movement speed.
        hit_dice (Optional[str]): Hit dice representation.

        death_save_successes (int): Number of successful death saves.
        death_save_failures (int): Number of failed death saves.

        st_* (bool): Saving throw proficiencies for each ability.
        prof_* (bool): Skill proficiencies.

        age (Optional[int]): Character age.
        height (Optional[str]): Character height.
        weight (Optional[str]): Character weight.
        eyes (Optional[str]): Eye color.
        skin (Optional[str]): Skin description.
        hair (Optional[str]): Hair description.
        appearance (Optional[str]): General appearance description.
        portrait_filename (Optional[str]): Portrait image filename.

        personality_traits (Optional[str]): Personality traits.
        ideals (Optional[str]): Ideals.
        bonds (Optional[str]): Bonds.
        flaws (Optional[str]): Flaws.
        backstory (Optional[str]): Full backstory.

        copper (int): Copper currency.
        silver (int): Silver currency.
        electrum (int): Electrum currency.
        gold (int): Gold currency.
        platinum (int): Platinum currency.

        created_at (Optional[datetime]): Timestamp of creation.

        user (User): Owning user.
        campaign (Optional[Campaign]): Associated campaign.
        character_spells (List[Spell]): List of spells known by the character.
    """
    __tablename__ = "characters"

    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    race: Mapped[Optional[str]] = mapped_column(String(50))
    subrace: Mapped[Optional[str]] = mapped_column(String(50))
    char_class: Mapped[Optional[str]] = mapped_column(String(50))  
    subclass: Mapped[Optional[str]] = mapped_column(String(50))
    level: Mapped[int] = mapped_column(default=1)
    background: Mapped[Optional[str]] = mapped_column(String(50))
    alignment: Mapped[Optional[str]] = mapped_column(String(20))
    experience_points: Mapped[int] = mapped_column(default=0)

    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    campaign_id: Mapped[Optional[int]] = mapped_column(ForeignKey("campaign.id"))

    
    strength: Mapped[int] = mapped_column(default=10)
    dexterity: Mapped[int] = mapped_column(default=10)
    constitution: Mapped[int] = mapped_column(default=10)
    intelligence: Mapped[int] = mapped_column(default=10)
    wisdom: Mapped[int] = mapped_column(default=10)
    charisma: Mapped[int] = mapped_column(default=10)

    
    max_hp: Mapped[int] = mapped_column(default=0)
    current_hp: Mapped[int] = mapped_column(default=0)
    temp_hp: Mapped[int] = mapped_column(default=0)
    armor_class: Mapped[int] = mapped_column(default=10)
    initiative: Mapped[int] = mapped_column(default=0)
    speed: Mapped[int] = mapped_column(default=30)
    hit_dice: Mapped[Optional[str]] = mapped_column(String(20))  
    death_save_successes: Mapped[int] = mapped_column(default=0)  
    death_save_failures: Mapped[int] = mapped_column(default=0)   

   
    st_strength: Mapped[bool] = mapped_column(default=False)
    st_dexterity: Mapped[bool] = mapped_column(default=False)
    st_constitution: Mapped[bool] = mapped_column(default=False)
    st_intelligence: Mapped[bool] = mapped_column(default=False)
    st_wisdom: Mapped[bool] = mapped_column(default=False)
    st_charisma: Mapped[bool] = mapped_column(default=False)

  
    prof_acrobatics: Mapped[bool] = mapped_column(default=False)
    prof_animal_handling: Mapped[bool] = mapped_column(default=False)
    prof_arcana: Mapped[bool] = mapped_column(default=False)
    prof_athletics: Mapped[bool] = mapped_column(default=False)
    prof_deception: Mapped[bool] = mapped_column(default=False)
    prof_history: Mapped[bool] = mapped_column(default=False)
    prof_insight: Mapped[bool] = mapped_column(default=False)
    prof_intimidation: Mapped[bool] = mapped_column(default=False)
    prof_investigation: Mapped[bool] = mapped_column(default=False)
    prof_medicine: Mapped[bool] = mapped_column(default=False)
    prof_nature: Mapped[bool] = mapped_column(default=False)
    prof_perception: Mapped[bool] = mapped_column(default=False)
    prof_performance: Mapped[bool] = mapped_column(default=False)
    prof_persuasion: Mapped[bool] = mapped_column(default=False)
    prof_religion: Mapped[bool] = mapped_column(default=False)
    prof_sleight_of_hand: Mapped[bool] = mapped_column(default=False)
    prof_stealth: Mapped[bool] = mapped_column(default=False)
    prof_survival: Mapped[bool] = mapped_column(default=False)


    age: Mapped[Optional[int]] = mapped_column()
    height: Mapped[Optional[str]] = mapped_column(String(20))
    weight: Mapped[Optional[str]] = mapped_column(String(20))
    eyes: Mapped[Optional[str]] = mapped_column(String(30))
    skin: Mapped[Optional[str]] = mapped_column(String(30))
    hair: Mapped[Optional[str]] = mapped_column(String(30))
    appearance: Mapped[Optional[str]] = mapped_column(String(500))
    portrait_filename: Mapped[Optional[str]] = mapped_column(String)

    personality_traits: Mapped[Optional[str]] = mapped_column(String(500))
    ideals: Mapped[Optional[str]] = mapped_column(String(500))
    bonds: Mapped[Optional[str]] = mapped_column(String(500))
    flaws: Mapped[Optional[str]] = mapped_column(String(500))
    backstory: Mapped[Optional[str]] = mapped_column(String)

    copper: Mapped[int] = mapped_column(default=0)
    silver: Mapped[int] = mapped_column(default=0)
    electrum: Mapped[int] = mapped_column(default=0)
    gold: Mapped[int] = mapped_column(default=0)
    platinum: Mapped[int] = mapped_column(default=0)

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    user: Mapped["User"] = relationship(back_populates="characters")
    campaign: Mapped[Optional["Campaign"]] = relationship(back_populates="characters")
    character_spells: Mapped[List["Spell"]] = relationship(back_populates = "character")

class Spell(Base):

    """
    SQLAlchemy model representing a spell.

    Stores spell data associated with a specific character.

    Attributes:
        id (int): Primary key identifier for the spell.
        character_id (int): Foreign key referencing the character.
        name (str): Name of the spell.
        school (str): Magic school of the spell.
        components (str): Required components (V, S, M).
        description (str): Spell description.
        level (int): Spell level.
        casting_time (str): Casting time.
        range (str): Spell range.
        duration (str): Duration of the spell.
        character (Character): The character who owns the spell.
    """

    __tablename__ = "spells"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"))
    name: Mapped[str] = mapped_column(String)
    school: Mapped[str] = mapped_column(String)
    components: Mapped[Optional[str]] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    level: Mapped[int] = mapped_column(default = 0)
    casting_time: Mapped[str] = mapped_column(String)
    range: Mapped[str] = mapped_column(String)
    duration: Mapped[str] = mapped_column(String)


    character: Mapped["Character"]  = relationship(back_populates = "character_spells")

class Token(Base):

    """
    SQLAlchemy model representing a token used in a campaign.

    Tokens can represent player characters or enemies and are used
    in battle maps and initiative tracking.

    Attributes:
        id (int): Primary key identifier for the token.
        campaign_id (Optional[int]): Foreign key referencing the campaign.
        filename (Optional[str]): Image filename for the token.
        token_type (TokenType): Type of token (PC or ENEMY).
        campaign (Optional[Campaign]): Associated campaign.
        combatants (List[InitiativeCombatant]): Linked combatants.
        battle_tokens (List[BattleToken]): Token placements in sessions.
    """

    __tablename__="tokens"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaign.id"))
    filename: Mapped[Optional[str]] = mapped_column(String)
    label: Mapped[str] = mapped_column(String(100))
    token_type: Mapped[TokenType] = mapped_column(Enum(TokenType))
    

    campaign: Mapped[Optional["Campaign"]] = relationship(back_populates="token")
    combatants: Mapped[List["InitiativeCombatant"]] = relationship(back_populates="token")
    battle_tokens: Mapped[List["BattleToken"]] = relationship(back_populates="token")

class InitiativeCombatant(Base):

    """
    SQLAlchemy model representing a combatant in an initiative order.

    Used during battle map sessions to track turn order and combat stats.

    Attributes:
        id (int): Primary key identifier.
        session_id (int): Foreign key referencing the battle session.
        name (str): Name of the combatant.
        initiative (int): Initiative value.
        hp (int): Current hit points.
        max_hp (int): Maximum hit points.
        ac (int): Armor class.
        description (Optional[str]): Description or notes.
        stat_block (Optional[str]): Full stat block text.
        token_id (Optional[int]): Associated token ID.
        is_player (bool): Whether this is a player-controlled combatant.
        user_id (Optional[int]): Associated user.

        session (BattleMapSession): Related session.
        token (Optional[Token]): Associated token.
        user (Optional[User]): Associated user.
    """

    __tablename__ = "initiative_combatants"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("battle_map_sessions.id"))
    name: Mapped[str] = mapped_column(String(100))
    initiative: Mapped[int] = mapped_column(default=0)
    hp: Mapped[int] = mapped_column(default=0)
    max_hp: Mapped[int] = mapped_column(default=0)
    ac: Mapped[int] = mapped_column(default=10)
    description: Mapped[Optional[str]] = mapped_column(String(500))
    stat_block: Mapped[Optional[str]] = mapped_column(String)
    token_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tokens.id"))
    is_player: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))


    session: Mapped["BattleMapSession"] = relationship(back_populates="combatants")
    token: Mapped[Optional["Token"]] = relationship(back_populates="combatants")
    user: Mapped[Optional["User"]] = relationship(back_populates="combatants")   

class BattleMapSession(Base):

    """
    SQLAlchemy model representing a battle map session.

    A session contains a map, grid settings, combatants, and token positions.

    Attributes:
        id (int): Primary key identifier.
        campaign_id (int): Foreign key referencing the campaign.
        map_image_filename (str): Filename of the battle map image.
        grid_enabled (bool): Whether a grid is displayed.
        grid_size (int): Size of each grid cell.

        campaign (Campaign): Associated campaign.
        combatants (List[InitiativeCombatant]): Combatants in the session.
        battle_tokens (List[BattleToken]): Tokens placed on the map.
    """

    __tablename__ = "battle_map_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaign.id"))
    map_image_filename: Mapped[str] = mapped_column(String)
    grid_enabled: Mapped[bool] = mapped_column(default=False)
    grid_size: Mapped[int] = mapped_column(default=50)

    
    campaign: Mapped["Campaign"] = relationship(back_populates="battle_sessions")
    combatants: Mapped[List["InitiativeCombatant"]] = relationship(back_populates="session")
    battle_tokens: Mapped[List["BattleToken"]] = relationship(back_populates="session")

class BattleToken(Base):

    """
    SQLAlchemy model representing token placement in a battle session.

    Stores positional data of tokens on a battle map.

    Attributes:
        id (int): Primary key identifier.
        session_id (int): Foreign key referencing the session.
        token_id (int): Foreign key referencing the token.
        x_pct (float): X position as a percentage of map width.
        y_pct (float): Y position as a percentage of map height.
        owner_user_id (Optional[int]): Owner of the token.

        session (BattleMapSession): Associated session.
        token (Token): Associated token.
        owner (Optional[User]): User who owns the token.
    """

    __tablename__ = "battle_tokens"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("battle_map_sessions.id"))
    token_id: Mapped[int] = mapped_column(ForeignKey("tokens.id"))
    x_pct: Mapped[float] = mapped_column()
    y_pct: Mapped[float] = mapped_column()
    owner_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))

    
    session: Mapped["BattleMapSession"] = relationship(back_populates="battle_tokens")
    token: Mapped["Token"] = relationship(back_populates="battle_tokens")
    owner: Mapped[Optional["User"]] = relationship(back_populates="battle_tokens")


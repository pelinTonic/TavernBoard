# Tavern Board — Build Checklist

> **Tag legend:**
> 
> - `[HARD]` — Tricky / common failure point
> - `[WS]` — WebSocket work
> - `[BE]` — Backend only
> - `[FE]` — Frontend only

---

## Phase 1 — Project scaffold & environment

### Local environment

- [x] Install Python 3.11+ and confirm version with `python --version`
- [x] Install Node.js 18+ and npm, confirm with `node --version`
- [x] Install git and initialise a repo: `git init tavern-board`
- [x] Create a Python virtual environment: `python -m venv .venv` and activate it

### Folder structure

- [x] Create root folders: `backend/`, `frontend/`, `uploads/` at the project root
- [x] Inside `backend/` create: `main.py`, `models.py`, `schemas.py`, `database.py`, `websocket_manager.py`
- [x] Inside `backend/` create subfolder `routers/` with empty `__init__.py` and five router files: `campaigns.py`, `characters.py`, `maps.py`, `initiative.py`, `battle.py`
- [x] Scaffold frontend with Vite: `npm create vite@latest frontend -- --template react`, then `cd frontend && npm install`
- [x] Install Tailwind CSS in the frontend: `npm install -D tailwindcss postcss autoprefixer && npx tailwindcss init -p`
- [x] Write a root `.gitignore` covering `.venv/`, `node_modules/`, `__pycache__/`, `*.db`, `uploads/`

### Python dependencies

- [x] `pip install fastapi uvicorn[standard] sqlalchemy python-jose[cryptography] passlib[bcrypt] python-multipart aiofiles`
- [x] `pip install weasyprint` (or `reportlab` if weasyprint gives OS-level dependency trouble) `[HARD]`
- [x] `pip install websockets` (FastAPI includes it, but pin it explicitly)
- [x] Freeze to requirements.txt: `pip freeze > requirements.txt`
- [x] Verify the app boots with a minimal FastAPI hello-world before moving on

---

## Phase 2 — Database models & schemas

### database.py

- [x] Set up SQLAlchemy engine pointing to SQLite file: `sqlite:///./tavern.db` `[BE]`
- [x] Create `SessionLocal` factory and `Base` declarative class `[BE]`
- [x] Write a `get_db()` dependency generator for use in route handlers `[BE]`

### models.py — SQLAlchemy ORM tables

- [x] `User` model: `id`, `username`, `hashed_password`, `role` (enum: dm / player), `created_at` `[BE]`
- [x] `Campaign` model: `id`, `name`, `description`, `dm_id` (FK → User), `created_at` `[BE]`
- [x] `CampaignMember` join table: `campaign_id`, `user_id`, `role` `[BE]`
- [x] `NPC` model: `id`, `campaign_id` (FK), `name`, `description`, `portrait_filename` `[BE]`
- [x] `Map` model: `id`, `campaign_id` (FK), `parent_map_id` (nullable self-FK for nesting), `name`, `image_filename` `[BE]`
- [x] `Character` model: all D&D 5e fields — str/dex/con/int/wis/cha, hp, max_hp, ac, speed, class, race, level, background, alignment, proficiency_bonus, saving_throws JSON, skills JSON, equipment text, backstory text, notes text, campaign_id, user_id `[BE]`
- [x] `Spell` model: `id`, `character_id` (FK), `name`, `level`, `school`, `casting_time`, `range`, `components`, `duration`, `description` `[BE]`
- [x] `Token` model: `id`, `campaign_id` (FK), `filename`, `label`, `type` (enum: pc / enemy) `[BE]`
- [x] `InitiativeCombatant` model: `id`, `session_id`, `name`, `initiative`, `hp`, `max_hp`, `ac`, `description`, `stat_block` text, `token_id` (nullable FK), `is_player` bool, `user_id` (nullable) `[BE]`
- [x] `BattleMapSession` model: `id`, `campaign_id` (FK), `map_image_filename`, `grid_enabled` bool, `grid_size` int `[BE]`
- [x] `BattleToken` model: `id`, `session_id` (FK), `token_id` (FK), `x_pct` float, `y_pct` float, `owner_user_id` (nullable) `[BE]`
- [x] Call `Base.metadata.create_all(engine)` in `main.py` startup to auto-create tables `[BE]`

### schemas.py — Pydantic models

- [ ] Write Base/Create/Update/Read schema pairs for every model above using pydantic v2 style `[BE]`
- [ ] Add token-response schemas (`UserRead` without `hashed_password`, etc.) `[BE]`
- [ ] Write `TokenPayload` schema (`sub`, `role`, `exp`) for JWT `[BE]`

---

## Phase 3 — Auth system

### Backend auth

- [ ] Create `auth/utils.py`: `hash_password()`, `verify_password()` using passlib bcrypt `[BE]`
- [ ] Create `auth/jwt.py`: `create_access_token()` and `decode_access_token()` using python-jose, HS256 algo `[BE]`
- [ ] Write a `get_current_user()` FastAPI dependency that reads `Authorization: Bearer` header, decodes JWT, and fetches user from DB `[BE]`
- [ ] Write `require_dm()` dependency that calls `get_current_user()` then checks `role == "dm"` `[BE]`
- [ ] Add `POST /auth/register` endpoint (username, password, role) `[BE]`
- [ ] Add `POST /auth/login` endpoint returning `access_token` and `token_type` `[BE]`
- [ ] Store `SECRET_KEY` and `ALGORITHM` in a `.env` file, load with `python-dotenv` `[HARD]`

### Frontend auth

- [ ] Create `AuthContext` (React context) to hold token + user info, stored in localStorage `[FE]`
- [ ] Write Login page with username/password form, calls `POST /auth/login`, stores token `[FE]`
- [ ] Write Register page (same form + role select) `[FE]`
- [ ] Create an axios (or fetch) wrapper that attaches the Bearer token to every request `[FE]`
- [ ] Add a `ProtectedRoute` component that redirects to `/login` if no token is present `[FE]`

---

## Phase 4 — Campaign & NPC management

### Backend routes — routers/campaigns.py

- [ ] `GET /campaigns` — list campaigns the current user belongs to (or all for DM) `[BE]`
- [ ] `POST /campaigns` — create campaign (DM only, auto-adds DM as member) `[BE]`
- [ ] `PUT /campaigns/{id}` — update name/description (DM only) `[BE]`
- [ ] `DELETE /campaigns/{id}` (DM only, cascade-delete members/maps/NPCs) `[BE]`
- [ ] `POST /campaigns/{id}/members` — add a player to the campaign by username `[BE]`
- [ ] `GET /campaigns/{id}/npcs`, `POST /campaigns/{id}/npcs` — CRUD NPCs `[BE]`
- [ ] Handle portrait image upload for NPCs using python-multipart, save to `/uploads/portraits/` `[HARD]`

### Frontend — campaign pages

- [ ] Campaign list page: cards showing name + member count, with Create button (DM only) `[FE]`
- [ ] Campaign detail page: tabs for Maps, NPCs, Members `[FE]`
- [ ] NPC list with portrait thumbnails, click to expand description `[FE]`
- [ ] NPC create/edit modal with image upload input `[FE]`

---

## Phase 5 — Hierarchical map system

### Backend — routers/maps.py

- [ ] `GET /campaigns/{id}/maps` — return tree structure (maps with children array), recursive query or eager-load `[BE]`
- [ ] `POST /campaigns/{id}/maps` — create map with optional `parent_map_id` and uploaded image file `[BE]`
- [ ] `PUT /maps/{id}` — update name or reparent (change `parent_map_id`) `[BE]`
- [ ] `DELETE /maps/{id}` — cascade delete children maps recursively `[HARD]`
- [ ] Serve uploaded map images as static files: `app.mount("/uploads", StaticFiles(directory="uploads"))` `[BE]`

### Frontend — map drill-down panel

- [ ] Build a `MapTree` sidebar component that renders maps as a collapsible tree `[FE]`
- [ ] Clicking a map loads its image in the main panel `[FE]`
- [ ] Add child map markers as clickable pins on the parent map image (absolute-positioned divs) `[FE]`
- [ ] Add Create child map button that opens a modal with name + image upload `[FE]`
- [ ] Track breadcrumb trail (continent → city → dungeon) as user drills down `[FE]`

---

## Phase 6 — Character sheets

### Backend — routers/characters.py

- [ ] `POST /campaigns/{id}/characters` — create character for current user `[BE]`
- [ ] `GET /campaigns/{id}/characters` — DM gets all, player gets only their own `[BE]`
- [ ] `GET /characters/{id}` — player gets own, DM gets read-only (enforce in schema response) `[BE]`
- [ ] `PUT /characters/{id}` — update (player only, DM read-only) `[BE]`
- [ ] CRUD endpoints for spells: `POST/PUT/DELETE /characters/{id}/spells` `[BE]`
- [ ] `GET /characters/{id}/export-pdf` — render PDF with ReportLab/WeasyPrint and return as file response `[HARD]`
- [ ] `GET /characters/{id}/export-json` — return full character as JSON download `[BE]`
- [ ] `POST /campaigns/{id}/characters/import-json` — accept JSON body and create a new character `[BE]`

### Frontend — character sheet UI

- [ ] Multi-tab character sheet component: Abilities, Combat, Spells, Equipment, Notes `[FE]`
- [ ] Abilities tab: stat blocks for STR/DEX/CON/INT/WIS/CHA with modifier calculated automatically `((stat-10)//2)` `[FE]`
- [ ] Combat tab: HP, max HP, AC, speed, initiative modifier, death saves, hit dice `[FE]`
- [ ] Skills tab: all 18 D&D skills with proficiency checkboxes and calculated totals `[FE]`
- [ ] Spells tab: list of known spells, Add spell modal, filter by level `[FE]`
- [ ] Equipment tab: inventory list with carry weight (optional) `[FE]`
- [ ] Notes tab: freeform textarea for personal notes `[FE]`
- [ ] Export buttons: Download PDF and Download JSON `[FE]`
- [ ] Import JSON button: file picker that POSTs the file contents `[FE]`
- [ ] DM view shows all fields as read-only (disabled inputs / plaintext) `[FE]`

---

## Phase 7 — WebSocket manager

### websocket_manager.py

- [ ] Create a `ConnectionManager` class with a dict of `{room_id: [WebSocket, ...]}` `[HARD]`
- [ ] Methods: `connect(ws, room)`, `disconnect(ws, room)`, `broadcast(room, message_dict)` `[WS]`
- [ ] Handle disconnect gracefully (client closes tab, network error) — wrap in `try/except WebSocketDisconnect` `[WS]`
- [ ] Make the manager a singleton imported by both `initiative.py` and `battle.py` routers `[WS]`
- [ ] Messages are JSON: `{ type: string, payload: dict }` — document the message types for each feature `[WS]`

---

## Phase 8 — Initiative tracker

### Backend — routers/initiative.py

- [ ] WebSocket endpoint: `WS /ws/initiative/{campaign_id}` — authenticate via token query param `(?token=...)` `[WS]`
- [ ] Handle message type `"add_combatant"`: save to DB, broadcast sorted list `[WS]`
- [ ] Handle message type `"update_combatant"`: update HP/initiative, broadcast `[WS]`
- [ ] Handle message type `"remove_combatant"`: delete from DB, broadcast `[WS]`
- [ ] Handle message type `"advance_turn"`: increment current_turn index (DM only), broadcast `[WS]`
- [ ] Sort combatants by initiative descending on every state change before broadcasting `[BE]`
- [ ] REST fallback: `GET /campaigns/{id}/initiative` to load current state on page join `[BE]`

### Frontend — initiative tracker UI

- [ ] Connect to WS on mount, disconnect on unmount (`useEffect` cleanup) `[FE]`
- [ ] Render a vertical sorted list of combatants, highlighted gold for current turn `[FE]`
- [ ] Each row shows: token image, name, initiative, HP bar, AC badge `[FE]`
- [ ] DM controls: Add enemy (name, initiative, HP, AC, stat block, token), Next Turn button, remove combatant `[FE]`
- [ ] Player controls: input own initiative roll when prompted, view HP (not edit) `[FE]`
- [ ] Animate turn transition (smooth highlight slide) `[FE]`

---

## Phase 9 — Token library

### Backend & frontend

- [ ] `POST /campaigns/{id}/tokens` — upload PNG file, set type (pc/enemy), save to `/uploads/tokens/` `[BE]`
- [ ] `GET /campaigns/{id}/tokens` — list all tokens with filename, label, type `[BE]`
- [ ] `DELETE /tokens/{id}` — DM only `[BE]`
- [ ] Token library page: grid of PNG thumbnails split into PC and Enemy sections `[FE]`
- [ ] Upload modal: file picker (PNG only), label input, type select (PC/Enemy) `[FE]`
- [ ] Token picker component (reusable in initiative tracker and battle map): click to select a token `[FE]`

---

## Phase 10 — Battle map

### Backend — routers/battle.py

- [ ] `WS /ws/battle/{campaign_id}` — authenticate via token query param `[WS]`
- [ ] On connect: send current battle_map state (image, grid settings, all token positions) to joining client `[WS]`
- [ ] Handle `"set_map"`: DM uploads new battle map image via REST first, then broadcasts new map `[WS]`
- [ ] Handle `"toggle_grid"`: broadcast `{grid_enabled, grid_size}` to all clients `[WS]`
- [ ] Handle `"move_token"`: validate that sender owns the token (or is DM), update `x_pct`/`y_pct` in DB, broadcast `[HARD]`
- [ ] Handle `"place_token"`: add a new BattleToken to session, broadcast `[WS]`
- [ ] Handle `"remove_token"`: DM only, remove from session, broadcast `[WS]`
- [ ] REST: `POST /campaigns/{id}/battle/map-image` — upload battle map image file `[BE]`

### Frontend — battle map UI

- [ ] Map canvas: a relative-positioned div with the battle map as `background-image`, takes majority of screen `[FE]`
- [ ] Grid overlay: CSS grid or SVG grid drawn on top, toggled by DM, configurable cell size `[FE]`
- [ ] Render each BattleToken as an absolutely-positioned `img` using `x_pct` / `y_pct` as `left%` / `top%` `[FE]`
- [ ] Implement drag-to-reposition: `mousedown` → `mousemove` → `mouseup`, compute new `x_pct`/`y_pct`, send WS `move_token` `[HARD]`
- [ ] On WS message `"move_token"`: update token position in local state (no re-render flash) `[FE]`
- [ ] Sidebar token palette: lists tokens in current session, click to place on map (DM for all, player for own) `[FE]`
- [ ] DM toolbar: Upload map image button, Toggle grid checkbox, grid size input `[FE]`
- [ ] Players can only drag tokens where `owner_user_id === their user ID`, enforce on frontend and validate on backend `[HARD]`

---

## Phase 11 — UI shell & dark fantasy theme

### Layout & navigation

- [ ] Build `App.jsx` with React Router: routes for `/`, `/login`, `/register`, `/campaigns`, `/campaigns/:id`, `/character`, `/initiative/:id`, `/battle/:id` `[FE]`
- [ ] Sidebar component: links to Campaigns, My Character, Initiative, Battle Map, Token Library, Notes `[FE]`
- [ ] Breadcrumb component for map drill-down `[FE]`
- [ ] Mobile responsive: sidebar collapses to hamburger on small screens `[FE]`

### Dark fantasy Tailwind theme

- [ ] In `tailwind.config.js` extend colors: stone/parchment tones, deep brown backgrounds, gold/amber accents `[FE]`
- [ ] Custom CSS font pairing: a serif for headings (e.g. Google Fonts: Cinzel), sans for body `[FE]`
- [ ] Style all form inputs with dark background, parchment text, gold focus ring `[FE]`
- [ ] Cards and modals: dark brown bg, thin gold border, slight inner glow (box-shadow) `[FE]`
- [ ] Buttons: primary = gold/amber fill + dark text, secondary = outlined gold, danger = dark red `[FE]`
- [ ] Initiative tracker current-turn highlight: gold background with subtle pulse animation `[FE]`

---

## Phase 12 — CORS, static files & integration

### main.py wiring

- [ ] Add `CORSMiddleware` allowing the Vite dev origin (`localhost:5173`) `[BE]`
- [ ] Mount all routers with prefixes: `/auth`, `/campaigns`, `/characters`, `/maps`, `/tokens`, `/ws` `[BE]`
- [ ] Mount uploads as static: `app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")` `[BE]`
- [ ] Add a lifespan startup event to run `Base.metadata.create_all` and seed a default DM user if DB is empty `[BE]`
- [ ] Set max upload file size with a custom middleware or Starlette limit `[BE]`

### Frontend API layer

- [ ] Create `src/api/` folder with one file per domain: `auth.js`, `campaigns.js`, `characters.js`, `maps.js`, `tokens.js` `[FE]`
- [ ] Each file exports async functions (`getCampaigns`, `createCharacter`, etc.) wrapping fetch/axios calls `[FE]`
- [ ] Global error handler: 401 → clear token + redirect to `/login`, 403 → show toast "Not authorised" `[FE]`

---

## Phase 13 — PDF export

### Backend PDF generation

- [ ] Design the character sheet layout in HTML/CSS (one long page or two pages) `[HARD]`
- [ ] Pass the HTML string to `weasyprint.HTML().write_pdf()` and return as `StreamingResponse` with `content-type: application/pdf` `[BE]`
- [ ] Include all character fields: stats, skills (with modifiers), spells table, equipment, backstory, notes `[BE]`
- [ ] Test PDF rendering — WeasyPrint needs system libs (`libcairo`, `pango`) on Linux/Mac; document this in README `[HARD]`
- [ ] Fallback: if WeasyPrint is too painful, implement with ReportLab using canvas drawing primitives `[BE]`

---

## Phase 14 — Testing & polish

### Manual test checklist

- [ ] Register a DM and two Player accounts, verify role restrictions everywhere
- [ ] Create a campaign, add players, create nested maps (3 levels deep)
- [ ] Create characters for each player, export PDF and JSON, re-import JSON
- [ ] Open initiative tracker in three browser tabs simultaneously, verify real-time sync
- [ ] Open battle map in three tabs, move a token, verify all tabs update within ~100ms
- [ ] Try to move another player's token as a non-DM — verify it is rejected `[HARD]`
- [ ] Upload a large image (>5MB) — verify the size limit middleware returns a clear error

### README.md

- [ ] Document system prerequisites (Python 3.11+, Node 18+, WeasyPrint system deps)
- [ ] Step-by-step local setup: clone → venv → pip install → uvicorn command
- [ ] Frontend setup: `cd frontend` → `npm install` → `npm run dev`
- [ ] Environment variables section: `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`
- [ ] Feature overview and known limitations section

---

## Build order notes

**Phases 1–3** are the non-negotiable foundation. Nothing else works until auth + DB are solid. Don't rush the JWT role guard logic — getting it right early saves massive pain later.

**Phases 4–6** are safe CRUD territory. The hierarchical map self-FK and recursive tree rendering in Phase 5 deserve extra attention.

**Phase 7** is the pivot point. Build the WebSocket manager as a clean singleton _before_ touching Phases 8 or 10. A leaky manager that doesn't handle disconnects causes mysterious bugs everywhere.

**Phases 8 and 10** are the hardest. The battle map drag-and-drop with real-time sync and ownership enforcement is the single most complex feature in the whole app. Budget extra time.

**Phases 11–14** are integration and polish. Apply the Tailwind theme incrementally as you build each page — don't leave it all to the end or you'll be restyling hundreds of components at once.
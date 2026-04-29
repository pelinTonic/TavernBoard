import { useEffect, useState } from "react"
import { useAuth } from "../context/AuthContext"
import { useNavigate } from "react-router-dom"
import api from "../api/axios"

function CampaignCard({ campaign, onClick }) {
    return (
        <div
            onClick={onClick}
            className="card-tavern cursor-pointer hover:border-amber-700 hover:shadow-[0_0_20px_#d4a01730] transition-all duration-300 group"
        >
            <div className="flex items-start justify-between mb-3">
                <h2 style={{ fontFamily: "'Cinzel', serif", fontSize: "1rem", color: "#e8d5b0", letterSpacing: "0.06em" }}>
                    {campaign.name || "Unnamed Campaign"}
                </h2>

                <span
                    style={{ color: "#d4a017" }}
                    className="group-hover:translate-x-1 transition-transform duration-200 inline-block"
                >
                    →
                </span>
            </div>

            <p
                style={{ fontFamily: "'Crimson Text', serif", fontSize: "1rem", color: "#8b7355", lineHeight: 1.5 }}
                className="mb-4"
            >
                {campaign.description || "No description yet."}
            </p>

            <div
                style={{ borderTop: "1px solid #6b4c1e33", paddingTop: "0.75rem" }}
                className="flex items-center justify-between"
            >
                <span
                    style={{ fontFamily: "'Cinzel', serif", fontSize: "11px", color: "#6b4c1e", letterSpacing: "0.1em" }}
                >
                    0 MEMBERS
                </span>

                <span
                    style={{ fontFamily: "'Cinzel', serif", fontSize: "10px", color: "#d4a01780", letterSpacing: "0.15em" }}
                >
                    ENTER CAMPAIGN
                </span>
            </div>
        </div>
    )
}

function CreateModal({ onClose, onCreated }) {
    const [name, setName] = useState("")
    const [description, setDescription] = useState("")
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    async function handleSubmit(e) {
        e.preventDefault()
        setLoading(true)
        setError(null)

        try {
            await api.post("/campaigns/", { name, description })
            onCreated()
            onClose()
        } catch (err) {
            setError(err.response?.data?.detail || "Failed to create campaign")
        } finally {
            setLoading(false)
        }
    }

    return (
        <div
            className="absolute top-full right-0 mt-3 w-80 z-50 card-tavern animate-fade-up"
            onClick={(e) => e.stopPropagation()}
        >
            <h2
                className="text-center text-amber-200 mb-1"
                style={{
                    fontFamily: "'Cinzel', serif",
                    fontSize: "1rem",
                    letterSpacing: "0.15em",
                }}
            >
                FORGE A CAMPAIGN
            </h2>

            <div className="divider-gold"><span>⚔</span></div>

            {error && (
                <div
                    className="mb-3 px-3 py-2 rounded text-red-300 text-sm text-center"
                    style={{ background: "#2a050510", border: "1px solid #7f1d1d60" }}
                >
                    {error}
                </div>
            )}

            <form onSubmit={handleSubmit} className="flex flex-col gap-3">
                <div>
                    <label className="label-tavern">Campaign Name</label>
                    <input
                        className="input-tavern"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        required
                    />
                </div>

                <div>
                    <label className="label-tavern">Description</label>
                    <textarea
                        className="input-tavern"
                        style={{ resize: "none", minHeight: "70px" }}
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                    />
                </div>

                <div className="flex gap-2 justify-end pt-2">
                    <button type="button" onClick={onClose} className="btn-ghost">
                        Cancel
                    </button>
                    <button type="submit" disabled={loading} className="btn-gold">
                        {loading ? "Creating..." : "Create"}
                    </button>
                </div>
            </form>
        </div>
    )
}

export default function CampaignListPage() {
    const { isDM, user, logout } = useAuth()
    const navigate = useNavigate()

    const [campaigns, setCampaigns] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [showModal, setShowModal] = useState(false)

    async function fetchCampaigns() {
        try {
            const res = await api.get("/campaigns/")
            setCampaigns(res.data)
        } catch {
            setError("Failed to load campaigns")
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchCampaigns()
    }, [])

    return (
        <div className="bg-tavern min-h-screen">

            {/* Navbar */}
            <nav className="navbar">
                <div className="flex items-center gap-4">
                    <button onClick={() => navigate("/dashboard")} className="btn-ghost">
                        ← Dashboard
                    </button>
                    <span style={{ fontFamily: "'Cinzel Decorative', serif", color: "#d4a017" }}>
                        TavernBoard
                    </span>
                </div>

                <div className="flex items-center gap-4">
                    <span style={{ fontFamily: "'Cinzel', serif", fontSize: "12px", color: "#8b6508" }}>
                        {user?.username}
                    </span>
                    <button
                        onClick={() => {
                            logout()
                            navigate("/login")
                        }}
                        className="btn-ghost"
                    >
                        Leave
                    </button>
                </div>
            </nav>

            <div className="max-w-5xl mx-auto px-6 pt-14 pb-12">

                {/* Header */}
                <div className="flex items-end justify-between mb-6 animate-fade-up">
                    <div>
                        <p
                            style={{
                                fontFamily: "'Cinzel', serif",
                                fontSize: "11px",
                                letterSpacing: "0.3em",
                                color: "#d4a017",
                            }}
                        >
                            ✦ Your Adventures
                        </p>

                        <h1
                            style={{
                                fontFamily: "'Cinzel', serif",
                                fontSize: "2.5rem",
                                color: "#f0e0b0",
                            }}
                        >
                            Campaigns
                        </h1>
                    </div>

                    {isDM && (
                        <div className="relative">
                            <button
                                onClick={() => setShowModal((v) => !v)}
                                className="btn-gold"
                            >
                                + New Campaign
                            </button>

                            {showModal && (
                                <CreateModal
                                    onClose={() => setShowModal(false)}
                                    onCreated={fetchCampaigns}
                                />
                            )}
                        </div>
                    )}
                </div>

                <div className="divider-gold"><span>⚔</span></div>

                {/* States */}
                {loading && <p className="mt-8 text-amber-100/70">Loading...</p>}
                {error && <p className="text-red-400 mt-8">{error}</p>}

                {!loading && campaigns.length === 0 && (
                    <p className="text-amber-100/70 mt-10">No campaigns yet.</p>
                )}

                {!loading && campaigns.length > 0 && (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 mt-4">
                        {campaigns.map((c) => (
                            <CampaignCard
                                key={c.id}
                                campaign={c}
                                onClick={() => navigate(`/campaigns/${c.id}`)}
                            />
                        ))}
                    </div>
                )}
            </div>
        </div>
    )
}
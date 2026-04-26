import { useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"

const NAV_CARDS = [
    {
        title: "Campaigns",
        icon: "🗺",
        desc: "Manage your campaigns, invite players, and begin your quests.",
        dmDesc: "View campaigns you have joined and track your adventures.",
        path: "/campaigns",
        available: true,
    },
    {
        title: "Characters",
        icon: "⚔",
        desc: "Build and manage your D&D 5e character sheets.",
        path: null,
        available: false,
    },
    {
        title: "Battle Map",
        icon: "🏰",
        desc: "Set up encounter maps, place tokens, track initiative.",
        path: null,
        available: false,
    },
    {
        title: "Spell Book",
        icon: "📖",
        desc: "Browse and manage spells for your characters.",
        path: null,
        available: false,
    },
]

export default function Dashboard() {
    const { user, logout, isDM } = useAuth()
    const navigate = useNavigate()

    function handleLogout() {
        logout()
        navigate("/login")
    }

    return (
        <div className="bg-tavern min-h-screen">

            {/* Navbar */}
            <nav className="navbar">
                <div className="flex items-center gap-3">
                    <span style={{
                        fontFamily: "'Cinzel Decorative', serif",
                        fontSize: "1.1rem",
                        color: "#d4a017"
                    }}>
                        TavernBoard
                    </span>
                </div>
                <div className="flex items-center gap-4">
                    <span style={{ fontFamily: "'Cinzel', serif", fontSize: "12px", color: "#8b6508", letterSpacing: "0.1em" }}>
                        {isDM ? "⚜ Dungeon Master" : "⚔ Adventurer"}
                    </span>
                    <button onClick={handleLogout} className="btn-ghost" style={{ padding: "0.4rem 1rem", fontSize: "12px" }}>
                        Leave
                    </button>
                </div>
            </nav>

            {/* Hero */}
            <div className="max-w-5xl mx-auto px-6 pt-16 pb-10">
                <div className="animate-fade-up">
                    <p style={{
                        fontFamily: "'Cinzel', serif",
                        fontSize: "11px",
                        letterSpacing: "0.3em",
                        color: "#d4a017",
                        textTransform: "uppercase",
                        marginBottom: "0.5rem"
                    }}>
                        ✦ &nbsp; Welcome back
                    </p>
                    <h1 style={{
                        fontFamily: "'Cinzel', serif",
                        fontSize: "clamp(2rem, 5vw, 3.5rem)",
                        color: "#f0e0b0",
                        lineHeight: 1.1,
                        marginBottom: "0.5rem"
                    }}>
                        {user?.username}
                    </h1>
                    <p style={{ fontFamily: "'Crimson Text', serif", fontSize: "1.2rem", color: "#8b7355", fontStyle: "italic" }}>
                        What adventure calls to you today?
                    </p>
                </div>

                <div className="divider-gold animate-fade-up delay-1"><span>⚔</span></div>

                {/* Grid */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-5 mt-2">
                    {NAV_CARDS.map((card, i) => (
                        <button
                            key={card.title}
                            onClick={() => card.available && card.path && navigate(card.path)}
                            disabled={!card.available}
                            className={`card-tavern text-left animate-fade-up delay-${i + 2} ${card.available
                                ? "cursor-pointer hover:border-amber-700 hover:shadow-[0_0_20px_#d4a01730] transition-all duration-300 group"
                                : "cursor-not-allowed opacity-40"
                            }`}
                            style={{ width: "100%" }}
                        >
                            <div className="flex items-start justify-between mb-3">
                                <div className="flex items-center gap-3">
                                    <span style={{ fontSize: "1.5rem" }}>{card.icon}</span>
                                    <h2 style={{
                                        fontFamily: "'Cinzel', serif",
                                        fontSize: "1rem",
                                        color: "#e8d5b0",
                                        letterSpacing: "0.08em"
                                    }}>
                                        {card.title}
                                    </h2>
                                </div>
                                {card.available ? (
                                    <span style={{ color: "#d4a017", fontSize: "1.2rem" }}
                                          className="group-hover:translate-x-1 transition-transform duration-200 inline-block">
                                        →
                                    </span>
                                ) : (
                                    <span style={{
                                        fontFamily: "'Cinzel', serif",
                                        fontSize: "9px",
                                        letterSpacing: "0.15em",
                                        color: "#6b4c1e",
                                        textTransform: "uppercase",
                                        border: "1px solid #6b4c1e40",
                                        padding: "2px 8px",
                                        borderRadius: "4px"
                                    }}>
                                        Soon
                                    </span>
                                )}
                            </div>
                            <p style={{
                                fontFamily: "'Crimson Text', serif",
                                fontSize: "1rem",
                                color: "#8b7355",
                                lineHeight: 1.5
                            }}>
                                {isDM ? card.desc : (card.dmDesc || card.desc)}
                            </p>
                        </button>
                    ))}
                </div>
            </div>
        </div>
    )
}
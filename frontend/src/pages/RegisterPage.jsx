import { useState } from "react"
import { useNavigate } from "react-router-dom"
import api from "../api/axios"

export default function RegisterPage() {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [role, setRole]         = useState("player")
    const [error, setError]       = useState(null)
    const [loading, setLoading]   = useState(false)
    const navigate = useNavigate()

    async function handleSubmit(e) {
        e.preventDefault()
        setError(null)
        setLoading(true)
        try {
            await api.post("/auth/register", { username, password, role })
            navigate("/login")
        } catch (err) {
            setError(err.response?.data?.detail || "Could not connect to server")
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="bg-tavern min-h-screen flex items-center justify-center px-4">
            <div className="w-full max-w-md">

                {/* Title */}
                <div className="text-center mb-10 animate-fade-up">
                    <p className="text-xs tracking-[0.3em] uppercase mb-3"
                       style={{ fontFamily: "'Cinzel', serif", color: "#d4a017" }}>
                        ✦ &nbsp; Begin Your Legend &nbsp; ✦
                    </p>
                    <h1 style={{ fontFamily: "'Cinzel Decorative', serif", fontSize: "2.8rem", lineHeight: 1.1 }}
                        className="text-amber-100 mb-3">
                        TavernBoard
                    </h1>
                    <p className="italic" style={{ fontFamily: "'Crimson Text', serif", fontSize: "1.2rem", color: "#92712a" }}>
                        Every hero needs an origin
                    </p>
                </div>

                {/* Card */}
                <div className="card-tavern animate-fade-up delay-1">
                    <h2 className="text-center text-amber-200 mb-1"
                        style={{ fontFamily: "'Cinzel', serif", fontSize: "1.1rem", letterSpacing: "0.15em" }}>
                        CREATE YOUR CHARACTER
                    </h2>

                    <div className="divider-gold"><span>⚔</span></div>

                    {error && (
                        <div className="mb-4 px-4 py-3 rounded-lg text-red-300 text-sm text-center"
                             style={{ background: "#2a050510", border: "1px solid #7f1d1d60" }}>
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="flex flex-col gap-5">
                        <div>
                            <label className="label-tavern">Username</label>
                            <input
                                className="input-tavern"
                                placeholder="Choose your name..."
                                value={username}
                                onChange={e => setUsername(e.target.value)}
                                required
                            />
                        </div>

                        <div>
                            <label className="label-tavern">Password</label>
                            <input
                                type="password"
                                className="input-tavern"
                                placeholder="Create a secret..."
                                value={password}
                                onChange={e => setPassword(e.target.value)}
                                required
                            />
                        </div>

                        <div>
                            <label className="label-tavern">Your Role</label>
                            <select
                                className="select-tavern"
                                value={role}
                                onChange={e => setRole(e.target.value)}
                            >
                                <option value="player">⚔ Player</option>
                                <option value="dm">👑 Dungeon Master</option>
                            </select>
                        </div>

                        <button type="submit" disabled={loading} className="btn-gold w-full mt-2">
                            {loading ? "Enrolling in the guild..." : "Begin Your Journey"}
                        </button>
                    </form>

                    <div className="divider-gold mt-6"><span>✦</span></div>

                    <p className="text-center text-sm" style={{ color: "#8b7355" }}>
                        Already a member?{" "}
                        <a href="/login" style={{ color: "#d4a017" }} className="hover:underline">
                            Enter the tavern
                        </a>
                    </p>
                </div>
            </div>
        </div>
    )
}
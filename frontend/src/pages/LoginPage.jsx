import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"
import api from "../api/axios"

export default function LoginPage() {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError]       = useState(null)
    const [loading, setLoading]   = useState(false)
    const { login } = useAuth()
    const navigate  = useNavigate()

    async function handleSubmit(e) {
        e.preventDefault()
        setError(null)
        setLoading(true)
        try {
            const { data } = await api.post("/auth/login/json", { username, password })
            login(data.access_token, data.user)
            navigate("/dashboard")
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
                    <p className="text-xs font-cinzel tracking-[0.3em] uppercase text-yellow-600 mb-3"
                       style={{ fontFamily: "'Cinzel', serif" }}>
                        ✦ &nbsp; Welcome, Traveller &nbsp; ✦
                    </p>
                    <h1 style={{ fontFamily: "'Cinzel Decorative', serif", fontSize: "2.8rem", lineHeight: 1.1 }}
                        className="text-amber-100 mb-3">
                        TavernBoard
                    </h1>
                    <p className="text-amber-700 italic" style={{ fontFamily: "'Crimson Text', serif", fontSize: "1.2rem" }}>
                        Where legends are forged
                    </p>
                </div>

                {/* Card */}
                <div className="card-tavern animate-fade-up delay-1">

                    <h2 className="text-center text-amber-200 mb-1"
                        style={{ fontFamily: "'Cinzel', serif", fontSize: "1.1rem", letterSpacing: "0.15em" }}>
                        ENTER THE TAVERN
                    </h2>

                    <div className="divider-gold"><span>⚔</span></div>

                    {error && (
                        <div className="mb-4 px-4 py-3 rounded-lg text-red-300 text-sm text-center animate-fade-up"
                             style={{ background: "#2a050510", border: "1px solid #7f1d1d60" }}>
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="flex flex-col gap-5">
                        <div>
                            <label className="label-tavern">Username</label>
                            <input
                                className="input-tavern"
                                placeholder="Your name, traveller..."
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
                                placeholder="Speak the password..."
                                value={password}
                                onChange={e => setPassword(e.target.value)}
                                required
                            />
                        </div>

                        <button type="submit" disabled={loading} className="btn-gold w-full mt-2">
                            {loading ? "Opening the gates..." : "Enter"}
                        </button>
                    </form>

                    <div className="divider-gold mt-6"><span>✦</span></div>

                    <p className="text-center text-sm" style={{ color: "#8b7355" }}>
                        No account yet?{" "}
                        <a href="/register"
                           style={{ color: "#d4a017" }}
                           className="hover:underline transition-colors">
                            Join the guild
                        </a>
                    </p>
                </div>
            </div>
        </div>
    )
}
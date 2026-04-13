import { useState } from "react"
import { useNavigate } from "react-router-dom"
import api from "../api/axios"   // ← added

function RegisterPage() {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [role, setRole] = useState("player")
    const [error, setError] = useState(null)
    const [loading, setLoading] = useState(false)

    const navigate = useNavigate()

    async function handleSubmit(e) {
        e.preventDefault()
        setError(null)
        setLoading(true)

        try {
            // axios replaces fetch — no need for headers or JSON.stringify
            await api.post("/auth/register", { username, password, role })

            // Registration successful — redirect to login
            navigate("/login")

        } catch (err) {
            // axios throws on 4xx/5xx so we catch it here
            setError(err.response?.data?.detail || "Could not connect to server")
        } finally {
            setLoading(false)
        }
    }

    return (
        <div>
            <h1>Register</h1>

            {error && <p style={{ color: "red" }}>{error}</p>}

            <form onSubmit={handleSubmit}>
                <div>
                    <label>Username</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>

                <div>
                    <label>Password</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>

                <div>
                    <label>Role</label>
                    <select
                        value={role}
                        onChange={(e) => setRole(e.target.value)}
                    >
                        <option value="player">Player</option>
                        <option value="dm">Dungeon Master</option>
                    </select>
                </div>

                <button type="submit" disabled={loading}>
                    {loading ? "Registering..." : "Register"}
                </button>
            </form>

            <p>
                Already have an account?
                <a href="/login"> Login here</a>
            </p>
        </div>
    )
}

export default RegisterPage
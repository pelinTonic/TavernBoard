import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"
import api from "../api/axios"   // ← added

function LoginPage() {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState(null)
    const [loading, setLoading] = useState(false)

    const { login } = useAuth()
    const navigate = useNavigate()

    async function handleSubmit(e) {
        e.preventDefault()
        setError(null)
        setLoading(true)

        try {
            // axios replaces fetch — no need for headers or JSON.stringify
            const response = await api.post("/auth/login/json", { username, password })
            const data = response.data   // ← axios puts response body in .data

            // Save token and user to context + localStorage
            login(data.access_token, data.user)

            // Redirect to dashboard
            navigate("/dashboard")

        } catch (err) {
            // axios throws on 4xx/5xx so we catch it here
            setError(err.response?.data?.detail || "Could not connect to server")
        } finally {
            setLoading(false)
        }
    }

    return (
        <div>
            <h1>Login</h1>

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

                <button type="submit" disabled={loading}>
                    {loading ? "Logging in..." : "Login"}
                </button>
            </form>

            <p>
                Don't have an account?
                <a href="/register"> Register here</a>
            </p>
        </div>
    )
}

export default LoginPage
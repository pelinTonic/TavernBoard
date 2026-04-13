import { useAuth } from "../context/AuthContext"
import { useNavigate } from "react-router-dom"

function Dashboard() {
    const { user, logout } = useAuth()
    const navigate = useNavigate()

    function handleLogout() {
        logout()
        navigate("/login")
    }

    return (
        <div>
            <h1>Welcome, {user?.username}!</h1>
            <p>Your role: {user?.role}</p>
            <button onClick={handleLogout}>Logout</button>
        </div>
    )
}

export default Dashboard
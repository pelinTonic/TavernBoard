import { Navigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"

function ProtectedRoute({ children }) {
    const { isLoggedIn } = useAuth()

    // If no token — redirect to login
    if (!isLoggedIn) {
        return <Navigate to="/login" />
    }

    // If token exists — render the page
    return children
}

export default ProtectedRoute
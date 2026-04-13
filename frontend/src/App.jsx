import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import ProtectedRoute from "./components/ProtectedRoute"   // ← import from its own file
import LoginPage from "./pages/LoginPage"
import RegisterPage from "./pages/RegisterPage"            // ← was missing
import Dashboard from "./pages/Dashboard"

function App() {
    return (
        <BrowserRouter>
            <Routes>
                {/* Public routes */}
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />

                {/* Protected routes — must be logged in */}
                <Route path="/dashboard" element={
                    <ProtectedRoute>
                        <Dashboard />
                    </ProtectedRoute>
                } />

                {/* Redirect root to login */}
                <Route path="/" element={<Navigate to="/login" />} />
            </Routes>
        </BrowserRouter>
    )
}

export default App
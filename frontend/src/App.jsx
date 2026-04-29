import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import ProtectedRoute from "./components/ProtectedRoute"
import LoginPage from "./pages/LoginPage"
import RegisterPage from "./pages/RegisterPage"
import Dashboard from "./pages/Dashboard"
import CampaignListPage from "./pages/CampaignListPage"
import CampaignDetailPage from "./pages/CampaignDetailPage"

function App() {
    return (
        <BrowserRouter>
            <Routes>
                {/* Public routes */}
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />

                {/* Protected routes */}
                <Route path="/dashboard" element={
                    <ProtectedRoute><Dashboard /></ProtectedRoute>
                } />

                <Route path="/campaigns" element={
                    <ProtectedRoute><CampaignListPage /></ProtectedRoute>
                } />

                {/* Root → login */}
                <Route path="/" element={<Navigate to="/login" />} />
                
                <Route path="/campaigns/:id" element={
                    <ProtectedRoute><CampaignDetailPage /></ProtectedRoute>} />
                    
            </Routes>
        </BrowserRouter>
    )
}

export default App
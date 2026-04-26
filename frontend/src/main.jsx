import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import { AuthProvider } from "./context/AuthContext"
import App from "./App"
import "./index.css"

createRoot(document.getElementById("root")).render(
    <StrictMode>
        <AuthProvider>   {/* ← wrap everything here */}
            <App />
        </AuthProvider>
    </StrictMode>
)
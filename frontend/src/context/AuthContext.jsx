import { createContext, useContext, useState, useEffect } from "react"

// 1. Create the context
const AuthContext = createContext(null)


// 2. Create the provider — wraps your app and shares state
export function AuthProvider({ children }) {

    // Read token from localStorage on first load
    // so login survives page refresh
    const [token, setToken] = useState(
        localStorage.getItem("token") || null
    )

    const [user, setUser] = useState(
        JSON.parse(localStorage.getItem("user")) || null
    )


    // Called after successful login
    function login(accessToken, userData) {
        // Save to state
        setToken(accessToken)
        setUser(userData)

        // Save to localStorage so it survives refresh
        localStorage.setItem("token", accessToken)
        localStorage.setItem("user", JSON.stringify(userData))
    }


    // Called when user logs out
    function logout() {
        // Clear state
        setToken(null)
        setUser(null)

        // Clear localStorage
        localStorage.removeItem("token")
        localStorage.removeItem("user")
    }


    // What we share with the rest of the app
    const value = {
        token,      // the JWT token
        user,       // { id, username, role }
        login,      // call this after successful login
        logout,     // call this to log out
        isLoggedIn: !!token,        // true if token exists
        isDM: user?.role === "dm"   // true if user is a DM
    }

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    )
}


// 3. Custom hook — makes using the context easier
// Instead of: const auth = useContext(AuthContext)
// You just write: const auth = useAuth()
export function useAuth() {
    return useContext(AuthContext)
}
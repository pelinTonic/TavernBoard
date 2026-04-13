import axios from "axios"

// 1. Create an axios instance with your backend URL as the base
const api = axios.create({
    baseURL: "http://127.0.0.1:8000",  // all requests start with this
    headers: {
        "Content-Type": "application/json"
    }
})


// 2. Request interceptor — runs before EVERY request
// This is where we attach the token automatically
api.interceptors.request.use(
    (config) => {
        // Read token from localStorage
        const token = localStorage.getItem("token")

        // If token exists, attach it to the Authorization header
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }

        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)


// 3. Response interceptor — runs after EVERY response
// This is where we handle global errors like expired tokens
api.interceptors.response.use(
    (response) => {
        // If response is fine just return it
        return response
    },
    (error) => {
        // If token is expired or invalid — log the user out
        if (error.response?.status === 401) {
            localStorage.removeItem("token")
            localStorage.removeItem("user")
            window.location.href = "/login"  // redirect to login
        }
        return Promise.reject(error)
    }
)


export default api
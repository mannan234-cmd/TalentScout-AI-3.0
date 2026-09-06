import React, { createContext, useContext, useState, useCallback } from 'react'
import * as authService from '../services/auth'
import api from '../services/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(authService.getStoredUser())

  // Re-fetches the current user (e.g. after connecting Gmail) so
  // gmail_connected reflects reality without a full re-login.
  const refreshUser = useCallback(async () => {
    const res = await api.get('/auth/me')
    setUser(res.data)
    localStorage.setItem('ts_user', JSON.stringify(res.data))
    return res.data
  }, [])

  const login = useCallback(async (email, password) => {
    const data = await authService.login(email, password)
    setUser(data.user)
    return data.user
  }, [])

  const signup = useCallback(async (full_name, email, password, role) => {
    const data = await authService.signup(full_name, email, password, role)
    setUser(data.user)
    return data.user
  }, [])

  const logout = useCallback(() => {
    authService.logout()
    setUser(null)
  }, [])

  return (
    <AuthContext.Provider value={{ user, login, signup, logout, refreshUser, isAdmin: user?.role === 'admin' || user?.role === 'reviewer' }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}

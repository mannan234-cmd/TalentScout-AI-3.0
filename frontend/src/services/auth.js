import api from './api'

export async function login(email, password) {
  const res = await api.post('/auth/login', { email, password })
  persist(res.data)
  return res.data
}

export async function signup(full_name, email, password, role) {
  const res = await api.post('/auth/signup', { full_name, email, password, role })
  persist(res.data)
  return res.data
}

export function logout() {
  localStorage.removeItem('ts_token')
  localStorage.removeItem('ts_user')
}

export function getStoredUser() {
  const raw = localStorage.getItem('ts_user')
  return raw ? JSON.parse(raw) : null
}

export function getStoredToken() {
  return localStorage.getItem('ts_token')
}

function persist(data) {
  localStorage.setItem('ts_token', data.access_token)
  localStorage.setItem('ts_user', JSON.stringify(data.user))
}

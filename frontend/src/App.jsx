import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import ProtectedRoute from './components/ProtectedRoute'

import Landing from './pages/Landing'
import Login from './pages/Login'
import Signup from './pages/Signup'
import StudentDashboard from './pages/StudentDashboard'
import AdminDashboard from './pages/AdminDashboard'
import Discovery from './pages/Discovery'
import StudentProfile from './pages/StudentProfile'
import HumanReview from './pages/HumanReview'
import Opportunities from './pages/Opportunities'
import Matches from './pages/Matches'
import ApplicationSupport from './pages/ApplicationSupport'

export default function App() {
  return (
    <div className="min-h-screen">
      <Navbar />
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        <Route path="/student" element={
          <ProtectedRoute roles={['student']}><StudentDashboard /></ProtectedRoute>
        } />
        <Route path="/student/profile" element={
          <ProtectedRoute roles={['student']}><StudentProfile /></ProtectedRoute>
        } />

        <Route path="/admin" element={
          <ProtectedRoute roles={['admin', 'reviewer']}><AdminDashboard /></ProtectedRoute>
        } />
        <Route path="/discovery" element={
          <ProtectedRoute roles={['admin', 'reviewer']}><Discovery /></ProtectedRoute>
        } />
        <Route path="/students/:id" element={
          <ProtectedRoute roles={['admin', 'reviewer']}><StudentProfile /></ProtectedRoute>
        } />
        <Route path="/review" element={
          <ProtectedRoute roles={['admin', 'reviewer']}><HumanReview /></ProtectedRoute>
        } />

        <Route path="/opportunities" element={
          <ProtectedRoute><Opportunities /></ProtectedRoute>
        } />
        <Route path="/matches" element={
          <ProtectedRoute><Matches /></ProtectedRoute>
        } />
        <Route path="/applications" element={
          <ProtectedRoute roles={['student']}><ApplicationSupport /></ProtectedRoute>
        } />
      </Routes>
    </div>
  )
}

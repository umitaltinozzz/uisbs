import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext.tsx';
import Layout from './components/Layout/Layout.tsx';
import ProtectedRoute from './components/Auth/ProtectedRoute.tsx';
import HomePage from './pages/HomePage.tsx';
import LoginPage from './pages/Auth/LoginPage.tsx';
import RegisterPage from './pages/Auth/RegisterPage.tsx';
import SearchPage from './pages/Search/SearchPage.tsx';
import PharmacyDashboard from './pages/Pharmacy/PharmacyDashboard.tsx';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/search" element={<SearchPage />} />
            <Route 
              path="/pharmacy/dashboard" 
              element={
                <ProtectedRoute allowedRoles={['eczane', 'admin']}>
                  <PharmacyDashboard />
                </ProtectedRoute>
              } 
            />
          </Routes>
        </Layout>
      </Router>
    </AuthProvider>
  );
}

export default App; 
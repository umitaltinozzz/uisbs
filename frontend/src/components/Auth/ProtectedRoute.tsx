import React from 'react';

interface ProtectedRouteProps {
  children: React.ReactNode;
  allowedRoles?: string[];
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ 
  children, 
  allowedRoles = [] 
}) => {
  // Bu component şu an için sadece children'ı render ediyor
  // Gerçek auth implementasyonu AuthContext ile yapılacak
  return <>{children}</>;
};

export default ProtectedRoute; 
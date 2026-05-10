import React, { createContext, useContext, useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { User, Role } from './types';
import { MockDB } from './services/db';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Members from './pages/Members';
import Board from './pages/Board';
import MeetingsAI from './pages/MeetingsAI';
import Files from './pages/Files';
import Marketplace from './pages/Marketplace';
import Users from './pages/Users';
import Profile from './pages/Profile';
import Layout from './components/Layout';

interface AuthContextType {
  user: User | null;
  login: (email: string, password?: string) => Promise<boolean>;
  logout: () => void;
  updateUser: (data: Partial<User>) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};

export default function App() {
  const [user, setUser] = useState<User | null>(MockDB.getCurrentUser());

  const login = async (email: string, password = 'password') => {
    // Simulated login logic
    const users = MockDB.getUsers();
    const foundUser = users.find(u => u.email === email);
    if (foundUser) {
      setUser(foundUser);
      MockDB.setCurrentUser(foundUser);
      return true;
    }
    return false;
  };

  const logout = () => {
    setUser(null);
    MockDB.setCurrentUser(null);
  };

  const updateUser = (data: Partial<User>) => {
    if (!user) return;
    const newUser = { ...user, ...data };
    setUser(newUser);
    MockDB.setCurrentUser(newUser);
    // Also update in users list
    const users = MockDB.getUsers();
    const updatedUsers = users.map(u => u.id === user.id ? newUser : u);
    MockDB.saveUsers(updatedUsers);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, updateUser }}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={!user ? <Login /> : <Navigate to="/" />} />
          
          <Route element={user ? <Layout /> : <Navigate to="/login" />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/members" element={<Members />} />
            <Route path="/board/:type" element={<Board />} />
            <Route path="/meetings-ai" element={<MeetingsAI />} />
            <Route path="/files" element={<Files />} />
            <Route path="/marketplace" element={<Marketplace />} />
            <Route path="/users" element={user?.role === 'SUPER_ADMIN' ? <Users /> : <Navigate to="/" />} />
            <Route path="/profile" element={<Profile />} />
          </Route>

          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </BrowserRouter>
    </AuthContext.Provider>
  );
}

import { User, Role } from '../types';

const USERS_KEY = 'hyta_users';
const CURRENT_USER_KEY = 'hyta_current_user';

const INITIAL_USERS: User[] = [
  { id: '1', email: 'superadmin@hyta.vn', name: 'Super Admin', role: 'SUPER_ADMIN', mustChangePassword: false },
  { id: '2', email: 'admin@hyta.vn', name: 'Admin Hiệp hội', role: 'ADMIN', mustChangePassword: false },
  { id: '3', email: 'member@gmail.com', name: 'Hội viên Demo', role: 'MEMBER', mustChangePassword: true },
];

export const MockDB = {
  getUsers: (): User[] => {
    const data = localStorage.getItem(USERS_KEY);
    return data ? JSON.parse(data) : INITIAL_USERS;
  },
  
  saveUsers: (users: User[]) => {
    localStorage.setItem(USERS_KEY, JSON.stringify(users));
  },
  
  getCurrentUser: (): User | null => {
    const data = localStorage.getItem(CURRENT_USER_KEY);
    return data ? JSON.parse(data) : null;
  },
  
  setCurrentUser: (user: User | null) => {
    if (user) {
      localStorage.setItem(CURRENT_USER_KEY, JSON.stringify(user));
    } else {
      localStorage.removeItem(CURRENT_USER_KEY);
    }
  }
};

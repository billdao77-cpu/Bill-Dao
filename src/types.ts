export type Role = 'SUPER_ADMIN' | 'ADMIN' | 'MEMBER';

export interface User {
  id: string;
  email: string;
  name: string;
  role: Role;
  avatar?: string;
  mustChangePassword?: boolean;
}

export interface BoardMember {
  id: string;
  name: string;
  position: string;
  organization: string;
  location: string;
  avatar?: string;
  type: 'BCH' | 'BTV' | 'BKT';
  isVacant?: boolean;
}

export interface Member {
  id: string;
  businessName: string;
  representative: string;
  taxCode: string;
  phone: string;
  email: string;
  website?: string;
  address: string;
  category: 'Lữ hành' | 'Lưu trú' | 'Nhà hàng' | 'Điểm đến' | 'OCOP' | 'Làng nghề' | 'Vận tải';
  feeStatus: 'Đã đóng' | 'Chưa đóng' | 'Quá hạn';
  logo?: string;
  documents?: string[];
}

export interface MarketplaceItem {
  id: string;
  memberId: string;
  title: string;
  description: string;
  price?: number;
  category: string;
  images: string[];
  createdAt: string;
}

export interface MeetingMinute {
  id: string;
  title: string;
  date: string;
  content: string;
  aiSummary?: string;
  aiTasks?: { task: string; PIC: string; deadline: string }[];
  aiSuggestions?: string;
}

export interface AppFile {
  id: string;
  name: string;
  type: string;
  size: number;
  category: 'members' | 'documents' | 'meetings' | 'marketplace';
  uploadDate: string;
  url: string;
}

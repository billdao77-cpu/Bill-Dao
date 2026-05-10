import { BoardMember, Member, MarketplaceItem, MeetingMinute } from './types';

export const BCH_MEMBERS: BoardMember[] = [
  { id: '1', name: 'Vũ Mạnh Thắng', position: 'Chủ tịch HĐTV', organization: 'Công ty Du lịch Quốc tế Việt – Lào', location: 'Thái Bình', type: 'BTV' },
  { id: '2', name: 'Nguyễn Văn Dương', position: 'Giám đốc', organization: 'Công ty TNHH Dương Thảo', location: 'Như Quỳnh', type: 'BTV' },
  { id: '3', name: 'Đào Ngọc Hoàng', position: 'Giám đốc', organization: 'CT CP XNK & ĐT XD Minh Khai Thái Bình', location: 'Thái Bình', type: 'BTV' },
  { id: '4', name: 'Đoàn Thế Hiển', position: 'Chủ cơ sở', organization: 'Khách sạn Hưng Thái', location: 'Phố Hiến', type: 'BTV' },
  { id: '5', name: 'Trần Quang Hà', position: 'Giám đốc', organization: 'Trung tâm kinh doanh Mobiphone Hưng Yên', location: 'Phố Hiến', type: 'BCH' },
  { id: '6', name: 'Nguyễn Thị Hồng Hải', position: 'Phó Giám đốc', organization: 'Khách sạn Phú Mỹ', location: 'Nguyễn văn Linh', type: 'BTV' },
  { id: '7', name: 'Đặng Quốc Thái', position: 'Chủ tịch HĐQT', organization: 'Thiên Trường Plaza', location: 'Trần Lãm', type: 'BTV' },
  { id: '8', name: 'Tạ Xuân Tỉnh', position: 'Chủ tịch HĐQT', organization: 'Công ty CP Long Phát Group', location: 'Thái Bình', type: 'BTV' },
  { id: '9', name: 'Trần Bá Phúc', position: 'Thủ nhang', organization: 'Quần thể DT Đình – Đền Bổng Điền', location: 'Tân Thuận', type: 'BTV' },
  { id: '10', name: 'Hoàng Văn Tường', position: 'Giám đốc', organization: 'Khách sạn Melia – Grand', location: '', type: 'BCH' },
  { id: '11', name: 'Đặng Tiến Vinh', position: 'Chuyên viên', organization: 'Phòng QLDL – Sở VHTTDL', location: 'Phố Hiến', type: 'BKT' },
  { id: '12', name: 'Nguyễn Văn Bình', position: 'Giám đốc', organization: 'Khách sạn Thái Bình', location: 'Phố Hiến', type: 'BCH' },
  { id: '13', name: 'Bùi Xuân Hoàn', position: 'Giám đốc', organization: 'Khách sạn Á Đông', location: 'Phố Hiến', type: 'BCH' },
  { id: '14', name: 'Nguyễn Văn Tám', position: 'Giám đốc', organization: 'Khách sạn Bình Minh', location: '', type: 'BCH' },
  { id: '15', name: 'Vũ Đồng Thanh', position: 'Giám đốc', organization: 'Khách sạn Phương Anh', location: 'Như Quỳnh', type: 'BCH' },
  { id: '16', name: 'Nguyễn Thị Thắm', position: 'Giám đốc', organization: 'Khách sạn Phương Anh', location: 'Như Quỳnh', type: 'BCH' },
  { id: '17', name: 'Nguyễn Như Khanh', position: 'Phó Chủ tịch', organization: 'Hội làng nghề Hương Xạ Thôn Cao', location: '', type: 'BCH' },
  { id: '18', name: 'Hoàng Thị Chung', position: 'Giám đốc', organization: 'HTX Mây tre Liên Khê, Khoái Châu', location: '', type: 'BCH' },
  { id: '19', name: 'Nguyễn Anh Tú', position: 'Giám đốc', organization: 'Công ty TNHH Đức Trung', location: '', type: 'BCH' },
  { id: '20', name: 'Vũ Hồng Ngân', position: 'Đại diện', organization: 'HTX Thủy sản Quang Hưng', location: '', type: 'BCH' },
  { id: '21', name: 'Vũ Phương Linh Anh', position: 'Phó Giám đốc', organization: 'Khách sạn Selegend', location: 'Trần Hưng Đạo', type: 'BCH' },
  { id: '22', name: 'Nguyễn Văn Trường', position: 'Giám đốc', organization: 'Công ty TNHH Trường Hưng', location: 'Trần lãm', type: 'BTV' },
  { id: '23', name: 'Nguyễn Thị Huyền Phin', position: 'Nghệ sỹ', organization: 'Nghệ sỹ nhân dân chèo', location: 'Trần Hưng Đạo', type: 'BCH' },
  { id: '24', name: 'Ngô Văn Phát', position: 'Chủ tịch HĐQT', organization: 'Tập đoàn Phú Thành', location: 'Thái bình', type: 'BCH' },
  { id: '25', name: 'Lê Tiến Lượng', position: 'Giám đốc', organization: 'Nhà hát Chèo Hưng Yên', location: 'Phố Hiến', type: 'BTV' },
  { id: '26', name: 'Lý Phương Hoa', position: 'Giám đốc', organization: 'Công ty CP Season World', location: 'Vũ Tiên', type: 'BCH' },
  { id: '27', name: 'Trần Thị Thuấn Hoa', position: 'Giám đốc', organization: 'Công ty TNHH New Đồng Châu', location: 'Ái Quốc', type: 'BCH' },
  { id: '28', name: 'Phạm Hữu Việt', position: 'Chủ tịch HĐQT', organization: 'Cty Cổ phần công nghệ Thái Bình Group', location: 'Trần Lãm', type: 'BTV' },
  { id: '29', name: 'Nguyễn Lan Anh', position: 'Giám đốc', organization: 'Công ty Du lịch VTB Travel', location: 'Thái Bình', type: 'BCH' },
  { id: '30', name: 'Nguyễn Quý Hưng', position: 'Giám đốc', organization: 'Nhà hàng Sen Vàng', location: 'Trần Lãm', type: 'BCH' },
  { id: '31', name: 'Nguyễn Thu Hương', position: 'Quản lý', organization: 'Trung tâm sự kiện Infinity', location: 'Trần Hưng Đạo', type: 'BCH' },
  { id: '32', name: 'Triệu Đăng Khoa', position: 'Chủ tịch', organization: 'Hội Mỹ nghệ Kim Hoàn Đồng Xâm', location: 'Trà Giang', type: 'BCH' },
  { id: '33', name: 'Bùi Văn Quang', position: 'Chủ tịch', organization: 'Hội đầu bếp Chuyên nghiệp Thái Bình', location: 'Thái Thụy', type: 'BCH' },
  { id: '34', name: 'Trần Văn Đông', position: 'Phó Giám đốc', organization: 'Nhà máy bánh kẹo Thiên Đức', location: 'Nam Đông Hưng', type: 'BCH' },
  { id: '35', name: 'Nguyễn Mạnh Đoan', position: 'Phó Giám đốc', organization: 'BQL các Khu Di tích, Chùa Keo', location: 'Vũ Tiên', type: 'BCH' },
  { id: '36', name: 'Đỗ Mạnh Hùng', position: 'Chi cục trưởng', organization: 'Chi cục ATVSTP – Sở Y tế Hưng Yên', location: 'Phố Hiến', type: 'BTV' },
  { id: '37', name: 'Trần Thị Oanh', position: 'Thư ký HHDL', organization: 'Nhà hàng Đông Dương', location: 'Trần Hưng Đạo', type: 'BCH' },
  { id: '38', name: 'Khổng Quang Vinh', position: 'Giám đốc điều hành', organization: 'Khách sạn An Thái TB', location: 'Thái Bình', type: 'BCH' },
  { id: '39', name: 'Nguyễn Văn Hạnh', position: 'Tổng Giám đốc', organization: 'Resort Làng Việt', location: 'Ái Quốc', type: 'BTV' },
  { id: '40', name: 'Nguyễn Viết Quân', position: 'CHT Chi hội HDV', organization: 'Cty Du lịch Quốc tế Việt – Lào', location: 'Thái Binh', type: 'BCH' },
  { id: '41', name: 'Vũ Hào Kiệt', position: 'Giám đốc', organization: 'Cty Du lịch Sao Việt', location: 'Trần Hưng Đạo', type: 'BCH' },
  { id: '42', name: 'Nguyễn Thị Cải', position: 'Chủ tịch HĐQT kiêm GĐ', organization: 'Cty CP DVTM & DL – Thúy Cải', location: 'Vũ Phúc', type: 'BCH' },
  { id: '43', name: 'Mai Ngọc Tuấn', position: 'Giám đốc', organization: 'Công ty TNHH Tâm Anh', location: 'Trần Lãm', type: 'BCH' },
  { id: '44', name: 'Nguyễn Tuấn Anh', position: 'Giám đốc', organization: 'Công ty GD&ĐT Quang Tuấn', location: 'Đông Hưng', type: 'BTV' },
  { id: '45', name: 'Đỗ Thị Bích Diệp', position: 'Giám đốc điều hành', organization: 'Khách sạn Sojo Thái Bình', location: 'Trần Hưng Đạo', type: 'BCH' },
  { id: '46', name: 'Phạm Thị Thơm', position: 'Giám đốc', organization: 'Cty TNHH & DVTMDL Hà Thanh', location: 'Trần Lãm', type: 'BCH' },
  { id: '47', name: 'Nguyễn Thị Huyền Trang', position: 'Phó Phòng KD', organization: 'Khách sạn Dream Thái Bình', location: 'Trần Lãm', type: 'BCH' },
  { id: '48', name: 'Lương Thanh Hạnh', position: 'Giám đốc', organization: 'HTX Lụa đũi Nam Cao', location: 'Lê Lợi', type: 'BCH' },
  { id: '49', name: 'Nguyễn Thế Đồng', position: 'BQL', organization: 'Di tích Lăng Mẫu Quế Hoa', location: 'Tân Thuận', type: 'BCH' },
  { id: '50', name: 'Trần Minh Hải', position: 'Giám đốc', organization: 'Cty Du lịch Sơn Hải', location: 'Thái Bình', type: 'BKT' },
  { id: '51', name: 'Bùi Thị Thu Trang', position: 'Giám đốc', organization: 'Cty Cổ phần Du lịch Araya Travel', location: 'Thái Thụy', type: 'BCH' },
  { id: '52', name: 'Vũ Trung Kiên', position: 'Giám đốc', organization: 'Khu Du lịch sinh thái biển Cồn Đen', location: 'Đông Thái Ninh', type: 'BCH' },
  { id: '53', name: 'Ngô Thị Phượng', position: 'Giám đốc', organization: 'Nhà hàng Tiền Hải TB', location: 'Tiền Hải', type: 'BCH' },
  { id: '54', name: 'Bùi Quốc Trung', position: 'Phòng AI', organization: 'Cty Hưng Thịnh Phát', location: 'Quang Trung', type: 'BCH' },
  { id: '55', name: 'Lê Văn Đông', position: 'Giám đốc', organization: 'Công ty TNHH Môi trường Xanh – Sạch – Đẹp', location: 'Trần Lãm', type: 'BCH' },
  { id: '56', name: 'Khuyết', position: 'Kiện toàn sau', organization: '', location: '', type: 'BCH', isVacant: true },
  { id: '57', name: 'Khuyết', position: 'Kiện toàn sau', organization: '', location: '', type: 'BCH', isVacant: true },
  { id: '58', name: 'Khuyết', position: 'Kiện toàn sau', organization: '', location: '', type: 'BCH', isVacant: true },
  { id: '59', name: 'Khuyết', position: 'Kiện toàn sau', organization: '', location: '', type: 'BCH', isVacant: true },
];

export const MOCK_MEMBERS: Member[] = [
  {
    id: 'm1',
    businessName: 'Du lịch Quốc tế Việt - Lào',
    representative: 'Vũ Mạnh Thắng',
    taxCode: '1000123456',
    phone: '0912345678',
    email: 'thang.vm@vietlaotour.com',
    website: 'vietlaotour.com',
    address: 'Thái Bình',
    category: 'Lữ hành',
    feeStatus: 'Đã đóng'
  },
  {
    id: 'm2',
    businessName: 'Khách sạn Hưng Thái',
    representative: 'Đoàn Thế Hiển',
    taxCode: '1000789012',
    phone: '0987654321',
    email: 'hungthaihotel@gmail.com',
    address: 'Phố Hiến, Hưng Yên',
    category: 'Lưu trú',
    feeStatus: 'Đã đóng'
  }
];

export const MOCK_MARKETPLACE: MarketplaceItem[] = [
  {
    id: 'p1',
    memberId: 'm1',
    title: 'Tour Hưng Yên - Thái Bình 2 ngày 1 đêm',
    description: 'Khám phá Phố Hiến và Chùa Keo với lịch trình đặc sắc.',
    price: 1500000,
    category: 'Tour du lịch',
    images: ['https://images.unsplash.com/photo-1540959733332-e94e270b4052?auto=format&fit=crop&w=800&q=80'],
    createdAt: new Date().toISOString()
  }
];

export const MOCK_MEETINGS: MeetingMinute[] = [
  {
    id: 'meet1',
    title: 'Họp BCH Thường kỳ Tháng 4/2026',
    date: '2026-04-10',
    content: 'Nội dung họp về công tác chuẩn bị Đại hội Khóa I. Thống nhất danh sách nhân dự 59 UV BCH...',
    aiSummary: 'Cuộc họp tập trung vào nhân sự Đại hội Khóa I và kế hoạch xúc tiến du lịch hè 2026.',
    aiTasks: [
      { task: 'Hoàn thiện hồ sơ nhân sự', PIC: 'Đào Ngọc Hoàng', deadline: '2026-04-20' },
      { task: 'Gửi thư mời đại biểu', PIC: 'Lê Tiến Lượng', deadline: '2026-04-25' }
    ]
  }
];

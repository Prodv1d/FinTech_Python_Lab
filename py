# Dữ liệu đầu vào thô
raw_data = [
    {
        "customer name": "  nGUyễn văn a  ",
        "phone_number": "+84 0912 345 678",
        "card_info": "Thanh toan qua the 4123-4567-8910-1112",
        "transaction_date": "31/12/2023",
        "amount": "$1,250.50",
        "notes": "Chuyen khoan mua chung khoan ma VNM gia 70"
    },
    {
        "customer name": "Trần Thị B",
        "phone_number": "0987654321",
        "card_info": "The tin dung: 5123456789109999 (NH Vietcombank)",
        "transaction_date": "2023-12-25",
        "amount": "5,000,000 VND",
        "notes": "Mua 500 co phieu FPT"
    },
    {
        "customer name": "lê văn C",
        "phone_number": "84-909-123-456",
        "card_info": "Visa 4000 1234 5678 9010",
        "transaction_date": "15-01-2024",
        "amount": "$ 50.00",
        "notes": "Thanh toan tien dien"
    }
]

# Yêu cầu 1: Chuẩn hóa Tên Khách Hàng
def normalize_name(name):
    # Loại bỏ khoảng trắng thừa ở hai đầu và thay thế khoảng trắng kép ở giữa bằng 1 khoảng trắng
    cleaned = re.sub(r'\s+', ' ', name.strip())
    # Viết hoa chữ cái đầu của mỗi từ (Title Case)
    return cleaned.title()

# Yêu cầu 2: Chuẩn hóa Số Điện Thoại
def normalize_phone(phone):
    # Xóa tất cả các ký tự không phải là số
    digits = re.sub(r'\D', '', phone)
    
    # Nếu bắt đầu bằng mã quốc gia 84 (ví dụ 8409... hoặc 84909...), ta xử lý về dạng 0 + 10 số
    if digits.startswith('84'):
        digits = '0' + digits[2:]
    
    # Đảm bảo trả về đúng 10 chữ số bắt đầu bằng số 0
    if not digits.startswith('0') and len(digits) == 9:
        digits = '0' + digits
        
    return digits

# Yêu cầu 3: Che dấu Dữ liệu Nhạy cảm - Data Masking
def mask_credit_card(text):
    # Biểu thức chính quy tìm các dãy 16 số, có thể phân cách bởi khoảng trắng, dấu gạch ngang hoặc viết liền
    # Ví dụ: 4123-4567-8910-1112 hoặc 5123456789109999 hoặc 4000 1234 5678 9010
    pattern = r'\b(?:\d[ -]*){15}\d\b'
    
    def replace_card(match):
        card_str = match.group(0)
        # Giữ lại các ký tự phân cách (nếu có) nhưng thay các chữ số trước 4 số cuối thành dấu *
        digits_only = re.sub(r'\D', '', card_str)
        if len(digits_only) == 16:
            last_4 = digits_only[-12:] # thực chất là giữ 4 số cuối, còn 12 số đầu che
            # Tái tạo lại định dạng ban đầu cho gọn hoặc che trực tiếp
            masked_digits = '****' + '-' + '****' + '-' + '****' + '-' + digits_only[-4:]
            return masked_digits
        return card_str

    return re.sub(pattern, replace_card, text)

# Yêu cầu 4: Xử lý Số liệu Tài chính
def clean_amount(amount_str):
    amount_str = str(amount_str)
    is_usd = '$' in amount_str
    
    # Loại bỏ các ký tự chữ cái, ký hiệu tiền tệ, dấu phẩy và khoảng trắng
    cleaned_str = re.sub(r'[^\d.]', '', amount_str)
    
    if cleaned_str == '':
        return 0.0
    
    value = float(cleaned_str)
    
    # Nếu là USD, chuyển đổi sang VND (tỷ giá 1 USD = 24,000 VND)
    if is_usd:
        value = value * 24000.0
        
    return value

# Yêu cầu 5: Trích xuất Dữ liệu - Information Extraction
def extract_stock_code(note):
    # Tìm mã chứng khoán gồm đúng 3 chữ cái in hoa viết liền nhau
    match = re.search(r'\b[A-Z]{3}\b', note)
    if match:
        return match.group(0)
    return None

# Xử lý toàn bộ danh sách dữ liệu thô
cleaned_data = []
for item in raw_data:
    cleaned_item = {
        "customer_name": normalize_name(item["customer name"]),
        "phone_number": normalize_phone(item["phone_number"]),
        "card_info": mask_credit_card(item["card_info"]),
        "transaction_date": item.get("transaction_date") or item.get("transaction date"),
        "amount_vnd": clean_amount(item["amount"]),
        "stock_code": extract_stock_code(item["notes"]),
        "notes": item["notes"]
    }
    cleaned_data.append(cleaned_item)

# In kết quả kiểm tra
for idx, data in enumerate(cleaned_data, 1):
    print(f"--- Bản ghi {idx} ---")
    for k, v in data.items():
        print(f"{k}: {v}")

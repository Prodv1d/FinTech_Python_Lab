import re

# Dữ liệu đầu vào thô chuẩn hóa theo đề bài
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
    cleaned = re.sub(r'\s+', ' ', name.strip())
    return cleaned.title()

# Yêu cầu 2: Chuẩn hóa Số Điện Thoại
def normalize_phone(phone):
    digits = re.sub(r'\D', '', phone)
    if digits.startswith('84'):
        digits = '0' + digits[2:]
    elif len(digits) == 9 and not digits.startswith('0'):
        digits = '0' + digits
    return digits

# Yêu cầu 3: Che dấu Dữ liệu Nhạy cảm - Data Masking
def mask_credit_card(text):
    # Biểu thức chính quy tìm chuỗi 16 số có phân cách hoặc liền nhau
    pattern = r'\b(?:\d[ -]*){15}\d\b'
    
    def replace_card(match):
        card_str = match.group(0)
        digits_only = re.sub(r'\D', '', card_str)
        if len(digits_only) == 16:
            return f"****-****-****-{digits_only[-4:]}"
        return card_str

    return re.sub(pattern, replace_card, text)

# Yêu cầu 4: Xử lý Số liệu Tài chính
def clean_amount(amount_str):
    amount_str = str(amount_str)
    is_usd = '$' in amount_str
    
    # Lọc lấy số và dấu chấm
    cleaned_str = re.sub(r'[^\d.]', '', amount_str)
    
    if not cleaned_str:
        return 0.0
    
    value = float(cleaned_str)
    if is_usd:
        value = value * 24000.0  # Quy đổi USD sang VND
        
    return value

# Yêu cầu 5: Trích xuất Dữ liệu - Information Extraction
def extract_stock_code(note):
    match = re.search(r'\b[A-Z]{3}\b', note)
    if match:
        return match.group(0)
    return None

# Xử lý toàn bộ danh sách dữ liệu thô
cleaned_data = []
for item in raw_data:
    # Lấy key ngày giao dịch linh hoạt phòng trường hợp khác biệt tên key
    t_date = item.get("transaction_date") if "transaction_date" in item else item.get("transaction date")
    
    cleaned_item = {
        "customer_name": normalize_name(item["customer name"]),
        "phone_number": normalize_phone(item["phone_number"]),
        "card_info": mask_credit_card(item["card_info"]),
        "transaction_date": t_date,
        "amount_vnd": clean_amount(item["amount"]),
        "stock_code": extract_stock_code(item["notes"]),
        "notes": item["notes"]
    }
    cleaned_data.append(cleaned_item)

# In kết quả ra màn hình IDLE
for idx, data in enumerate(cleaned_data, 1):
    print(f"=== BAN GHI {idx} ===")
    for k, v in data.items():
        print(f"{k}: {v}")
    print()

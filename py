import re

# Dữ liệu đầu vào thô đã được đổi key thành 'customer_name' cho đồng bộ[span_3](start_span)[span_3](end_span)[span_4](start_span)[span_4](end_span)
raw_data = [
    {
        "customer_name": "  nGUyễn văn a  ",
        "phone_number": "+84 0912 345 678",
        "card_info": "Thanh toan qua the 4123-4567-8910-1112",
        "transaction_date": "31/12/2023",
        "amount": "$1,250.50",
        "notes": "Chuyen khoan mua chung khoan ma VNM gia 70"
    },
    {
        "customer_name": "Trần Thị B",
        "phone_number": "0987654321",
        "card_info": "The tin dung: 5123456789109999 (NH Vietcombank)",
        "transaction_date": "2023-12-25",
        "amount": "5,000,000 VND",
        "notes": "Mua 500 co phieu FPT"
    },
    {
        "customer_name": "lê văn C",
        "phone_number": "84-909-123-456",
        "card_info": "Visa 4000 1234 5678 9010",
        "transaction_date": "15-01-2024",
        "amount": "$ 50.00",
        "notes": "Thanh toan tien dien"
    }
]

# 1. Hàm chuẩn hóa tên khách hàng[span_5](start_span)[span_5](end_span)
def normalize_name(name):
    name = name.strip()
    words = name.split()
    result = []
    for w in words:
        result.append(w.capitalize())
    return " ".join(result)

# 2. Hàm chuẩn hóa số điện thoại[span_6](start_span)[span_6](end_span)
def normalize_phone(phone):
    digits = ""
    for c in phone:
        if c.isdigit():
            digits = digits + c
            
    if digits.startswith("84"):
        digits = "0" + digits[2:]
    elif len(digits) == 9 and not digits.startswith("0"):
        digits = "0" + digits
    return digits

# 3. Hàm che số thẻ tín dụng (Data Masking)[span_7](start_span)[span_7](end_span)[span_8](start_span)[span_8](end_span)
def mask_credit_card(text):
    pattern = r"\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}"
    match = re.search(pattern, text)
    if match:
        card = match.group(0)
        digits = ""
        for c in card:
            if c.isdigit():
                digits = digits + c
        last_4 = digits[-4:]
        masked = "****-****-****-" + last_4
        return text.replace(card, masked)
    return text

# 4. Hàm xử lý số liệu tài chính và quy đổi USD[span_9](start_span)[span_9](end_span)
def clean_amount(amount_str):
    amount_str = str(amount_str)
    is_usd = "$" in amount_str
    
    cleaned = ""
    for c in amount_str:
        if c.isdigit() or c == ".":
            cleaned = cleaned + c
            
    if cleaned == "":
        return 0.0
        
    value = float(cleaned)
    if is_usd:
        value = value * 24000  # Tỷ giá 1 USD = 24,000 VND
    return value

# 5. Hàm trích xuất mã chứng khoán[span_10](start_span)[span_10](end_span)
def extract_stock_code(note):
    match = re.search(r"\b[A-Z]{3}\b", note)
    if match:
        return match.group(0)
    return None

# --- CHƯƠNG TRÌNH CHÍNH ---
cleaned_data = []

for item in raw_data:
    # Lấy trực tiếp dữ liệu từ các key đã đồng bộ
    name = item.get("customer_name")
    phone = item.get("phone_number")
    card = item.get("card_info")
    date = item.get("transaction_date")
    amount = item.get("amount")
    note = item.get("notes")
    
    # Tạo từ điển mới lưu kết quả sạch
    new_item = {
        "customer_name": normalize_name(name),
        "phone_number": normalize_phone(phone),
        "card_info": mask_credit_card(card),
        "transaction_date": date,
        "amount_vnd": clean_amount(amount),
        "stock_code": extract_stock_code(note)
    }
    cleaned_data.append(new_item)

# In kết quả kiểm tra ra màn hình[span_11](start_span)[span_11](end_span)
for i in range(len(cleaned_data)):
    print("Bản ghi số:", i + 1)
    for key in cleaned_data[i]:
        print("  -", key, ":", cleaned_data[i][key])
    print()
    

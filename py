import re

# 1. Dữ liệu đầu vào thô
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
        "card info": "The tin dung: 5123456789109999 (NH Vietcombank)",
        "transaction_date": "2023-12-25",
        "amount": "5,000,000 VND",
        "notes": "Mua 500 co phieu FPT"
    },
    {
        "customer name": "lê văn C",
        "phone_number": "84-909-123-456",
        "card info": "Visa 4000 1234 5678 9010",
        "transaction_date": "15-01-2024",
        "amount": "$ 50.00",
        "notes": "Thanh toan tien dien"
    }
]

# 2. Hàm chuẩn hóa tên: bỏ khoảng trắng thừa, viết hoa chữ cái đầu
def normalize_name(name):
    name = name.strip()
    words = name.split()
    result = []
    for w in words:
        result.append(w.capitalize())
    return " ".join(result)

# 3. Hàm chuẩn hóa số điện thoại: chỉ lấy số, đổi 84 thành 0
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

# 4. Hàm che số thẻ tín dụng: giữ lại 4 số cuối
def mask_credit_card(text):
    pattern = r"\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}"
    match = re.search(pattern, text)
    if match:
        card = match.group(0)
        # Lấy các chữ số của thẻ
        digits = ""
        for c in card:
            if c.isdigit():
                digits = digits + c
        last_4 = digits[-4:]
        masked = "****-****-****-" + last_4
        return text.replace(card, masked)
    return text

# 5. Hàm làm sạch tiền tệ và quy đổi USD sang VND
def clean_amount(amount_str):
    amount_str = str(amount_str)
    is_usd = "$" in amount_str
    
    # Lọc lấy số và dấu chấm
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

# 6. Hàm tìm mã chứng khoán (3 chữ cái in hoa)
def extract_stock_code(note):
    match = re.search(r"\b[A-Z]{3}\b", note)
    if match:
        return match.group(0)
    return None

# --- CHẠY CHƯƠNG TRÌNH CHÍNH ---
cleaned_data = []

for item in raw_data:
    # Lấy dữ liệu an toàn phòng trường hợp tên key khác nhau
    name = item.get("customer name")
    phone = item.get("phone_number")
    
    # Kiểm tra key thẻ (card_info hoặc card info)
    card = item.get("card_info")
    if card is None:
        card = item.get("card info")
        
    # Kiểm tra key ngày tháng
    date = item.get("transaction_date")
    if date is None:
        date = item.get("transaction date")
        
    amount = item.get("amount")
    note = item.get("notes")
    
    # Đưa vào từ điển mới
    new_item = {
        "customer_name": normalize_name(name),
        "phone_number": normalize_phone(phone),
        "card_info": mask_credit_card(card),
        "transaction_date": date,
        "amount_vnd": clean_amount(amount),
        "stock_code": extract_stock_code(note)
    }
    cleaned_data.append(new_item)

# In kết quả ra màn hình IDLE
for i in range(len(cleaned_data)):
    print("Bản ghi số:", i + 1)
    for key in cleaned_data[i]:
        print("  -", key, ":", cleaned_data[i][key])
    print()

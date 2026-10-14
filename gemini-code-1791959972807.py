import pandas as pd
import re

# 1. Khởi tạo dữ liệu đầu vào (Raw Data)
raw_data = [
    {
        "customer_name": " nGUyễn vĂn a ",
        "phone_number": "+84 0912 345 678",
        "card_info": "Thanh toan qua the 4123-4567-8910-1112",
        "transaction_date": "31/12/2023",
        "amount": "$1,250.50",
        "notes": "Chuyen khoan mua chung khoan ma VNM gia 70"
    },
    {
        "customer_name": "TRần ThỊ B ",
        "phone_number": "+84987654321",
        "card_info": "The tin dung: 5123456789109999 (NH Vietcombank)",
        "transaction_date": "2023-12-25",
        "amount": " 5,000,000 VND ",
        "notes": " Mua 500 co phieu FPT "
    }
]

df = pd.DataFrame(raw_data)

# 2. Hàm làm sạch và chuẩn hóa dữ liệu
def clean_customer_data(df):
    cleaned = df.copy()
    
    # Chuẩn hóa tên khách hàng
    cleaned['customer_name'] = cleaned['customer_name'].str.strip().str.title()
    
    # CẬP NHẬT: Chuẩn hóa số điện thoại (Chuyển +84 thành 0)
    def clean_phone(phone):
        # Bước 1: Xóa toàn bộ khoảng trắng
        phone = re.sub(r'\s+', '', phone)
        
        # Bước 2: Thay thế +840 thành 0 hoặc +84 thành 0
        phone = re.sub(r'^\+840', '0', phone)
        phone = re.sub(r'^\+84', '0', phone)
        
        return phone
        
    cleaned['phone_number'] = cleaned['phone_number'].apply(clean_phone)
    
    # Xử lý thông tin thẻ (Bảo mật số thẻ & lấy tên ngân hàng)
    def process_card(card_str):
        match = re.search(r'(\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4})', card_str)
        if match:
            raw_card = re.sub(r'\D', '', match.group(1))
            masked_card = f"****-****-****-{raw_card[-4:]}"
        else:
            masked_card = "N/A"
            
        bank_match = re.search(r'\(NH\s+([^)]+)\)', card_str, re.IGNORECASE)
        bank_name = bank_match.group(1) if bank_match else "Unknown"
        
        return masked_card, bank_name

    card_results = cleaned['card_info'].apply(process_card)
    cleaned['card_number_masked'] = [res[0] for res in card_results]
    cleaned['bank_name'] = [res[1] for res in card_results]
    
    # Chuẩn hóa ngày giao dịch (YYYY-MM-DD)
    def parse_date(date_str):
        for fmt in ('%d/%m/%Y', '%Y-%m-%d'):
            try:
                return pd.to_datetime(date_str, format=fmt).strftime('%Y-%m-%d')
            except ValueError:
                continue
        return date_str
    cleaned['transaction_date'] = cleaned['transaction_date'].apply(parse_date)
    
    # Chuẩn hóa số tiền và tách đơn vị
    def parse_amount(amt_str):
        amt_str = amt_str.strip()
        if '$' in amt_str:
            val = float(amt_str.replace('$', '').replace(',', ''))
            return val, 'USD'
        elif 'VND' in amt_str:
            val = float(amt_str.replace('VND', '').replace(',', '').strip())
            return val, 'VND'
        return 0.0, 'UNKNOWN'

    amount_results = cleaned['amount'].apply(parse_amount)
    cleaned['amount_value'] = [res[0] for res in amount_results]
    cleaned['currency'] = [res[1] for res in amount_results]
    
    # Trích xuất thông tin chứng khoán từ ghi chú
    def extract_notes(notes_str):
        stock_match = re.search(r'\b(VNM|FPT|VIC|VCB|HPG)\b', notes_str, re.IGNORECASE)
        stock_symbol = stock_match.group(1).upper() if stock_match else None
        
        qty_match = re.search(r'(\d+)\s*(?:co phieu|cổ phiếu)', notes_str, re.IGNORECASE)
        quantity = int(qty_match.group(1)) if qty_match else None
        
        return stock_symbol, quantity

    notes_results = cleaned['notes'].apply(extract_notes)
    cleaned['stock_symbol'] = [res[0] for res in notes_results]
    cleaned['quantity'] = [res[1] for res in notes_results]
    
    # Bỏ các cột thô ban đầu
    final_df = cleaned.drop(columns=['card_info', 'amount'])
    return final_df

# 3. Thực thi
cleaned_df = clean_customer_data(df)
print(cleaned_df[['customer_name', 'phone_number', 'card_number_masked', 'transaction_date', 'amount_value', 'currency']])
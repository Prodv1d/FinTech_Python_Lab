"""
Bài tập 1: Mở ví điện tử ban đầu (e_wallet_init.py)
Nhập thông tin khách hàng, tự động trừ phí mở ví, in biên lai khởi tạo.
"""

PHI_MO_VI = 50_000  # phí mở tài khoản (VND)

def nhap_so_tien():
    """nhập số tiền nạp đảm bảo là số hợp lệt và đủ để trừ phí."""
    while true:
        try:
            so_tien = float(input("nhập số tiền nạp ban đầu vào ví (VND): "))
        except ValueError:
            print("lỗi vui lòng nhập một con số hợp lệ (ví dụ:100000).")
            continue

        if so_tien < 0:
            print("lỗi số tiền không thể âm")
            continue
        if so_tien < PHI_MO_VI:
            print("số tiền nạp vào phải >= phí mở ví ({PHI_MO_VI:,.0f} VND).")
            continue
        return so_tien
def nhap_so_cccd():
    while true:
        so_cccd = float(input("Nhập số Căn cước công dân (CCCD): ")).strip()
        if not so_cccd.isdigit():
            print("lỗi CCCD chỉ được chứa chữ số.")
            continue

        if len(so_cccd) < 4:
            print("lỗi số CCCD phải có ít nhất 4 số")
            continue
        return so_cccd
def main():
    # 1. Nhập thông tin từ người dùng
    ho_ten = input("Nhập họ tên khách hàng: ")
    so_dien_thoai = input("Nhập số điện thoại: ")
    so_cccd = input("Nhập số Căn cước công dân (CCCD): ")
    so_tien_nap = float(input("Nhập số tiền nạp ban đầu vào ví (VND): "))

    # 2. Xử lý dữ liệu
    ho_ten_in_hoa = ho_ten.upper()          # Họ tên in hoa toàn bộ
    cccd_4_so_cuoi = so_cccd[-4:]           # Cắt chuỗi lấy 4 số cuối CCCD
    so_du_kha_dung = so_tien_nap - PHI_MO_VI  # Số dư thực tế sau khi trừ phí

    # 3. In biên lai khởi tạo ví
    print("\n" + "=" * 40)
    print("      BIÊN LAI KHỞI TẠO VÍ ĐIỆN TỬ")
    print("=" * 40)
    print(f"Họ tên khách hàng   : {ho_ten_in_hoa}")
    print(f"Số điện thoại       : {so_dien_thoai}")
    print(f"CCCD (4 số cuối)    : ****{cccd_4_so_cuoi}")
    print(f"Số tiền nạp ban đầu : {so_tien_nap:,.0f} VND")
    print(f"Phí mở ví           : {PHI_MO_VI:,.0f} VND")
    print("-" * 40)
    print(f"Số dư khả dụng      : {so_du_kha_dung:,.0f} VND")
    print("=" * 40)


if __name__ == "__main__":
    main()

"""
Bài tập 2: Tính hóa đơn bán lẻ thương mại điện tử (e_invoice.py)
Nhập thông tin sản phẩm, tính tổng tiền hàng, VAT, tổng thanh toán,
in hóa đơn với số tiền có dấu phân cách hàng nghìn.
"""

VAT_RATE = 0.08  # Thuế VAT 8%


def main():
    # 1. Nhập thông tin
    ten_san_pham = input("Nhập tên sản phẩm: ")
    so_luong = int(input("Nhập số lượng: "))
    don_gia = float(input("Nhập đơn giá (VND): "))

    # 2. Tính toán
    tong_tien_hang = so_luong * don_gia
    thue_vat = tong_tien_hang * VAT_RATE
    tong_thanh_toan = tong_tien_hang + thue_vat

    # 3. In hóa đơn
    print("\n" + "=" * 40)
    print("           HÓA ĐƠN BÁN HÀNG")
    print("=" * 40)
    print(f"Tên sản phẩm   : {ten_san_pham}")
    print(f"Số lượng       : {so_luong}")
    print(f"Đơn giá        : {don_gia:,.0f} VND")
    print("-" * 40)
    print(f"Tổng tiền hàng : {tong_tien_hang:,.0f} VND")
    print(f"Thuế VAT (8%)  : {thue_vat:,.0f} VND")
    print("-" * 40)
    print(f"Tổng thanh toán: {tong_thanh_toan:,.0f} VND")
    print("=" * 40)


if __name__ == "__main__":
    main()

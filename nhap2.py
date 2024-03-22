def kiem_tra_so_nguyen(n):
    if isinstance(n, int):
        return True
    else:
        return False

# Kiểm tra số nguyên
so_nguyen = 5
if kiem_tra_so_nguyen(so_nguyen):
    print(f"{so_nguyen} là số nguyên.")
else:
    print(f"{so_nguyen} không phải là số nguyên.")

# Kiểm tra số không phải số nguyên
so_nhat = 5.0
if kiem_tra_so_nguyen(so_nhat):
    print(f"{so_nhat} là số nguyên.")
else:
    print(f"{so_nhat} không phải là số nguyên.")

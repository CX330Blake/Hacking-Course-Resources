import string

cipher_text = "ifpmluglesecdlqp_rclfrseljpkq"
charset = string.ascii_lowercase + "_"


def modular_inverse(a, m):
    for i in range(m):
        if (a * i) % m == 1:
            return i
    return None


mod_inv_4 = modular_inverse(4, 27)  # 27 elements

plain_text = ""
for char in cipher_text:
    position = charset.index(char)
    original_pos = (mod_inv_4 * (position - 15)) % 27  # 逆向計算原始位置
    plain_text += charset[original_pos]  # 對應回原始字母

print(plain_text)

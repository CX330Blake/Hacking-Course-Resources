import string

charset = string.ascii_lowercase + string.digits
# 將數字們放前面並不影響，但是數字放中間不行，因為影響英文字母的次序性。


def caesar(input_string, rot):
    output_string = ""
    for i in range(len(input_string)):
        if input_string[i].isalnum():  # 判斷是不是數字
            idx = (charset.find(input_string[i]) + rot) % len(charset)
            output_string += charset[idx]
        else:  # 文字
            output_string += input_string[i]
    return output_string


enc = "7sj-ighm-742q3w4t"  # encrypt data

for i in range(len(charset)):
    flag = caesar(enc, i).upper()
    if "RC3" in flag:
        print(flag)

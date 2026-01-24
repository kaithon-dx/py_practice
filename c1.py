# データの型の変換
a = 10          # 整数型
b = 3.14        # 浮動小数点型
c = "42"        # 文字列型
# 整数型から浮動小数点型へ変換
a_float = float(a)
# 浮動小数点型から整数型へ変換
b_int = int(b)
# 文字列型から整数型へ変換
c_int = int(c)
print("a_float:", a_float)  # 出力: a_float: 10.0
print("b_int:", b_int) # 出力: b_int: 3
print("c_int:", c_int) # 出力: c_int: 42

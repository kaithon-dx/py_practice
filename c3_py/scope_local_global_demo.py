"""scope_local_global_demo.py

Pythonの「スコープ」と、ローカル変数/グローバル変数（+ nonlocal）を
1ファイルで確認するためのデモ。

ポイント（ざっくり）
- モジュール(ファイル)直下 = グローバル（正確には「モジュールスコープ」）
- def の中 = ローカル（関数ローカル）
- 関数内で「代入」した名前は、基本的にその関数のローカルになる
- グローバル変数へ関数内から代入したいなら global 宣言
- 入れ子関数で外側関数の変数へ代入したいなら nonlocal 宣言
- if/for/while/try のブロックは「新しいスコープ」を作らない（C/Javaと違う）

このファイルは「上から順に」読む＆実行してOKです。
"""

from __future__ import annotations


# ========== 0) グローバル（モジュール）スコープ ==========
MODULE_X = 100  # これは「このファイルのトップレベル」にあるのでグローバル


def demo_read_global_ok() -> None:
    """関数内からグローバル変数を『読むだけ』ならOK"""
    print("\n[demo_read_global_ok]")
    print("MODULE_X =", MODULE_X)


def demo_assign_makes_local() -> None:
    """関数内で代入があると、その名前はローカルになる（原則）"""
    print("\n[demo_assign_makes_local]")

    # ここで MODULE_X に代入すると、その瞬間この関数内の MODULE_X はローカル扱いになる。
    # そのため「代入より前で MODULE_X を読む」ようなコードを書くとエラーになりやすい。
    #
    # 例）下の2行をコメントアウト解除すると UnboundLocalError になる：
    # print(MODULE_X)      # ←『ローカルの MODULE_X』を読みに行くが、まだ未代入
    # MODULE_X = MODULE_X + 1

    local_value = MODULE_X + 1  # これは別名なのでOK（MODULE_X は参照だけ）
    print("local_value =", local_value)


def demo_global_keyword() -> None:
    """global を使うと、関数内からグローバル変数へ代入できる"""
    print("\n[demo_global_keyword]")

    global MODULE_X
    print("before MODULE_X =", MODULE_X)
    MODULE_X = MODULE_X + 1
    print("after  MODULE_X =", MODULE_X)


def demo_local_scope_is_per_function() -> None:
    """ローカルは関数ごとに独立している"""
    print("\n[demo_local_scope_is_per_function]")

    def inner1() -> None:
        v = "inner1 only"
        print("inner1 v =", v)

    def inner2() -> None:
        v = "inner2 only"
        print("inner2 v =", v)

    inner1()
    inner2()


def demo_nonlocal_keyword() -> None:
    """nonlocal は『1つ外側の関数スコープ』へ代入したい時に使う"""
    print("\n[demo_nonlocal_keyword]")

    def outer() -> None:
        count = 0

        def inc() -> None:
            nonlocal count
            count += 1
            print("count =", count)

        inc()
        inc()
        inc()

    outer()


def demo_block_scope_note() -> None:
    """if/for/try は新しいスコープを作らない（関数の中では同じローカル）"""
    print("\n[demo_block_scope_note]")

    if True:
        x = "made in if block"
    print("x (still visible) =", x)

    for i in range(1):
        y = "made in for block"
    print("y (still visible) =", y)

    try:
        z = "made in try block"
    except Exception:
        pass
    print("z (still visible) =", z)


def run_all() -> None:
    demo_read_global_ok()
    demo_assign_makes_local()
    demo_global_keyword()
    demo_local_scope_is_per_function()
    demo_nonlocal_keyword()
    demo_block_scope_note()


if __name__ == "__main__":
    run_all()

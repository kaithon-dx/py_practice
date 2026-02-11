import time, sys
indent = 0 # インデントの幅
indent_increasing = True # インデントが増えているかどうか

try:
    # try は「ここでエラー（例外）が起きるかもしれない処理」を囲って、
    # 起きたときの処理を except に書ける仕組み
    while True: # メインのプログラムのループ
        print(' ' * indent, end='')
        print('*************')
        time.sleep(0.1) # 0.1秒間止める
        if indent_increasing:
            # インデントを増やす
            indent += 1
            if indent == 20:
                # 方向を変える
                indent_increasing = False
        else:
            # インデントを減らす
            indent = indent - 1
            if indent == 0:
                # 方向を変える
                indent_increasing = True
except KeyboardInterrupt:
    sys.exit() # Ctrl-Cで終了
# finally: エラーの有無に関係なく必ず実行（後片付け向き、任意）を追加することも


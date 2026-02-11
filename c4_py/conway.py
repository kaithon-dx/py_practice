# Conwayのライフゲーム
import random, time, copy, sys
WIDTH = 60
HEIGHT = 20

# セルを格納するリストのリストを作成
next_cells = []
for x in range(WIDTH):
    column = [] # 新しい列を作成
    for y in range(HEIGHT):
        if random.randint(0, 1) == 0:
            column.append('#') # 生きたセルを追加
        else:
            column.append(' ') # 死んだセルを追加
    next_cells.append(column) # next_cellsは列のリストのリスト

try:
    while True: # メインループ
        print('\n' * 5) # ステップ間を開業で分ける
        current_cells = copy.deepcopy(next_cells)

        # current_cellsの内容を表示する
        for y in range(HEIGHT):
            for x in range(WIDTH):
                print(current_cells[x][y], end='') # #または空白を表示
            print() # 各行の終わりで改行する

        # 現在のセルに基づきnext_cellsの内容を計算する
        for x in range(WIDTH):
            for y in range(HEIGHT):
                # 隣接座標を取得
                # `% WIDTH`により left_coord を0〜WIDTH-1の範囲の値にする
                left_coord  = (x - 1) % WIDTH
                right_coord = (x + 1) % WIDTH
                above_coord = (y - 1) % HEIGHT
                below_coord = (y + 1) % HEIGHT

                # 生きた隣接セルの数を数える
                num_neighbors = 0
                if current_cells[left_coord][above_coord] == '#':
                    num_neighbors += 1 # 左上
                if current_cells[x][above_coord] == '#':
                    num_neighbors += 1 # 上
                if current_cells[right_coord][above_coord] == '#':
                    num_neighbors += 1 # 右上
                if current_cells[left_coord][y] == '#':
                    num_neighbors += 1 # 左
                if current_cells[right_coord][y] == '#':
                    num_neighbors += 1 # 右
                if current_cells[left_coord][below_coord] == '#':
                    num_neighbors += 1 # 左下
                if current_cells[x][below_coord] == '#':
                    num_neighbors += 1 # 下
                if current_cells[right_coord][below_coord] == '#':
                    num_neighbors += 1 # 右下

                # ライフゲームのルールに基づき、次の世代のセルを決定する
                if current_cells[x][y] == '#' and (num_neighbors == 2 or num_neighbors == 3):
                    # 生きたセルに隣接する生きたセルが2個か3個
                    next_cells[x][y] = '#' # 生きたセルはそのまま生きる
                elif current_cells[x][y] == ' ' and num_neighbors == 3:
                    # 死んだセルに隣接する生きたセルが3個
                    next_cells[x][y] = '#' # 死んだセルは誕生する
                else:
                    next_cells[x][y] = ' ' # その他の場合は死ぬ

        time.sleep(1) # ちらつきを防ぐため1秒間待つ
except KeyboardInterrupt:
    sys.exit() # Ctrl-Cで終了
"""
X/Y/Z カード対戦ゲーム
- X > Y > Z > X の力関係（じゃんけん式）
- 役の強さ: 3枚同じ > 3枚全部違う > 2枚+1枚
- CPUのヒントを読み取り、カード交換で有利に立て！
- 連勝数に応じて難易度が上昇！
"""

import random


def deal_hand():
    """ランダムに3枚のカードを配る"""
    cards = ['X', 'Y', 'Z']
    return [random.choice(cards) for _ in range(3)]


def get_hand_rank(hand):
    """
    役の強さを判定
    3: 3枚同じ（最強）
    2: 3枚全部違う（次点）
    1: 2枚+1枚（最弱）
    """
    unique = len(set(hand))
    if unique == 1:
        return 3  # 3枚同じ
    elif unique == 3:
        return 2  # 3枚全部違う
    else:
        return 1  # 2枚+1枚


def get_majority(hand):
    """手札のマジョリティ（最も多いカード）を返す"""
    count = {'X': 0, 'Y': 0, 'Z': 0}
    for card in hand:
        count[card] += 1
    return max(count, key=count.get)


def get_difficulty_mode(win_count):
    """連勝数に応じた難易度モードを返す"""
    if win_count < 10:
        return "かんたん"
    elif win_count < 30:
        return "やりがい"
    elif win_count < 50:
        return "挑戦"
    elif win_count < 100:
        return "鬼"
    elif win_count < 200:
        return "地獄篇"
    else:
        return "無限地獄篇"


def get_cpu_comment(hand, win_count):
    """CPUの手札に応じたコメントを生成（難易度で変化）"""
    mode = get_difficulty_mode(win_count)
    majority = get_majority(hand)
    rank = get_hand_rank(hand)
    
    # 無限地獄篇: 30%の確率で嘘をつく
    if mode == "無限地獄篇" and random.random() < 0.3:
        # 嘘のマジョリティと役を生成
        fake_majority = random.choice([c for c in ['X', 'Y', 'Z'] if c != majority])
        fake_rank = random.choice([r for r in [1, 2, 3] if r != rank])
        majority = fake_majority
        rank = fake_rank
    
    # 笑い声（マジョリティで決まる）
    if majority == 'X':
        laugh = "へへ！"
    elif majority == 'Y':
        laugh = "わっはっは、"
    else:  # Z
        laugh = "ゼハハハッ"
    
    # 調子のよさ（役で決まる）- 鬼モード以上は曖昧に
    if mode in ["鬼", "地獄篇", "無限地獄篇"]:
        if rank == 3 or rank == 2:
            condition = "調子良さげだ"
        else:
            condition = "知らん、早くしろ"
    else:
        if rank == 3:
            condition = "絶好調だ"
        elif rank == 2:
            condition = "そこそこだ"
        else:
            condition = "知らん、早くしろ"
    
    return f"{laugh}{condition}"


def get_card_reveal(cpu_hand, win_count):
    """難易度に応じてCPUのカードを開示"""
    mode = get_difficulty_mode(win_count)
    
    if mode == "かんたん":
        # 左端と右端を開示
        return f"  💡 ヒント: 左端は[{cpu_hand[0]}]、右端は[{cpu_hand[2]}]だ"
    elif mode == "やりがい":
        # 左端のみ開示
        return f"  💡 ヒント: 左端は[{cpu_hand[0]}]だ"
    elif mode == "挑戦":
        # 開示なし
        return "  💡 ヒント: ふふふ、教えないよ"
    elif mode == "鬼":
        # 開示なし + 役が曖昧
        return "  💡 ヒント: さあ、どうかな？"
    elif mode == "地獄篇":
        # 交換必須
        return "  💡 ヒント: 交換は必須だ、覚悟しろ"
    else:  # 無限地獄篇
        # 嘘をつく可能性あり
        return "  💡 ヒント: 信じるか信じないかはあなた次第..."


def compare_single_card(card1, card2):
    """
    単一カードの比較（じゃんけん式）
    X > Y, Y > Z, Z > X
    戻り値: 1=card1の勝ち, -1=card2の勝ち, 0=引き分け
    """
    if card1 == card2:
        return 0
    wins = {'X': 'Y', 'Y': 'Z', 'Z': 'X'}
    if wins[card1] == card2:
        return 1
    return -1


def compare_hands(player_hand, cpu_hand):
    """
    手札同士を比較
    戻り値: 1=プレイヤー勝利, -1=CPU勝利, 0=引き分け
    """
    player_rank = get_hand_rank(player_hand)
    cpu_rank = get_hand_rank(cpu_hand)
    
    # 役が違えば役の強さで決まる
    if player_rank != cpu_rank:
        return 1 if player_rank > cpu_rank else -1
    
    # 同じ役同士の場合、マジョリティで勝負
    player_majority = get_majority(player_hand)
    cpu_majority = get_majority(cpu_hand)
    
    return compare_single_card(player_majority, cpu_majority)


def display_hand(hand, name=""):
    """手札を表示"""
    if name:
        print(f"{name}: [{hand[0]}] [{hand[1]}] [{hand[2]}]")
    else:
        print(f"[{hand[0]}] [{hand[1]}] [{hand[2]}]")


def get_rank_name(hand):
    """役の名前を返す"""
    rank = get_hand_rank(hand)
    if rank == 3:
        return "【3枚同じ】"
    elif rank == 2:
        return "【3種全部】"
    else:
        return "【2枚+1枚】"


def select_position(prompt, valid_options):
    """ユーザーに位置を選択させる"""
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_options:
            return choice
        print("無効な入力です。もう一度選んでください。")


def play_round(win_count):
    """1ラウンドをプレイ（引き分けなら再配布でループ）"""
    
    while True:  # 引き分けの場合は再配布してループ
        mode = get_difficulty_mode(win_count)
        
        print("\n" + "=" * 50)
        print(f"【第{win_count + 1}戦】 - {mode}モード")
        print("=" * 50)
        
        # カードを配る
        player_hand = deal_hand()
        cpu_hand = deal_hand()
        
        # プレイヤーの手札を表示
        print("\n▼ あなたの手札:")
        display_hand(player_hand)
        print(f"  役: {get_rank_name(player_hand)}")
        
        # CPUのコメント（ヒント）
        print("\n▼ CPUのコメント:")
        print(f"  「{get_cpu_comment(cpu_hand, win_count)}」")
        
        # 難易度に応じたカード開示
        print(get_card_reveal(cpu_hand, win_count))
        
        # 交換するかどうか（地獄篇以上は強制交換）
        if mode in ["地獄篇", "無限地獄篇"]:
            print("\n▼ 地獄篇以上では交換は必須だ！")
            do_exchange = 'はい'
        else:
            print("\n▼ カードを交換しますか？")
            print("  （はい / いいえ）")
            do_exchange = select_position("  選択: ", ['はい', 'いいえ'])
        
        if do_exchange == 'はい':
            while True:  # 戻る操作用のループ
                # CPUのカードを選択
                print("\n▼ CPUの3枚のカードのうち、どれと交換する？")
                print("  （左 / まん中 / 右）")
                cpu_choice = select_position("  選択: ", ['左', 'まん中', '右'])
                cpu_index = {'左': 0, 'まん中': 1, '右': 2}[cpu_choice]
                
                # 自分のカードを選択
                print("\n▼ あなたの手札のどれと交換する？")
                display_hand(player_hand)
                print("  （左 / まん中 / 右 / 戻る）")
                player_choice = select_position("  選択: ", ['左', 'まん中', '右', '戻る'])
                
                if player_choice == '戻る':
                    print("\n← CPUの手札選択に戻ります...")
                    continue  # ループの最初に戻る
                
                player_index = {'左': 0, 'まん中': 1, '右': 2}[player_choice]
                break  # 選択完了、ループを抜ける
            
            # 交換実行
            player_hand[player_index], cpu_hand[cpu_index] = cpu_hand[cpu_index], player_hand[player_index]
            
            print("\n★ 交換成立！ ★")
        else:
            print("\n★ 交換なし！ ★")
        
        print("\n▼ 現在のあなたの手札:")
        display_hand(player_hand)
        print(f"  役: {get_rank_name(player_hand)}")
        
        # 対戦
        input("\n[Enter]を押したら対戦！")
        
        print("\n" + "-" * 50)
        print("【対戦結果】")
        print("-" * 50)
        
        print("\n▼ CPUの手札:")
        display_hand(cpu_hand)
        print(f"  役: {get_rank_name(cpu_hand)}")
        
        print("\n▼ あなたの手札:")
        display_hand(player_hand)
        print(f"  役: {get_rank_name(player_hand)}")
        
        # 勝敗判定
        result = compare_hands(player_hand, cpu_hand)
        
        print("\n" + "=" * 50)
        if result == 1:
            print("🎉 勝利！！ 🎉")
            return True
        elif result == -1:
            print("💀 敗北... 💀")
            return False
        else:
            # 引き分けは再配布
            print("😐 引き分け！ カードを配り直します...")
            input("[Enter]を押して再配布")
            # ループ継続（再配布）


def main():
    """メインゲームループ"""
    print("=" * 50)
    print("   X/Y/Z カード対戦ゲーム")
    print("=" * 50)
    print("""
【ルール説明】
・X/Y/Zの3枚がランダムに配られます
・力関係: X→Yに勝つ, Y→Zに勝つ, Z→Xに勝つ
・役の強さ:
  最強: 3枚同じ (例: X,X,X)
  次点: 3枚全部違う (例: X,Y,Z)
  最弱: 2枚+1枚 (例: X,X,Y)
・CPUのコメントをヒントに、カード交換（または交換なし）で勝負！
・引き分けの場合はカードを配り直し

【CPUのヒント解読】
  笑い声で多いカードがわかる:
    「へへ！」→X多め
    「わっはっは、」→Y多め  
    「ゼハハハッ」→Z多め
  調子で役がわかる:
    「絶好調だ」→3枚同じ
    「そこそこだ」→3枚全部違う
    「知らん、早くしろ」→2枚+1枚

【難易度モード】
  ～9連勝:   かんたん   → 左端と右端のカードを教えてもらえる
  10～29連勝: やりがい  → 左端のカードだけ教えてもらえる
  30～49連勝: 挑戦     → カード開示なし
  50～99連勝: 鬼       → 役のヒントが曖昧に
  100～199連勝: 地獄篇  → 「交換しない」を選べない
  200連勝～: 無限地獄篇 → CPUが30%の確率で嘘をつく
""")
    
    input("[Enter]を押してゲーム開始！")
    
    win_count = 0
    
    while True:
        if play_round(win_count):
            win_count += 1
            
            # 難易度変更の通知
            if win_count == 10:
                print("\n🔥 やりがいモード突入！ヒントが減ります...")
            elif win_count == 30:
                print("\n🔥🔥 挑戦モード突入！カード開示がなくなります...")
            elif win_count == 50:
                print("\n🔥🔥🔥 鬼モード突入！役のヒントが曖昧に...")
            elif win_count == 100:
                print("\n�🔥🔥🔥 地獄篇突入！交換は必須になります...")
            elif win_count == 200:
                print("\n👹 無限地獄篇突入！CPUが嘘をつくようになります...")
            
            print(f"\n現在 {win_count} 連勝中！")
            cont = input("続けますか？ (y/n): ").strip().lower()
            if cont != 'y':
                print(f"\n最終結果: {win_count} 連勝でした！")
                break
        else:
            print(f"\n【ゲームオーバー】")
            print(f"最終結果: {win_count} 連勝でした！")
            break
    
    print("\nまた遊んでね！")


if __name__ == "__main__":
    main()

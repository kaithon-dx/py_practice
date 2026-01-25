"""
X/Y/Z カード対戦ゲーム - Streamlit版
"""

import streamlit as st
import random

# ページ設定
st.set_page_config(
    page_title="X/Y/Z カード対戦",
    page_icon="🎴",
    layout="centered"
)

# カスタムCSS
st.markdown("""
<style>
    .card {
        display: inline-block;
        font-size: 2rem;
        padding: 15px 25px;
        margin: 5px;
        border: 3px solid #333;
        border-radius: 10px;
        background: linear-gradient(145deg, #ffffff, #e6e6e6);
        box-shadow: 5px 5px 10px #999;
    }
    .card-x { border-color: #e74c3c; color: #e74c3c; }
    .card-y { border-color: #3498db; color: #3498db; }
    .card-z { border-color: #2ecc71; color: #2ecc71; }
    .win-text { 
        color: #27ae60; 
        font-size: 3rem; 
        font-weight: bold;
        text-align: center;
    }
    .lose-text { 
        color: #e74c3c; 
        font-size: 3rem; 
        font-weight: bold;
        text-align: center;
    }
    .draw-text { 
        color: #f39c12; 
        font-size: 3rem; 
        font-weight: bold;
        text-align: center;
    }
    .cpu-comment {
        font-size: 1.8rem;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        background: linear-gradient(145deg, #f0f0f0, #e0e0e0);
        border-radius: 15px;
        margin: 10px 0;
    }
    .result-text {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
    }
    .mode-badge {
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


def deal_hand():
    """ランダムに3枚のカードを配る"""
    cards = ['X', 'Y', 'Z']
    return [random.choice(cards) for _ in range(3)]


def get_hand_rank(hand):
    """役の強さを判定"""
    unique = len(set(hand))
    if unique == 1:
        return 3  # 3枚同じ
    elif unique == 3:
        return 2  # 3枚全部違う
    else:
        return 1  # 2枚+1枚


def get_majority(hand):
    """手札のマジョリティを返す"""
    count = {'X': 0, 'Y': 0, 'Z': 0}
    for card in hand:
        count[card] += 1
    return max(count, key=count.get)


def get_difficulty_mode(win_count):
    """連勝数に応じた難易度モードを返す"""
    if win_count < 10:
        return "かんたん", "🟢"
    elif win_count < 30:
        return "やりがい", "🟡"
    elif win_count < 50:
        return "挑戦", "🟠"
    elif win_count < 100:
        return "鬼", "🔴"
    elif win_count < 200:
        return "地獄篇", "💀"
    else:
        return "無限地獄篇", "👹"


def get_cpu_comment(hand, win_count):
    """CPUの手札に応じたコメントを生成"""
    mode, _ = get_difficulty_mode(win_count)
    majority = get_majority(hand)
    rank = get_hand_rank(hand)
    
    # 無限地獄篇: 30%の確率で嘘をつく
    if mode == "無限地獄篇" and random.random() < 0.3:
        fake_majority = random.choice([c for c in ['X', 'Y', 'Z'] if c != majority])
        fake_rank = random.choice([r for r in [1, 2, 3] if r != rank])
        majority = fake_majority
        rank = fake_rank
    
    # 笑い声
    if majority == 'X':
        laugh = "へへ！"
    elif majority == 'Y':
        laugh = "わっはっは、"
    else:
        laugh = "ゼハハハッ"
    
    # 調子のよさ
    if mode in ["鬼", "地獄篇", "無限地獄篇"]:
        condition = "調子良さげだ" if rank in [2, 3] else "知らん、早くしろ"
    else:
        if rank == 3:
            condition = "絶好調だ"
        elif rank == 2:
            condition = "そこそこだ"
        else:
            condition = "知らん、早くしろ"
    
    return f"「{laugh}{condition}」"


def get_card_reveal(cpu_hand, win_count):
    """難易度に応じてCPUのカードを開示"""
    mode, _ = get_difficulty_mode(win_count)
    
    if mode == "かんたん":
        return f"💡 左端は **{cpu_hand[0]}**、右端は **{cpu_hand[2]}** だ"
    elif mode == "やりがい":
        return f"💡 左端は **{cpu_hand[0]}** だ"
    elif mode == "挑戦":
        return "💡 ふふふ、教えないよ"
    elif mode == "鬼":
        return "💡 さあ、どうかな？"
    elif mode == "地獄篇":
        return "💡 交換は必須だ、覚悟しろ"
    else:
        return "💡 信じるか信じないかはあなた次第..."


def compare_single_card(card1, card2):
    """単一カードの比較"""
    if card1 == card2:
        return 0
    wins = {'X': 'Y', 'Y': 'Z', 'Z': 'X'}
    return 1 if wins[card1] == card2 else -1


def compare_hands(player_hand, cpu_hand):
    """手札同士を比較"""
    player_rank = get_hand_rank(player_hand)
    cpu_rank = get_hand_rank(cpu_hand)
    
    if player_rank != cpu_rank:
        return 1 if player_rank > cpu_rank else -1
    
    player_majority = get_majority(player_hand)
    cpu_majority = get_majority(cpu_hand)
    
    return compare_single_card(player_majority, cpu_majority)


def get_rank_name(hand):
    """役の名前を返す"""
    rank = get_hand_rank(hand)
    if rank == 3:
        return "3枚同じ 👑"
    elif rank == 2:
        return "3種全部 ⭐"
    else:
        return "2枚+1枚"


def display_cards(hand, hidden=False):
    """カードを表示"""
    cards_html = ""
    for card in hand:
        if hidden:
            cards_html += '<span class="card">?</span>'
        else:
            card_class = f"card-{card.lower()}"
            cards_html += f'<span class="card {card_class}">{card}</span>'
    return f'<div style="text-align: center;">{cards_html}</div>'


# セッション状態の初期化
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'title'
    st.session_state.win_count = 0
    st.session_state.player_hand = []
    st.session_state.cpu_hand = []
    st.session_state.message = ""


def start_new_round():
    """新しいラウンドを開始"""
    st.session_state.player_hand = deal_hand()
    st.session_state.cpu_hand = deal_hand()
    st.session_state.game_state = 'playing'
    st.session_state.exchange_done = False


def reset_game():
    """ゲームをリセット"""
    st.session_state.game_state = 'title'
    st.session_state.win_count = 0
    st.session_state.player_hand = []
    st.session_state.cpu_hand = []


# タイトル画面
if st.session_state.game_state == 'title':
    st.markdown("# 🎴 X/Y/Z カード対戦ゲーム")
    
    with st.expander("📖 ルール説明", expanded=True):
        st.markdown("""
        ### 基本ルール
        - X/Y/Zの3枚がランダムに配られます
        - **力関係**: X→Yに勝つ, Y→Zに勝つ, Z→Xに勝つ
        
        ### 役の強さ
        1. 👑 **3枚同じ** (例: X,X,X) - 最強
        2. ⭐ **3枚全部違う** (例: X,Y,Z) - 次点
        3. **2枚+1枚** (例: X,X,Y) - 最弱
        
        ### CPUのヒント解読
        | 笑い声 | 意味 |
        |--------|------|
        | 「へへ！」 | X多め |
        | 「わっはっは、」 | Y多め |
        | 「ゼハハハッ」 | Z多め |
        
        | 調子 | 意味 |
        |------|------|
        | 「絶好調だ」 | 3枚同じ |
        | 「そこそこだ」 | 3枚全部違う |
        | 「知らん、早くしろ」 | 2枚+1枚 |
        """)
    
    with st.expander("🔥 難易度モード"):
        st.markdown("""
        | 連勝数 | モード | 特徴 |
        |--------|--------|------|
        | 0～9 | 🟢 かんたん | 左端と右端のカードを開示 |
        | 10～29 | 🟡 やりがい | 左端のカードのみ開示 |
        | 30～49 | 🟠 挑戦 | カード開示なし |
        | 50～99 | 🔴 鬼 | 役ヒントが曖昧に |
        | 100～199 | 💀 地獄篇 | 交換必須 |
        | 200～ | 👹 無限地獄篇 | CPUが30%で嘘をつく |
        """)
    
    st.markdown("---")
    if st.button("🎮 ゲームスタート", type="primary", use_container_width=True):
        start_new_round()
        st.rerun()


# ゲームプレイ画面
elif st.session_state.game_state == 'playing':
    mode, mode_icon = get_difficulty_mode(st.session_state.win_count)
    
    # ヘッダー
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"## 第{st.session_state.win_count + 1}戦")
    with col2:
        st.markdown(f"### {mode_icon} {mode}モード")
    
    st.markdown(f"### 🏆 現在 {st.session_state.win_count} 連勝中")
    
    st.markdown("---")
    
    # プレイヤーの手札
    st.markdown("### 🎴 あなたの手札")
    st.markdown(display_cards(st.session_state.player_hand), unsafe_allow_html=True)
    st.markdown(f"**役: {get_rank_name(st.session_state.player_hand)}**")
    
    st.markdown("---")
    
    # CPUのコメント
    st.markdown("### 🤖 CPUのコメント")
    cpu_comment = get_cpu_comment(st.session_state.cpu_hand, st.session_state.win_count)
    st.markdown(f'<div class="cpu-comment">{cpu_comment}</div>', unsafe_allow_html=True)
    st.markdown(get_card_reveal(st.session_state.cpu_hand, st.session_state.win_count))
    
    st.markdown("---")
    
    # 交換選択
    st.markdown("### 🔄 カード交換")
    
    # 地獄篇以上は交換必須
    can_skip = mode not in ["地獄篇", "無限地獄篇"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**CPUのカードを選択:**")
        cpu_choice = st.radio(
            "CPU",
            ["左", "まん中", "右"],
            horizontal=True,
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("**あなたのカードを選択:**")
        player_choice = st.radio(
            "Player",
            ["左", "まん中", "右"],
            horizontal=True,
            label_visibility="collapsed"
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 交換して勝負！", type="primary", use_container_width=True):
            cpu_index = {"左": 0, "まん中": 1, "右": 2}[cpu_choice]
            player_index = {"左": 0, "まん中": 1, "右": 2}[player_choice]
            
            # 交換実行
            st.session_state.player_hand[player_index], st.session_state.cpu_hand[cpu_index] = \
                st.session_state.cpu_hand[cpu_index], st.session_state.player_hand[player_index]
            
            st.session_state.game_state = 'result'
            st.rerun()
    
    with col2:
        if can_skip:
            if st.button("⏭️ 交換せずに勝負！", use_container_width=True):
                st.session_state.game_state = 'result'
                st.rerun()
        else:
            st.button("🚫 交換必須！", disabled=True, use_container_width=True)


# 結果画面
elif st.session_state.game_state == 'result':
    result = compare_hands(st.session_state.player_hand, st.session_state.cpu_hand)
    
    st.markdown("## 🎯 対戦結果")
    
    st.markdown("---")
    
    # CPUの手札
    st.markdown("### 🤖 CPUの手札")
    st.markdown(display_cards(st.session_state.cpu_hand), unsafe_allow_html=True)
    st.markdown(f"**役: {get_rank_name(st.session_state.cpu_hand)}**")
    
    st.markdown("### 🎴 あなたの手札")
    st.markdown(display_cards(st.session_state.player_hand), unsafe_allow_html=True)
    st.markdown(f"**役: {get_rank_name(st.session_state.player_hand)}**")
    
    st.markdown("---")
    
    # 勝敗表示
    if result == 1:
        st.markdown('<div class="win-text">🎉 勝利！！ 🎉</div>', unsafe_allow_html=True)
        
        st.session_state.win_count += 1
        
        # 難易度変更通知
        if st.session_state.win_count == 10:
            st.warning("🔥 やりがいモード突入！ヒントが減ります...")
        elif st.session_state.win_count == 30:
            st.warning("🔥🔥 挑戦モード突入！カード開示がなくなります...")
        elif st.session_state.win_count == 50:
            st.warning("🔥🔥🔥 鬼モード突入！役のヒントが曖昧に...")
        elif st.session_state.win_count == 100:
            st.error("💀 地獄篇突入！交換は必須になります...")
        elif st.session_state.win_count == 200:
            st.error("👹 無限地獄篇突入！CPUが嘘をつくようになります...")
        
        st.markdown(f'<div class="result-text">🏆 {st.session_state.win_count} 連勝！</div>', unsafe_allow_html=True)
        
        if st.button("▶️ 次の対戦へ", type="primary", use_container_width=True):
            start_new_round()
            st.rerun()
            
    elif result == -1:
        st.markdown('<div class="lose-text">💀 敗北... 💀</div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="result-text">最終結果: {st.session_state.win_count} 連勝でした！</div>', unsafe_allow_html=True)
        
        if st.button("🔄 もう一度プレイ", type="primary", use_container_width=True):
            reset_game()
            st.rerun()
    
    else:
        st.markdown('<div class="draw-text">😐 引き分け！</div>', unsafe_allow_html=True)
        st.markdown('<div class="result-text">カードを配り直します...</div>', unsafe_allow_html=True)
        
        if st.button("🔄 再配布", type="primary", use_container_width=True):
            start_new_round()
            st.rerun()


# フッター
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888;'>X/Y/Z カード対戦ゲーム v1.0</div>",
    unsafe_allow_html=True
)

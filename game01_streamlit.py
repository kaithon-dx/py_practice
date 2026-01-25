"""
X/Y/Z カード対戦ゲーム - Streamlit版
"""

import streamlit as st
import random

# ページ設定
st.set_page_config(
    page_title="X/Y/Z カード対戦",
    page_icon="🎴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# カスタムCSS
st.markdown("""
<style>
    /* スマホ対応: 余白・フォントをさらに圧縮 */
    .block-container {
        padding-top: 0.6rem !important;
        padding-bottom: 0rem !important;
    }
    h1, h2, h3, h4, h5 {
        margin-top: 0.2rem !important;
        margin-bottom: 0.2rem !important;
        line-height: 1.1 !important;
    }
    p, .stMarkdown {
        margin-bottom: 0.15rem !important;
        line-height: 1.2 !important;
    }
    hr {
        margin: 0.2rem 0 !important;
    }
    /* 画面上部の不要な余白を詰める */
    header, footer { visibility: hidden; height: 0; }
    .card {
        display: inline-block;
        font-size: 1.2rem;
        padding: 8px 12px;
        margin: 2px;
        border: 3px solid #333;
        border-radius: 8px;
        background: linear-gradient(145deg, #ffffff, #e6e6e6);
        box-shadow: 2px 2px 4px #999;
    }
    .card-x { border-color: #e74c3c; color: #e74c3c; }
    .card-y { border-color: #3498db; color: #3498db; }
    .card-z { border-color: #2ecc71; color: #2ecc71; }
    .win-text { 
        color: #27ae60; 
        font-size: 1.8rem; 
        font-weight: bold;
        text-align: center;
        margin: 0.2rem 0 !important;
    }
    .lose-text { 
        color: #e74c3c; 
        font-size: 1.8rem; 
        font-weight: bold;
        text-align: center;
        margin: 0.2rem 0 !important;
    }
    .draw-text { 
        color: #f39c12; 
        font-size: 1.8rem; 
        font-weight: bold;
        text-align: center;
        margin: 0.2rem 0 !important;
    }
    .cpu-comment {
        font-size: 1.1rem;
        font-weight: bold;
        text-align: center;
        padding: 8px;
        background: linear-gradient(145deg, #f0f0f0, #e0e0e0);
        border-radius: 10px;
        margin: 4px 0;
        color: #333333;
    }
    .result-text {
        font-size: 1.2rem;
        font-weight: bold;
        text-align: center;
        margin: 0.2rem 0 !important;
    }
    /* ボタンの余白を減らす */
    .stButton > button {
        margin-top: 0.1rem;
        margin-bottom: 0.1rem;
        padding: 0.35rem 0.6rem;
        font-size: 0.9rem;
    }
    /* ラジオボタンの余白を減らす */
    .stRadio > div {
        gap: 0.2rem;
    }
    /* モバイル用の文字サイズ調整 */
    @media (max-width: 480px) {
        h1 { font-size: 1.4rem !important; }
        h2 { font-size: 1.2rem !important; }
        h3 { font-size: 1.05rem !important; }
        h4, h5 { font-size: 0.95rem !important; }
        .stMarkdown, p { font-size: 0.9rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 定数
# =============================================================================
CARDS = ['X', 'Y', 'Z']
WINS_AGAINST = {'X': 'Y', 'Y': 'Z', 'Z': 'X'}  # X→Yに勝つ
POSITION_TO_INDEX = {"左": 0, "まん中": 1, "右": 2}

# 難易度設定 (閾値, モード名, アイコン)
DIFFICULTY_LEVELS = [
    (10, "かんたん", "🟢"),
    (30, "やりがい", "🟡"),
    (50, "挑戦", "🟠"),
    (100, "鬼", "🔴"),
    (200, "地獄篇", "💀"),
    (float('inf'), "無限地獄篇", "👹"),
]

# =============================================================================
# ゲームロジック関数
# =============================================================================
def deal_hand():
    """ランダムに3枚のカードを配る"""
    return [random.choice(CARDS) for _ in range(3)]


def get_hand_rank(hand):
    """
    役の強さを判定
    3: 3枚同じ（最強）, 2: 3枚全部違う（次点）, 1: 2枚+1枚（最弱）
    """
    unique_count = len(set(hand))
    return {1: 3, 3: 2, 2: 1}[unique_count]


def get_majority(hand):
    """手札のマジョリティ（最も多いカード）を返す"""
    return max(set(hand), key=hand.count)


def get_difficulty_mode(win_count):
    """連勝数に応じた難易度モードを返す"""
    for threshold, mode, icon in DIFFICULTY_LEVELS:
        if win_count < threshold:
            return mode, icon
    return DIFFICULTY_LEVELS[-1][1], DIFFICULTY_LEVELS[-1][2]


def compare_hands(player_hand, cpu_hand):
    """
    手札同士を比較
    戻り値: 1=プレイヤー勝利, -1=CPU勝利, 0=引き分け
    """
    player_rank = get_hand_rank(player_hand)
    cpu_rank = get_hand_rank(cpu_hand)
    
    if player_rank != cpu_rank:
        return 1 if player_rank > cpu_rank else -1
    
    # 同じ役同士の場合
    # 3種全部同士は力関係が成立しないため引き分け
    if player_rank == 2:
        return 0

    # それ以外はマジョリティで勝負
    player_maj = get_majority(player_hand)
    cpu_maj = get_majority(cpu_hand)

    if player_maj == cpu_maj:
        return 0
    return 1 if WINS_AGAINST[player_maj] == cpu_maj else -1


def get_rank_name(hand):
    """役の名前を返す"""
    rank = get_hand_rank(hand)
    return {3: "3枚同じ 👑", 2: "3種全部 ⭐", 1: "2枚+1枚"}[rank]


# =============================================================================
# CPU関連関数
# =============================================================================
def get_cpu_comment(hand, win_count):
    """CPUの手札に応じたコメントを生成"""
    mode, _ = get_difficulty_mode(win_count)
    majority = get_majority(hand)
    rank = get_hand_rank(hand)
    
    # 無限地獄篇: 30%の確率で嘘をつく
    if mode == "無限地獄篇" and random.random() < 0.3:
        majority = random.choice([c for c in CARDS if c != majority])
        rank = random.choice([r for r in [1, 2, 3] if r != rank])
    
    # 3種全部の場合は笑い声なしで「まあ、そこそこだ」
    if rank == 2:
        return "「まあ、そこそこだ」"
    
    # 笑い声（マジョリティで決まる）
    laughs = {'X': "へへ！", 'Y': "わっはっは、", 'Z': "ゼハハハッ"}
    laugh = laughs[majority]
    
    # 調子のよさ（役で決まる）
    if mode in ["鬼", "地獄篇", "無限地獄篇"]:
        condition = "調子良さげだ" if rank == 3 else "知らん、早くしろ"
    else:
        condition = "絶好調だ" if rank == 3 else "知らん、早くしろ"
    
    return f"「{laugh}{condition}」"


def get_card_reveal(cpu_hand, win_count):
    """難易度に応じてCPUのカードを開示"""
    mode, _ = get_difficulty_mode(win_count)
    
    reveals = {
        "かんたん": f"💡 左端は **{cpu_hand[0]}**、右端は **{cpu_hand[2]}** だ",
        "やりがい": f"💡 左端は **{cpu_hand[0]}** だ",
        "挑戦": "💡 ふふふ、教えないよ",
        "鬼": "💡 さあ、どうかな？",
        "地獄篇": "💡 交換は必須だ、覚悟しろ",
        "無限地獄篇": "💡 信じるか信じないかはあなた次第...",
    }
    return reveals.get(mode, "")


# =============================================================================
# 表示関数
# =============================================================================
def display_cards(hand):
    """カードをHTMLで表示"""
    cards_html = "".join(
        f'<span class="card card-{card.lower()}">{card}</span>' 
        for card in hand
    )
    return f'<div style="text-align: center;">{cards_html}</div>'


# =============================================================================
# セッション状態管理
# =============================================================================
def init_session_state():
    """セッション状態を初期化"""
    defaults = {
        'game_state': 'title',
        'win_count': 0,
        'player_hand': [],
        'cpu_hand': [],
        'result_processed': False,  # 結果処理済みフラグ
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def start_new_round():
    """新しいラウンドを開始"""
    st.session_state.player_hand = deal_hand()
    st.session_state.cpu_hand = deal_hand()
    st.session_state.game_state = 'playing'
    st.session_state.result_processed = False  # リセット


def reset_game():
    """ゲームをリセット"""
    st.session_state.game_state = 'title'
    st.session_state.win_count = 0
    st.session_state.player_hand = []
    st.session_state.cpu_hand = []
    st.session_state.result_processed = False


# 初期化
init_session_state()

# =============================================================================
# 画面表示
# =============================================================================

# -----------------------------------------------------------------------------
# タイトル画面
# -----------------------------------------------------------------------------
if st.session_state.game_state == 'title':
    st.markdown("# 🎴 X/Y/Z カード対戦ゲーム")
    
    with st.expander("📖 ルール説明", expanded=False):
        rules_col1, rules_col2 = st.columns(2)
        with rules_col1:
            st.markdown("""
            **基本ルール**
            - X/Y/Zの3枚がランダムに配られます
            - **力関係**: X→Yに勝つ, Y→Zに勝つ, Z→Xに勝つ
            """)
        with rules_col2:
            st.markdown("""
            **役の強さ**
            1. 👑 **3枚同じ** (例: X,X,X) - 最強
            2. ⭐ **3枚全部違う** (例: X,Y,Z) - 次点
            3. **2枚+1枚** (例: X,X,Y) - 最弱
            """)

        st.markdown("**CPUのヒント解読**")
        hint_col1, hint_col2 = st.columns(2)
        with hint_col1:
            st.markdown("""
            | 笑い声 | 意味 |
            |--------|------|
            | 「へへ！」 | X多め |
            | 「わっはっは、」 | Y多め |
            | 「ゼハハハッ」 | Z多め |
            """)
        with hint_col2:
            st.markdown("""
            | 調子 | 意味 |
            |------|------|
            | 「絶好調だ」 | 3枚同じ |
            | 「まあ、そこそこだ」 | 3枚全部違う |
            | 「知らん、早くしろ」 | 2枚+1枚 |
            """)
    
    with st.expander("🔥 難易度モード", expanded=False):
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

# -----------------------------------------------------------------------------
# ゲームプレイ画面
# -----------------------------------------------------------------------------
elif st.session_state.game_state == 'playing':
    mode, mode_icon = get_difficulty_mode(st.session_state.win_count)
    
    # ヘッダー（1行にまとめて縦幅を削減）
    st.markdown(
        f"### 第{st.session_state.win_count + 1}戦　{mode_icon} {mode}モード（{st.session_state.win_count}連勝中）"
    )
    st.markdown("---")
    
    # プレイヤーの手札（横並び）
    hand_col1, hand_col2 = st.columns([1, 3])
    with hand_col1:
        st.markdown("**🎴 あなたの手札**")
    with hand_col2:
        st.markdown(display_cards(st.session_state.player_hand), unsafe_allow_html=True)
    st.markdown(f"**役: {get_rank_name(st.session_state.player_hand)}**")
    st.markdown("---")
    
    # CPUのコメント（横並び）
    cpu_col1, cpu_col2 = st.columns([1, 3])
    with cpu_col1:
        st.markdown("**🤖 CPUのコメント**")
    with cpu_col2:
        cpu_comment = get_cpu_comment(st.session_state.cpu_hand, st.session_state.win_count)
        st.markdown(f'<div class="cpu-comment">{cpu_comment}</div>', unsafe_allow_html=True)
    st.markdown(get_card_reveal(st.session_state.cpu_hand, st.session_state.win_count))
    st.markdown("---")
    
    # 交換選択
    st.markdown("### 🔄 カード交換")
    can_skip = mode not in ["地獄篇", "無限地獄篇"]
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**CPUのカードを選択:**")
        cpu_choice = st.radio("CPU", ["左", "まん中", "右"], horizontal=True, label_visibility="collapsed")
    with col2:
        st.markdown("**あなたのカードを選択:**")
        player_choice = st.radio("Player", ["左", "まん中", "右"], horizontal=True, label_visibility="collapsed")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 交換して勝負！", type="primary", use_container_width=True):
            cpu_idx = POSITION_TO_INDEX[cpu_choice]
            player_idx = POSITION_TO_INDEX[player_choice]
            # 交換実行
            st.session_state.player_hand[player_idx], st.session_state.cpu_hand[cpu_idx] = \
                st.session_state.cpu_hand[cpu_idx], st.session_state.player_hand[player_idx]
            st.session_state.game_state = 'result'
            st.rerun()
    
    with col2:
        if can_skip:
            if st.button("⏭️ 交換せずに勝負！", use_container_width=True):
                st.session_state.game_state = 'result'
                st.rerun()
        else:
            st.button("🚫 交換必須！", disabled=True, use_container_width=True)

# -----------------------------------------------------------------------------
# 結果画面
# -----------------------------------------------------------------------------
elif st.session_state.game_state == 'result':
    result = compare_hands(st.session_state.player_hand, st.session_state.cpu_hand)
    
    # 勝利時のカウントアップは一度だけ実行
    if result == 1 and not st.session_state.result_processed:
        st.session_state.win_count += 1
        st.session_state.result_processed = True
    
    st.markdown("## 🎯 対戦結果")
    st.markdown("---")
    
    # CPUの手札
    st.markdown("### 🤖 CPUの手札")
    st.markdown(display_cards(st.session_state.cpu_hand), unsafe_allow_html=True)
    st.markdown(f"**役: {get_rank_name(st.session_state.cpu_hand)}**")
    
    # プレイヤーの手札
    st.markdown("### 🎴 あなたの手札")
    st.markdown(display_cards(st.session_state.player_hand), unsafe_allow_html=True)
    st.markdown(f"**役: {get_rank_name(st.session_state.player_hand)}**")
    st.markdown("---")
    
    # 勝敗表示
    if result == 1:
        st.markdown('<div class="win-text">🎉 勝利！！ 🎉</div>', unsafe_allow_html=True)
        
        # 難易度変更通知
        milestone_messages = {
            10: ("warning", "🔥 やりがいモード突入！ヒントが減ります..."),
            30: ("warning", "🔥🔥 挑戦モード突入！カード開示がなくなります..."),
            50: ("warning", "🔥🔥🔥 鬼モード突入！役のヒントが曖昧に..."),
            100: ("error", "💀 地獄篇突入！交換は必須になります..."),
            200: ("error", "👹 無限地獄篇突入！CPUが嘘をつくようになります..."),
        }
        if st.session_state.win_count in milestone_messages:
            msg_type, msg = milestone_messages[st.session_state.win_count]
            getattr(st, msg_type)(msg)
        
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
    
    else:  # 引き分け
        st.markdown('<div class="draw-text">😐 引き分け！</div>', unsafe_allow_html=True)
        st.markdown('<div class="result-text">カードを配り直します...</div>', unsafe_allow_html=True)
        
        if st.button("🔄 再配布", type="primary", use_container_width=True):
            start_new_round()
            st.rerun()

# -----------------------------------------------------------------------------
# フッター
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888;'>X/Y/Z カード対戦ゲーム v1.1</div>",
    unsafe_allow_html=True
)

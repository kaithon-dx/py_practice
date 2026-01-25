"""
X/Y/Z Card Battle - Streamlit (English)
"""

import streamlit as st
import random
import urllib.parse

# Page config
st.set_page_config(
    page_title="X/Y/Z Card Battle",
    page_icon="🎴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    /* Mobile-friendly compact layout */
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
    .help-box {
        font-size: 0.85rem;
        line-height: 1.2;
        background: #f7f7f7;
        border: 1px solid #e2e2e2;
        border-radius: 8px;
        padding: 6px 8px;
        color: #222222;
    }
    .stButton > button {
        margin-top: 0.1rem;
        margin-bottom: 0.1rem;
        padding: 0.35rem 0.6rem;
        font-size: 0.9rem;
    }
    .stRadio > div {
        gap: 0.2rem;
    }
    .stMarkdown table {
        font-size: 0.85rem !important;
        table-layout: auto;
    }
    .stMarkdown th, .stMarkdown td {
        padding: 4px 6px !important;
        white-space: nowrap;
    }
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
# Constants
# =============================================================================
CARDS = ['X', 'Y', 'Z']
WINS_AGAINST = {'X': 'Y', 'Y': 'Z', 'Z': 'X'}
POSITION_TO_INDEX = {"Left": 0, "Middle": 1, "Right": 2}
APP_URL = "https://testgame0125.streamlit.app"
SHARE_HASHTAG = "#XYZCardBattle"

DIFFICULTY_LEVELS = [
    (10, "Easy", "🟢"),
    (30, "Challenging", "🟡"),
    (50, "Hard", "🟠"),
    (100, "Oni", "🔴"),
    (200, "Hell", "💀"),
    (float('inf'), "Endless Hell", "👹"),
]

# =============================================================================
# Game logic
# =============================================================================
def deal_hand():
    return [random.choice(CARDS) for _ in range(3)]


def get_hand_rank(hand):
    unique_count = len(set(hand))
    return {1: 3, 3: 2, 2: 1}[unique_count]


def get_majority(hand):
    return max(set(hand), key=hand.count)


def get_difficulty_mode(win_count):
    for threshold, mode, icon in DIFFICULTY_LEVELS:
        if win_count < threshold:
            return mode, icon
    return DIFFICULTY_LEVELS[-1][1], DIFFICULTY_LEVELS[-1][2]


def compare_hands(player_hand, cpu_hand):
    player_rank = get_hand_rank(player_hand)
    cpu_rank = get_hand_rank(cpu_hand)

    if player_rank != cpu_rank:
        return 1 if player_rank > cpu_rank else -1

    if player_rank == 2:
        return 0

    player_maj = get_majority(player_hand)
    cpu_maj = get_majority(cpu_hand)

    if player_maj == cpu_maj:
        return 0
    return 1 if WINS_AGAINST[player_maj] == cpu_maj else -1


def get_rank_name(hand):
    rank = get_hand_rank(hand)
    return {3: "Three of a kind 👑", 2: "All different ⭐", 1: "Two + One"}[rank]


# =============================================================================
# CPU helpers
# =============================================================================
def get_cpu_comment(hand, win_count):
    mode, _ = get_difficulty_mode(win_count)
    majority = get_majority(hand)
    rank = get_hand_rank(hand)

    if mode == "Endless Hell" and random.random() < 0.3:
        majority = random.choice([c for c in CARDS if c != majority])
        rank = random.choice([r for r in [1, 2, 3] if r != rank])

    if rank == 2:
        return "\"Well, not bad.\""

    laughs = {'X': "Heh!", 'Y': "Hahaha!", 'Z': "Zehahaha!"}
    laugh = laughs[majority]

    if mode in ["Oni", "Hell", "Endless Hell"]:
        condition = "Feeling good." if rank == 3 else "Whatever. Hurry up."
    else:
        condition = "Perfect." if rank == 3 else "Whatever. Hurry up."

    return f"\"{laugh} {condition}\""


def get_card_reveal(cpu_hand, win_count):
    mode, _ = get_difficulty_mode(win_count)

    reveals = {
        "Easy": f"💡 Left is **{cpu_hand[0]}**, right is **{cpu_hand[2]}**",
        "Challenging": f"💡 Left is **{cpu_hand[0]}**",
        "Hard": "💡 I won't tell you.",
        "Oni": "💡 Guess if you can.",
        "Hell": "💡 Exchange is mandatory.",
        "Endless Hell": "💡 Believe me if you want...",
    }
    return reveals.get(mode, "")


# =============================================================================
# UI helpers
# =============================================================================
def display_cards(hand):
    cards_html = "".join(
        f'<span class="card card-{card.lower()}">{card}</span>'
        for card in hand
    )
    return f'<div style="text-align: center;">{cards_html}</div>'


def build_share_text(win_count, result_label):
    return f"{result_label}! My streak is {win_count} wins. {SHARE_HASHTAG}"


def render_share_section(win_count, result_label):
    share_text = build_share_text(win_count, result_label)
    tweet_text = urllib.parse.quote(share_text)
    tweet_url = urllib.parse.quote(APP_URL)
    x_share_url = f"https://twitter.com/intent/tweet?text={tweet_text}&url={tweet_url}"

    st.markdown("**Share your streak on SNS**")
    col_share1, col_share2 = st.columns(2)
    with col_share1:
        st.link_button("Post on X", x_share_url, use_container_width=True)
    with col_share2:
        st.link_button("Open Instagram", "https://www.instagram.com/", use_container_width=True)
    st.text_input(
        "Instagram caption (copy & paste)",
        value=f"{share_text} {APP_URL}",
        label_visibility="collapsed",
    )


# =============================================================================
# Session state
# =============================================================================
def init_session_state():
    defaults = {
        'game_state': 'title',
        'win_count': 0,
        'player_hand': [],
        'cpu_hand': [],
        'result_processed': False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def start_new_round():
    st.session_state.player_hand = deal_hand()
    st.session_state.cpu_hand = deal_hand()
    st.session_state.game_state = 'playing'
    st.session_state.result_processed = False


def reset_game():
    st.session_state.game_state = 'title'
    st.session_state.win_count = 0
    st.session_state.player_hand = []
    st.session_state.cpu_hand = []
    st.session_state.result_processed = False


init_session_state()

# =============================================================================
# Screens
# =============================================================================

# Title
if st.session_state.game_state == 'title':
    st.markdown("# 🎴 X/Y/Z Card Battle")

    with st.expander("📖 Rules", expanded=False):
        rules_col1, rules_col2 = st.columns(2)
        with rules_col1:
            st.markdown("""
            **Basics**
            - You get 3 cards: X/Y/Z
            - **Power**: X beats Y, Y beats Z, Z beats X
            """)
        with rules_col2:
            st.markdown("""
            **Hands**
            1. 👑 **Three of a kind** - strongest
            2. ⭐ **All different** - next
            3. **Two + One** - weakest
            """)

        st.markdown("**CPU Hints**")
        hint_col1, hint_col2 = st.columns(2)
        with hint_col1:
            st.markdown("""
            | Laugh | Meaning |
            |------|--------|
            | "Heh!" | X majority |
            | "Hahaha!" | Y majority |
            | "Zehahaha!" | Z majority |
            """)
        with hint_col2:
            st.markdown("""
            | Condition | Meaning |
            |----------|---------|
            | "Perfect." | Three of a kind |
            | "Well, not bad." | All different |
            | "Whatever. Hurry up." | Two + One |
            """)

    with st.expander("🔥 Difficulty", expanded=False):
        st.markdown("""
        | Streak | Mode | Feature |
        |--------|------|---------|
        | 0–9 | 🟢 Easy | Reveal left & right |
        | 10–29 | 🟡 Challenging | Reveal left only |
        | 30–49 | 🟠 Hard | No reveal |
        | 50–99 | 🔴 Oni | Vague hand hint |
        | 100–199 | 💀 Hell | Exchange required |
        | 200+ | 👹 Endless Hell | 30% lie chance |
        """)

    st.markdown("---")
    if st.button("🎮 Start Game", type="primary", use_container_width=True):
        start_new_round()
        st.rerun()

# Gameplay
elif st.session_state.game_state == 'playing':
    mode, mode_icon = get_difficulty_mode(st.session_state.win_count)

    st.markdown(
        f"### Round {st.session_state.win_count + 1}  {mode_icon} {mode} ({st.session_state.win_count} wins)"
    )
    st.markdown("---")

    hand_col1, hand_col2 = st.columns([1, 3])
    with hand_col1:
        st.markdown("**🎴 Your hand**")
    with hand_col2:
        st.markdown(display_cards(st.session_state.player_hand), unsafe_allow_html=True)
    st.markdown(f"**Hand: {get_rank_name(st.session_state.player_hand)}**")
    st.markdown("---")

    cpu_col1, cpu_col2 = st.columns([1, 3])
    with cpu_col1:
        st.markdown("**🤖 CPU comment**")
    with cpu_col2:
        cpu_comment = get_cpu_comment(st.session_state.cpu_hand, st.session_state.win_count)
        st.markdown(f'<div class="cpu-comment">{cpu_comment}</div>', unsafe_allow_html=True)
    st.markdown(get_card_reveal(st.session_state.cpu_hand, st.session_state.win_count))
    st.markdown("---")

    exchange_col, help_col = st.columns([3, 2])

    with exchange_col:
        st.markdown("### 🔄 Exchange")
        can_skip = mode not in ["Hell", "Endless Hell"]

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Select your card:**")
            player_choice = st.radio("Player", ["Left", "Middle", "Right"], horizontal=True, label_visibility="collapsed")
        with col2:
            st.markdown("**Select CPU card:**")
            cpu_choice = st.radio("CPU", ["Left", "Middle", "Right"], horizontal=True, label_visibility="collapsed")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Exchange & Battle!", type="primary", use_container_width=True):
                cpu_idx = POSITION_TO_INDEX[cpu_choice]
                player_idx = POSITION_TO_INDEX[player_choice]
                st.session_state.player_hand[player_idx], st.session_state.cpu_hand[cpu_idx] = \
                    st.session_state.cpu_hand[cpu_idx], st.session_state.player_hand[player_idx]
                st.session_state.game_state = 'result'
                st.rerun()

        with col2:
            if can_skip:
                if st.button("⏭️ Battle without exchange", use_container_width=True):
                    st.session_state.game_state = 'result'
                    st.rerun()
            else:
                st.button("🚫 Exchange required", disabled=True, use_container_width=True)

    with help_col:
        st.markdown("**Mini Rules**")
        st.markdown(
            """
            <div class="help-box">
            <div>• Power: X > Y > Z > X</div>
            <div>• Hands: 3 same > all different > 2+1</div>
            <div>• Same hand → majority wins</div>
            <hr style="margin:4px 0;" />
            <div>• Hell+ requires exchange</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Result
elif st.session_state.game_state == 'result':
    result = compare_hands(st.session_state.player_hand, st.session_state.cpu_hand)

    if result == 1 and not st.session_state.result_processed:
        st.session_state.win_count += 1
        st.session_state.result_processed = True

    st.markdown("## 🎯 Result")
    st.markdown("---")

    st.markdown("### 🤖 CPU hand")
    st.markdown(display_cards(st.session_state.cpu_hand), unsafe_allow_html=True)
    st.markdown(f"**Hand: {get_rank_name(st.session_state.cpu_hand)}**")

    st.markdown("### 🎴 Your hand")
    st.markdown(display_cards(st.session_state.player_hand), unsafe_allow_html=True)
    st.markdown(f"**Hand: {get_rank_name(st.session_state.player_hand)}**")
    st.markdown("---")

    if result == 1:
        st.markdown('<div class="win-text">🎉 Victory!! 🎉</div>', unsafe_allow_html=True)

        milestone_messages = {
            10: ("warning", "🔥 Challenging mode unlocked!"),
            30: ("warning", "🔥🔥 Hard mode unlocked!"),
            50: ("warning", "🔥🔥🔥 Oni mode unlocked!"),
            100: ("error", "💀 Hell mode unlocked! Exchange required."),
            200: ("error", "👹 Endless Hell unlocked! 30% lie chance."),
        }
        if st.session_state.win_count in milestone_messages:
            msg_type, msg = milestone_messages[st.session_state.win_count]
            getattr(st, msg_type)(msg)

        st.markdown(f'<div class="result-text">🏆 {st.session_state.win_count} wins!</div>', unsafe_allow_html=True)

        if st.button("▶️ Next battle", type="primary", use_container_width=True):
            start_new_round()
            st.rerun()

        render_share_section(st.session_state.win_count, "Victory")

    elif result == -1:
        st.markdown('<div class="lose-text">💀 Defeat... 💀</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-text">Final: {st.session_state.win_count} wins</div>', unsafe_allow_html=True)
        render_share_section(st.session_state.win_count, "Defeat")

        if st.button("🔄 Play again", type="primary", use_container_width=True):
            reset_game()
            st.rerun()

    else:
        st.markdown('<div class="draw-text">😐 Draw!</div>', unsafe_allow_html=True)
        st.markdown('<div class="result-text">Redeal the cards...</div>', unsafe_allow_html=True)

        if st.button("🔄 Redeal", type="primary", use_container_width=True):
            start_new_round()
            st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888;'>X/Y/Z Card Battle v1.1</div>",
    unsafe_allow_html=True
)

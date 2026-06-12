import os
from pathlib import Path

import streamlit as st
from openai import OpenAI

# ローカルで試す場合だけここにAPIキーを入れてOK。
# Streamlit Cloudでは、Secretsに OPENAI_API_KEY を入れるので空のままでOK。
OPENAI_API_KEY = ""

st.set_page_config(page_title="Tarot Reflection", page_icon="🃏", layout="centered")

BASE_DIR = Path(__file__).parent
CARDS_DIR = BASE_DIR / "cards"

TAROT_CARDS = [
    {"number": 0, "name_en": "THE FOOL", "name_ja": "愚者", "image": "00_fool.jpg", "symbol": "始まり、無垢、未知への一歩、自由、衝動、まだ形になる前の可能性"},
    {"number": 1, "name_en": "THE MAGUS", "name_ja": "魔術師", "image": "01_magus.jpg", "symbol": "意志、創造、言葉にする力、始動、手元にある道具を使うこと"},
    {"number": 2, "name_en": "THE HIGH PRIESTESS", "name_ja": "女教皇", "image": "02_high_priestess.jpg", "symbol": "沈黙、直感、まだ言葉にならない知、隠された本音、内側の水面"},
    {"number": 3, "name_en": "THE EMPRESS", "name_ja": "女帝", "image": "03_empress.jpg", "symbol": "豊かさ、育つもの、受容、身体感覚、愛情、自然な実り"},
    {"number": 4, "name_en": "THE EMPEROR", "name_ja": "皇帝", "image": "04_emperor.jpg", "symbol": "秩序、父性、責任、構造、守る力、揺るがない土台"},
    {"number": 5, "name_en": "THE HIEROPHANT", "name_ja": "教皇", "image": "05_hierophant.jpg", "symbol": "制度、信仰、教え、伝統、形式、形骸化したルール、受け継がれるもの"},
    {"number": 6, "name_en": "THE LOVERS", "name_ja": "恋人", "image": "06_lovers.jpg", "symbol": "選択、関係性、惹かれ合い、価値観、他者を通して自分を知ること"},
    {"number": 7, "name_en": "THE CHARIOT", "name_ja": "戦車", "image": "07_chariot.jpg", "symbol": "前進、意志、制御、葛藤を抱えたまま進む力、勝利への集中"},
    {"number": 8, "name_en": "STRENGTH", "name_ja": "力", "image": "08_strength.jpg", "symbol": "やさしい強さ、本能との和解、忍耐、内側から湧く力、支配しない勇気"},
    {"number": 9, "name_en": "THE HERMIT", "name_ja": "隠者", "image": "09_hermit.jpg", "symbol": "孤独、探求、内省、静かな知恵、自分だけの灯り、距離を置くこと"},
    {"number": 10, "name_en": "WHEEL OF FORTUNE", "name_ja": "運命の輪", "image": "10_wheel_of_fortune.jpg", "symbol": "変化、循環、タイミング、抗えない流れ、偶然に見える必然"},
    {"number": 11, "name_en": "JUSTICE", "name_ja": "正義", "image": "11_justice.jpg", "symbol": "公平さ、判断、均衡、責任、感情に流されない視線、張り詰めた誠実さ"},
    {"number": 12, "name_en": "THE HANGED MAN", "name_ja": "吊るされた男", "image": "12_hanged_man.jpg", "symbol": "停止、視点の反転、信念に基づく静止、手放し、意味の熟成"},
    {"number": 13, "name_en": "DEATH", "name_ja": "死神", "image": "13_death.jpg", "symbol": "終わり、変容、脱皮、避けられない区切り、新しい状態への移行"},
    {"number": 14, "name_en": "TEMPERANCE", "name_ja": "節制", "image": "14_temperance.jpg", "symbol": "調和、混ざり合うもの、回復、バランス、少しずつ整えること"},
    {"number": 15, "name_en": "THE DEVIL", "name_ja": "悪魔", "image": "15_devil.jpg", "symbol": "執着、快楽、依存、湿った欲望、見たくない本音、鎖に見えるもの"},
    {"number": 16, "name_en": "THE TOWER", "name_ja": "塔", "image": "16_tower.jpg", "symbol": "崩壊、衝撃、壊れるべき構造、突然の気づき、偽りの安全の破壊"},
    {"number": 17, "name_en": "THE STAR", "name_ja": "星", "image": "17_star.jpg", "symbol": "希望、癒し、透明さ、祈り、遠くにある光、無防備な信頼"},
    {"number": 18, "name_en": "THE MOON", "name_ja": "月", "image": "18_moon.jpg", "symbol": "不安、夢、幻想、無意識、曖昧さ、見えないものへの感受性"},
    {"number": 19, "name_en": "THE SUN", "name_ja": "太陽", "image": "19_sun.jpg", "symbol": "生命力、祝福、明るさ、無邪気さ、肯定、隠れない喜び"},
    {"number": 20, "name_en": "JUDGEMENT", "name_ja": "審判", "image": "20_judgement.jpg", "symbol": "呼び声、再生、目覚め、過去からの浮上、応答すること"},
    {"number": 21, "name_en": "THE WORLD", "name_ja": "世界", "image": "21_world.jpg", "symbol": "完成、統合、循環の終わりと始まり、全体性、ひとつの物語の成就"},
]

def get_api_key():
    if OPENAI_API_KEY.strip():
        return OPENAI_API_KEY.strip()
    try:
        if st.secrets.get("OPENAI_API_KEY"):
            return st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass
    return os.getenv("OPENAI_API_KEY", "").strip()

def generate_reflection(question, card, impression):
    api_key = get_api_key()
    if not api_key:
        return "APIキーが設定されていません。Streamlit Cloud の Secrets に OPENAI_API_KEY を登録してください。"

    client = OpenAI(api_key=api_key)
    prompt = f"""
あなたは、未来を断定する占い師ではありません。
タロットカードを使って、ユーザーの無意識や感情を丁寧に言語化する内省の案内人です。

【ユーザーの悩み・問い】
{question}

【引いたカード】
{card['number']}: {card['name_en']} / {card['name_ja']}

【カードの象徴】
{card['symbol']}

【ユーザーがカードを見て感じたこと】
{impression}

条件:
- 未来を断定しない
- 相手の気持ちや未来を決めつけない
- カードの意味を押しつけない
- ユーザーが画像を見て感じたことを最優先する
- やさしく、静かで、詩的すぎない文章
- 300〜500字程度
- 最後はユーザー自身に返す問いで終える
- 宗教的・霊感商法的な言い方は避ける
- 現実の選択や感情整理に戻れるようにする
"""
    try:
        response = client.responses.create(model="gpt-4.1-mini", input=prompt)
        return response.output_text
    except Exception as e:
        return f"AI生成中にエラーが出ました。\n\n{e}"

def reset_reading():
    st.session_state.step = 1
    st.session_state.question = ""
    st.session_state.selected_number = 0
    st.session_state.impression = ""
    st.session_state.reflection = ""

for key, value in {
    "step": 1,
    "question": "",
    "selected_number": 0,
    "impression": "",
    "reflection": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.markdown("""
<style>
.block-container { max-width: 780px; padding-top: 3rem; padding-bottom: 4rem; }
.stApp { background: #fbf7ef; color: #4f4638; }
h1, h2, h3 { color: #4f4638; letter-spacing: 0.04em; }
.intro-box { padding: 1.2rem 1.4rem; border: 1px solid rgba(160,130,80,.35); border-radius: 18px; background: rgba(255,252,244,.8); line-height: 1.9; margin-bottom: 1.5rem; }
.card-title { text-align: center; font-size: 1.5rem; letter-spacing: .14em; margin-top: 1rem; color: #8a6f3f; }
.card-subtitle { text-align: center; font-size: 1rem; margin-bottom: 1.5rem; color: #6d6355; }
.reflection-box { padding: 1.4rem 1.5rem; border-left: 4px solid #b89b5e; background: rgba(255,252,244,.9); border-radius: 12px; line-height: 2; white-space: pre-wrap; }
</style>
""", unsafe_allow_html=True)

st.title("Tarot Reflection")
st.markdown("""
<div class="intro-box">
これは未来を断定する占いではありません。<br>
タロットカードの象徴と、あなた自身が絵から受け取った印象を通して、<br>
まだ言葉になっていない感覚をそっと見つけるための場所です。
</div>
""", unsafe_allow_html=True)

if st.session_state.step == 1:
    st.subheader("1. 問いを置く")
    question = st.text_area("いま考えたい悩みや問いを書いてください。", value=st.session_state.question, height=140)
    selected_number = st.slider("0〜21の中から、いま気になる数字をひとつ選んでください。", 0, 21, st.session_state.selected_number)
    if st.button("カードをひらく", use_container_width=True):
        if not question.strip():
            st.warning("まず、悩みや問いを書いてください。")
        else:
            st.session_state.question = question.strip()
            st.session_state.selected_number = selected_number
            st.session_state.step = 2
            st.rerun()

elif st.session_state.step == 2:
    card = TAROT_CARDS[st.session_state.selected_number]
    image_path = CARDS_DIR / card["image"]
    st.subheader("2. カードを見る")
    st.markdown(f"<div class='card-title'>{card['name_en']}</div><div class='card-subtitle'>{card['number']} / {card['name_ja']}</div>", unsafe_allow_html=True)
    if image_path.exists():
        st.image(str(image_path), use_container_width=True)
    else:
        st.error(f"画像が見つかりません: cards/{card['image']}")
    st.markdown("### このカードを見て、何を感じましたか？")
    impression = st.text_area("正解っぽく書かなくて大丈夫です。目に入ったもの、色、人物への印象などを自由に書いてください。", value=st.session_state.impression, height=150)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("戻る", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("内省文を生成する", use_container_width=True):
            if not impression.strip():
                st.warning("カードを見て感じたことを書いてください。")
            else:
                st.session_state.impression = impression.strip()
                with st.spinner("言葉になりきらない感覚を、そっと拾っています..."):
                    st.session_state.reflection = generate_reflection(st.session_state.question, card, st.session_state.impression)
                st.session_state.step = 3
                st.rerun()

elif st.session_state.step == 3:
    card = TAROT_CARDS[st.session_state.selected_number]
    image_path = CARDS_DIR / card["image"]
    st.subheader("3. 内省のための言葉")
    st.markdown(f"<div class='card-title'>{card['name_en']}</div><div class='card-subtitle'>{card['number']} / {card['name_ja']}</div>", unsafe_allow_html=True)
    if image_path.exists():
        st.image(str(image_path), use_container_width=True)
    st.markdown("#### あなたの問い")
    st.write(st.session_state.question)
    st.markdown("#### カードを見て感じたこと")
    st.write(st.session_state.impression)
    st.markdown("#### 内省文")
    st.markdown(f"<div class='reflection-box'>{st.session_state.reflection}</div>", unsafe_allow_html=True)
    st.divider()
    if st.button("もう一度ひく", use_container_width=True):
        reset_reading()
        st.rerun()

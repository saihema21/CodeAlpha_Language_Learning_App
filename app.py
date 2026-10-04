import streamlit as st
import pandas as pd
import random

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="LinguaFlow | Language Learning",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# LANGUAGE DATA
# ---------------------------------------------------------
language_data = {
    "Spanish 🇪🇸": {
        "Vocabulary": [
            ("Hola", "Hello", "OH-la"),
            ("Gracias", "Thank you", "GRAH-see-as"),
            ("Amigo", "Friend", "ah-MEE-go"),
            ("Casa", "House", "KAH-sa"),
            ("Agua", "Water", "AH-gwa"),
            ("Comida", "Food", "ko-MEE-da"),
            ("Buenos días", "Good morning", "BWEH-nos DEE-as"),
            ("Adiós", "Goodbye", "ah-DYOS")
        ],
        "Grammar": [
            ("Yo soy", "I am", "yoh soy"),
            ("Tú eres", "You are", "too EH-res"),
            ("Él es", "He is", "el es"),
            ("Nosotros somos", "We are", "no-SOH-tros SO-mos")
        ]
    },

    "French 🇫🇷": {
        "Vocabulary": [
            ("Bonjour", "Hello", "bon-ZHOOR"),
            ("Merci", "Thank you", "mehr-SEE"),
            ("Ami", "Friend", "ah-MEE"),
            ("Maison", "House", "meh-ZON"),
            ("Eau", "Water", "OH"),
            ("Nourriture", "Food", "noo-ree-TOOR"),
            ("Au revoir", "Goodbye", "oh ruh-VWAHR"),
            ("Livre", "Book", "LEEV-ruh")
        ],
        "Grammar": [
            ("Je suis", "I am", "zhuh swee"),
            ("Tu es", "You are", "too eh"),
            ("Il est", "He is", "eel eh"),
            ("Nous sommes", "We are", "noo SOM")
        ]
    },

    "German 🇩🇪": {
        "Vocabulary": [
            ("Hallo", "Hello", "HAH-loh"),
            ("Danke", "Thank you", "DAHN-kuh"),
            ("Freund", "Friend", "froynt"),
            ("Haus", "House", "howss"),
            ("Wasser", "Water", "VAH-ser"),
            ("Essen", "Food", "ESS-en"),
            ("Guten Morgen", "Good morning", "GOO-ten MOR-gen"),
            ("Tschüss", "Goodbye", "chooss")
        ],
        "Grammar": [
            ("Ich bin", "I am", "ikh bin"),
            ("Du bist", "You are", "doo bist"),
            ("Er ist", "He is", "air ist"),
            ("Wir sind", "We are", "veer zint")
        ]
    },

    "Japanese 🇯🇵": {
        "Vocabulary": [
            ("こんにちは", "Hello", "Konnichiwa"),
            ("ありがとう", "Thank you", "Arigatou"),
            ("友達", "Friend", "Tomodachi"),
            ("家", "House", "Ie"),
            ("水", "Water", "Mizu"),
            ("食べ物", "Food", "Tabemono"),
            ("さようなら", "Goodbye", "Sayounara"),
            ("本", "Book", "Hon")
        ],
        "Grammar": [
            ("私は学生です", "I am a student", "Watashi wa gakusei desu"),
            ("これは本です", "This is a book", "Kore wa hon desu"),
            ("私は元気です", "I am fine", "Watashi wa genki desu"),
            ("彼は先生です", "He is a teacher", "Kare wa sensei desu")
        ]
    }
}

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "score" not in st.session_state:
    st.session_state.score = 0

if "learned" not in st.session_state:
    st.session_state.learned = 0

if "flashcard_index" not in st.session_state:
    st.session_state.flashcard_index = 0

if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

if "quiz_question" not in st.session_state:
    st.session_state.quiz_question = None

if "quiz_answer" not in st.session_state:
    st.session_state.quiz_answer = None

if "quiz_result" not in st.session_state:
    st.session_state.quiz_result = None

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:

    st.title("🌍 LinguaFlow")

    st.caption("Smart Language Learning")

    st.divider()

    st.subheader("🌐 Learning Language")

    selected_language = st.selectbox(
        "Choose a language",
        list(language_data.keys())
    )

    st.divider()

    st.subheader("📚 Learning Categories")

    category = st.radio(
        "Choose category",
        ["Vocabulary", "Grammar"]
    )

    st.divider()

    st.subheader("🎯 Daily Goal")

    daily_goal = st.slider(
        "Words / phrases",
        min_value=5,
        max_value=30,
        value=10
    )

    progress = min(
        st.session_state.learned / daily_goal,
        1.0
    )

    st.progress(progress)

    st.caption(
        f"{st.session_state.learned} / {daily_goal} completed"
    )

# ---------------------------------------------------------
# CURRENT DATA
# ---------------------------------------------------------
current_words = language_data[selected_language][category]

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.title("🌍 LinguaFlow")

st.subheader(
    f"Learn {selected_language} through vocabulary, grammar and practice."
)

st.write(
    "Build your language skills step by step with interactive "
    "flashcards and quizzes."
)

st.divider()

# ---------------------------------------------------------
# DASHBOARD METRICS
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📚 Words Available",
        len(current_words)
    )

with col2:
    st.metric(
        "✅ Learned",
        st.session_state.learned
    )

with col3:
    st.metric(
        "🏆 Quiz Score",
        st.session_state.score
    )

with col4:
    completion = int(progress * 100)

    st.metric(
        "📈 Progress",
        f"{completion}%"
    )

# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs(
    [
        "🃏 Flashcards",
        "🧠 Quiz",
        "📊 Progress"
    ]
)

# =========================================================
# FLASHCARDS
# =========================================================
with tab1:

    st.header("🃏 Interactive Flashcards")

    word, translation, pronunciation = current_words[
        st.session_state.flashcard_index
    ]

    st.info(
        f"Card {st.session_state.flashcard_index + 1} "
        f"of {len(current_words)}"
    )

    st.subheader(word)

    if st.session_state.show_answer:

        st.success(
            f"🇬🇧 Translation: {translation}"
        )

        st.write(
            f"🔊 Pronunciation: **{pronunciation}**"
        )

    else:

        st.write(
            "Think about the meaning before revealing the answer."
        )

    st.divider()

    button1, button2, button3 = st.columns(3)

    with button1:

        if st.button(
            "⬅️ Previous",
            use_container_width=True
        ):

            st.session_state.flashcard_index = (
                st.session_state.flashcard_index - 1
            ) % len(current_words)

            st.session_state.show_answer = False

            st.rerun()

    with button2:

        if st.button(
            "👁️ Show Answer",
            use_container_width=True
        ):

            st.session_state.show_answer = True

    with button3:

        if st.button(
            "Next ➡️",
            use_container_width=True
        ):

            st.session_state.flashcard_index = (
                st.session_state.flashcard_index + 1
            ) % len(current_words)

            st.session_state.show_answer = False

            st.rerun()

    st.divider()

    if st.button(
        "✅ Mark as Learned",
        use_container_width=True
    ):

        st.session_state.learned += 1

        st.success(
            "Great! This word has been added to your learning progress."
        )

# =========================================================
# QUIZ
# =========================================================
with tab2:

    st.header("🧠 Vocabulary Quiz")

    st.write(
        "Test your knowledge by selecting the correct translation."
    )

    if st.button(
        "🎲 Generate New Question",
        use_container_width=True
    ):

        question = random.choice(current_words)

        correct_answer = question[1]

        all_answers = [
            item[1] for item in current_words
        ]

        wrong_answers = [
            answer
            for answer in all_answers
            if answer != correct_answer
        ]

        options = random.sample(
            wrong_answers,
            min(2, len(wrong_answers))
        )

        options.append(correct_answer)

        random.shuffle(options)

        st.session_state.quiz_question = question
        st.session_state.quiz_answer = options
        st.session_state.quiz_result = None

    if st.session_state.quiz_question:

        question = st.session_state.quiz_question

        st.subheader(
            f"What does **{question[0]}** mean?"
        )

        selected_answer = st.radio(
            "Choose your answer:",
            st.session_state.quiz_answer
        )

        if st.button(
            "✅ Check Answer",
            use_container_width=True
        ):

            if selected_answer == question[1]:

                st.session_state.score += 1

                st.session_state.quiz_result = "correct"

                st.success(
                    "🎉 Correct! Excellent work!"
                )

            else:

                st.session_state.quiz_result = "wrong"

                st.error(
                    f"❌ Incorrect. Correct answer: {question[1]}"
                )

    else:

        st.info(
            "Click 'Generate New Question' to start your quiz."
        )

# =========================================================
# PROGRESS
# =========================================================
with tab3:

    st.header("📊 Learning Progress")

    progress_value = min(
        st.session_state.learned / daily_goal,
        1.0
    )

    st.subheader("🎯 Daily Learning Goal")

    st.progress(progress_value)

    st.write(
        f"You have completed **{st.session_state.learned}** "
        f"out of **{daily_goal}** learning items."
    )

    st.divider()

    progress_data = pd.DataFrame({
        "Metric": [
            "Learning Items",
            "Quiz Score"
        ],
        "Value": [
            st.session_state.learned,
            st.session_state.score
        ]
    })

    st.bar_chart(
        progress_data.set_index("Metric")
    )

    if progress_value >= 1:

        st.success(
            "🏆 Daily goal completed! Amazing work!"
        )

    elif progress_value >= 0.5:

        st.info(
            "🔥 You're more than halfway through today's goal!"
        )

    else:

        st.warning(
            "Keep learning! Complete a few more flashcards today."
        )

# ---------------------------------------------------------
# LEARNING TIPS
# ---------------------------------------------------------
st.divider()

st.header("💡 Learning Tips")

tip1, tip2, tip3 = st.columns(3)

with tip1:
    st.info(
        "📖 **Learn Daily**\n\n"
        "Practice a small number of new words every day."
    )

with tip2:
    st.info(
        "🔁 **Review Often**\n\n"
        "Use flashcards repeatedly to strengthen memory."
    )

with tip3:
    st.info(
        "🧠 **Test Yourself**\n\n"
        "Use quizzes to check how much you remember."
    )

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.divider()

st.caption(
    "LinguaFlow • Language Learning App • "
    "Built with Python, Streamlit & Pandas • "
    "CodeAlpha App Development Internship"
)
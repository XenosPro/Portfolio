import streamlit as st

from game import get_questions, check_answer
from scoring import calculate_xp


# -------------------------
# INITIALIZE GAME
# -------------------------

if "questions" not in st.session_state:
    st.session_state.questions = get_questions(
        topic="machine learning",
        difficulty="easy",
        number=5
    )

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# -------------------------
# CURRENT QUESTION
# -------------------------

questions = st.session_state.questions
index = st.session_state.question_index

if index >= len(questions):

    st.title("Level Complete")

    st.metric("XP", st.session_state.score)
    st.metric("Best Streak", st.session_state.streak)

    if st.button("Play Again"):
        st.session_state.questions = get_questions()
        st.session_state.question_index = 0
        st.session_state.score = 0
        st.session_state.streak = 0
        st.session_state.answered = False
        st.session_state.last_result = None
        st.rerun()

    st.stop()


question = questions[index]


# -------------------------
# HEADER
# -------------------------

st.title("AI Trainer")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("XP", st.session_state.score)

with col2:
    st.metric("Streak", st.session_state.streak)

with col3:
    st.metric(
        "Question",
        f"{index + 1}/{len(questions)}"
    )


st.divider()


# -------------------------
# QUESTION
# -------------------------

st.subheader(question["question"])

selected = st.radio(
    "Choose your answer:",
    question["options"],
    index=None
)


# -------------------------
# SUBMIT
# -------------------------

if not st.session_state.answered:

    if st.button("Submit Answer"):

        if selected is None:
            st.warning("Choose an answer first.")

        else:

            correct = check_answer(
                question,
                selected
            )

            if correct:

                st.session_state.streak += 1

                xp = calculate_xp(
                    True,
                    question["difficulty"]
                )

                st.session_state.score += xp

                st.session_state.last_result = (
                    True,
                    xp
                )

            else:

                st.session_state.streak = 0

                st.session_state.last_result = (
                    False,
                    0
                )

            st.session_state.answered = True
            st.rerun()


# -------------------------
# FEEDBACK
# -------------------------

if st.session_state.answered:

    correct, xp = st.session_state.last_result

    if correct:

        st.success(f"Correct! +{xp} XP")

    else:

        st.error("Incorrect.")

        correct_answer = question["answer"]

        st.write(
            f"Correct answer: **{correct_answer}**"
        )

    st.info(question["explanation"])

    if st.button("Next Question"):

        st.session_state.question_index += 1
        st.session_state.answered = False
        st.session_state.last_result = None
        st.rerun()
        
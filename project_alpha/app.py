import streamlit as st

from game import get_question, check_answer
from scoring import calculate_xp


# -------------------------
# INITIALIZE GAME
# -------------------------

if "current_question" not in st.session_state:
    st.session_state.current_question = get_question()

if "previous_questions" not in st.session_state:
    st.session_state.previous_questions = []

if "score" not in st.session_state:
    st.session_state.score = 0

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "question_number" not in st.session_state:
    st.session_state.question_number = 1

if "answered" not in st.session_state:
    st.session_state.answered = False

if "last_result" not in st.session_state:
    st.session_state.last_result = None


question = st.session_state.current_question


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
        st.session_state.question_number
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

        st.write(
            f"Correct answer: **{question['answer']}**"
        )

    st.info(question["explanation"])

    # -------------------------
    # NEXT QUESTION
    # -------------------------

    if st.button("Next Question"):

        st.session_state.previous_questions.append(
            question["question"]
        )

        st.session_state.current_question = get_question(
            topic=question["topic"],
            difficulty=question["difficulty"],
            previous_questions=st.session_state.previous_questions
        )

        st.session_state.question_number += 1
        st.session_state.answered = False
        st.session_state.last_result = None

        st.rerun()
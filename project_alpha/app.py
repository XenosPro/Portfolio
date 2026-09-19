import streamlit as st

from game import get_question, check_answer
from scoring import calculate_xp


MAX_QUESTIONS = 10


# -------------------------
# INITIALIZE GAME
# -------------------------

if "current_question" not in st.session_state:
    st.session_state.current_question = get_question(
        previous_questions=[]
    )

if "previous_questions" not in st.session_state:
    st.session_state.previous_questions = []

if "score" not in st.session_state:
    st.session_state.score = 0

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "best_streak" not in st.session_state:
    st.session_state.best_streak = 0

if "question_number" not in st.session_state:
    st.session_state.question_number = 1

if "correct_answers" not in st.session_state:
    st.session_state.correct_answers = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "game_finished" not in st.session_state:
    st.session_state.game_finished = False


# -------------------------
# END OF GAME
# -------------------------

if st.session_state.game_finished:

    st.title("Quiz Complete")

    st.divider()

    st.metric(
        "XP",
        st.session_state.score
    )

    st.metric(
        "Correct Answers",
        f"{st.session_state.correct_answers}/{MAX_QUESTIONS}"
    )

    st.metric(
        "Best Streak",
        st.session_state.best_streak
    )

    accuracy = (
        st.session_state.correct_answers / MAX_QUESTIONS
    ) * 100

    st.metric(
        "Accuracy",
        f"{accuracy:.0f}%"
    )

    st.divider()

    if st.button("Play Again"):

        # Generate a new question while keeping
        # the questions from previous games.
        st.session_state.current_question = get_question(
            topic="machine learning",
            difficulty="easy",
            previous_questions=(
                st.session_state.previous_questions
            )
        )

        # IMPORTANT:
        # Do NOT clear previous_questions here.
        #
        # This allows the AI to see questions
        # from previous games and avoid repeating them.

        st.session_state.score = 0
        st.session_state.streak = 0
        st.session_state.best_streak = 0

        st.session_state.question_number = 1
        st.session_state.correct_answers = 0

        st.session_state.answered = False
        st.session_state.last_result = None
        st.session_state.game_finished = False

        st.rerun()

    st.stop()


# -------------------------
# CURRENT QUESTION
# -------------------------

question = st.session_state.current_question


# -------------------------
# HEADER
# -------------------------

st.title("AI Trainer")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "XP",
        st.session_state.score
    )

with col2:
    st.metric(
        "Streak",
        st.session_state.streak
    )

with col3:
    st.metric(
        "Question",
        f"{st.session_state.question_number}/{MAX_QUESTIONS}"
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
# SUBMIT ANSWER
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

                st.session_state.correct_answers += 1

                if (
                    st.session_state.streak
                    > st.session_state.best_streak
                ):
                    st.session_state.best_streak = (
                        st.session_state.streak
                    )

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

        st.success(
            f"Correct! +{xp} XP"
        )

    else:

        st.error("Incorrect.")

        st.write(
            f"Correct answer: **{question['answer']}**"
        )

    st.info(
        question["explanation"]
    )


    # -------------------------
    # NEXT QUESTION
    # -------------------------

    if st.session_state.question_number < MAX_QUESTIONS:

        if st.button("Next Question"):

            # Save the current question to history
            # BEFORE generating the next one.
            if question["question"] not in st.session_state.previous_questions:

                st.session_state.previous_questions.append(
                    question["question"]
                )

            st.session_state.current_question = get_question(
                topic=question["topic"],
                difficulty=question["difficulty"],
                previous_questions=(
                    st.session_state.previous_questions
                )
            )

            st.session_state.question_number += 1

            st.session_state.answered = False

            st.session_state.last_result = None

            st.rerun()

    else:

        if st.button("Finish Quiz"):

            # Save the final question to history.
            if question["question"] not in st.session_state.previous_questions:

                st.session_state.previous_questions.append(
                    question["question"]
                )

            st.session_state.game_finished = True

            st.rerun()
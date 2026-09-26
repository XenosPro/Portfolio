# Project Alpha — AI Quiz Engine

A Streamlit learning app that generates machine-learning quiz questions with the Gemini API.

## Features

- Generates one multiple-choice question at a time with Gemini.
- Uses Pydantic structured outputs to validate question format.
- Tracks XP, streaks, accuracy and quiz progress.
- Runs 10-question quiz sessions.
- Keeps question history during the session to reduce repetition.
- Retries transient API failures.

## Tech

Python · Streamlit · Google Gemini API · Pydantic

## Run locally

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set your Gemini API key:

   ```bash
   set GEMINI_API_KEY=your_key_here
   ```

3. Start the app:

   ```bash
   streamlit run app.py
   ```

## Live demo

https://portfolio-jtfvvzbahmudyad4e7binz.streamlit.app/

> Educational project for practicing machine-learning concepts through active recall.

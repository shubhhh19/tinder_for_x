# Tinder for X

A relevance-training loop for your X timeline. Swipe right to like, left to discard.

## Prerequisites

- Docker & Docker Compose
- Node.js 18+
- X (Twitter) API Credentials
- OpenAI API Key

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/shubhhh19/tinder_for_x.git
   cd tinder_for_x
   ```

2. **Environment Variables**
   Copy `.env.example` to `.env` and fill in your keys.
   ```bash
   cp .env.example .env
   ```

   ### Getting API Keys
   
   **1. Hugging Face API Key (Free Embeddings)**
   - Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
   - Create a new Access Token (Read permissions are fine).
   - Add it as `HUGGINGFACE_API_KEY` in your `.env` file.

   **2. X (Twitter) API Credentials (for Ingestion)**
   - Go to the [X Developer Portal](https://developer.twitter.com/en/portal/dashboard).
   - Sign up for a Basic (or Pro) account.
   - Create a new Project & App.
   - Under "Keys and tokens", generate:
     - **API Key & Secret** (Consumer Keys)
     - **Bearer Token** (Authentication Token)
   - Add them to your `.env` file.


3. **Start Backend & Database**
   ```bash
   docker-compose up --build
   ```
   The API will be available at `http://localhost:8000`.

4. **Start Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Open `http://localhost:3000` in your browser.

## Features

- **Ingestion**: Fetches tweets from X based on keywords.
- **Embedding**: Generates vector embeddings for tweets using OpenAI.
- **Swipe UI**: Tinder-like interface to rate tweets.
- **Ranking**: (Coming Soon) Personalized feed based on your swipe history.

## Tech Stack

- **Frontend**: Next.js, TailwindCSS, Framer Motion
- **Backend**: FastAPI, SQLModel, pgvector
- **Database**: PostgreSQL with pgvector extension

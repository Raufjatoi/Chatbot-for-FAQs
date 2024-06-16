# Chatbot for FAQs

Welcome to the Chatbot for FAQs, a Streamlit-based application designed to answer common questions related to mental health and more. This chatbot not only provides responses from a predefined knowledge base but also integrates external APIs to fetch additional information and entertain users with jokes and memes.

## Features

- **FAQ Responses**: Provides answers to common questions related to mental health and general queries.
- **Conversation History**: Saves user interactions in a conversation history file (`conversation_history.txt`).
- **External APIs Integration**:
  - **Wikipedia API**: Fetches detailed explanations from Wikipedia for broader topics.
  - **Stack Overflow API**: Retrieves relevant answers from Stack Overflow for programming-related questions.
- **Additional Features**:
  - **Random Joke**: Fetches a random joke from an external API for entertainment.
  - **Generate a Random Meme**: Retrieves a random meme template from an external API and displays it.
  - **Translation Model**: Placeholder button to explore translation capabilities using a specified API link.

## Setup

### Prerequisites

Before running the application, ensure you have Python installed on your system. You can download Python from [python.org](https://www.python.org/downloads/).

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository

2. **Install dependencies :**
    ```bash
    pip install -r requirements.txt
   
3. **Start the application: :**
    ```bash
    streamlit run app.py

    
# Rule-Based Chatbot

## 1. Project Overview
This project is a simple, lightweight Python chatbot that operates entirely using predefined rules, keywords, and pattern matching logic. Developed as Task 1 of an internship, it simulates an interactive conversational agent in the terminal without relying on external machine learning models, cloud APIs, or third-party libraries.

## 2. Internship Task
The project fulfills the following core internship requirements:
- Respond to user inputs using predefined rules and keywords.
- Handle common greetings effectively.
- Handle common user questions and FAQs.
- Provide friendly fallback responses when inputs are not recognized.
- Use core Python `if`-`elif`-`else` conditional branches or pattern matching.
- Include thorough code comments explaining decision-making logic and rule matching.

## 3. Objectives
The key learning objectives achieved through this project include:
- **Python Conditional Logic**: Implementing robust multi-condition decision trees with `if`, `elif`, and `else`.
- **String Handling & Normalization**: Stripping punctuation, trimming whitespace, and converting case for uniform matching.
- **Functions & Modularity**: Organizing the application into modular, single-responsibility functions.
- **Loops & Control Flow**: Driving an interactive conversational loop with graceful break and exception handling.
- **Keyword & Pattern Matching**: Leveraging exact matches and regular expressions (`re`) for intent recognition.
- **Basic Conversation Flow & State Management**: Maintaining temporary in-memory session state for user names and conversation logs.

## 4. Features
The chatbot includes the following core functionalities:
- **Rule-Based Keyword Matching**: Maps user queries to predefined responses using standard Python logic.
- **Greetings**: Recognizes greetings such as `hello`, `hi`, `hey`, `good morning`, `good afternoon`, and `good evening`.
- **Multiple Predefined Responses**: Uses randomized pools of responses to make interactions feel natural and varied.
- **Chatbot Identity**: Answers queries about who it is (`what is your name`, `who are you`).
- **How Are You Responses**: Responds to user inquiries about its operational status (`how are you`, `how are you doing`).
- **User Name Memory**: Recognizes patterns like `my name is [Name]` or `I am [Name]`, saves the name in runtime memory, and recalls it when asked (`what is my name`, `do you know my name`).
- **Current Date**: Queries and formats the current system date using Python's `datetime` module.
- **Current Time**: Queries and formats the current local time using Python's `datetime` module.
- **Predefined Jokes**: Delivers clean, programmer-friendly jokes chosen randomly from an internal collection.
- **Help Menu & Capabilities**: Provides a formatted reference list of all available commands upon receiving `help`, `capabilities`, or `what can you do`.
- **Conversation History**: Records user queries and bot replies in memory during the active session and displays them upon typing `history`.
- **Clear History**: Resets and clears the session conversation log when typing `clear history`.
- **Fallback Responses**: Gracefully provides friendly fallback guidance whenever an input cannot be mapped to any predefined rule.
- **Exit Command**: Closes the conversational session cleanly when typing `bye`, `goodbye`, `exit`, or `quit`.

## 5. Technologies Used
- **Python 3**: Core programming language.
- **Python Standard Library**:
  - `datetime`: For system date and timestamp retrieval.
  - `random`: For non-deterministic selection among predefined responses.
  - `re`: For regular expression string normalization and name extraction.
  - `sys`: For clean script termination and handling session interruption.

> **Note**: This project strictly adheres to a rule-based architecture. It does **not** use AI, machine learning algorithms, Natural Language Processing (NLP) libraries, external APIs, databases, or an active internet connection.

## 6. How It Works
The chatbot follows a deterministic pipeline to process every incoming line of user text:

```text
User Input
    ↓
Input Normalization (lowercase, strip trailing punctuation, remove extra spaces)
    ↓
Keyword / Pattern Matching (evaluate conditions via if-elif-else & regex)
    ↓
Predefined Rule Execution (fetch matching answer, extract name, or read date/time)
    ↓
Chatbot Response Output
```

### Fallback Mechanism
If the normalized text fails to match any exit commands, history actions, name patterns, date/time lookups, greetings, or predefined questions, control falls through to an `else` fallback handler. The chatbot then randomly picks a helpful response reminding the user of the `help` command so they can continue navigating the supported features.

## 7. Project Structure
```text
Rule-based Chatbot/
├── app.py
├── chatbot.py
├── README.md
├── requirements.txt
└── screenshots/
    └── .gitkeep
```

- **`app.py`**: Modern interactive web interface built with Streamlit.
- **`chatbot.py`**: The complete source code containing the rule engine, response datasets, and terminal loop.
- **`README.md`**: Project documentation, usage guidelines, and architecture breakdown.
- **`requirements.txt`**: Dependency manifest documenting standard library and Streamlit usage.
- **`screenshots/`**: Directory designated for terminal and web execution screenshots.

## 8. Installation & Running

### Prerequisites
Ensure Python (version 3.8 or newer) is installed on your Windows system.

Check your Python installation:
```bash
python --version
```

### Running the Chatbot (Terminal Interface)
Navigate to the project directory and run `chatbot.py`:
```bash
cd "Rule-based Chatbot"
python chatbot.py
```

### Running the Web Application (Streamlit)
To launch the interactive modern browser-based interface:
```bash
cd "Rule-based Chatbot"
streamlit run app.py
```

### Optional: Virtual Environment
Because this project utilizes only the Python Standard Library, a virtual environment is not strictly necessary. However, if you prefer to isolate your environments as a standard practice:
```bash
# 1. Create a virtual environment (outside the project directory or in your global envs folder)
python -m venv venv

# 2. Activate the virtual environment on Windows
.\venv\Scripts\activate

# 3. Run the chatbot
python chatbot.py
```
*(Do not commit or create virtual environment folders inside the project repository.)*

## 9. Example Conversation
Here is an actual interactive terminal session demonstrated by the chatbot:

```text
=================================================================
           WELCOME TO THE RULE-BASED PYTHON CHATBOT           
                     Internship Task 1                        
=================================================================
Description : A simple chatbot built using keyword & pattern rules.
Instruction : Type your message and press Enter.
Commands    : Type 'help' to view all capabilities.
Exit        : Type 'bye', 'goodbye', 'exit', or 'quit' to end.
=================================================================

You: Hello
Bot: Hi there! Great to see you. What's on your mind?

You: What is your name?
Bot: I am a Python Rule-Based Chatbot created for Task 1 of the internship.

You: My name is Kaushik
Bot: Nice to meet you, Kaushik! I will remember your name for this session.

You: What is my name?
Bot: Your name is Kaushik! I remember it from our conversation.

You: Tell me a joke
Bot: Why do programmers prefer dark mode? Because light attracts bugs!

You: What is today's date?
Bot: Today's date is Wednesday, September 30, 2026.

You: What time is it?
Bot: The current system time is 02:20:26 PM.

You: What is quantum computing?
Bot: Hmm, that doesn't match any of my known rules. Type 'help' for a list of topics I understand.

You: Bye
Bot: Goodbye, Kaushik! Have a wonderful day ahead. Exiting session...
```

## 10. Future Improvements
While the current submission satisfies all Task 1 requirements with standard rule-based Python logic, potential future enhancements could include:
- **Graphical User Interface (GUI)**: Implementing a clean desktop UI using `tkinter` or `PyQt`.
- **Expanded Rule Base**: Expanding the keyword dictionary to cover broader topic domains, FAQs, and mathematical calculations.
- **Voice Input / Output**: Integrating offline speech recognition and text-to-speech modules.
- **Persistent Conversation Storage**: Storing conversation histories and user preferences in a local SQLite database or JSON file across sessions.

*(Note: These are potential areas for future iteration and are not implemented in the current rule-based submission.)*

## 11. Conclusion
The Rule-Based Chatbot successfully fulfills all objectives set out for Task 1 of the internship. By utilizing structured conditional logic, input sanitization, regular expressions, and modular function architecture, the project proves that effective, interactive terminal chatbots can be constructed cleanly using purely native Python tools.

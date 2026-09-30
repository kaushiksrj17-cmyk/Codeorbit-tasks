"""
Task 1: Rule-Based Chatbot
==========================
Internship Project: Rule-Based Chatbot in Python

Core Features:
- Rule-based keyword and pattern matching using if-elif-else statements
- Standard greetings handling with randomized responses
- Chatbot identity and status queries
- Capabilities overview and comprehensive help menu
- In-memory session user name storage
- System date and time reporting using Python datetime
- Curated clean jokes selection
- Politeness and appreciation handling
- In-memory conversation history tracking and clearing
- Friendly fallback handling for unrecognized user inputs
- Graceful session exit handling
- Built purely with the Python Standard Library (no external APIs or ML)
"""

import datetime
import random
import re
import sys


# ============================================================================
# PREDEFINED RESPONSE DATA & KNOWLEDGE BASE
# ============================================================================

GREETING_RESPONSES = [
    "Hello! How can I help you today?",
    "Hi there! Great to see you. What's on your mind?",
    "Hey! How can I assist you today?",
    "Greetings! Hope you are having a wonderful day. How can I help?",
    "Hello! I am ready to assist you. Ask me anything from my capabilities list!"
]

STATUS_RESPONSES = [
    "I'm functioning perfectly! Thank you for asking. How are you doing?",
    "All systems are running smoothly! Ready to assist you.",
    "I'm doing great! Ready to chat and answer your questions.",
    "Doing wonderful, thank you! How can I assist you today?"
]

IDENTITY_RESPONSES = [
    "I am a Python Rule-Based Chatbot created for Task 1 of the internship.",
    "I'm a virtual rule-based assistant built purely using Python's standard library!",
    "I am your friendly Rule-Based Chatbot. I match keywords and rules to chat with you."
]

THANK_YOU_RESPONSES = [
    "You're very welcome! Let me know if you need anything else.",
    "Happy to help! Feel free to ask more questions.",
    "Anytime! I'm here to assist you.",
    "Glad I could be of help! Have a great time."
]

FALLBACK_RESPONSES = [
    "I'm sorry, I didn't quite understand that. Type 'help' to see what I can do!",
    "I'm not sure how to respond to that yet. Try asking for 'date', 'time', or a 'joke'!",
    "Hmm, that doesn't match any of my known rules. Type 'help' for a list of topics I understand.",
    "I didn't catch that. Feel free to ask about my capabilities by typing 'help'."
]

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why did the Python developer need glasses? Because they couldn't C#!",
    "There are only 10 types of people in the world: those who understand binary, and those who don't.",
    "Why was the computer cold? It left its Windows open!",
    "What do you call a fake noodle? An impasta!",
    "Why do programmers hate nature? It has too many bugs and no debugging tool.",
    "How do you comfort a JavaScript bug? You console it!"
]


# ============================================================================
# HELPER & DISPLAY FUNCTIONS
# ============================================================================

def print_banner():
    """
    Display a welcoming and professional header in the terminal with clean
    separators, description, instructions, and exit commands.
    """
    border = "=" * 65
    print(border)
    print("           WELCOME TO THE RULE-BASED PYTHON CHATBOT           ")
    print("                     Internship Task 1                        ")
    print(border)
    print("Description : A simple chatbot built using keyword & pattern rules.")
    print("Instruction : Type your message and press Enter.")
    print("Commands    : Type 'help' to view all capabilities.")
    print("Exit        : Type 'bye', 'goodbye', 'exit', or 'quit' to end.")
    print(border)
    print()


def get_help_menu() -> str:
    """Return a formatted string detailing all supported features and commands."""
    menu = [
        "-----------------------------------------------------------------",
        "                      CHATBOT HELP & CAPABILITIES                ",
        "-----------------------------------------------------------------",
        " 1. Greetings     : Say 'hello', 'hi', 'hey', 'good morning', etc.",
        " 2. Identity      : Ask 'who are you', 'what is your name'",
        " 3. Status        : Ask 'how are you', 'how are you doing'",
        " 4. Name Memory   : Say 'my name is [Name]' or 'I am [Name]'",
        "                    Ask 'what is my name' or 'do you know my name'",
        " 5. Date & Time   : Ask 'date', 'today's date', 'time', 'what time is it'",
        " 6. Jokes         : Ask 'joke', 'tell me a joke', 'make me laugh'",
        " 7. Politeness    : Say 'thank you', 'thanks'",
        " 8. History       : Type 'history' to view conversation history",
        "                    Type 'clear history' to reset history",
        " 9. Capabilities  : Type 'help', 'capabilities', or 'what can you do'",
        "10. Exit          : Type 'bye', 'goodbye', 'exit', or 'quit'",
        "-----------------------------------------------------------------"
    ]
    return "\n".join(menu)


def normalize_input(user_input: str) -> str:
    """
    Input Normalization:
    - Trims leading and trailing whitespaces.
    - Converts text to lowercase for uniform, case-insensitive keyword matching.
    - Normalizes smart/curly quotes to standard straight quotes.
    - Condenses multiple consecutive spaces into a single space.
    """
    text = user_input.strip().lower()
    text = text.replace("’", "'").replace("‘", "'")
    text = re.sub(r"\s+", " ", text)
    return text


def clean_punctuation(text: str) -> str:
    """
    Strip common trailing punctuation marks from user input so questions
    like 'What time is it?' match clean rule patterns like 'what time is it'.
    """
    return text.rstrip("?!.,;:")


# ============================================================================
# CORE RULE-MATCHING ENGINE
# ============================================================================

def process_message(raw_input: str, session: dict) -> tuple[str, bool]:
    """
    Evaluate user input against predefined rules and patterns.

    Parameters:
        raw_input (str): The raw text entered by the user.
        session (dict): In-memory dictionary holding 'user_name' and 'history'.

    Returns:
        tuple[str, bool]: (chatbot_response, should_exit)
    """
    # ------------------------------------------------------------------------
    # STEP 1: INPUT NORMALIZATION
    # Convert input to lowercase and strip extraneous whitespace & punctuation
    # ------------------------------------------------------------------------
    normalized = normalize_input(raw_input)
    cleaned = clean_punctuation(normalized)

    # Handle empty input
    if not cleaned:
        return "Please type something so I can respond! Type 'help' if you need guidance.", False

    # ------------------------------------------------------------------------
    # STEP 2: EXIT HANDLING
    # Detects session termination keywords: 'bye', 'goodbye', 'exit', 'quit'
    # ------------------------------------------------------------------------
    if cleaned in ["bye", "goodbye", "exit", "quit", "close"]:
        name_part = f", {session['user_name']}" if session.get("user_name") else ""
        farewell = f"Goodbye{name_part}! Have a wonderful day ahead. Exiting session..."
        return farewell, True

    # ------------------------------------------------------------------------
    # STEP 3: CONVERSATION HISTORY (CLEARING)
    # Allows user to reset their session conversation history
    # Checked before 'history' to avoid substring conflict
    # ------------------------------------------------------------------------
    elif cleaned in ["clear history", "reset history", "delete history", "clear chat"]:
        session["history"].clear()
        return "Your conversation history has been cleared for this session.", False

    # ------------------------------------------------------------------------
    # STEP 4: CONVERSATION HISTORY (VIEWING)
    # Displays all previous exchanges stored in memory for the active session
    # ------------------------------------------------------------------------
    elif cleaned in ["history", "show history", "view history"]:
        if not session["history"]:
            return "There is no conversation history in this session yet.", False

        lines = [
            "----------------------- CONVERSATION HISTORY -----------------------"
        ]
        for index, item in enumerate(session["history"], start=1):
            lines.append(f"[{index}] User: {item['user']}")
            lines.append(f"    Bot : {item['bot']}")
        lines.append("--------------------------------------------------------------------")
        return "\n".join(lines), False

    # ------------------------------------------------------------------------
    # STEP 5: CAPABILITIES & HELP MENU
    # Recognizes: 'what can you do', 'capabilities', 'help'
    # ------------------------------------------------------------------------
    elif cleaned in ["help", "capabilities", "what can you do", "commands", "menu"]:
        return get_help_menu(), False

    # ------------------------------------------------------------------------
    # STEP 6: USER NAME MEMORY (RETRIEVAL)
    # Checks if the user's name is stored in current session memory
    # Recognizes: 'what is my name', "what's my name", 'do you know my name'
    # ------------------------------------------------------------------------
    elif any(phrase in cleaned for phrase in [
        "what is my name",
        "what's my name",
        "whats my name",
        "do you know my name",
        "tell me my name",
        "who am i"
    ]):
        if session.get("user_name"):
            return f"Your name is {session['user_name']}! I remember it from our conversation.", False
        else:
            return "You haven't told me your name yet! You can tell me by saying 'My name is [your name]'.", False

    # ------------------------------------------------------------------------
    # STEP 7: USER NAME MEMORY (LEARNING / EXTRACTION)
    # Extracts the user's name using regex pattern matching
    # Recognizes: 'my name is Kaushik', 'I am Kaushik', "I'm Kaushik"
    # Note: Stored strictly in memory during runtime; never saved permanently.
    # ------------------------------------------------------------------------
    elif any(cleaned.startswith(prefix) for prefix in ["my name is ", "i am ", "i'm ", "im "]):
        match = re.search(r"^(?:my name is|i am|i'm|im)\s+([a-zA-Z\s'-]+)", cleaned)
        if match:
            extracted_name = match.group(1).strip()
            # Guard: Avoid misinterpreting emotional or status phrases as names
            status_adjectives = [
                "good", "fine", "well", "great", "ok", "okay", "happy",
                "sad", "tired", "bored", "busy", "here", "doing well"
            ]
            if extracted_name in status_adjectives:
                return "Glad to know that! How can I assist you today?", False

            # Format name nicely with title casing and store in session state
            formatted_name = extracted_name.title()
            session["user_name"] = formatted_name
            return f"Nice to meet you, {formatted_name}! I will remember your name for this session.", False
        else:
            return "I couldn't quite extract your name. Please try: 'My name is [Your Name]'.", False

    # ------------------------------------------------------------------------
    # STEP 8: CHATBOT IDENTITY
    # Recognizes: 'what is your name', "what's your name", 'who are you'
    # ------------------------------------------------------------------------
    elif any(phrase in cleaned for phrase in [
        "what is your name",
        "what's your name",
        "whats your name",
        "who are you",
        "your name"
    ]):
        return random.choice(IDENTITY_RESPONSES), False

    # ------------------------------------------------------------------------
    # STEP 9: HOW ARE YOU / STATUS
    # Recognizes: 'how are you', 'how are you doing'
    # ------------------------------------------------------------------------
    elif any(phrase in cleaned for phrase in [
        "how are you",
        "how are you doing",
        "how's it going",
        "how are things"
    ]):
        return random.choice(STATUS_RESPONSES), False

    # ------------------------------------------------------------------------
    # STEP 10: GREETINGS (KEYWORD MATCHING)
    # Recognizes: 'hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'
    # Uses randomized greeting responses.
    # ------------------------------------------------------------------------
    elif any(
        cleaned == greeting
        or cleaned.startswith(greeting + " ")
        or re.search(rf"\b{re.escape(greeting)}\b", cleaned)
        for greeting in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
    ):
        base_greeting = random.choice(GREETING_RESPONSES)
        # If user's name is known, personalize the greeting
        if session.get("user_name"):
            return f"{base_greeting[:-1]}, {session['user_name']}!", False
        return base_greeting, False

    # ------------------------------------------------------------------------
    # STEP 11: CURRENT DATE
    # Recognizes: "what is today's date", "what's today's date", "today's date", "date"
    # Fetches real-time system date via Python datetime module
    # ------------------------------------------------------------------------
    elif any(phrase in cleaned for phrase in [
        "what is today's date",
        "what's today's date",
        "whats today's date",
        "today's date",
        "todays date",
        "today date",
        "current date",
        "what date is it",
        "date"
    ]) or cleaned == "date":
        today_str = datetime.date.today().strftime("%A, %B %d, %Y")
        return f"Today's date is {today_str}.", False

    # ------------------------------------------------------------------------
    # STEP 12: CURRENT TIME
    # Recognizes: 'what time is it', "what's the time", 'current time', 'time'
    # Fetches real-time system time via Python datetime module
    # ------------------------------------------------------------------------
    elif any(phrase in cleaned for phrase in [
        "what time is it",
        "what's the time",
        "whats the time",
        "current time",
        "the time",
        "what is the time"
    ]) or cleaned == "time":
        current_time_str = datetime.datetime.now().strftime("%I:%M:%S %p")
        return f"The current system time is {current_time_str}.", False

    # ------------------------------------------------------------------------
    # STEP 13: JOKES
    # Recognizes: 'tell me a joke', 'tell me a funny joke', 'joke', 'make me laugh'
    # Selects a clean joke randomly from predefined list
    # ------------------------------------------------------------------------
    elif any(phrase in cleaned for phrase in [
        "tell me a joke",
        "tell me a funny joke",
        "joke",
        "make me laugh",
        "tell a joke",
        "say a joke"
    ]):
        return random.choice(JOKES), False

    # ------------------------------------------------------------------------
    # STEP 14: THANK YOU / POLITENESS
    # Recognizes: 'thank you', 'thanks', 'thank'
    # ------------------------------------------------------------------------
    elif any(phrase in cleaned for phrase in [
        "thank you",
        "thanks",
        "thank u",
        "thank you so much",
        "thanks a lot"
    ]) or cleaned == "thank":
        return random.choice(THANK_YOU_RESPONSES), False

    # ------------------------------------------------------------------------
    # STEP 15: FALLBACK HANDLING (UNKNOWN INPUT)
    # When no rule or pattern matches, return a friendly random fallback
    # ------------------------------------------------------------------------
    else:
        return random.choice(FALLBACK_RESPONSES), False


# ============================================================================
# MAIN APPLICATION LOOP
# ============================================================================

def main():
    """
    Main loop driver:
    - Maintains in-memory session variables (user_name, conversation history).
    - Presents the professional terminal interface.
    - Loops continuously accepting user input until an exit condition triggers.
    """
    # In-memory session state (resets upon exit/restart, no permanent storage)
    session_state = {
        "user_name": None,
        "history": []  # Stores list of dicts: [{"user": ..., "bot": ...}]
    }

    # Print startup banner and terminal interface
    print_banner()

    # Continuous conversational loop
    while True:
        try:
            # Capture user input from the terminal
            user_input = input("You: ")
        except (KeyboardInterrupt, EOFError):
            print("\n\nSession interrupted. Goodbye!")
            sys.exit(0)

        # Evaluate user input against the rule engine
        response, should_exit = process_message(user_input, session_state)

        # Output the response to the user
        print(f"Bot: {response}\n")

        # Record conversation exchange in history (excluding exit and history commands)
        cleaned_cmd = clean_punctuation(normalize_input(user_input))
        meta_commands = [
            "history", "show history", "view history",
            "clear history", "reset history", "delete history", "clear chat"
        ]
        if not should_exit and user_input.strip() and cleaned_cmd not in meta_commands:
            session_state["history"].append({
                "user": user_input.strip(),
                "bot": response
            })

        # Break loop when exit command is received
        if should_exit:
            break


if __name__ == "__main__":
    main()

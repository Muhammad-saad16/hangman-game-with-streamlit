import streamlit as st
import random
import time
from typing import List, Dict, Tuple

# Configure Streamlit page
st.set_page_config(
    page_title="Hangman Game",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Word lists with categories and hints
WORD_LISTS = {
    "programming": [
        ("python", "A snake-like programming language"),
        ("javascript", "Powers interactivity on the web"),
        ("algorithm", "Step-by-step procedure to solve problems"),
        ("database", "Organized collection of data"),
        ("function", "A reusable block of code"),
        ("variable", "A container for storing data values"),
        ("framework", "Platform for developing software applications"),
        ("interface", "Point of interaction between components"),
        ("streamlit", "Python library for creating web apps")
    ],
    "animals": [
        ("elephant", "Largest land mammal with a trunk"),
        ("penguin", "Flightless bird that loves the cold"),
        ("dolphin", "Intelligent marine mammal"),
        ("giraffe", "Tallest living animal"),
        ("kangaroo", "Marsupial known for hopping"),
        ("octopus", "Sea creature with eight arms"),
        ("cheetah", "Fastest land animal"),
        ("panda", "Black and white bear that eats bamboo"),
        ("koala", "Australian marsupial that sleeps a lot")
    ],
    "countries": [
        ("brazil", "Home to the Amazon rainforest"),
        ("japan", "Land of the rising sun"),
        ("egypt", "Famous for ancient pyramids"),
        ("canada", "Known for maple syrup and politeness"),
        ("australia", "Island continent with unique wildlife"),
        ("france", "Known for the Eiffel Tower"),
        ("mexico", "Land of tacos and ancient Mayan ruins"),
        ("italy", "Boot-shaped country known for pasta"),
        ("india", "Land of spices and the Taj Mahal")
    ],
    "movies": [
        ("avatar", "Blue aliens on a distant moon"),
        ("inception", "Dreams within dreams"),
        ("titanic", "Famous ship disaster love story"),
        ("matrix", "Reality is a simulation"),
        ("gladiator", "Roman warrior seeking revenge"),
        ("frozen", "Let it go, let it go..."),
        ("jaws", "Dangerous shark terrorizes a beach town"),
        ("godfather", "Iconic mafia family saga"),
        ("jurassic", "Dinosaurs brought back to life")
    ]
}

# Hangman drawing stages - more detailed ASCII art
HANGMAN_STAGES = [
    """
    +---+
    |   |
        |
        |
        |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
        |
        |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
    |   |
        |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
   /|   |
        |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
   /|\\  |
        |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
   /|\\  |
   /    |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
   /|\\  |
   / \\  |
        |
    =========
    """
]

# Custom CSS with improved styling
def load_css():
    st.markdown("""
    <style>
    /* Main container */
    .main {
        background-color: #f8f9fa;
        padding: 20px;
    }
    
    /* Game title */
    .game-title {
        color: #6200ea;
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Game subtitle */
    .game-subtitle {
        color: #7c4dff;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }
    
    /* Game container */
    .game-container {
        background-color: white;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* Category selector */
    .category-selector {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-bottom: 20px;
        flex-wrap: wrap;
    }
    
    .category-button {
        background-color: #7c4dff;
        color: white;
        border: none;
        border-radius: 20px;
        padding: 8px 16px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .category-button:hover {
        background-color: #6200ea;
        transform: translateY(-2px);
    }
    
    .category-button.active {
        background-color: #6200ea;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Hangman drawing */
    .hangman-drawing {
        font-family: monospace;
        font-size: 1.2rem;
        line-height: 1.2;
        text-align: center;
        background-color: #f0f4f8;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    /* Word display */
    .word-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin: 30px 0;
        flex-wrap: wrap;
    }
    
    .letter-box {
        width: 50px;
        height: 60px;
        border-bottom: 3px solid #6200ea;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        font-weight: bold;
        color: #6200ea;
        transition: all 0.3s;
    }
    
    /* Keyboard */
    .keyboard {
        display: flex;
        flex-direction: column;
        gap: 8px;
        align-items: center;
        margin-top: 20px;
    }
    
    .keyboard-row {
        display: flex;
        gap: 5px;
    }
    
    .key {
        width: 40px;
        height: 40px;
        border-radius: 5px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.2s;
        background-color: #7c4dff;
        color: white;
        border: none;
    }
    
    .key:hover {
        transform: translateY(-2px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .key.used {
        opacity: 0.6;
        cursor: not-allowed;
    }
    
    .key.correct {
        background-color: #00c853;
    }
    
    .key.wrong {
        background-color: #ff3d00;
    }
    
    /* Game status */
    .game-status {
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 20px 0;
        padding: 10px;
        border-radius: 10px;
    }
    
    .status-win {
        background-color: #e8f5e9;
        color: #00c853;
    }
    
    .status-lose {
        background-color: #ffebee;
        color: #ff3d00;
    }
    
    /* Hint section */
    .hint-container {
        text-align: center;
        margin: 20px 0;
    }
    
    .hint-text {
        font-style: italic;
        color: #7c4dff;
        background-color: #f3e5f5;
        padding: 10px;
        border-radius: 10px;
        display: inline-block;
    }
    
    /* Score display */
    .score-display {
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        color: #6200ea;
        margin-bottom: 20px;
    }
    
    /* Animations */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .animate-pulse {
        animation: pulse 1s infinite;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .letter-box {
            width: 40px;
            height: 50px;
            font-size: 1.5rem;
        }
        
        .key {
            width: 30px;
            height: 30px;
            font-size: 0.9rem;
        }
        
        .game-title {
            font-size: 2rem;
        }
    }
    
    /* Custom button styles */
    .correct-letter button {
        background-color: #00c853 !important;
        color: white !important;
    }
    
    .wrong-letter button {
        background-color: #ff3d00 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_game_state():
    if "initialized" not in st.session_state:
        st.session_state.category = "programming"
        word_data = random.choice(WORD_LISTS[st.session_state.category])
        st.session_state.word = word_data[0].lower()
        st.session_state.hint = word_data[1]
        st.session_state.guessed_letters = set()
        st.session_state.wrong_guesses = 0
        st.session_state.max_attempts = 6
        st.session_state.game_over = False
        st.session_state.victory = False
        st.session_state.show_hint = False
        st.session_state.score = 0
        st.session_state.games_played = 0
        st.session_state.initialized = True
        st.session_state.animation_key = 0  # For triggering animations

# Game logic functions
def start_new_game():
    word_data = random.choice(WORD_LISTS[st.session_state.category])
    st.session_state.word = word_data[0].lower()
    st.session_state.hint = word_data[1]
    st.session_state.guessed_letters = set()
    st.session_state.wrong_guesses = 0
    st.session_state.game_over = False
    st.session_state.victory = False
    st.session_state.show_hint = False
    st.session_state.games_played += 1
    st.session_state.animation_key += 1

def check_game_status():
    # Check for victory
    if all(letter in st.session_state.guessed_letters for letter in st.session_state.word if letter.isalpha()):
        st.session_state.victory = True
        st.session_state.game_over = True
        # Calculate score based on word length and remaining attempts
        points = len(st.session_state.word) * 2 + (st.session_state.max_attempts - st.session_state.wrong_guesses) * 3
        st.session_state.score += points
        return True
    
    # Check for loss
    if st.session_state.wrong_guesses >= st.session_state.max_attempts:
        st.session_state.game_over = True
        return True
    
    return False

def handle_guess(letter):
    if st.session_state.game_over or letter in st.session_state.guessed_letters:
        return
    
    st.session_state.guessed_letters.add(letter)
    
    if letter not in st.session_state.word:
        st.session_state.wrong_guesses += 1
    
    check_game_status()

def change_category(category):
    if category != st.session_state.category:
        st.session_state.category = category
        start_new_game()

def toggle_hint():
    st.session_state.show_hint = not st.session_state.show_hint
    # Small penalty for using hint
    if st.session_state.show_hint and not st.session_state.game_over:
        st.session_state.score = max(0, st.session_state.score - 1)

# UI Components
def render_header():
    st.markdown('<h1 class="game-title">Hangman Game</h1>', unsafe_allow_html=True)
    st.markdown('<p class="game-subtitle">Guess the word before the hangman is complete!</p>', unsafe_allow_html=True)

def render_score():
    st.markdown(f'<div class="score-display">Score: {st.session_state.score} | Games Played: {st.session_state.games_played}</div>', unsafe_allow_html=True)

def render_category_selector():
    st.markdown('<div class="category-selector">', unsafe_allow_html=True)
    
    cols = st.columns(len(WORD_LISTS))
    for i, category in enumerate(WORD_LISTS.keys()):
        with cols[i]:
            if st.button(
                category.capitalize(),
                key=f"cat_{category}",
                use_container_width=True,
                type="primary" if category == st.session_state.category else "secondary"
            ):
                change_category(category)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_hangman():
    stage = min(st.session_state.wrong_guesses, len(HANGMAN_STAGES) - 1)
    st.code(HANGMAN_STAGES[stage], language=None)
    
    # Progress bar
    progress = st.session_state.wrong_guesses / st.session_state.max_attempts
    remaining = st.session_state.max_attempts - st.session_state.wrong_guesses
    st.progress(progress, text=f"Attempts: {st.session_state.wrong_guesses}/{st.session_state.max_attempts} ({remaining} remaining)")

def render_word_display():
    cols = st.columns([1, 3, 1])
    with cols[1]:
        # Create a container for the word
        word_container = st.container()
        
        # Display each letter
        letter_cols = word_container.columns(len(st.session_state.word))
        for i, letter in enumerate(st.session_state.word):
            with letter_cols[i]:
                if letter.isalpha():
                    is_guessed = letter in st.session_state.guessed_letters
                    should_reveal = is_guessed or st.session_state.game_over
                    
                    if should_reveal:
                        st.markdown(f'<div class="letter-box">{letter.upper()}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="letter-box">&nbsp;</div>', unsafe_allow_html=True)
                else:
                    # For spaces or special characters
                    st.markdown(f'<div style="width: 50px;">&nbsp;</div>', unsafe_allow_html=True)

def render_keyboard():
    if st.session_state.game_over:
        return
    
    keyboard_rows = [
        ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
        ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
        ["z", "x", "c", "v", "b", "n", "m"]
    ]
    
    for row in keyboard_rows:
        cols = st.columns(len(row))
        for i, letter in enumerate(row):
            with cols[i]:
                is_guessed = letter in st.session_state.guessed_letters
                is_correct = letter in st.session_state.word
                
                # FIX: Changed "danger" to "tertiary" for wrong guesses
                button_type = "secondary"
                if is_guessed:
                    button_type = "primary" if is_correct else "tertiary"
                
                # Apply custom CSS for colored buttons
                if is_guessed:
                    if is_correct:
                        st.markdown('<div class="correct-letter">', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="wrong-letter">', unsafe_allow_html=True)
                
                if st.button(
                    letter.upper(),
                    key=f"key_{letter}_{st.session_state.animation_key}",  # Add animation key to force refresh
                    disabled=is_guessed,
                    type=button_type,
                    use_container_width=True
                ):
                    handle_guess(letter)
                
                # Close the div if we opened one
                if is_guessed:
                    st.markdown('</div>', unsafe_allow_html=True)

def render_hint_section():
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("Show Hint", use_container_width=True):
            toggle_hint()
    
    if st.session_state.show_hint:
        st.markdown(f'<div class="hint-container"><div class="hint-text">{st.session_state.hint}</div></div>', unsafe_allow_html=True)

def render_game_status():
    if not st.session_state.game_over:
        return
    
    if st.session_state.victory:
        st.markdown('<div class="game-status status-win">Congratulations! You won! 🎉</div>', unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown('<div class="game-status status-lose">Game Over! Better luck next time 😞</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="text-align: center; margin-bottom: 20px;">The word was: <strong>{st.session_state.word.upper()}</strong></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Play Again", type="primary", use_container_width=True):
            start_new_game()

# Main app
def main():
    # Load CSS
    load_css()
    
    # Initialize game state
    init_game_state()
    
    # Render header
    render_header()
    
    # Game container
    with st.container():
        st.markdown('<div class="game-container">', unsafe_allow_html=True)
        
        # Score display
        render_score()
        
        # Category selector
        render_category_selector()
        
        # Game layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Hangman drawing
            render_hangman()
        
        with col2:
            # Hint section
            render_hint_section()
            
            # Game status
            render_game_status()
        
        # Word display
        render_word_display()
        
        # Keyboard
        render_keyboard()
        
        st.markdown('</div>', unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
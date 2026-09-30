# Tic-Tac-Toe AI

A modern, responsive, client-side web application implementing a Human vs. Computer Tic-Tac-Toe game powered by an intelligent decision engine featuring an unbeatable Minimax algorithm.

---

## 📌 Project Overview

**Tic-Tac-Toe AI** is an interactive, browser-native strategy game built from the ground up using pure web technologies. The player competes as **X** against an automated opponent playing as **O**. The game offers a seamless experience across desktop, tablet, and mobile devices, complete with real-time analytics, animated visual feedback, native sound synthesis, and accessible controls.

---

## 🎯 Internship Task Objective

The objective of this project is to develop an independent, self-contained, and production-ready front-end application demonstrating:
- Core game state architecture and win/draw condition evaluations.
- Artificial intelligence game algorithms ranging from heuristic checks to recursive adversarial search.
- Modern CSS design system principles (Dark/Light modes, glassmorphism, responsive grids).
- Screen-reader accessibility (WCAG AA/AAA standards).
- 100% static deployment readiness compatible with GitHub Pages without external dependencies or build tools.

---

## ✨ Key Features

- **Human vs AI Gameplay**: Human plays X (Electric Cyan); Computer plays O (Rose Coral).
- **Three Distinct AI Modes**: Easy (Random), Medium (Rule-based Heuristic), and Hard (Optimal Minimax).
- **Visual AI Thinking Indicator**: Non-blocking simulation of computation with turn guards.
- **Dynamic Scoreboard & Session Analytics**: Tracks Player Wins, AI Wins, Draws, Total Matches, and Win Percentage with animated progress bar.
- **Local Persistence**: Preserves scores, statistics, difficulty preference, sound setting, and theme across browser refreshes via `localStorage`.
- **Browser-Native Audio Synthesizer**: Procedural sound effects generated through the Web Audio API (`OscillatorNode` / `GainNode`) with zero external audio assets.
- **Dark and Light Theme Toggle**: Seamless theme switching with system preference detection and CSS custom properties.
- **Tactile Board Feedback**: Translucent ghost 'X' hover preview on empty cells and celebratory pulsing animations for winning lines.
- **Full Accessibility (a11y)**: Accessible keyboard controls (Tab, Enter, Space), screen-reader announcements via `aria-live`, and high-contrast focus rings.

---

## 🤖 AI Difficulty Explanation

### 1. Easy Mode
- Gathers all currently available vacant squares on the 3×3 grid.
- Selects a move at random using uniform probability distribution.
- Ideal for beginners or casual play.

### 2. Medium Mode (Heuristic Rule Engine)
1. **Immediate Win**: Scans all vacant squares; if placing an `'O'` results in an immediate victory, that move is played.
2. **Immediate Block**: Scans all vacant squares; if the human `'X'` could win on their next turn, the AI plays that square to block.
3. **Center Control**: Takes the center cell (`index 4`) if unoccupied.
4. **Corner Control**: Evaluates corner positions (`[0, 2, 6, 8]`) and randomly takes an available corner.
5. **Fallback**: Selects any remaining edge cell.

### 3. Hard Mode (Minimax Algorithm)
- Evaluates the game tree through recursive backtracking.
- Mathematically optimal play guaranteeing that the AI cannot be defeated under any sequence of human moves.

---

## 🧠 How the Minimax Algorithm is Used

The Minimax algorithm models Tic-Tac-Toe as a zero-sum, two-player game with complete information:

1. **Role Definition**:
   - **Maximizing Player**: AI (`'O'`) attempts to maximize the outcome score.
   - **Minimizing Player**: Human (`'X'`) attempts to minimize the outcome score.

2. **Terminal State Evaluation & Depth Penalty**:
   - **AI Victory**: `+10 - depth` (incentivizes faster wins).
   - **Human Victory**: `-10 + depth` (incentivizes delaying defeat).
   - **Draw**: `0`.

3. **Recursive Decision Tree**:
   - For every available square, the algorithm simulates placing the current player's mark and recursively explores all resulting game states until a terminal condition is reached.
   - The maximizing branch takes the maximum score among valid moves; the minimizing branch takes the minimum score.

4. **Tie-Breaking Variety**:
   - When multiple moves produce the identical optimal score (e.g., in early-game positions), the AI randomly selects among the top moves. This preserves unbeatable play while keeping matches varied and engaging.

---

## 🎮 Game Features & Technical Highlights

- **Human vs AI**: Player plays **X**; Computer plays **O**.
- **Accurate Win / Loss / Draw Detection**: All 8 winning axes (3 rows, 3 columns, 2 diagonals) and full-board conditions are checked instantaneously.
- **Scoreboard**: Clean counter cards with active turn glow indicators.
- **Session Statistics**: Detailed breakdown of games played and player win rate percentage.
- **Theme Switcher**: Instant transition between dark and light color palettes.
- **Sound Toggle**: Instant mute/unmute control; audio context initializes safely upon first user interaction.
- **Responsive Layout**: Designed for mobile phones, tablets, and desktop displays.

---

## 🛠️ Technologies Used

- **HTML5**: Semantic document structure, accessibility attributes, and vector SVG elements.
- **CSS3**: CSS Custom Properties (variables), CSS Grid, Flexbox, glassmorphic filters, and keyframe animations.
- **JavaScript (ES6+)**: Modular vanilla JS managing game state, recursive Minimax logic, Web Audio API synthesis, and DOM manipulation.

---

## 📁 Project Structure

```text
Task2_Tic_Tac_Toe_AI/
├── index.html        # Semantic HTML structure, game board markup, and controls
├── style.css         # Design system tokens, responsive styles, and animations
├── script.js         # Core engine, Minimax algorithm, audio synth, and stats
├── README.md         # Comprehensive project documentation
└── screenshots/      # Directory for application preview screenshots
    └── .gitkeep      # Preserves directory in git tracking
```

---

## 🚀 How to Run Locally

Because this project is completely self-contained with no server, package manager, or compilation requirements, it runs directly in any modern browser:

1. Clone or download the repository folder to your local computer.
2. Double-click **`index.html`** or right-click and choose **"Open with"** -> **Google Chrome**, **Microsoft Edge**, **Mozilla Firefox**, or **Safari**.
3. The game will launch and run immediately.

---

## 🌐 GitHub Pages Deployment Instructions

To deploy this project to GitHub Pages:

1. Create a new GitHub repository named `Task2_Tic_Tac_Toe_AI`.
2. Open your terminal inside the `Task2_Tic_Tac_Toe_AI` folder and run:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Tic-Tac-Toe AI"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/Task2_Tic_Tac_Toe_AI.git
   git push -u origin main
   ```
3. In your GitHub repository:
   - Go to **Settings** > **Pages**.
   - Under **Build and deployment** > **Branch**, select `main` and `/ (root)`.
   - Click **Save**.
4. Within a few moments, your application will be live.

### Example Public URL Format
```text
https://YOUR-USERNAME.github.io/Task2_Tic_Tac_Toe_AI/
```

---

## 🔮 Future Enhancement Ideas

- **Custom Board Dimensions**: Extend the game engine to support 4×4 or 5×5 grids with configurable connect-N rules.
- **Two-Player Local Mode**: Add an offline pass-and-play toggle for two human players on the same device.
- **AI Persona Dialogues**: Introduce subtle contextual reaction messages based on the current match progression.

---

## 🎓 Internship Learning Outcomes

- **Adversarial Search & Game Theory**: Implemented and optimized the Minimax algorithm with depth penalty heuristics.
- **Asynchronous State Coordination**: Managed simulated computational latency with turn locks to prevent race conditions during player actions.
- **Procedural Audio Synthesis**: Utilized the native browser Web Audio API to create dynamic sound effects without external audio files.
- **Design Systems & Accessibility**: Built a responsive, accessible interface with dark/light themes and full keyboard/screen-reader compatibility.
- **Zero-Dependency Production Architecture**: Maintained clean, modular code suitable for immediate static deployment.

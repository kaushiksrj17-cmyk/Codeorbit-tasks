/**
 * ============================================================================
 * Tic-Tac-Toe AI — Game Engine & AI Logic
 * Internship Project • Task 2
 * 
 * Features:
 *  - Human (X) vs Computer (O)
 *  - 3 AI Difficulties: Easy (Random), Medium (Heuristic), Hard (Minimax)
 *  - Web Audio API Sound Synthesizer (Zero External Dependencies)
 *  - Accessible Keyboard & Screen Reader Support
 *  - Local Browser Persistence (Scores, Statistics, Themes, Sound)
 *  - GitHub Pages Ready (Pure Client-Side Vanilla JS)
 * ============================================================================
 */

(function () {
  'use strict';

  // --------------------------------------------------------------------------
  // 1. Constants & Configurations
  // --------------------------------------------------------------------------
  const PLAYER_HUMAN = 'X';
  const PLAYER_AI = 'O';

  // All 8 possible winning lines on a 3x3 grid (indices 0 to 8)
  const WINNING_COMBINATIONS = [
    [0, 1, 2], // Row 1
    [3, 4, 5], // Row 2
    [6, 7, 8], // Row 3
    [0, 3, 6], // Column 1
    [1, 4, 7], // Column 2
    [2, 5, 8], // Column 3
    [0, 4, 8], // Diagonal top-left to bottom-right
    [2, 4, 6]  // Diagonal top-right to bottom-left
  ];

  // SVG Mark Templates for high-DPI crisp rendering
  const SVG_MARK_X = `
    <svg viewBox="0 0 100 100" stroke-width="12" stroke-linecap="round" aria-hidden="true">
      <line x1="22" y1="22" x2="78" y2="78"></line>
      <line x1="78" y1="22" x2="22" y2="78"></line>
    </svg>
  `;

  const SVG_MARK_O = `
    <svg viewBox="0 0 100 100" stroke-width="12" fill="none" aria-hidden="true">
      <circle cx="50" cy="50" r="30"></circle>
    </svg>
  `;

  // LocalStorage Keys
  const STORAGE_KEYS = {
    STATS: 'tictactoe_ai_stats',
    THEME: 'tictactoe_theme',
    SOUND: 'tictactoe_sound_enabled',
    DIFFICULTY: 'tictactoe_difficulty'
  };

  // --------------------------------------------------------------------------
  // 2. Application State
  // --------------------------------------------------------------------------
  const state = {
    board: Array(9).fill(''),
    currentPlayer: PLAYER_HUMAN,
    isGameActive: true,
    isAiThinking: false,
    aiTimeoutId: null,
    difficulty: 'hard', // 'easy' | 'medium' | 'hard'
    soundEnabled: true,
    theme: 'dark',
    stats: {
      totalGames: 0,
      playerWins: 0,
      aiWins: 0,
      draws: 0
    }
  };

  // --------------------------------------------------------------------------
  // 3. DOM Element References
  // --------------------------------------------------------------------------
  const elements = {
    html: document.documentElement,
    board: document.getElementById('board'),
    cells: document.querySelectorAll('.cell'),
    statusBanner: document.getElementById('status-banner'),
    statusIcon: document.getElementById('status-icon'),
    statusText: document.getElementById('status-text'),
    aiThinkingSpinner: document.getElementById('ai-thinking-spinner'),
    newGameBtn: document.getElementById('new-game-btn'),
    diffBtns: document.querySelectorAll('.diff-btn'),
    soundToggleBtn: document.getElementById('sound-toggle-btn'),
    soundIconOn: document.getElementById('sound-icon-on'),
    soundIconOff: document.getElementById('sound-icon-off'),
    themeToggleBtn: document.getElementById('theme-toggle-btn'),
    themeIconMoon: document.getElementById('theme-icon-moon'),
    themeIconSun: document.getElementById('theme-icon-sun'),
    playerScoreCard: document.getElementById('player-score-card'),
    aiScoreCard: document.getElementById('ai-score-card'),
    playerScoreVal: document.getElementById('player-score-val'),
    aiScoreVal: document.getElementById('ai-score-val'),
    drawsScoreVal: document.getElementById('draws-score-val'),
    statTotalGames: document.getElementById('stat-total-games'),
    statPlayerWins: document.getElementById('stat-player-wins'),
    statAiWins: document.getElementById('stat-ai-wins'),
    statDraws: document.getElementById('stat-draws'),
    statWinRate: document.getElementById('stat-win-rate'),
    winRateBar: document.getElementById('win-rate-bar'),
    resetStatsBtn: document.getElementById('reset-stats-btn')
  };

  // --------------------------------------------------------------------------
  // 4. Web Audio Synthesizer (Native Browser Audio)
  // --------------------------------------------------------------------------
  let audioCtx = null;

  function getAudioContext() {
    if (!audioCtx && (window.AudioContext || window.webkitAudioContext)) {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      audioCtx = new AudioContextClass();
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume().catch(() => {});
    }
    return audioCtx;
  }

  /**
   * Generates a tone using an oscillator with exponential volume decay.
   * @param {number} frequency - Tone frequency in Hz
   * @param {number} duration - Duration in seconds
   * @param {string} type - Wave type ('sine', 'triangle', etc.)
   * @param {number} startDelay - Offset in seconds before starting
   */
  function playTone(frequency, duration = 0.1, type = 'sine', startDelay = 0) {
    if (!state.soundEnabled) return;
    try {
      const ctx = getAudioContext();
      if (!ctx) return;

      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      const startTime = ctx.currentTime + startDelay;
      const stopTime = startTime + duration;

      osc.type = type;
      osc.frequency.setValueAtTime(frequency, startTime);

      gain.gain.setValueAtTime(0.15, startTime);
      gain.gain.exponentialRampToValueAtTime(0.001, stopTime);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start(startTime);
      osc.stop(stopTime);
    } catch {
      // Audio playback fails silently if restricted by browser autoplay policy
    }
  }

  // Pre-configured Sound Effects
  const soundEffects = {
    humanMove: () => playTone(540, 0.09, 'sine'),
    aiMove: () => playTone(380, 0.12, 'triangle'),
    win: () => {
      playTone(523.25, 0.12, 'sine', 0);     // C5
      playTone(659.25, 0.14, 'sine', 0.12);  // E5
      playTone(783.99, 0.25, 'sine', 0.26);  // G5
    },
    loss: () => {
      playTone(440.00, 0.14, 'sawtooth', 0);    // A4
      playTone(370.00, 0.15, 'sawtooth', 0.14); // F#4
      playTone(293.66, 0.25, 'sawtooth', 0.29); // D4
    },
    draw: () => {
      playTone(392.00, 0.15, 'triangle', 0);    // G4
      playTone(349.23, 0.22, 'triangle', 0.15); // F4
    },
    click: () => playTone(800, 0.04, 'sine')
  };

  // --------------------------------------------------------------------------
  // 5. Game Logic & Board Evaluation Functions
  // --------------------------------------------------------------------------

  /**
   * Checks whether a given board configuration contains a winning line.
   * @param {Array<string>} board - 9-element array representing the board
   * @returns {{ winner: string, combo: number[] } | null}
   */
  function checkWinner(board) {
    for (let i = 0; i < WINNING_COMBINATIONS.length; i++) {
      const [a, b, c] = WINNING_COMBINATIONS[i];
      if (board[a] && board[a] === board[b] && board[a] === board[c]) {
        return { winner: board[a], combo: [a, b, c] };
      }
    }
    return null;
  }

  /**
   * Checks if all cells are filled with no moves remaining.
   * @param {Array<string>} board
   * @returns {boolean}
   */
  function isBoardFull(board) {
    return board.every(cell => cell !== '');
  }

  /**
   * Returns an array of empty cell indices on the board.
   * @param {Array<string>} board
   * @returns {number[]}
   */
  function getEmptyIndices(board) {
    const emptyIndices = [];
    for (let i = 0; i < board.length; i++) {
      if (board[i] === '') emptyIndices.push(i);
    }
    return emptyIndices;
  }

  // --------------------------------------------------------------------------
  // 6. AI Algorithms: Easy, Medium, and Hard (Minimax)
  // --------------------------------------------------------------------------

  /**
   * EASY AI:
   * Selects an entirely random valid empty square.
   */
  function getEasyMove(board) {
    const emptyIndices = getEmptyIndices(board);
    if (emptyIndices.length === 0) return null;
    const randomIndex = Math.floor(Math.random() * emptyIndices.length);
    return emptyIndices[randomIndex];
  }

  /**
   * MEDIUM AI:
   * 1. Checks if AI can win immediately (Winning move).
   * 2. Checks if Human can win immediately (Blocking move).
   * 3. Selects center (cell 4) if available.
   * 4. Selects a corner (0, 2, 6, 8) if available.
   * 5. Otherwise picks any remaining valid square.
   */
  function getMediumMove(board) {
    const emptyIndices = getEmptyIndices(board);
    if (emptyIndices.length === 0) return null;

    // Step 1: Look for immediate AI win
    for (const idx of emptyIndices) {
      board[idx] = PLAYER_AI;
      const winCheck = checkWinner(board);
      board[idx] = ''; // Undo simulation
      if (winCheck && winCheck.winner === PLAYER_AI) {
        return idx;
      }
    }

    // Step 2: Block immediate Human win
    for (const idx of emptyIndices) {
      board[idx] = PLAYER_HUMAN;
      const winCheck = checkWinner(board);
      board[idx] = ''; // Undo simulation
      if (winCheck && winCheck.winner === PLAYER_HUMAN) {
        return idx;
      }
    }

    // Step 3: Prioritize Center
    if (board[4] === '') return 4;

    // Step 4: Prioritize Corners (0, 2, 6, 8)
    const corners = [0, 2, 6, 8].filter(idx => board[idx] === '');
    if (corners.length > 0) {
      const randomCorner = corners[Math.floor(Math.random() * corners.length)];
      return randomCorner;
    }

    // Step 5: Fallback to any remaining edge
    return emptyIndices[Math.floor(Math.random() * emptyIndices.length)];
  }

  /**
   * HARD AI — MINIMAX ALGORITHM:
   * Recursively traverses all future states of the game tree.
   * - AI (PLAYER_AI = 'O') is the MAXIMIZING player.
   * - Human (PLAYER_HUMAN = 'X') is the MINIMIZING player.
   * - Depth penalty ensures AI achieves fast wins and delays losses.
   * 
   * @param {Array<string>} board - Simulated board state
   * @param {number} depth - Recursion depth
   * @param {boolean} isMaximizing - True if current turn is AI
   * @returns {number} Score of the branch
   */
  function minimax(board, depth, isMaximizing) {
    const winResult = checkWinner(board);

    // Terminal Evaluation: AI Win (+10 - depth)
    if (winResult && winResult.winner === PLAYER_AI) {
      return 10 - depth;
    }

    // Terminal Evaluation: Human Win (-10 + depth)
    if (winResult && winResult.winner === PLAYER_HUMAN) {
      return depth - 10;
    }

    // Terminal Evaluation: Draw (0)
    if (isBoardFull(board)) {
      return 0;
    }

    const emptyIndices = getEmptyIndices(board);

    if (isMaximizing) {
      let maxScore = -Infinity;
      for (const idx of emptyIndices) {
        board[idx] = PLAYER_AI;
        const score = minimax(board, depth + 1, false);
        board[idx] = ''; // Backtrack
        maxScore = Math.max(maxScore, score);
      }
      return maxScore;
    } else {
      let minScore = Infinity;
      for (const idx of emptyIndices) {
        board[idx] = PLAYER_HUMAN;
        const score = minimax(board, depth + 1, true);
        board[idx] = ''; // Backtrack
        minScore = Math.min(minScore, score);
      }
      return minScore;
    }
  }

  /**
   * Determines the optimal move for Hard difficulty using Minimax.
   * Collects all moves achieving the maximum score and randomly picks
   * among them to provide natural non-repetitive play while remaining unbeatable.
   */
  function getHardMove(board) {
    const emptyIndices = getEmptyIndices(board);
    if (emptyIndices.length === 0) return null;

    let bestScore = -Infinity;
    let bestMoves = [];

    for (const idx of emptyIndices) {
      board[idx] = PLAYER_AI;
      const score = minimax(board, 0, false);
      board[idx] = ''; // Backtrack

      if (score > bestScore) {
        bestScore = score;
        bestMoves = [idx];
      } else if (score === bestScore) {
        bestMoves.push(idx);
      }
    }

    // Pick randomly among the tied optimal moves
    return bestMoves[Math.floor(Math.random() * bestMoves.length)];
  }

  /**
   * Dispatches move selection to the selected AI difficulty.
   */
  function computeAiMove(board, difficulty) {
    switch (difficulty) {
      case 'easy':
        return getEasyMove(board);
      case 'medium':
        return getMediumMove(board);
      case 'hard':
      default:
        return getHardMove(board);
    }
  }

  // --------------------------------------------------------------------------
  // 7. UI Rendering & Game Flow Controllers
  // --------------------------------------------------------------------------

  /**
   * Updates visual presentation of the 3x3 board based on state.
   */
  function renderBoard() {
    state.board.forEach((cellValue, idx) => {
      const cellElement = elements.cells[idx];
      const row = Math.floor(idx / 3) + 1;
      const col = (idx % 3) + 1;

      if (cellValue === PLAYER_HUMAN) {
        if (!cellElement.classList.contains('cell-x')) {
          cellElement.innerHTML = SVG_MARK_X;
          cellElement.classList.add('taken', 'cell-x');
          cellElement.classList.remove('cell-o');
          cellElement.setAttribute('aria-label', `Row ${row}, Column ${col}, X`);
          cellElement.disabled = true;
        }
      } else if (cellValue === PLAYER_AI) {
        if (!cellElement.classList.contains('cell-o')) {
          cellElement.innerHTML = SVG_MARK_O;
          cellElement.classList.add('taken', 'cell-o');
          cellElement.classList.remove('cell-x');
          cellElement.setAttribute('aria-label', `Row ${row}, Column ${col}, O`);
          cellElement.disabled = true;
        }
      } else {
        cellElement.innerHTML = '';
        cellElement.className = 'cell';
        cellElement.setAttribute('aria-label', `Row ${row}, Column ${col}, empty`);
        cellElement.disabled = !state.isGameActive || state.isAiThinking;
      }
    });

    // Toggle board interaction lock
    if (!state.isGameActive || state.isAiThinking) {
      elements.board.classList.add('locked');
    } else {
      elements.board.classList.remove('locked');
    }

    // Update active player card highlighting
    if (state.isGameActive) {
      if (state.currentPlayer === PLAYER_HUMAN) {
        elements.playerScoreCard.classList.add('active-turn');
        elements.aiScoreCard.classList.remove('active-turn');
      } else {
        elements.aiScoreCard.classList.add('active-turn');
        elements.playerScoreCard.classList.remove('active-turn');
      }
    } else {
      elements.playerScoreCard.classList.remove('active-turn');
      elements.aiScoreCard.classList.remove('active-turn');
    }
  }

  /**
   * Sets game status message and banner styling.
   */
  function setStatus(text, icon = '🎮', type = 'default') {
    elements.statusText.textContent = text;
    elements.statusIcon.textContent = icon;

    elements.statusBanner.classList.remove('win-x', 'win-o', 'draw');
    if (type === 'win-x') elements.statusBanner.classList.add('win-x');
    if (type === 'win-o') elements.statusBanner.classList.add('win-o');
    if (type === 'draw') elements.statusBanner.classList.add('draw');
  }

  /**
   * Highlights the three cells that formed the winning line.
   */
  function highlightWinningCombo(combo) {
    combo.forEach(idx => {
      elements.cells[idx].classList.add('win-cell');
    });
  }

  /**
   * Handles human player move on cell click.
   */
  function handleCellClick(e) {
    const cell = e.currentTarget;
    const index = parseInt(cell.getAttribute('data-index'), 10);

    // Prevent move if cell occupied, game over, or AI currently thinking
    if (!state.isGameActive || state.isAiThinking || state.board[index] !== '') {
      return;
    }

    // Apply Human Move
    state.board[index] = PLAYER_HUMAN;
    soundEffects.humanMove();
    renderBoard();

    // Check for Human Win or Draw
    const winCheck = checkWinner(state.board);
    if (winCheck) {
      endGame('human', winCheck.combo);
      return;
    }

    if (isBoardFull(state.board)) {
      endGame('draw');
      return;
    }

    // Pass turn to AI
    triggerAiTurn();
  }

  /**
   * Triggers the AI move with a simulated thinking delay.
   */
  function triggerAiTurn() {
    state.currentPlayer = PLAYER_AI;
    state.isAiThinking = true;
    renderBoard();

    // Show thinking indicator
    elements.aiThinkingSpinner.classList.remove('hidden');
    setStatus('AI is calculating move...', '🧠');

    // Natural delay (~350ms to 450ms) to simulate computational thinking
    const thinkingDelay = Math.floor(Math.random() * 100) + 350;

    // Clear any previous timer if one exists
    if (state.aiTimeoutId) {
      clearTimeout(state.aiTimeoutId);
      state.aiTimeoutId = null;
    }

    state.aiTimeoutId = setTimeout(() => {
      state.aiTimeoutId = null;

      // Re-verify that game is still active and it is still AI turn
      if (!state.isGameActive || state.currentPlayer !== PLAYER_AI) {
        state.isAiThinking = false;
        elements.aiThinkingSpinner.classList.add('hidden');
        return;
      }

      const aiMoveIndex = computeAiMove(state.board, state.difficulty);

      if (aiMoveIndex !== null && state.board[aiMoveIndex] === '') {
        state.board[aiMoveIndex] = PLAYER_AI;
        soundEffects.aiMove();
      }

      state.isAiThinking = false;
      elements.aiThinkingSpinner.classList.add('hidden');
      renderBoard();

      // Check for AI Win or Draw
      const winCheck = checkWinner(state.board);
      if (winCheck) {
        endGame('ai', winCheck.combo);
        return;
      }

      if (isBoardFull(state.board)) {
        endGame('draw');
        return;
      }

      // Return turn to Human
      state.currentPlayer = PLAYER_HUMAN;
      setStatus('Your Turn (X) — Select a square', '🎮');
      renderBoard();
    }, thinkingDelay);
  }

  /**
   * Concludes the game, updates statistics, triggers audio and animations.
   */
  function endGame(result, winningCombo = null) {
    if (state.aiTimeoutId) {
      clearTimeout(state.aiTimeoutId);
      state.aiTimeoutId = null;
    }

    state.isGameActive = false;
    state.isAiThinking = false;
    elements.aiThinkingSpinner.classList.add('hidden');

    state.stats.totalGames++;

    if (result === 'human') {
      state.stats.playerWins++;
      highlightWinningCombo(winningCombo);
      setStatus('Victory! You defeated the AI 🎉', '🏆', 'win-x');
      soundEffects.win();
    } else if (result === 'ai') {
      state.stats.aiWins++;
      highlightWinningCombo(winningCombo);
      setStatus('AI wins! Better luck next round 🤖', '🤖', 'win-o');
      soundEffects.loss();
    } else {
      state.stats.draws++;
      setStatus("It's a draw! Well matched 🤝", '🤝', 'draw');
      soundEffects.draw();
    }

    saveStats();
    updateStatsDisplay();
    renderBoard();
  }

  /**
   * Resets board state for a new match while preserving historical statistics.
   */
  function resetGame() {
    if (state.aiTimeoutId) {
      clearTimeout(state.aiTimeoutId);
      state.aiTimeoutId = null;
    }

    soundEffects.click();
    state.board = Array(9).fill('');
    state.currentPlayer = PLAYER_HUMAN;
    state.isGameActive = true;
    state.isAiThinking = false;

    elements.aiThinkingSpinner.classList.add('hidden');
    elements.cells.forEach(cell => {
      cell.classList.remove('win-cell', 'taken', 'cell-x', 'cell-o');
      cell.innerHTML = '';
      cell.disabled = false;
    });

    setStatus('Your Turn (X) — Select a square', '🎮');
    renderBoard();
  }

  // --------------------------------------------------------------------------
  // 8. Statistics & Persistence
  // --------------------------------------------------------------------------

  function loadStats() {
    try {
      const stored = localStorage.getItem(STORAGE_KEYS.STATS);
      if (stored) {
        const parsed = JSON.parse(stored);
        if (parsed && typeof parsed === 'object') {
          state.stats = {
            totalGames: Math.max(0, parseInt(parsed.totalGames, 10) || 0),
            playerWins: Math.max(0, parseInt(parsed.playerWins, 10) || 0),
            aiWins: Math.max(0, parseInt(parsed.aiWins, 10) || 0),
            draws: Math.max(0, parseInt(parsed.draws, 10) || 0)
          };
        }
      }
    } catch {
      // LocalStorage access may be restricted; fallback to in-memory state
    }
  }

  function saveStats() {
    try {
      localStorage.setItem(STORAGE_KEYS.STATS, JSON.stringify(state.stats));
    } catch {
      // Fallback silently
    }
  }

  function updateStatsDisplay() {
    const { totalGames, playerWins, aiWins, draws } = state.stats;

    // Scoreboard header numbers
    elements.playerScoreVal.textContent = playerWins;
    elements.aiScoreVal.textContent = aiWins;
    elements.drawsScoreVal.textContent = draws;

    // Performance detail items
    elements.statTotalGames.textContent = totalGames;
    elements.statPlayerWins.textContent = playerWins;
    elements.statAiWins.textContent = aiWins;
    elements.statDraws.textContent = draws;

    // Win Rate Percentage calculation
    const winRate = totalGames > 0 ? ((playerWins / totalGames) * 100).toFixed(1) : '0.0';
    elements.statWinRate.textContent = `${winRate}%`;
    elements.winRateBar.style.width = `${Math.min(100, Math.max(0, parseFloat(winRate)))}%`;
  }

  function resetStatistics() {
    if (confirm('Are you sure you want to reset all session statistics and scoreboard records?')) {
      state.stats = {
        totalGames: 0,
        playerWins: 0,
        aiWins: 0,
        draws: 0
      };
      saveStats();
      updateStatsDisplay();
      soundEffects.click();
    }
  }

  // --------------------------------------------------------------------------
  // 9. Theme, Sound & Settings Management
  // --------------------------------------------------------------------------

  function applyTheme(theme) {
    state.theme = theme;
    elements.html.setAttribute('data-theme', theme);
    if (theme === 'dark') {
      elements.themeIconMoon.classList.remove('hidden');
      elements.themeIconSun.classList.add('hidden');
    } else {
      elements.themeIconMoon.classList.add('hidden');
      elements.themeIconSun.classList.remove('hidden');
    }
    try {
      localStorage.setItem(STORAGE_KEYS.THEME, theme);
    } catch {
      // Fallback
    }
  }

  function toggleTheme() {
    soundEffects.click();
    const newTheme = state.theme === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);
  }

  function applySoundState(enabled) {
    state.soundEnabled = enabled;
    if (enabled) {
      elements.soundIconOn.classList.remove('hidden');
      elements.soundIconOff.classList.add('hidden');
    } else {
      elements.soundIconOn.classList.add('hidden');
      elements.soundIconOff.classList.remove('hidden');
    }
    try {
      localStorage.setItem(STORAGE_KEYS.SOUND, enabled ? 'true' : 'false');
    } catch {
      // Fallback
    }
  }

  function toggleSound() {
    const newState = !state.soundEnabled;
    applySoundState(newState);
    if (newState) soundEffects.click();
  }

  function setDifficulty(diff, isUserAction = false) {
    if (state.aiTimeoutId) {
      clearTimeout(state.aiTimeoutId);
      state.aiTimeoutId = null;
    }

    if (state.difficulty === diff && !isUserAction) return;

    if (isUserAction) {
      soundEffects.click();
    }
    state.difficulty = diff;

    elements.diffBtns.forEach(btn => {
      const isSelected = btn.getAttribute('data-difficulty') === diff;
      btn.classList.toggle('active', isSelected);
      btn.setAttribute('aria-checked', isSelected ? 'true' : 'false');
    });

    try {
      localStorage.setItem(STORAGE_KEYS.DIFFICULTY, diff);
    } catch {
      // Fallback
    }

    // Restart game when difficulty changes by user action
    if (isUserAction) {
      resetGame();
    }
  }

  // --------------------------------------------------------------------------
  // 10. Initialization & Event Listeners
  // --------------------------------------------------------------------------
  function initialize() {
    // Load persisted settings
    loadStats();

    try {
      const storedTheme = localStorage.getItem(STORAGE_KEYS.THEME);
      if (storedTheme === 'light' || storedTheme === 'dark') {
        applyTheme(storedTheme);
      } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
        applyTheme('light');
      } else {
        applyTheme('dark');
      }

      const storedSound = localStorage.getItem(STORAGE_KEYS.SOUND);
      if (storedSound !== null) {
        applySoundState(storedSound === 'true');
      }

      const storedDiff = localStorage.getItem(STORAGE_KEYS.DIFFICULTY);
      if (storedDiff && ['easy', 'medium', 'hard'].includes(storedDiff)) {
        setDifficulty(storedDiff, false);
      }
    } catch {
      // Fallback to defaults
    }

    // Attach Board Cell Listeners
    elements.cells.forEach(cell => {
      cell.addEventListener('click', handleCellClick);
      // Support keyboard Enter & Space
      cell.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          cell.click();
        }
      });
    });

    // Primary Action Listeners
    elements.newGameBtn.addEventListener('click', resetGame);
    elements.resetStatsBtn.addEventListener('click', resetStatistics);
    elements.themeToggleBtn.addEventListener('click', toggleTheme);
    elements.soundToggleBtn.addEventListener('click', toggleSound);

    // Difficulty Button Listeners
    elements.diffBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const diff = btn.getAttribute('data-difficulty');
        setDifficulty(diff, true);
      });
    });

    // Initial Render
    updateStatsDisplay();
    renderBoard();
    setStatus('Your Turn (X) — Select a square', '🎮');
  }

  // Launch when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
  } else {
    initialize();
  }
})();

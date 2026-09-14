# 🐍 Classic Snake Game (with Blue & Red Balls)

A modern, light-weight HTML5 Canvas implementation of the classic Snake game with a custom rule twist featuring **Blue** and **Red** balls!

## 🎮 Game Rules

1. **Blue Balls (🔵)**:
   - Increase the snake's length by +1 segment.
   - Increase your total score by +1.
2. **Red Balls (🔴)**:
   - Decrease the snake's length by -1 segment.
   - Decrease your total score by -1.
   - *Warning:* If the snake shrinks to a length less than 1, it's Game Over!
3. **Score System**:
   - Total Score = `(Blue Balls Eaten - Red Balls Eaten)`
4. **Game Over Conditions**:
   - Hitting the canvas boundary walls.
   - Colliding with the snake's own body.
   - Shrinking down to 0 segments from eating red balls.

---

## 🕹️ Controls

- **Movement**:
  - `Arrow Keys` or `W`, `A`, `S`, `D`

---

## 🛠️ Built With

- **HTML5 Canvas**: For fast rendering of game graphics.
- **CSS3**: For sleek, dark-themed styling and UI overlays.
- **Vanilla JavaScript**: Pure JS without external dependencies or frameworks.

---

## 🚀 How to Run

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/snake-game.git](https://github.com/your-username/snake-game.git)

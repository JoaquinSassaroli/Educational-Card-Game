# Educational Card Game (Pairs Mode / Intruder Mode)

## 🎮 Project Overview

This project is an educational card game developed in Python using Pygame.
Its main goal is to reinforce school subjects through two interactive game modes:

* Pairs Mode → The player must match related pairs of cards based on the selected subject (Math, History, Chemistry, or Geography).

* Intruder Mode → The player must identify which card does not belong to the thematic set.

The game includes a scoring system, timer, subject selection, audio effects, level progression, and a Game Over screen.

## 🧩 Key Features
✔️ Main Menu

The player can select:

* Game Mode: Pairs / Intruder

* Subject: Math, History, Chemistry, Geography

* Background music

* Start and Exit buttons

<img width="1533" height="1006" alt="image" src="https://github.com/user-attachments/assets/595138df-882f-421a-b1ac-d45b4ec04939" />


✔️ Pairs Mode

* Randomized face-down cards based on the chosen subject

* The player must find the correct related pairs

* Score penalties for mistakes

* Customizable time limit

<img width="1527" height="1007" alt="image" src="https://github.com/user-attachments/assets/62996b1a-2a1e-4528-b308-fa23af294164" />
<img width="1535" height="1004" alt="image" src="https://github.com/user-attachments/assets/59efb70b-f73e-43ae-b179-5b08b4d5ab95" />


✔️ Intruder Mode

* Six cards are displayed (five correct + one intruder)

* Content adapts to the selected subject

* Intruder detection is based on semantic categories (dates, historical figures, chemical compounds, countries, etc.)

* Level progression with increasing difficulty and decreasing time

<img width="1535" height="1007" alt="image" src="https://github.com/user-attachments/assets/e38398e6-0159-4072-b02a-706455a364d6" />
  

✔️ Game Over Screen

Displays:

* Final score

* Total time used

* Win or loss message

* Restart and Main Menu options

<img width="1530" height="1008" alt="image" src="https://github.com/user-attachments/assets/435b0149-5cce-4263-b6fb-e6f50e31ad37" />
  

## 🚀 Installation and Execution
1️⃣ Clone the repository: 
git clone https://github.com/your-user/your-repo.git
cd your-repo

2️⃣ Create a virtual environment (optional but recommended): 
python -m venv venv


Activate it:

**Windows**

venv\Scripts\activate


**Mac/Linux**

source venv/bin/activate

3️⃣ Install dependencies: 
pip install pygame

4️⃣ Run the game: 
python main.py

## 🎨 Technologies Used

* Python 3

* Pygame (game engine)

* Custom implementations for:

  - Game state machine

  - Card rendering

  - Collision detection

  - Audio effects

  - Timer and score logic

## 🔧 Technical Summary
🧠 State Machine Architecture

The Game class manages all core states:

* MENU

* PAIRS

* INTRUDER

* GAME_OVER

Each state includes:

* handle_event()

* update()

* draw()

This allows for a clean, scalable game structure.

## 🃏 Card System

Each card includes:

* content

* type (normal / intruder)

* Display and flip methods

* A rect for click detection

## ⏱️ Timer System

The Cronometro class manages:

* Remaining time

* Level resets

* Time-out detection

# ⭐ Scoring

The Puntuacion class:

* Adds/removes points

* Displays score on screen


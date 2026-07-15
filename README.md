Good progress — the fences around Project Structure are now correct (opens before Danger_Maze_Game/, closes after projectiles/). Two small things left:

Double --- right after the closing ``` fence and before "What's Next" — two dash-lines in a row where only one is needed.
Indentation still not applied — backgrounds/, characters/, environment/, hazards/, mechanisms/, projectiles/ are all sitting at the same column as assets/ itself, instead of indented under it. You didn't paste in the indentation fix from my last message.

Since you're right that spacing matters here and back-and-forth patches keep missing something — here's the complete file, start to finish, ready to copy in one shot:
markdown# 🗡️ Danger Maze Game

A 2D maze survival game built with Python and Pygame.

---

## 💡 The Setup

You're the hero. Somewhere at the end of a hostile desert maze, there's a portal → your way out.

Between you and it: Orks that won't stop walking toward you, a Dragon that attacks from range, spike traps, cannons that fire on a timer, and a Great Dragon boss with more than one way to kill you depending on how close you get.

You have a bow, ten fingers on the arrow keys, and one shot at getting through.
You → move through the maze → dodge/fight enemies → reach the portal → survive

---

## 📺 Demo Video
*(coming soon)*

---

## 🎮 Controls

| Key | Action |
|-----|--------|
| Arrow Keys | Move |
| Space | Shoot arrow |

---

## ⚔️ What You're Up Against

| Threat | Behavior |
|---|---|
| Ork | Walks toward you, melee |
| Dragon | Ranged fireball attacks |
| Great Dragon (boss) | Idle → battle → melee/ranged attack phases, depending on distance |
| Spike hazards | Instant lethal damage on contact |
| Cannons | Fire on a timer; timing matters |
| Laser gates | Open/close; mistime it, you're dead |

---

## 🚀 Run It Yourself

```bash
pip install -r requirements.txt
python Game_launch.py
```

Requires Python 3.13 + Pygame 2.6.1.

---

## 📁 Project Structure
Danger_Maze_Game/
├── Game_launch.py
├── requirements.txt
└── assets/
├── backgrounds/
├── characters/
│   ├── archer/
│   │   ├── move/
│   │   ├── aiming/
│   │   └── died/
│   ├── ork/
│   ├── red_dragon/
│   └── great_dragon/
├── environment/
├── hazards/
├── mechanisms/
└── projectiles/

---

## 🔮 What's Next

- [ ] Demo video / gameplay footage
- [ ] A next level after the portal; right now, reaching it ends the run. That won't always be true.

---

## 👤 Author

**Ibrahim Mejjadi** — Digital Infrastructure Student, CMC Tangier
🔗 LinkedIn: [linkedin.com/in/ibrahimmejjadi](https://linkedin.com/in/ibrahimmejjadi)
📧 Email: ibrahim.mejjadi@gmail.com

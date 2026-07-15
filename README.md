# 🗡️ Danger Maze Game

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

**Ibrahim Mejjadi** : Digital Infrastructure Student, CMC Tangier
🔗 LinkedIn: [linkedin.com/in/ibrahimmejjadi](https://linkedin.com/in/ibrahimmejjadi)
📧 Email: ibrahim.mejjadi@gmail.com

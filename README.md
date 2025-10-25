# Star Shooter

Star Shooter is a retro-inspired 3D space shooter game developed using Pygame. Navigate your spaceship through a vast grid-based universe, collect keys, manage your fuel, and engage in thrilling combat against enemy ships. Your ultimate goal is to defeat the formidable boss and emerge victorious.

## Features

*   **First-Person 3D Perspective:** Experience space combat from within your immersive cockpit.
*   **Dynamic Starfield:** A visually engaging starfield with twinkling, multi-colored stars that reacts to your movement.
*   **Grid-Based Exploration:** Navigate a 16x16 universe divided into sectors, each with its own challenges and resources, including planets, nebulas and asteroid fields.
*   **Resource Management:** Keep an eye on your fuel levels, which deplete with movement, combat, and warping. Refuel at friendly starbases.
*   **Dual Weapon System:** Engage enemies with rapid-fire lasers or powerful, limited-supply missiles.
*   **Long-Range Missiles:** Fire missiles at enemies on the galactic map for strategic advantage.
*   **Radar and Map Displays:** Utilize on-screen instruments to track enemies, bases, planets, and keys.
*   **Varied Enemy Types:** Encounter different enemy types, including Fighters, Bombers, and powerful Cruisers, each with unique behaviors.
*   **Procedurally Generated Sounds:** Immersive and varied sound effects for lasers, missiles, explosions, and and shield hits.
*   **Improved Explosions:** More visually impressive explosion animation with particles.
*   **Shield Hit Effect:** A visual effect with particles when the player's shield is hit.
*   **Date/Time System:** An in-game date that advances with actions, adding a time-based challenge.
*   **Win/Loss Conditions:** Collect all keys from planets to summon the boss, defeat it to win, or face defeat if your fuel runs out, the boss reaches you, or the maximum date is exceeded.
*   **Complex Scoring System:** Earn bonuses for clearing sectors of enemies and for completing the game quickly.

## Installation

To set up and run Star Shooter, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/star-shooter.git
    cd star-luster
    ```
    (If not a git repository, download the project files and navigate to the project directory.)

2.  **Install Python:**
    Ensure you have Python 3.x installed. You can download it from [python.org](https://www.python.org/downloads/).

3.  **Install dependencies:**
    The game requires Pygame. Install it using pip:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Generate Sound Files:**
    The game uses procedurally generated sound effects. Run the `generate_sounds.py` script to create them:
    ```bash
    python generate_sounds.py
    ```

## How to Play Star Shooter

### Objective

Your primary objective depends on the game mode you choose:

*   **Adventure Mode:** Explore the galaxy to find and collect 7 keys from different planets. Once all keys are collected, the location of the final planet, where the boss awaits, will be revealed. Navigate to the final planet and defeat the boss to win the game.
*   **Command Mode:** Your mission is to defend your starbases from relentless waves of enemy attacks. You must strategically manage your resources and prioritize threats to keep your bases operational. The game ends if all your bases are destroyed.
*   **Training Mode:** A sandbox mode where you can freely practice your flying and combat skills without any specific objectives or threats.

### Controls

*   **Arrow Keys (UP/DOWN):** Increase or decrease your ship's speed.
*   **Arrow Keys (LEFT/RIGHT):** Rotate your ship left or right.
*   **Spacebar:** Fire your laser weapon. This consumes a small amount of energy.
*   **N Key:** Launch a powerful missile. You have a limited supply, which can be restocked at starbases.
*   **W Key:** Toggle warp targeting mode. When activated, use the arrow keys to select a target sector on the galactic map. Press 'W' again to initiate the warp. Warping consumes a significant amount of energy, and the amount depends on the distance traveled.
*   **H Key:** Execute a random warp to an unknown sector. This is a risky maneuver but can be useful for a quick escape. It consumes a fixed amount of energy.
*   **M Key:** Open the galactic map. In this view, you can see the entire grid, including the locations of planets, bases, and enemies. You can also use the arrow keys to move a targeting cursor and press the **Spacebar** to fire a long-range missile at an enemy in the targeted sector. This consumes one missile. Press 'M' again to exit the map.

### On-Screen Displays & Cockpit

Your view is from the cockpit of your starfighter, the "Gaia". The cockpit provides you with all the necessary information to navigate and survive in the galaxy.

*   **Main Viewport:** Your primary view of the 3D space in front of your ship.
*   **Energy Gauge (Bottom Left):** An arc-shaped gauge that displays your remaining energy. Energy is consumed by firing weapons, warping, and taking damage.
*   **Missile Count (Bottom Right):** A series of vertical bars indicating your remaining missiles.
*   **System Status (Top Left):** Shows the current status of your ship's critical systems: Radar, Computer, Engine, Life Support, and Targeting Computer. The health of each system is displayed as a percentage, and the color changes from green to yellow to red as damage is sustained.
*   **Score & High Score (Top Center):** Your current score and the high score.
*   **Date (Bottom Center):** The in-game date, which advances with actions like warping. Be mindful of the date, as some events may be time-sensitive.
*   **Key Count (Bottom Center):** Shows how many keys you have collected out of the required 7 in Adventure Mode.
*   **Radar (Bottom Center):** A circular radar display that shows the immediate vicinity around your ship.
    *   **Yellow Blip (Center):** Your ship.
    *   **Red Blips:** Enemy ships.
    *   The radar can be damaged, causing it to flicker, show less information, or fail completely.

### Damage and Repairs

Your ship has five critical systems that can be damaged by enemy fire or collisions with asteroids:

*   **Radar:** Damage to the radar will cause it to malfunction. At moderate damage, it may flicker or only show your position. At critical damage, it will be completely disabled.
*   **Computer:** A damaged computer will affect your ability to warp. At moderate damage, you will lose the ability to perform targeted warps. At critical damage, all warp functions will be disabled.
*   **Engine:** Engine damage will reduce your ship's speed and maneuverability. At critical damage, your ship will be unable to move.
*   **Life Support:** Damage to your life support system will cause your energy to drain at a faster rate.
*   **Targeting Computer:** A damaged targeting computer will reduce the accuracy of your weapons.

To repair your systems and replenish your energy and missiles, you must dock at a friendly **starbase** (indicated by a blue square on the galactic map).

### Sector Types

The galaxy is divided into different types of sectors, each with its own unique challenges:

*   **Empty Space:** The most common type of sector. No special effects.
*   **Nebula:** A dense cloud of gas and dust that will slow down your ship.
*   **Asteroid Field:** A dangerous sector filled with asteroids that will damage your ship if you collide with them.

### Enemies

You will encounter several types of enemy ships, each with its own behavior:

*   **Fighters:** Small, agile ships that attack in groups.
*   **Bombers:** Slower, more durable ships that target your starbases.
*   **Cruisers:** Large, powerful ships that are slow but heavily armed.
*   **Boss:** A massive, heavily armed ship that appears in Adventure Mode after you have collected all 7 keys.

## A Note on Inspiration

This game is a heartfelt tribute to the classic 1985 Namco game, "Star Luster." Many of the gameplay mechanics, the overall aesthetic, and the core design principles are directly inspired by this legendary title.

The recent updates, including the redesigned cockpit, the circular radar, the enhanced damage system, and the new enemy sprites, were all implemented to bring the game even closer to the original "Star Luster" experience. The goal is to capture the spirit and challenge of the original, while still providing a fun and engaging experience for modern players.

## Sound Generation

The game's sound effects are procedurally generated by `generate_sounds.py`. This script creates `.wav` files for various in-game actions (laser, missile, explosion, warp, game over, win) and places them in the `assets/sounds/` directory. You must run this script once after installation to ensure all sound assets are available.

## Credits

*   Developed by [Your Name/Team Name]
*   Inspired by classic space combat games.
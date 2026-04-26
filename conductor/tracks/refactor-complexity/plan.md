# Refactor for Simplicity and Readability

This track will focus on reducing code complexity, eliminating duplication, and improving the overall readability of the codebase. The primary target for refactoring is the `play` function in `main.py`, which currently has a cyclomatic complexity of 104.

## Plan

1.  **Deconstruct the `play` Function:** Break down the main game loop into smaller, more focused functions to improve readability and separation of concerns.
    -   `handle_input()`: Manages all user input and game events.
    -   `update_game_state()`: Handles all sprite updates and game logic.
    -   `handle_collisions()`: Manages all collision detection and resulting actions.
    -   `render_screen()`: Orchestrates all drawing and screen updates.

2.  **Abstract Collision Handling:** Create dedicated functions for each type of collision to reduce complexity and make the logic easier to follow.
    -   `handle_player_-to-environment_collisions()`: Manages collisions between the player and environmental hazards.
    -   `handle_asteroid-to-laser_collisions()`: Handles interactions between asteroids and lasers.
    -   `handle_boss_collisions()`: Centralizes all boss-related collision logic.

3.  **Create a Collision-Handler Module:** Move all collision-handling functions into a new `collisions.py` module to better organize the code and separate collision logic from the main game loop.

4.  **Update the Main Game Loop:** Refactor the `play` function to call the new, smaller functions in a clear and concise sequence, making the game's flow easy to understand.

5.  **Eliminate Ternary Operators and Inline Conditionals:** Replace ternary operators and inline conditional statements with standard `if-else` blocks to improve readability and make the code easier to debug.

6.  **Refactor `None` Checks:** Rework the logic to avoid checking for `None` where possible, especially in performance-critical parts of the game loop. This may involve restructuring how sprites and other game objects are accessed and managed.

7.  **Decompose Complex Functions:** Break down the `handle_asteroid_collisions`, `handle_boss_collisions`, and `Upgrade.update` functions into smaller, more focused functions to reduce their complexity and improve readability.

8.  **Apply Polymorphism:**
    -   Refactor the `Laser` class to use a polymorphic design. Create a base `Laser` class and subclasses for each laser type (e.g., `MainLaser`, `Bomb`, `Shrapnel`, `SinLaser`, `Ray`) to eliminate conditional logic based on `self.kind`.
    -   Refactor the `Upgrade` class to use a similar polymorphic approach, creating a base `Upgrade` class with subclasses for each upgrade type, each with its own `apply` method.

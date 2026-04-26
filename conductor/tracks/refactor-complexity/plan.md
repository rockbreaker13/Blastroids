# Refactor for Simplicity and Readability

This track will focus on reducing code complexity, eliminating duplication, and improving the overall readability of the codebase.

## Plan

1.  **Deconstruct the `play` Function:** Break down the main game loop into smaller, more focused functions.
2.  **Abstract Collision Handling:** Create dedicated functions for each type of collision.
3.  **Create a Collision-Handler Module:** Move all collision-handling functions into a new `collisions.py` module.
4.  **Update the Main Game Loop:** Refactor the `play` function to call the new, smaller functions.
5.  **Eliminate Ternary Operators and Inline Conditionals:** Replace complex inline conditionals with standard `if-else` blocks.
6.  **Refactor `None` Checks:** Rework logic to avoid checking for `None` where possible.
7.  **Decompose Complex Functions:** Break down the remaining complex functions (`handle_asteroid_collisions`, `handle_boss_collisions`, `Upgrade.update`) into smaller pieces.
8.  **Apply Polymorphism:**
    -   Refactor the `Laser` class to use subclasses for each laser type.
    -   Refactor the `Upgrade` class to use a polymorphic approach for applying upgrades.
9.  **Code Formatting and Linting:**
    -   Use `ruff` to format the codebase and fix linting issues like unused imports.
    -   Remove all "hello world" print statements.
10. **Project and Environment Management:**
    -   Migrate the project to be managed by Poetry.
    -   Configure the project to support the `src` layout.
    -   Convert all relative imports to absolute imports to improve maintainability and clarity.
    -   Add a console script entry point to run the game.

# Dialog System

## Mechanics

    - Dialog will pause normal gameplay
    - Dialog will scroll text per line. 
    - Pressing enter while text scrolls will complete the text.
    - Pressing enter after all text has scrolled will complete the dialog.

## Implementation

    Similar to a scene, I can do a dialog through a function that paints
    to the screen. The difference is:

    - Dialog only paints text
    - Dialog paints to a specific area of the screen
    - Dialog will need to manage multiple lines:
        - 6 lines per group of lines scrolling
            - :. chunking
        - 31 characters per line

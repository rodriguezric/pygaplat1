# First Edition

This is a platformer made with pygame.


## How to play
- Arrow keys to move and spacebar to jump.
- Press escape to pause the game if you're into that.
- Don't touch the red blocks, you'll die.
- Touch blue blocks to beat the level.


## Tech Notes and Opinions
- Scenes are defined in functions. 
- Scenes react to events and paint to the screen.
- Since function calls work as a stack, it's pretty easy to make a pause screen return to a previous screen (just return)
- I wrote a class for handling Text objects (surf + rect) I don't know if I care too much about this.
- I have movement logic in the Player class coupled with the pygame keys but the game scenes listen to K_SPACE event to trigger a jump on the player. I think this is gross
- My screen menu code is CP'd across multiple scene functions. Definitely should refactor.
- Yeah, this is pretty fun 

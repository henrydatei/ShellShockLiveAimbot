# ShellShockLiveAimbot

A simple Python script using [ilyaki's formula](https://steamcommunity.com/sharedfiles/filedetails/?id=1327582953) for finding the optimal power and angle for [ShellShock Live](https://store.steampowered.com/app/326460/ShellShock_Live/).

I've added 2 modi
- power and angle with lowest possible power
- power and angle with highest angle and power below 100

### Use
- Start the game via Steam and start the aimbot with `python3 shellshock.py`
- Focus the game window by clicking in it (select a game mode etc.)
- When you're in the game, press <kbd>CTRL</kbd> + <kbd>ALT</kbd> + <kbd>P</kbd> and click in the middle of your tank. You should see the ccordinates in the console window. If you have misclicked you can press <kbd>CTRL</kbd> + <kbd>ALT</kbd> + <kbd>P</kbd> again and select your tank. This will override the old coordinates.
- Same procedure for the enemy tank, press <kbd>CTRL</kbd> + <kbd>ALT</kbd> + <kbd>E</kbd> and click on it. Pressing <kbd>CTRL</kbd> + <kbd>ALT</kbd> + <kbd>E</kbd> again will override the old coordinates. You should see the ccordinates in the console window.
- If you have selected your and your enemy's tank, the script will calculate the required angle and power for the above described modi.
- You can set power and angle by hand or let the computer do the work for you: For the first modus press <kbd>CTRL</kbd> + <kbd>ALT</kbd> + <kbd>S</kbd> and for the sedond modus press <kbd>CTRL</kbd> + <kbd>ALT</kbd> + <kbd>H</kbd>
- Press <kbd>SPACE</kbd> to fire the projectile

### shellshock2.py
In `shellshock2.py` I've tried a bit around with automatic image processing to automatically find the tanks and also include wind calculation but I'm not finished yet. This is still WIP because the accuracy is sometimes really bad. If you have any suggestions on how to improve this please write a issue or create a PR. Thanks!

### Todo:
- [ ] wind calculation

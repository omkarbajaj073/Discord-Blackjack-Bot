# Discord-Blackjack-Bot


## Instructions to run
- Requirements - `pip install discord.py`.
- Clone this repository - `https://github.com/omkarbajaj073/Discord-Casino-Bot-School-Project.git`
- Create a bot on the <a href="https://discord.com/developers/applications">discord developers portal</a>.
- Create a `.env` file. Make an environment variable `TOKEN` for the bot token.
- Run the bot script `bot.py`.

## Bot Commands
- !bj <value>: Starts a new game with the player, putting the given amount on the stake. If no amount is entered the default stake amount is used (starts as 500 coins). If the player is playing for the first time, an account is created to store his/her balance (starts as 10,000 coins).
- !hit: Draw a card
- !stay: Dealer draws cards
- !double: Doubles the stake and deals one card. Then the dealer's hand is revealed.
- !split: You get two hands and play separately for each hand
- !continue: In case you do not want to split
- !surrender: Give up the match. Half the stake will be lost
- !help: To see rules and commands
- !balance: See your game balance
- !set <option> <value>: Set the default stake (!set stake <value>) or default starting balance (!set start-balance <value>)
- !view <option> : View the default stake (!view stake) or default starting balance (!view start-balance)
- !reset: Reset your account to the default starting balance
- Note - !reset is only valid if you have less than 100 coins
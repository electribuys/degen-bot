import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ------------------------------
# SAMPLE DIRECTIVES
# (Replace with your own full set if desired)
# ------------------------------
raw_sheet_directives = """
Directive #1: Break Actions - Go to the **casino’s ATM or cash-out area** and count your winnings or losses before continuing.	
Directive #2: Break Actions - Walk around the **casino floor for exactly 5 minutes** before placing your next bet. Switch to a nearby table and try a new strategy.	
Directive #3: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**. Try betting a completely new way—if you normally bet red, try black!	
Directive #4: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively. Double your bet for the next round, then walk away if you win.	
Directive #5: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**. Find a game with the fewest players and place your next bet there.	
Directive #6: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**. Find a game with the fewest players and place your next bet there.	
Directive #7: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #8: Break Actions - Take a **bathroom break** and wash your hands before returning to the tables. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #9: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**.	
Directive #10: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #11: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #12: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #14: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.	
Directive #15: Craps - Bet on the **field bet** only if **the last two rolls missed field numbers**.	
Directive #16: Craps - Locate a **cold craps table (quiet and losses happening)**. Bet **2 units on don't pass**.	
Directive #17: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**.	
Directive #18: Break Actions - Walk to the **VIP section and pretend to belong there** for 5 minutes before returning.	
Directive #19: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**. Try betting a completely new way—if you normally bet red, try black!	
Directive #20: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #21: Break Actions - Find a **TV screen showing live sports** and stand there for 10 minutes before playing again.	
Directive #22: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #23: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer. Find a game with the fewest players and place your next bet there.	
Directive #24: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card. Switch to a nearby table and try a new strategy.	
Directive #25: Slots - Locate an **Western-themed slot machine** and play **10 spins at minimum bet** before deciding to increase. Order a drink before making your next wager, and chat with the dealer.	
Directive #26: Break Actions - Go to the **nearest bartender** and ask them to **make you their best drink**.	
Directive #27: Break Actions - Take a **5-minute phone break** outside before going back inside to play. Find a game with the fewest players and place your next bet there.	
Directive #28: Craps - Bet **4 units on the pass line** if the **last shooter hit two points in a row**.	
Directive #29: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #30: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #31: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card. Find a game with the fewest players and place your next bet there.	
Directive #32: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**. Order a drink before making your next wager, and chat with the dealer.	
Directive #33: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #34: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.	
Directive #37: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.	
Directive #38: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**. Switch to a nearby table and try a new strategy.	
Directive #39: Break Actions - Grab a **complimentary coffee or tea** and sip it while standing near a lively table. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #40: Slots - Locate an **Water-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #41: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #42: Craps - Place a **come bet** only after the shooter **rolls at least one point**. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #43: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**.	
Directive #44: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.	
Directive #46: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #47: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer. Switch to a nearby table and try a new strategy.	
Directive #48: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**. Place a side bet if available, and observe how it changes your outcome.	
Directive #51: Break Actions - Stop and **watch a game you’ve never played before for 5 minutes**, then decide if you want to try it.	
Directive #52: Break Actions - Ask a **pit boss what table is the hottest**, then walk to it and observe before betting.	
Directive #53: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy.	
Directive #54: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #55: Slots - Locate an **Robot-themed slot machine** and play **10 spins at minimum bet** before deciding to increase. Switch to a nearby table and try a new strategy.	
Directive #57: Break Actions - Find a **casino promotional booth** and ask about any deals or giveaways.	
Directive #58: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #59: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand. Place a side bet if available, and observe how it changes your outcome.	
Directive #60: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #61: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #62: Slots - Locate an **Ghost-themed slot machine** and play **10 spins at minimum bet** before deciding to increase. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #63: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**. Order a drink before making your next wager, and chat with the dealer.	
Directive #65: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #66: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**. Try betting a completely new way—if you normally bet red, try black!	
Directive #69: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #70: Break Actions - Take a **5-minute phone break** outside before going back inside to play.	
Directive #72: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win.	
Directive #73: Craps - Look for a table where **the last roll was a 7**. Bet **small on pass line and increase if you win**.	
Directive #74: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #75: Break Actions - Walk around the **casino floor for exactly 5 minutes** before placing your next bet. Order a drink before making your next wager, and chat with the dealer.	
Directive #76: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #77: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**. Order a drink before making your next wager, and chat with the dealer.	
Directive #78: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #79: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.	
Directive #80: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**.	
Directive #81: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**. Order a drink before making your next wager, and chat with the dealer.	
Directive #83: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #84: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #85: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #87: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #91: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #93: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**. Try betting a completely new way—if you normally bet red, try black!	
Directive #94: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck. Find a game with the fewest players and place your next bet there.	
Directive #95: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #96: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #97: Break Actions - Take a **deep breath, relax, and count your cash** before placing your next bet.	
Directive #100: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**. Double your bet for the next round, then walk away if you win.	
Directive #103: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**. Find a game with the fewest players and place your next bet there.	
Directive #104: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.	
Directive #106: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins. Find a game with the fewest players and place your next bet there.	
Directive #107: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.	
Directive #108: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #109: Break Actions - Stand near a high-stakes table and **watch quietly for 10 minutes before continuing your own gambling**.	
Directive #110: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**. Find a game with the fewest players and place your next bet there.	
Directive #111: Break Actions - Take a **10-minute break and scroll through social media** before playing again.	
Directive #112: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #113: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #114: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #115: Craps - Bet **4 units on the pass line** if the **last shooter hit two points in a row**. Try betting a completely new way—if you normally bet red, try black!	
Directive #116: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #117: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.	
Directive #118: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #119: Break Actions - Walk to the **casino floor's self-serve drink station** and grab a **free soda**. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #120: Slots - Locate an **Sports-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #121: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #122: Craps - Place a **come bet** only after the shooter **rolls at least one point**.	
Directive #123: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #124: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.	
Directive #125: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.	
Directive #130: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing.	
Directive #131: Craps - Place a **come bet** only after the shooter **rolls at least one point**.	
Directive #132: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #133: Break Actions - Grab a **complimentary coffee or tea** and sip it while standing near a lively table. Switch to a nearby table and try a new strategy.	
Directive #134: Craps - Find a **table with a new shooter** and bet **the table minimum on pass line first, then adjust strategy**.	
Directive #135: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck. Try betting a completely new way—if you normally bet red, try black!	
Directive #136: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #137: Break Actions - Find a **bar and order a random drink** from the menu without looking. Find a game with the fewest players and place your next bet there.	
Directive #139: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #140: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #144: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #145: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak. Place a side bet if available, and observe how it changes your outcome.	
Directive #146: Slots - Locate an **Alien-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #147: Break Actions - Find a **bar and order a random drink** from the menu without looking.	
Directive #148: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**. Place a side bet if available, and observe how it changes your outcome.	
Directive #149: Craps - If you see a player **pressing their bets aggressively**, match their come bet for one roll.	
Directive #153: Slots - Locate an **Asian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #154: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.	
Directive #155: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #157: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**. Switch to a nearby table and try a new strategy.	
Directive #158: Break Actions - Take a **casual walk through the high-roller section** without placing a bet. Place a side bet if available, and observe how it changes your outcome.	
Directive #160: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #161: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #162: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.	
Directive #163: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**. Place a side bet if available, and observe how it changes your outcome.	
Directive #165: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #167: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #168: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #169: Break Actions - Find the **nearest bar** and order a **local beer**. Sip it slowly while watching a game.	
Directive #170: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #173: Break Actions - Take a **quick walk to the nearest drinking fountain** and take a sip before returning.	
Directive #174: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #175: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #176: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #177: Break Actions - Go to the **casino's sports bar** and **watch a game for 10 minutes before returning**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #178: Craps - If you see a player **pressing their bets aggressively**, match their come bet for one roll. Switch to a nearby table and try a new strategy.	
Directive #179: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #180: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**. Switch to a nearby table and try a new strategy.	
Directive #182: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #183: Break Actions - Walk to the **casino floor's self-serve drink station** and grab a **free soda**. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #185: Break Actions - Walk to the **closest cocktail waitress** and order a **free casino drink**.	
Directive #186: Break Actions - Find a **casino promotional booth** and ask about any deals or giveaways. Double your bet for the next round, then walk away if you win.	
Directive #188: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18. Double your bet for the next round, then walk away if you win.	
Directive #193: Break Actions - Take a **bathroom break** and wash your hands before returning to the tables.	
Directive #194: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**. Double your bet for the next round, then walk away if you win.	
Directive #197: Slots - Locate an **Mythology-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #198: Break Actions - Take a **casual walk through the high-roller section** without placing a bet.	
Directive #200: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**. Switch to a nearby table and try a new strategy.	
Directive #202: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #204: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #207: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #209: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #210: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #212: Break Actions - Go to the **casino's sports bar** and **watch a game for 10 minutes before returning**.	
Directive #213: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #214: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #215: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #216: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively. Find a game with the fewest players and place your next bet there.	
Directive #217: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #218: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #221: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what. Switch to a nearby table and try a new strategy.	
Directive #224: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #225: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #226: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #229: Break Actions - Find a **slot machine near a bar** and **sit there with a drink without playing**. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #230: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #231: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #233: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #237: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**. Order a drink before making your next wager, and chat with the dealer.	
Directive #238: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #240: Break Actions - Stop and **watch a game you’ve never played before for 5 minutes**, then decide if you want to try it. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #242: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18. Place a side bet if available, and observe how it changes your outcome.	
Directive #243: Slots - Locate an **Jungle-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #244: Slots - Locate an **Dragon-themed slot machine** and play **10 spins at minimum bet** before deciding to increase. Find a game with the fewest players and place your next bet there.	
Directive #245: Break Actions - Find a **casino promotional booth** and ask about any deals or giveaways. Try betting a completely new way—if you normally bet red, try black!	
Directive #246: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #248: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**. Place a side bet if available, and observe how it changes your outcome.	
Directive #250: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #251: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #252: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #253: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #254: Break Actions - Find a **TV screen showing live sports** and stand there for 10 minutes before playing again. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #255: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #256: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak. Order a drink before making your next wager, and chat with the dealer.	
Directive #257: Break Actions - Walk to the **nearest food stand and grab a snack** before returning.	
Directive #259: Craps - Locate a **cold craps table (quiet and losses happening)**. Bet **2 units on don't pass**. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #260: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**. Order a drink before making your next wager, and chat with the dealer.	
Directive #261: Break Actions - Walk to the **nearest bar** and order a **shot of tequila**. Take it immediately.	
Directive #264: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #265: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #268: Break Actions - Find a **comfortable chair in the lounge** and **sit for 10 minutes** before playing again. Try betting a completely new way—if you normally bet red, try black!	
Directive #271: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**. Double your bet for the next round, then walk away if you win.	
Directive #272: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #273: Slots - Locate an **Mythology-themed slot machine** and play **10 spins at minimum bet** before deciding to increase. Double your bet for the next round, then walk away if you win.	
Directive #274: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #276: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what. Place a side bet if available, and observe how it changes your outcome.	
Directive #280: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #283: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**. Place a side bet if available, and observe how it changes your outcome.	
Directive #284: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #286: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #287: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #288: Break Actions - Stand near a high-stakes table and **watch quietly for 10 minutes before continuing your own gambling**. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #290: Slots - Locate an **Cartoon-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #295: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #296: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**. Try betting a completely new way—if you normally bet red, try black!	
Directive #297: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #300: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #301: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win. Try betting a completely new way—if you normally bet red, try black!	
Directive #302: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #303: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins. Double your bet for the next round, then walk away if you win.	
Directive #304: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #305: Break Actions - Find the **nearest bar** and order a **local beer**. Sip it slowly while watching a game. Order a drink before making your next wager, and chat with the dealer.	
Directive #306: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #307: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #310: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #311: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**. Switch to a nearby table and try a new strategy.	
Directive #312: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #313: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #316: Craps - Find a **hot craps table (lots of cheering)** and bet **3 units on the pass line**.	
Directive #318: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #321: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #322: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #325: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #326: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #327: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #328: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #329: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #331: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #332: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand. Switch to a nearby table and try a new strategy.	
Directive #333: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #334: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #337: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #338: Break Actions - Find the **nearest bar** and order a **local beer**. Sip it slowly while watching a game. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #339: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.	
Directive #340: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #341: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #344: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #345: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #347: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**. Place a side bet if available, and observe how it changes your outcome.	
Directive #348: Slots - Locate an **Space-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #350: Craps - Place a **come bet** only after the shooter **rolls at least one point**.	
Directive #351: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #352: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #353: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #354: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #356: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #360: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #361: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #362: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**. Double your bet for the next round, then walk away if you win.	
Directive #364: Craps - Place a **come bet** only after the shooter **rolls at least one point**.	
Directive #365: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**. Double your bet for the next round, then walk away if you win.	
Directive #368: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #369: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #371: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #372: Break Actions - Take a **5-minute phone break** outside before going back inside to play. Place a side bet if available, and observe how it changes your outcome.	
Directive #377: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #378: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #379: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #380: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.	
Directive #381: Slots - Locate an **Cartoon-themed slot machine** and play **10 spins at minimum bet** before deciding to increase. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #382: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #383: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #384: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #386: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #388: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing. Try betting a completely new way—if you normally bet red, try black!	
Directive #391: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #394: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #395: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.	
Directive #396: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #398: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #400: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy. Double your bet for the next round, then walk away if you win.	
Directive #401: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #402: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #403: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #404: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #406: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins. Order a drink before making your next wager, and chat with the dealer.	
Directive #407: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #408: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card. Order a drink before making your next wager, and chat with the dealer.	
Directive #410: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #411: Break Actions - Walk to the **nearest bar** and order a **shot of tequila**. Take it immediately. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #414: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #420: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.	
Directive #421: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #422: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**. Try betting a completely new way—if you normally bet red, try black!	
Directive #423: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #424: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #425: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #426: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer. Try betting a completely new way—if you normally bet red, try black!	
Directive #427: Break Actions - Walk to the **casino floor's self-serve drink station** and grab a **free soda**.	
Directive #429: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #434: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #436: Craps - Find a **hot craps table (lots of cheering)** and bet **3 units on the pass line**. Try betting a completely new way—if you normally bet red, try black!	
Directive #440: Craps - Locate a **cold craps table (quiet and losses happening)**. Bet **2 units on don't pass**. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #441: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #442: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #444: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #445: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #446: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**. Order a drink before making your next wager, and chat with the dealer.	
Directive #447: Break Actions - Find a **slot machine near a bar** and **sit there with a drink without playing**. Double your bet for the next round, then walk away if you win.	
Directive #448: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #449: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.	
Directive #450: Slots - Locate an **Vampire-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #451: Break Actions - Go to the **casino's sports bar** and **watch a game for 10 minutes before returning**. Try betting a completely new way—if you normally bet red, try black!	
Directive #452: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #453: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #457: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #460: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #461: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck. Double your bet for the next round, then walk away if you win.	
Directive #462: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins. Try betting a completely new way—if you normally bet red, try black!	
Directive #463: Break Actions - Find a **casino promotional booth** and ask about any deals or giveaways. Order a drink before making your next wager, and chat with the dealer.	
Directive #465: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #466: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #467: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #472: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #474: Craps - Place a **come bet** only after the shooter **rolls at least one point**.	
Directive #475: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #476: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #478: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #481: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #482: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #484: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.	
Directive #486: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**. Try betting a completely new way—if you normally bet red, try black!	
Directive #487: Break Actions - Find a **casino lounge** and **sit for 15 minutes** while sipping a drink.	
Directive #489: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #490: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #492: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #493: Break Actions - Find a **slot machine near a bar** and **sit there with a drink without playing**. Try betting a completely new way—if you normally bet red, try black!	
Directive #495: Craps - Bet **4 units on the pass line** if the **last shooter hit two points in a row**. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #497: Craps - Bet on the **field bet** only if **the last two rolls missed field numbers**. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #498: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #499: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #500: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #502: Break Actions - Find a **bar and order a random drink** from the menu without looking. Double your bet for the next round, then walk away if you win.	
Directive #503: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #504: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #506: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #507: Break Actions - Walk to the **bar closest to the high-limit area** and order an **Old Fashioned**. Find a game with the fewest players and place your next bet there.	
Directive #510: Break Actions - Walk to the **casino floor's self-serve drink station** and grab a **free soda**. Order a drink before making your next wager, and chat with the dealer.	
Directive #512: Break Actions - Take a **quick walk to the nearest drinking fountain** and take a sip before returning. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #514: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #519: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #520: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #521: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #522: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively. Order a drink before making your next wager, and chat with the dealer.	
Directive #525: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #526: Break Actions - Find a **casino promotional booth** and ask about any deals or giveaways. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #528: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #530: Break Actions - Find a **bar and order a random drink** from the menu without looking. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #531: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**. Switch to a nearby table and try a new strategy.	
Directive #532: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #533: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #534: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #537: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #539: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #544: Break Actions - Take a **bathroom break** and wash your hands before returning to the tables. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #545: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #548: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #553: Craps - Find a **table with a new shooter** and bet **the table minimum on pass line first, then adjust strategy**. Order a drink before making your next wager, and chat with the dealer.	
Directive #554: Break Actions - Go to the **casino's sports bar** and **watch a game for 10 minutes before returning**. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #555: Break Actions - Walk to the **VIP section and pretend to belong there** for 5 minutes before returning. Place a side bet if available, and observe how it changes your outcome.	
Directive #556: Break Actions - Find a **comfortable chair in the lounge** and **sit for 10 minutes** before playing again.	
Directive #558: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #559: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**. Place a side bet if available, and observe how it changes your outcome.	
Directive #560: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #565: Break Actions - Walk to the **closest cocktail waitress** and order a **free casino drink**. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #568: Craps - Place a **come bet** only after the shooter **rolls at least one point**.	
Directive #570: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #571: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #572: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #574: Break Actions - Head to the **casino gift shop** and buy something under $10 before going back to play.	
Directive #577: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**. Place a side bet if available, and observe how it changes your outcome.	
Directive #578: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #579: Break Actions - Walk around the **casino floor for exactly 5 minutes** before placing your next bet.	
Directive #580: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #582: Break Actions - Take a **quick walk to the nearest drinking fountain** and take a sip before returning. Double your bet for the next round, then walk away if you win.	
Directive #583: Break Actions - Stand near a high-stakes table and **watch quietly for 10 minutes before continuing your own gambling**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #585: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #586: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd. Find a game with the fewest players and place your next bet there.	
Directive #587: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer. Place a side bet if available, and observe how it changes your outcome.	
Directive #593: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #596: Break Actions - Walk to the **bar closest to the high-limit area** and order an **Old Fashioned**.	
Directive #597: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #599: Craps - Locate a **cold craps table (quiet and losses happening)**. Bet **2 units on don't pass**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #601: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #603: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #607: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #609: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #611: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #614: Break Actions - Walk around the **casino floor for exactly 5 minutes** before placing your next bet. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #615: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**. Order a drink before making your next wager, and chat with the dealer.	
Directive #616: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.	
Directive #619: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #621: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #622: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #623: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #626: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #627: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #628: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #631: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**. Find a game with the fewest players and place your next bet there.	
Directive #634: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #635: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #639: Break Actions - Walk to the **bar closest to the high-limit area** and order an **Old Fashioned**. Switch to a nearby table and try a new strategy.	
Directive #641: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #643: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #646: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #647: Slots - Locate an **Vampire-themed slot machine** and play **10 spins at minimum bet** before deciding to increase. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #648: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #649: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #650: Break Actions - Walk to the **casino floor's self-serve drink station** and grab a **free soda**. Place a side bet if available, and observe how it changes your outcome.	
Directive #655: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #660: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #662: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #668: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.	
Directive #670: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #672: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #676: Craps - Bet on the **field bet** only if **the last two rolls missed field numbers**. Switch to a nearby table and try a new strategy.	
Directive #677: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #679: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #687: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #688: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #690: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**. Try betting a completely new way—if you normally bet red, try black!	
Directive #691: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #692: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak. Switch to a nearby table and try a new strategy.	
Directive #693: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.	
Directive #695: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**. Try betting a completely new way—if you normally bet red, try black!	
Directive #697: Break Actions - Take a **casual walk through the high-roller section** without placing a bet. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #700: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand. Double your bet for the next round, then walk away if you win.	
Directive #702: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #706: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #707: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #708: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #711: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #713: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #715: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #716: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**. Find a game with the fewest players and place your next bet there.	
Directive #717: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #720: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #721: Slots - Locate an **Treasure-themed slot machine** and play **10 spins at minimum bet** before deciding to increase. Double your bet for the next round, then walk away if you win.	
Directive #724: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #725: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #727: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #728: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #730: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #732: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #734: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #735: Break Actions - Take a **10-minute break and scroll through social media** before playing again. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #737: Break Actions - Find a **slot machine near a bar** and **sit there with a drink without playing**.	
Directive #739: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #740: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #741: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.	
Directive #742: Break Actions - Take a **5-minute phone break** outside before going back inside to play. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #747: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.	
Directive #750: Break Actions - Find a **casino lounge** and **sit for 15 minutes** while sipping a drink. Find a game with the fewest players and place your next bet there.	
Directive #751: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #754: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #757: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #760: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #761: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.	
Directive #762: Craps - Look for a table where **the last roll was a 7**. Bet **small on pass line and increase if you win**. Double your bet for the next round, then walk away if you win.	
Directive #763: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #764: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #766: Break Actions - Walk around the **casino floor for exactly 5 minutes** before placing your next bet. Find a game with the fewest players and place your next bet there.	
Directive #771: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #773: Break Actions - Find a **comfortable chair in the lounge** and **sit for 10 minutes** before playing again. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #775: Slots - Locate an **Ice-themed slot machine** and play **10 spins at minimum bet** before deciding to increase. Find a game with the fewest players and place your next bet there.	
Directive #776: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #777: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #779: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #780: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #782: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #784: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #785: Break Actions - Walk to the **bar closest to the high-limit area** and order an **Old Fashioned**. Order a drink before making your next wager, and chat with the dealer.	
Directive #786: Break Actions - Go to the **nearest bartender** and ask them to **make you their best drink**. Find a game with the fewest players and place your next bet there.	
Directive #787: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #791: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #792: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #794: Break Actions - Walk to the **nearest bar** and order a **shot of tequila**. Take it immediately. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #795: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #796: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #797: Break Actions - Find the **nearest bar** and order a **local beer**. Sip it slowly while watching a game. Double your bet for the next round, then walk away if you win.	
Directive #798: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #800: Slots - Locate an **Alien-themed slot machine** and play **10 spins at minimum bet** before deciding to increase. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #804: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #805: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #809: Craps - Look for a table where **the last roll was a 7**. Bet **small on pass line and increase if you win**. Order a drink before making your next wager, and chat with the dealer.	
Directive #810: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #814: Craps - Bet **4 units on the pass line** if the **last shooter hit two points in a row**. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #817: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**. Find a game with the fewest players and place your next bet there.	
Directive #820: Slots - Locate an **Dinosaur-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #821: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**. Double your bet for the next round, then walk away if you win.	
Directive #822: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #823: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #824: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #826: Break Actions - Find a **casino promotional booth** and ask about any deals or giveaways. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #828: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #829: Break Actions - Walk to the **bar closest to the high-limit area** and order an **Old Fashioned**. Double your bet for the next round, then walk away if you win.	
Directive #830: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #833: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**. Switch to a nearby table and try a new strategy.	
Directive #835: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #837: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #838: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #839: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #841: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #842: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #843: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak. Try betting a completely new way—if you normally bet red, try black!	
Directive #844: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #846: Break Actions - Walk around the **casino floor for exactly 5 minutes** before placing your next bet.	
Directive #847: Craps - Place a **come bet** only after the shooter **rolls at least one point**.	
Directive #848: Break Actions - Find the **nearest bar** and order a **local beer**. Sip it slowly while watching a game. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #851: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #852: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #854: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #856: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #857: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #859: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #865: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #866: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #867: Slots - Locate an **Cyberpunk-themed slot machine** and play **10 spins at minimum bet** before deciding to increase. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #868: Slots - Locate an **Steampunk-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #869: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #871: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll. Double your bet for the next round, then walk away if you win.	
Directive #872: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #873: Break Actions - Take a **10-minute break and scroll through social media** before playing again. Double your bet for the next round, then walk away if you win.	
Directive #875: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #876: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins. Switch to a nearby table and try a new strategy.	
Directive #880: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #881: Break Actions - Take a **deep breath, relax, and count your cash** before placing your next bet. Find a game with the fewest players and place your next bet there.	
Directive #882: Break Actions - Take a **casual walk through the high-roller section** without placing a bet. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #886: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**. Place a side bet if available, and observe how it changes your outcome.	
Directive #890: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**. Switch to a nearby table and try a new strategy.	
Directive #893: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #895: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #896: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #898: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #899: Break Actions - Take a **10-minute break and scroll through social media** before playing again. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #901: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #905: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #908: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #910: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #911: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #914: Break Actions - Take a **bathroom break** and wash your hands before returning to the tables. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #916: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**. Switch to a nearby table and try a new strategy.	
Directive #918: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #921: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**. Double your bet for the next round, then walk away if you win.	
Directive #922: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #924: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #925: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #926: Slots - Locate an **Ice-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #927: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #928: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #929: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #931: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd. Switch to a nearby table and try a new strategy.	
Directive #939: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #944: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #945: Break Actions - Take a **deep breath, relax, and count your cash** before placing your next bet. Try betting a completely new way—if you normally bet red, try black!	
Directive #946: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #947: Break Actions - Walk around the **casino floor for exactly 5 minutes** before placing your next bet.	
Directive #950: Break Actions - Find a **slot machine near a bar** and **sit there with a drink without playing**. Find a game with the fewest players and place your next bet there.	
Directive #951: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #952: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #954: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18. Order a drink before making your next wager, and chat with the dealer.	
Directive #956: Break Actions - Find a **slot machine near a bar** and **sit there with a drink without playing**. Order a drink before making your next wager, and chat with the dealer.	
Directive #960: Break Actions - Stop and **watch a game you’ve never played before for 5 minutes**, then decide if you want to try it. Double your bet for the next round, then walk away if you win.	
Directive #963: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #964: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #967: Break Actions - Find a **TV screen showing live sports** and stand there for 10 minutes before playing again. Switch to a nearby table and try a new strategy.	
Directive #969: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**. Order a drink before making your next wager, and chat with the dealer.	
Directive #973: Break Actions - Go to the **nearest bartender** and ask them to **make you their best drink**. Switch to a nearby table and try a new strategy.	
Directive #974: Craps - Place a **come bet** only after the shooter **rolls at least one point**.	
Directive #976: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #978: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #979: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #983: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #985: Break Actions - Take a **10-minute break and scroll through social media** before playing again. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #986: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively. Place a side bet if available, and observe how it changes your outcome.	
Directive #987: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #989: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #990: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #993: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #994: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.	
Directive #995: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll. Find a game with the fewest players and place your next bet there.	
Directive #997: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #998: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #999: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #1000: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Gambling Directives	
Directive #1: Break Actions - Go to the **casino’s ATM or cash-out area** and count your winnings or losses before continuing.	
Directive #2: Break Actions - Walk around the **casino floor for exactly 5 minutes** before placing your next bet. Switch to a nearby table and try a new strategy.	
Directive #3: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**. Try betting a completely new way—if you normally bet red, try black!	
Directive #4: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively. Double your bet for the next round, then walk away if you win.	
Directive #5: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**. Find a game with the fewest players and place your next bet there.	
Directive #6: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**. Find a game with the fewest players and place your next bet there.	
Directive #7: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #8: Break Actions - Take a **bathroom break** and wash your hands before returning to the tables. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #9: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**.	
Directive #10: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #11: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #12: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #14: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.	
Directive #15: Craps - Bet on the **field bet** only if **the last two rolls missed field numbers**.	
Directive #16: Craps - Locate a **cold craps table (quiet and losses happening)**. Bet **2 units on don't pass**.	
Directive #17: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**.	
Directive #18: Break Actions - Walk to the **VIP section and pretend to belong there** for 5 minutes before returning.	
Directive #19: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**. Try betting a completely new way—if you normally bet red, try black!	
Directive #20: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #21: Break Actions - Find a **TV screen showing live sports** and stand there for 10 minutes before playing again.	
Directive #22: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #23: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer. Find a game with the fewest players and place your next bet there.	
Directive #24: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card. Switch to a nearby table and try a new strategy.	
Directive #25: Slots - Locate an **Western-themed slot machine** and play **10 spins at minimum bet** before deciding to increase. Order a drink before making your next wager, and chat with the dealer.	
Directive #26: Break Actions - Go to the **nearest bartender** and ask them to **make you their best drink**.	
Directive #27: Break Actions - Take a **5-minute phone break** outside before going back inside to play. Find a game with the fewest players and place your next bet there.	
Directive #28: Craps - Bet **4 units on the pass line** if the **last shooter hit two points in a row**.	
Directive #29: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #30: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #31: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card. Find a game with the fewest players and place your next bet there.	
Directive #32: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**. Order a drink before making your next wager, and chat with the dealer.	
Directive #33: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #34: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.	
Directive #37: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.	
Directive #38: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**. Switch to a nearby table and try a new strategy.	
Directive #39: Break Actions - Grab a **complimentary coffee or tea** and sip it while standing near a lively table. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #40: Slots - Locate an **Water-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #41: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #42: Craps - Place a **come bet** only after the shooter **rolls at least one point**. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #43: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**.	
Directive #44: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.	
Directive #46: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #47: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer. Switch to a nearby table and try a new strategy.	
Directive #48: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**. Place a side bet if available, and observe how it changes your outcome.	
Directive #51: Break Actions - Stop and **watch a game you’ve never played before for 5 minutes**, then decide if you want to try it.	
Directive #52: Break Actions - Ask a **pit boss what table is the hottest**, then walk to it and observe before betting.	
Directive #53: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy.	
Directive #54: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #55: Slots - Locate an **Robot-themed slot machine** and play **10 spins at minimum bet** before deciding to increase. Switch to a nearby table and try a new strategy.	
Directive #57: Break Actions - Find a **casino promotional booth** and ask about any deals or giveaways.	
Directive #58: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #59: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand. Place a side bet if available, and observe how it changes your outcome.	
Directive #60: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #61: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #62: Slots - Locate an **Ghost-themed slot machine** and play **10 spins at minimum bet** before deciding to increase. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #63: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**. Order a drink before making your next wager, and chat with the dealer.	
Directive #65: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #66: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**. Try betting a completely new way—if you normally bet red, try black!	
Directive #69: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #70: Break Actions - Take a **5-minute phone break** outside before going back inside to play.	
Directive #72: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win.	
Directive #73: Craps - Look for a table where **the last roll was a 7**. Bet **small on pass line and increase if you win**.	
Directive #74: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #75: Break Actions - Walk around the **casino floor for exactly 5 minutes** before placing your next bet. Order a drink before making your next wager, and chat with the dealer.	
Directive #76: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #77: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**. Order a drink before making your next wager, and chat with the dealer.	
Directive #78: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #79: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.	
Directive #80: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**.	
Directive #81: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**. Order a drink before making your next wager, and chat with the dealer.	
Directive #83: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #84: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #85: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #87: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #91: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #93: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**. Try betting a completely new way—if you normally bet red, try black!	
Directive #94: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck. Find a game with the fewest players and place your next bet there.	
Directive #95: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #96: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #97: Break Actions - Take a **deep breath, relax, and count your cash** before placing your next bet.	
Directive #100: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**. Double your bet for the next round, then walk away if you win.	
Directive #103: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**. Find a game with the fewest players and place your next bet there.	
Directive #104: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.	
Directive #106: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins. Find a game with the fewest players and place your next bet there.	
Directive #107: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.	
Directive #108: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #109: Break Actions - Stand near a high-stakes table and **watch quietly for 10 minutes before continuing your own gambling**.	
Directive #110: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**. Find a game with the fewest players and place your next bet there.	
Directive #111: Break Actions - Take a **10-minute break and scroll through social media** before playing again.	
Directive #112: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #113: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #114: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #115: Craps - Bet **4 units on the pass line** if the **last shooter hit two points in a row**. Try betting a completely new way—if you normally bet red, try black!	
Directive #116: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #117: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.	
Directive #118: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #119: Break Actions - Walk to the **casino floor's self-serve drink station** and grab a **free soda**. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #120: Slots - Locate an **Sports-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #121: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #122: Craps - Place a **come bet** only after the shooter **rolls at least one point**.	
Directive #123: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #124: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.	
Directive #125: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.	
Directive #130: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing.	
Directive #131: Craps - Place a **come bet** only after the shooter **rolls at least one point**.	
Directive #132: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #133: Break Actions - Grab a **complimentary coffee or tea** and sip it while standing near a lively table. Switch to a nearby table and try a new strategy.	
Directive #134: Craps - Find a **table with a new shooter** and bet **the table minimum on pass line first, then adjust strategy**.	
Directive #135: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck. Try betting a completely new way—if you normally bet red, try black!	
Directive #136: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #137: Break Actions - Find a **bar and order a random drink** from the menu without looking. Find a game with the fewest players and place your next bet there.	
Directive #139: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #140: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #144: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #145: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak. Place a side bet if available, and observe how it changes your outcome.	
Directive #146: Slots - Locate an **Alien-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #147: Break Actions - Find a **bar and order a random drink** from the menu without looking.	
Directive #148: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**. Place a side bet if available, and observe how it changes your outcome.	
Directive #149: Craps - If you see a player **pressing their bets aggressively**, match their come bet for one roll.	
Directive #153: Slots - Locate an **Asian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #154: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.	
Directive #155: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #157: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**. Switch to a nearby table and try a new strategy.	
Directive #158: Break Actions - Take a **casual walk through the high-roller section** without placing a bet. Place a side bet if available, and observe how it changes your outcome.	
Directive #160: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #161: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #162: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.	
Directive #163: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**. Place a side bet if available, and observe how it changes your outcome.	
Directive #165: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #167: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #168: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #169: Break Actions - Find the **nearest bar** and order a **local beer**. Sip it slowly while watching a game.	
Directive #170: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #173: Break Actions - Take a **quick walk to the nearest drinking fountain** and take a sip before returning.	
Directive #174: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #175: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #176: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #177: Break Actions - Go to the **casino's sports bar** and **watch a game for 10 minutes before returning**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #178: Craps - If you see a player **pressing their bets aggressively**, match their come bet for one roll. Switch to a nearby table and try a new strategy.	
Directive #179: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #180: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**. Switch to a nearby table and try a new strategy.	
Directive #182: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #183: Break Actions - Walk to the **casino floor's self-serve drink station** and grab a **free soda**. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #185: Break Actions - Walk to the **closest cocktail waitress** and order a **free casino drink**.	
Directive #186: Break Actions - Find a **casino promotional booth** and ask about any deals or giveaways. Double your bet for the next round, then walk away if you win.	
Directive #188: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18. Double your bet for the next round, then walk away if you win.	
Directive #193: Break Actions - Take a **bathroom break** and wash your hands before returning to the tables.	
Directive #194: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**. Double your bet for the next round, then walk away if you win.	
Directive #197: Slots - Locate an **Mythology-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #198: Break Actions - Take a **casual walk through the high-roller section** without placing a bet.	
Directive #200: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**. Switch to a nearby table and try a new strategy.	
Directive #202: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #204: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #207: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #209: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #210: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #212: Break Actions - Go to the **casino's sports bar** and **watch a game for 10 minutes before returning**.	
Directive #213: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #214: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #215: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #216: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively. Find a game with the fewest players and place your next bet there.	
Directive #217: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #218: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #221: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what. Switch to a nearby table and try a new strategy.	
Directive #224: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #225: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #226: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #229: Break Actions - Find a **slot machine near a bar** and **sit there with a drink without playing**. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #230: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #231: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #233: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #237: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**. Order a drink before making your next wager, and chat with the dealer.	
Directive #238: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #240: Break Actions - Stop and **watch a game you’ve never played before for 5 minutes**, then decide if you want to try it. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #242: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18. Place a side bet if available, and observe how it changes your outcome.	
Directive #243: Slots - Locate an **Jungle-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #244: Slots - Locate an **Dragon-themed slot machine** and play **10 spins at minimum bet** before deciding to increase. Find a game with the fewest players and place your next bet there.	
Directive #245: Break Actions - Find a **casino promotional booth** and ask about any deals or giveaways. Try betting a completely new way—if you normally bet red, try black!	
Directive #246: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #248: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**. Place a side bet if available, and observe how it changes your outcome.	
Directive #250: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #251: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #252: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #253: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #254: Break Actions - Find a **TV screen showing live sports** and stand there for 10 minutes before playing again. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #255: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #256: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak. Order a drink before making your next wager, and chat with the dealer.	
Directive #257: Break Actions - Walk to the **nearest food stand and grab a snack** before returning.	
Directive #259: Craps - Locate a **cold craps table (quiet and losses happening)**. Bet **2 units on don't pass**. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #260: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**. Order a drink before making your next wager, and chat with the dealer.	
Directive #261: Break Actions - Walk to the **nearest bar** and order a **shot of tequila**. Take it immediately.	
Directive #264: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #265: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #268: Break Actions - Find a **comfortable chair in the lounge** and **sit for 10 minutes** before playing again. Try betting a completely new way—if you normally bet red, try black!	
Directive #271: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**. Double your bet for the next round, then walk away if you win.	
Directive #272: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #273: Slots - Locate an **Mythology-themed slot machine** and play **10 spins at minimum bet** before deciding to increase. Double your bet for the next round, then walk away if you win.	
Directive #274: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #276: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what. Place a side bet if available, and observe how it changes your outcome.	
Directive #280: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #283: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**. Place a side bet if available, and observe how it changes your outcome.	
Directive #284: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #286: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #287: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #288: Break Actions - Stand near a high-stakes table and **watch quietly for 10 minutes before continuing your own gambling**. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #290: Slots - Locate an **Cartoon-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #295: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #296: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**. Try betting a completely new way—if you normally bet red, try black!	
Directive #297: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #300: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #301: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win. Try betting a completely new way—if you normally bet red, try black!	
Directive #302: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #303: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins. Double your bet for the next round, then walk away if you win.	
Directive #304: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #305: Break Actions - Find the **nearest bar** and order a **local beer**. Sip it slowly while watching a game. Order a drink before making your next wager, and chat with the dealer.	
Directive #306: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #307: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #310: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #311: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**. Switch to a nearby table and try a new strategy.	
Directive #312: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #313: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #316: Craps - Find a **hot craps table (lots of cheering)** and bet **3 units on the pass line**.	
Directive #318: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #321: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #322: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #325: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #326: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #327: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #328: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #329: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #331: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #332: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand. Switch to a nearby table and try a new strategy.	
Directive #333: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #334: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #337: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #338: Break Actions - Find the **nearest bar** and order a **local beer**. Sip it slowly while watching a game. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #339: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.	
Directive #340: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #341: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #344: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #345: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #347: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**. Place a side bet if available, and observe how it changes your outcome.	
Directive #348: Slots - Locate an **Space-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #350: Craps - Place a **come bet** only after the shooter **rolls at least one point**.	
Directive #351: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #352: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #353: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #354: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #356: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #360: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #361: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #362: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**. Double your bet for the next round, then walk away if you win.	
Directive #364: Craps - Place a **come bet** only after the shooter **rolls at least one point**.	
Directive #365: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**. Double your bet for the next round, then walk away if you win.	
Directive #368: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #369: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #371: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #372: Break Actions - Take a **5-minute phone break** outside before going back inside to play. Place a side bet if available, and observe how it changes your outcome.	
Directive #377: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #378: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #379: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #380: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.	
Directive #381: Slots - Locate an **Cartoon-themed slot machine** and play **10 spins at minimum bet** before deciding to increase. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #382: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #383: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #384: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #386: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #388: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing. Try betting a completely new way—if you normally bet red, try black!	
Directive #391: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #394: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #395: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.	
Directive #396: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #398: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #400: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy. Double your bet for the next round, then walk away if you win.	
Directive #401: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #402: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #403: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #404: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #406: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins. Order a drink before making your next wager, and chat with the dealer.	
Directive #407: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #408: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card. Order a drink before making your next wager, and chat with the dealer.	
Directive #410: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #411: Break Actions - Walk to the **nearest bar** and order a **shot of tequila**. Take it immediately. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #414: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #420: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.	
Directive #421: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #422: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**. Try betting a completely new way—if you normally bet red, try black!	
Directive #423: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #424: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #425: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #426: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer. Try betting a completely new way—if you normally bet red, try black!	
Directive #427: Break Actions - Walk to the **casino floor's self-serve drink station** and grab a **free soda**.	
Directive #429: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #434: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #436: Craps - Find a **hot craps table (lots of cheering)** and bet **3 units on the pass line**. Try betting a completely new way—if you normally bet red, try black!	
Directive #440: Craps - Locate a **cold craps table (quiet and losses happening)**. Bet **2 units on don't pass**. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #441: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #442: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #444: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #445: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #446: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**. Order a drink before making your next wager, and chat with the dealer.	
Directive #447: Break Actions - Find a **slot machine near a bar** and **sit there with a drink without playing**. Double your bet for the next round, then walk away if you win.	
Directive #448: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #449: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.	
Directive #450: Slots - Locate an **Vampire-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #451: Break Actions - Go to the **casino's sports bar** and **watch a game for 10 minutes before returning**. Try betting a completely new way—if you normally bet red, try black!	
Directive #452: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #453: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #457: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #460: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #461: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck. Double your bet for the next round, then walk away if you win.	
Directive #462: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins. Try betting a completely new way—if you normally bet red, try black!	
Directive #463: Break Actions - Find a **casino promotional booth** and ask about any deals or giveaways. Order a drink before making your next wager, and chat with the dealer.	
Directive #465: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #466: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #467: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #472: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #474: Craps - Place a **come bet** only after the shooter **rolls at least one point**.	
Directive #475: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #476: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #478: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #481: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #482: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #484: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.	
Directive #486: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**. Try betting a completely new way—if you normally bet red, try black!	
Directive #487: Break Actions - Find a **casino lounge** and **sit for 15 minutes** while sipping a drink.	
Directive #489: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #490: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #492: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #493: Break Actions - Find a **slot machine near a bar** and **sit there with a drink without playing**. Try betting a completely new way—if you normally bet red, try black!	
Directive #495: Craps - Bet **4 units on the pass line** if the **last shooter hit two points in a row**. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #497: Craps - Bet on the **field bet** only if **the last two rolls missed field numbers**. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #498: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #499: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #500: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #502: Break Actions - Find a **bar and order a random drink** from the menu without looking. Double your bet for the next round, then walk away if you win.	
Directive #503: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #504: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #506: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #507: Break Actions - Walk to the **bar closest to the high-limit area** and order an **Old Fashioned**. Find a game with the fewest players and place your next bet there.	
Directive #510: Break Actions - Walk to the **casino floor's self-serve drink station** and grab a **free soda**. Order a drink before making your next wager, and chat with the dealer.	
Directive #512: Break Actions - Take a **quick walk to the nearest drinking fountain** and take a sip before returning. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #514: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #519: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #520: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #521: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #522: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively. Order a drink before making your next wager, and chat with the dealer.	
Directive #525: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #526: Break Actions - Find a **casino promotional booth** and ask about any deals or giveaways. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #528: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #530: Break Actions - Find a **bar and order a random drink** from the menu without looking. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #531: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**. Switch to a nearby table and try a new strategy.	
Directive #532: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #533: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #534: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #537: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #539: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #544: Break Actions - Take a **bathroom break** and wash your hands before returning to the tables. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #545: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #548: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #553: Craps - Find a **table with a new shooter** and bet **the table minimum on pass line first, then adjust strategy**. Order a drink before making your next wager, and chat with the dealer.	
Directive #554: Break Actions - Go to the **casino's sports bar** and **watch a game for 10 minutes before returning**. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #555: Break Actions - Walk to the **VIP section and pretend to belong there** for 5 minutes before returning. Place a side bet if available, and observe how it changes your outcome.	
Directive #556: Break Actions - Find a **comfortable chair in the lounge** and **sit for 10 minutes** before playing again.	
Directive #558: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #559: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**. Place a side bet if available, and observe how it changes your outcome.	
Directive #560: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #565: Break Actions - Walk to the **closest cocktail waitress** and order a **free casino drink**. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #568: Craps - Place a **come bet** only after the shooter **rolls at least one point**.	
Directive #570: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #571: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #572: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #574: Break Actions - Head to the **casino gift shop** and buy something under $10 before going back to play.	
Directive #577: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**. Place a side bet if available, and observe how it changes your outcome.	
Directive #578: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #579: Break Actions - Walk around the **casino floor for exactly 5 minutes** before placing your next bet.	
Directive #580: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #582: Break Actions - Take a **quick walk to the nearest drinking fountain** and take a sip before returning. Double your bet for the next round, then walk away if you win.	
Directive #583: Break Actions - Stand near a high-stakes table and **watch quietly for 10 minutes before continuing your own gambling**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #585: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #586: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd. Find a game with the fewest players and place your next bet there.	
Directive #587: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer. Place a side bet if available, and observe how it changes your outcome.	
Directive #593: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #596: Break Actions - Walk to the **bar closest to the high-limit area** and order an **Old Fashioned**.	
Directive #597: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #599: Craps - Locate a **cold craps table (quiet and losses happening)**. Bet **2 units on don't pass**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #601: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #603: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #607: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #609: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #611: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #614: Break Actions - Walk around the **casino floor for exactly 5 minutes** before placing your next bet. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #615: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**. Order a drink before making your next wager, and chat with the dealer.	
Directive #616: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.	
Directive #619: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #621: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #622: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #623: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #626: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #627: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #628: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #631: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**. Find a game with the fewest players and place your next bet there.	
Directive #634: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #635: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #639: Break Actions - Walk to the **bar closest to the high-limit area** and order an **Old Fashioned**. Switch to a nearby table and try a new strategy.	
Directive #641: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #643: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #646: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #647: Slots - Locate an **Vampire-themed slot machine** and play **10 spins at minimum bet** before deciding to increase. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #648: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #649: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #650: Break Actions - Walk to the **casino floor's self-serve drink station** and grab a **free soda**. Place a side bet if available, and observe how it changes your outcome.	
Directive #655: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #660: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #662: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #668: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.	
Directive #670: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #672: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #676: Craps - Bet on the **field bet** only if **the last two rolls missed field numbers**. Switch to a nearby table and try a new strategy.	
Directive #677: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #679: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #687: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #688: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #690: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**. Try betting a completely new way—if you normally bet red, try black!	
Directive #691: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #692: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak. Switch to a nearby table and try a new strategy.	
Directive #693: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.	
Directive #695: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**. Try betting a completely new way—if you normally bet red, try black!	
Directive #697: Break Actions - Take a **casual walk through the high-roller section** without placing a bet. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #700: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand. Double your bet for the next round, then walk away if you win.	
Directive #702: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #706: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #707: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #708: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #711: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #713: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #715: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #716: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**. Find a game with the fewest players and place your next bet there.	
Directive #717: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #720: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #721: Slots - Locate an **Treasure-themed slot machine** and play **10 spins at minimum bet** before deciding to increase. Double your bet for the next round, then walk away if you win.	
Directive #724: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #725: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #727: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #728: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #730: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #732: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #734: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #735: Break Actions - Take a **10-minute break and scroll through social media** before playing again. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #737: Break Actions - Find a **slot machine near a bar** and **sit there with a drink without playing**.	
Directive #739: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #740: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #741: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.	
Directive #742: Break Actions - Take a **5-minute phone break** outside before going back inside to play. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #747: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.	
Directive #750: Break Actions - Find a **casino lounge** and **sit for 15 minutes** while sipping a drink. Find a game with the fewest players and place your next bet there.	
Directive #751: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #754: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #757: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #760: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #761: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.	
Directive #762: Craps - Look for a table where **the last roll was a 7**. Bet **small on pass line and increase if you win**. Double your bet for the next round, then walk away if you win.	
Directive #763: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #764: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #766: Break Actions - Walk around the **casino floor for exactly 5 minutes** before placing your next bet. Find a game with the fewest players and place your next bet there.	
Directive #771: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #773: Break Actions - Find a **comfortable chair in the lounge** and **sit for 10 minutes** before playing again. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #775: Slots - Locate an **Ice-themed slot machine** and play **10 spins at minimum bet** before deciding to increase. Find a game with the fewest players and place your next bet there.	
Directive #776: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #777: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #779: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #780: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #782: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #784: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #785: Break Actions - Walk to the **bar closest to the high-limit area** and order an **Old Fashioned**. Order a drink before making your next wager, and chat with the dealer.	
Directive #786: Break Actions - Go to the **nearest bartender** and ask them to **make you their best drink**. Find a game with the fewest players and place your next bet there.	
Directive #787: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #791: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #792: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #794: Break Actions - Walk to the **nearest bar** and order a **shot of tequila**. Take it immediately. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #795: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #796: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #797: Break Actions - Find the **nearest bar** and order a **local beer**. Sip it slowly while watching a game. Double your bet for the next round, then walk away if you win.	
Directive #798: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #800: Slots - Locate an **Alien-themed slot machine** and play **10 spins at minimum bet** before deciding to increase. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #804: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #805: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #809: Craps - Look for a table where **the last roll was a 7**. Bet **small on pass line and increase if you win**. Order a drink before making your next wager, and chat with the dealer.	
Directive #810: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #814: Craps - Bet **4 units on the pass line** if the **last shooter hit two points in a row**. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #817: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**. Find a game with the fewest players and place your next bet there.	
Directive #820: Slots - Locate an **Dinosaur-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #821: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**. Double your bet for the next round, then walk away if you win.	
Directive #822: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #823: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #824: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #826: Break Actions - Find a **casino promotional booth** and ask about any deals or giveaways. Switch tables if you lose 3 times in a row, or double down if you win twice in a row.	
Directive #828: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #829: Break Actions - Walk to the **bar closest to the high-limit area** and order an **Old Fashioned**. Double your bet for the next round, then walk away if you win.	
Directive #830: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #833: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**. Switch to a nearby table and try a new strategy.	
Directive #835: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #837: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #838: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #839: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #841: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #842: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #843: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak. Try betting a completely new way—if you normally bet red, try black!	
Directive #844: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #846: Break Actions - Walk around the **casino floor for exactly 5 minutes** before placing your next bet.	
Directive #847: Craps - Place a **come bet** only after the shooter **rolls at least one point**.	
Directive #848: Break Actions - Find the **nearest bar** and order a **local beer**. Sip it slowly while watching a game. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #851: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #852: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #854: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #856: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #857: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #859: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #865: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.	
Directive #866: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #867: Slots - Locate an **Cyberpunk-themed slot machine** and play **10 spins at minimum bet** before deciding to increase. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #868: Slots - Locate an **Steampunk-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #869: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #871: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll. Double your bet for the next round, then walk away if you win.	
Directive #872: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #873: Break Actions - Take a **10-minute break and scroll through social media** before playing again. Double your bet for the next round, then walk away if you win.	
Directive #875: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #876: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins. Switch to a nearby table and try a new strategy.	
Directive #880: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #881: Break Actions - Take a **deep breath, relax, and count your cash** before placing your next bet. Find a game with the fewest players and place your next bet there.	
Directive #882: Break Actions - Take a **casual walk through the high-roller section** without placing a bet. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #886: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**. Place a side bet if available, and observe how it changes your outcome.	
Directive #890: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**. Switch to a nearby table and try a new strategy.	
Directive #893: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #895: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #896: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #898: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #899: Break Actions - Take a **10-minute break and scroll through social media** before playing again. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #901: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #905: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #908: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #910: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #911: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**. Bet using a pattern of your choosing (e.g., every other number, or only high numbers).	
Directive #914: Break Actions - Take a **bathroom break** and wash your hands before returning to the tables. Walk around the casino floor for 5 minutes before placing another bet.	
Directive #916: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**. Switch to a nearby table and try a new strategy.	
Directive #918: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #921: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**. Double your bet for the next round, then walk away if you win.	
Directive #922: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.	
Directive #924: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18. Locate a game with a big crowd and match a high roller’s bet once.	
Directive #925: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #926: Slots - Locate an **Ice-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.	
Directive #927: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #928: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #929: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card. Take a seat at a random slot machine and spin exactly 7 times.	
Directive #931: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd. Switch to a nearby table and try a new strategy.	
Directive #939: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #944: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.	
Directive #945: Break Actions - Take a **deep breath, relax, and count your cash** before placing your next bet. Try betting a completely new way—if you normally bet red, try black!	
Directive #946: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #947: Break Actions - Walk around the **casino floor for exactly 5 minutes** before placing your next bet.	
Directive #950: Break Actions - Find a **slot machine near a bar** and **sit there with a drink without playing**. Find a game with the fewest players and place your next bet there.	
Directive #951: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.	
Directive #952: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #954: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18. Order a drink before making your next wager, and chat with the dealer.	
Directive #956: Break Actions - Find a **slot machine near a bar** and **sit there with a drink without playing**. Order a drink before making your next wager, and chat with the dealer.	
Directive #960: Break Actions - Stop and **watch a game you’ve never played before for 5 minutes**, then decide if you want to try it. Double your bet for the next round, then walk away if you win.	
Directive #963: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #964: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #967: Break Actions - Find a **TV screen showing live sports** and stand there for 10 minutes before playing again. Switch to a nearby table and try a new strategy.	
Directive #969: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**. Order a drink before making your next wager, and chat with the dealer.	
Directive #973: Break Actions - Go to the **nearest bartender** and ask them to **make you their best drink**. Switch to a nearby table and try a new strategy.	
Directive #974: Craps - Place a **come bet** only after the shooter **rolls at least one point**.	
Directive #976: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.	
Directive #978: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #979: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.	
Directive #983: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #985: Break Actions - Take a **10-minute break and scroll through social media** before playing again. Find a slot near an ATM or cashier and play for 10 spins.	
Directive #986: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively. Place a side bet if available, and observe how it changes your outcome.	
Directive #987: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.	
Directive #989: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.	
Directive #990: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #993: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
Directive #994: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.	
Directive #995: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll. Find a game with the fewest players and place your next bet there.	
Directive #997: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.	
Directive #998: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.	
Directive #999: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.	
Directive #1000: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.	
"""
sheet_directives = [line.strip() for line in raw_sheet_directives.splitlines() if line.strip()]
all_directives = list(dict.fromkeys(sheet_directives))

def filter_directives(categories):
    if not categories:
        return all_directives
    filtered = []
    for d in all_directives:
        if any(cat.lower() in d.lower() for cat in categories):
            filtered.append(d)
    return filtered

@app.route('/')
def home():
    return render_template('index.html')

# Existing random tip route
@app.route('/api/random-tip', methods=['POST'])
def random_tip():
    data = request.get_json() or {}
    categories = data.get("categories", [])
    filtered = filter_directives(categories)
    if not filtered:
        return jsonify({"tip": "No tip found for the selected categories."})
    tip = random.choice(filtered)
    return jsonify({"tip": tip})

# Existing roulette routes
@app.route('/api/random-roulette-number', methods=['GET'])
def random_roulette_number():
    numbers = ["00", "0"] + [str(i) for i in range(1, 37)]
    return jsonify({"result": random.choice(numbers)})

@app.route('/api/random-color', methods=['GET'])
def random_color():
    return jsonify({"result": random.choice(["RED", "BLACK"])})

@app.route('/api/random-odd-even', methods=['GET'])
def random_odd_even():
    return jsonify({"result": random.choice(["ODD", "EVEN"])})

@app.route('/api/random-roulette-multi', methods=['GET'])
def random_roulette_multi():
    numbers = ["00", "0"] + [str(i) for i in range(1, 37)]
    how_many = random.randint(1, 20)
    picks = random.sample(numbers, how_many)
    return jsonify({"result": picks})

# ------------------------------
# NEW: Random Drink Route
# ------------------------------
@app.route('/api/random-drink', methods=['GET'])
def random_drink():
    """
    Returns a random mixed drink from a big list.
    Expand this list as you like for hundreds of drinks.
    """
    drinks = [
        "Old Fashioned", "Margarita", "Mojito", "Whiskey Sour", "Manhattan",
        "Martini", "Cosmopolitan", "Daiquiri", "Tom Collins", "Gin and Tonic",
        "Tequila Sunrise", "Long Island Iced Tea", "Bloody Mary", "Screwdriver",
        "Piña Colada", "Mai Tai", "Negroni", "Paloma", "French 75", "Sidecar",
        "Mint Julep", "White Russian", "Caipirinha", "Sex on the Beach",
        "Irish Coffee", "Amaretto Sour", "Hurricane", "Planter's Punch",
        "Singapore Sling", "Moscow Mule", "Dark 'n' Stormy", "Bahama Mama",
        "Gimlet", "Vesper", "Sazerac", "Hot Toddy", "Bellini", "Aperol Spritz",
        "Kir Royale", "Michelada", "Lemon Drop Martini", "Apple Martini",
        "Espresso Martini", "Black Russian", "Boulevardier", "Paper Plane",
        "Mezcal Margarita", "Smoky Paloma", "Hemingway Daiquiri", "Clover Club",
        "Gold Rush", "Rusty Nail", "El Diablo", "The Last Word", "Vieux Carré",
        "Penicillin", "Southside", "Ward Eight", "Jäger Bomb", "Tokyo Tea",
        "Blue Lagoon", "Electric Lemonade", "Death in the Afternoon",
        "Midnight Mule (Moscow Mule with black vodka)", 
        "Neon Margarita (Blue Curaçao, Tequila, Lime)",
        "Flaming Dr. Pepper", "Vegas Bomb", "Liquid Cocaine Shot", "Four Horsemen Shot",
        "Mind Eraser", "Starburst Shot", "Scooby Snack Shot", "Pineapple Upside Down Shot",
        "Kamikaze Shot", "Irish Car Bomb", "Lemon Drop Shot", "Green Tea Shot", 
        "Red Headed Slut", "Surfer on Acid", "Royal Flush", "Washington Apple", 
        "Cactus Cooler Shot", "Cherry Bomb", "Pickleback Shot", "Oatmeal Cookie Shot", 
        "Cinnamon Toast Crunch Shot", "A Shot of Tequila (Jose Cuervo, Patrón, Don Julio, Casamigos)",
        "A Shot of Whiskey (Jack Daniel's, Jameson, Crown Royal, Maker's Mark, Buffalo Trace)",
        "A Shot of Rum (Bacardi, Captain Morgan, Malibu)", 
        "A Shot of Vodka (Grey Goose, Tito's, Smirnoff)",
        "A Shot of Fireball", "A Local Beer", "A Corona with Lime", "A Bud Light",
        "A Heineken", "A Modelo", "A Stella Artois", "A Michelob Ultra",
        "A Guinness", "A Blue Moon with Orange", "A Pabst Blue Ribbon",
        "A Red Bull Vodka", "Jack and Coke", "Rum and Coke", "Vodka Cranberry",
        "Whiskey Ginger", "Gin and Juice", "Cuba Libre", "Tequila and Soda with Lime",
        "Malibu Bay Breeze", "Vodka Redbull", "John Collins", "Tennessee Mule (Jack Daniel's, Ginger Beer, Lime)",
        "Texas Tea (Long Island Iced Tea with Bourbon)", "Blackberry Whiskey Smash",
        "Peach Bourbon Smash", "Cherry Whiskey Sour", "Mimosa", "Tequila Mule",
        "Spiked Arnold Palmer (Half Iced Tea, Half Lemonade with Vodka or Bourbon)",
        "Strawberry Daiquiri", "Frozen Margarita", "Frozen Piña Colada",
        "Mai Tai on the Rocks", "Spicy Margarita", "Coconut Mojito", "Dirty Shirley",
        "Rum Punch", "Zombie", "Bahama Mama", "Hurricane", "Painkiller",
        "Rum Runner", "Madras", "Sea Breeze", "Bay Breeze", "Sex in the Driveway",
        "Dirty Martini", "Chocolate Martini", "White Gummy Bear Shot",
        "A Glass of House Wine (Red or White)", "A Glass of Champagne",
        "A Bottle of Sparkling Water", "A Non-Alcoholic Beer",
        "A Shirley Temple", "An Arnold Palmer", "Club Soda with Lime",
        "Cranberry Juice on the Rocks", "Pineapple Juice with a Cherry Garnish"
    ]
    return jsonify({"result": random.choice(drinks)})

if __name__ == '__main__':
    app.run(debug=True, port=5001)

import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ------------------------------
# SAMPLE DIRECTIVES
# (Replace with your own full set if desired)
# ------------------------------
raw_sheet_directives = """
Directive #1: Break Actions - Go to the **casino’s ATM or cash-out area** and count your winnings or losses before continuing.
Directive #2: Break Actions - Walk around the **casino floor for exactly 5 minutes** before placing your next bet.
Directive #3: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.
Directive #4: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.
Directive #5: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**.
Directive #6: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.
Directive #7: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #8: Break Actions - Take a **bathroom break** and wash your hands before returning to the tables.
Directive #9: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**.
Directive #10: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #11: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #12: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #13: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**.
Directive #14: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.
Directive #15: Craps - Bet on the **field bet** only if **the last two rolls missed field numbers**.
Directive #16: Craps - Locate a **cold craps table (quiet and losses happening)**. Bet **2 units on don't pass**.
Directive #17: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**.
Directive #18: Break Actions - Walk to the **VIP section and pretend to belong there** for 5 minutes before returning.
Directive #19: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**.
Directive #20: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #21: Break Actions - Find a **TV screen showing live sports** and stand there for 10 minutes before playing again.
Directive #22: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.
Directive #23: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #24: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.
Directive #25: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #26: Break Actions - Go to the **nearest bartender** and ask them to **make you their best drink**.
Directive #27: Break Actions - Take a **5-minute phone break** outside before going back inside to play.
Directive #28: Craps - Bet **4 units on the pass line** if the **last shooter hit two points in a row**.
Directive #29: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #30: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.
Directive #31: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.
Directive #32: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #33: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #34: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #35: Craps - Locate a **cold craps table (quiet and losses happening)**. Bet **2 units on don't pass**.
Directive #36: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #37: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #38: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.
Directive #39: Break Actions - Grab a **complimentary coffee or tea** and sip it while standing near a lively table.
Directive #40: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #41: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #42: Craps - Place a **come bet** only after the shooter **rolls at least one point**.
Directive #43: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**.
Directive #44: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.
Directive #45: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**.
Directive #46: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #47: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #48: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**.
Directive #49: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.
Directive #50: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**.
Directive #51: Break Actions - Stop and **watch a game you’ve never played before for 5 minutes**, then decide if you want to try it.
Directive #52: Break Actions - Ask a **pit boss what table is the hottest**, then walk to it and observe before betting.
Directive #53: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy.
Directive #54: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #55: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #56: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy.
Directive #57: Break Actions - Find a **casino promotional booth** and ask about any deals or giveaways.
Directive #58: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #59: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.
Directive #60: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.
Directive #61: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #62: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #63: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #64: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #65: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win.
Directive #66: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #67: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy.
Directive #68: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #69: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #70: Break Actions - Take a **5-minute phone break** outside before going back inside to play.
Directive #71: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #72: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win.
Directive #73: Craps - Look for a table where **the last roll was a 7**. Bet **small on pass line and increase if you win**.
Directive #74: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #75: Break Actions - Walk around the **casino floor for exactly 5 minutes** before placing your next bet.
Directive #76: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.
Directive #77: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**.
Directive #78: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #79: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.
Directive #80: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**.
Directive #81: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.
Directive #82: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.
Directive #83: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #84: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #85: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #86: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #87: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #88: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win.
Directive #89: Break Actions - Stop and **watch a game you’ve never played before for 5 minutes**, then decide if you want to try it.
Directive #90: Craps - Bet **4 units on the pass line** if the **last shooter hit two points in a row**.
Directive #91: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.
Directive #92: Break Actions - Go to the **casino’s ATM or cash-out area** and count your winnings or losses before continuing.
Directive #93: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #94: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #95: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.
Directive #96: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.
Directive #97: Break Actions - Take a **deep breath, relax, and count your cash** before placing your next bet.
Directive #98: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.
Directive #99: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy.
Directive #100: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #101: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #102: Craps - Locate a **cold craps table (quiet and losses happening)**. Bet **2 units on don't pass**.
Directive #103: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #104: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.
Directive #105: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**.
Directive #106: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #107: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.
Directive #108: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #109: Break Actions - Stand near a high-stakes table and **watch quietly for 10 minutes before continuing your own gambling**.
Directive #110: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #111: Break Actions - Take a **10-minute break and scroll through social media** before playing again.
Directive #112: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #113: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing.
Directive #114: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #115: Craps - Bet **4 units on the pass line** if the **last shooter hit two points in a row**.
Directive #116: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #117: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.
Directive #118: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #119: Break Actions - Walk to the **casino floor's self-serve drink station** and grab a **free soda**.
Directive #120: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #121: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #122: Craps - Place a **come bet** only after the shooter **rolls at least one point**.
Directive #123: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #124: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.
Directive #125: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.
Directive #126: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**.
Directive #127: Break Actions - Stand near a high-stakes table and **watch quietly for 10 minutes before continuing your own gambling**.
Directive #128: Break Actions - Walk to the **VIP section and pretend to belong there** for 5 minutes before returning.
Directive #129: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.
Directive #130: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing.
Directive #131: Craps - Place a **come bet** only after the shooter **rolls at least one point**.
Directive #132: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**.
Directive #133: Break Actions - Grab a **complimentary coffee or tea** and sip it while standing near a lively table.
Directive #134: Craps - Find a **table with a new shooter** and bet **the table minimum on pass line first, then adjust strategy**.
Directive #135: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #136: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #137: Break Actions - Find a **bar and order a random drink** from the menu without looking.
Directive #138: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**.
Directive #139: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.
Directive #140: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.
Directive #141: Break Actions - Stand near a high-stakes table and **watch quietly for 10 minutes before continuing your own gambling**.
Directive #142: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.
Directive #143: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.
Directive #144: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**.
Directive #145: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #146: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #147: Break Actions - Find a **bar and order a random drink** from the menu without looking.
Directive #148: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**.
Directive #149: Craps - If you see a player **pressing their bets aggressively**, match their come bet for one roll.
Directive #150: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win.
Directive #151: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #152: Craps - Find a **table with a new shooter** and bet **the table minimum on pass line first, then adjust strategy**.
Directive #153: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #154: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.
Directive #155: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #156: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #157: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**.
Directive #158: Break Actions - Take a **casual walk through the high-roller section** without placing a bet.
Directive #159: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy.
Directive #160: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #161: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.
Directive #162: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.
Directive #163: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #164: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #165: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #166: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #167: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #168: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #169: Break Actions - Find the **nearest bar** and order a **local beer**. Sip it slowly while watching a game.
Directive #170: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #171: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #172: Craps - Bet on the **field bet** only if **the last two rolls missed field numbers**.
Directive #173: Break Actions - Take a **quick walk to the nearest drinking fountain** and take a sip before returning.
Directive #174: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #175: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #176: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #177: Break Actions - Go to the **casino's sports bar** and **watch a game for 10 minutes before returning**.
Directive #178: Craps - If you see a player **pressing their bets aggressively**, match their come bet for one roll.
Directive #179: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #180: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #181: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #182: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #183: Break Actions - Walk to the **casino floor's self-serve drink station** and grab a **free soda**.
Directive #184: Break Actions - Find a **TV screen showing live sports** and stand there for 10 minutes before playing again.
Directive #185: Break Actions - Walk to the **closest cocktail waitress** and order a **free casino drink**.
Directive #186: Break Actions - Find a **casino promotional booth** and ask about any deals or giveaways.
Directive #187: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #188: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #189: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #190: Break Actions - Go to the **casino’s ATM or cash-out area** and count your winnings or losses before continuing.
Directive #191: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.
Directive #192: Break Actions - Take a **10-minute break and scroll through social media** before playing again.
Directive #193: Break Actions - Take a **bathroom break** and wash your hands before returning to the tables.
Directive #194: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.
Directive #195: Craps - Look for a table where **the last roll was a 7**. Bet **small on pass line and increase if you win**.
Directive #196: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.
Directive #197: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #198: Break Actions - Take a **casual walk through the high-roller section** without placing a bet.
Directive #199: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.
Directive #200: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**.
Directive #201: Break Actions - Go to the **nearest bartender** and ask them to **make you their best drink**.
Directive #202: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #203: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #204: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #205: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.
Directive #206: Break Actions - Take a **casual walk through the high-roller section** without placing a bet.
Directive #207: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #208: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.
Directive #209: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #210: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.
Directive #211: Break Actions - Grab a **complimentary coffee or tea** and sip it while standing near a lively table.
Directive #212: Break Actions - Go to the **casino's sports bar** and **watch a game for 10 minutes before returning**.
Directive #213: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.
Directive #214: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #215: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #216: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.
Directive #217: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #218: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #219: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**.
Directive #220: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.
Directive #221: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.
Directive #222: Break Actions - Ask a **pit boss what table is the hottest**, then walk to it and observe before betting.
Directive #223: Break Actions - Take a **quick walk to the nearest drinking fountain** and take a sip before returning.
Directive #224: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #225: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.
Directive #226: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.
Directive #227: Craps - Locate a **cold craps table (quiet and losses happening)**. Bet **2 units on don't pass**.
Directive #228: Break Actions - Take a **casual walk through the high-roller section** without placing a bet.
Directive #229: Break Actions - Find a **slot machine near a bar** and **sit there with a drink without playing**.
Directive #230: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #231: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**.
Directive #232: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy.
Directive #233: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.
Directive #234: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #235: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.
Directive #236: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing.
Directive #237: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.
Directive #238: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #239: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #240: Break Actions - Stop and **watch a game you’ve never played before for 5 minutes**, then decide if you want to try it.
Directive #241: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**.
Directive #242: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #243: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #244: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #245: Break Actions - Find a **casino promotional booth** and ask about any deals or giveaways.
Directive #246: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #247: Craps - Bet on the **field bet** only if **the last two rolls missed field numbers**.
Directive #248: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.
Directive #249: Break Actions - Find a **TV screen showing live sports** and stand there for 10 minutes before playing again.
Directive #250: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #251: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #252: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #253: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #254: Break Actions - Find a **TV screen showing live sports** and stand there for 10 minutes before playing again.
Directive #255: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #256: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #257: Break Actions - Walk to the **nearest food stand and grab a snack** before returning.
Directive #258: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.
Directive #259: Craps - Locate a **cold craps table (quiet and losses happening)**. Bet **2 units on don't pass**.
Directive #260: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.
Directive #261: Break Actions - Walk to the **nearest bar** and order a **shot of tequila**. Take it immediately.
Directive #262: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**.
Directive #263: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**.
Directive #264: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #265: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #266: Break Actions - Find a **casino promotional booth** and ask about any deals or giveaways.
Directive #267: Break Actions - Go to the **casino’s ATM or cash-out area** and count your winnings or losses before continuing.
Directive #268: Break Actions - Find a **comfortable chair in the lounge** and **sit for 10 minutes** before playing again.
Directive #269: Break Actions - Take a **5-minute phone break** outside before going back inside to play.
Directive #270: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.
Directive #271: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**.
Directive #272: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #273: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #274: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #275: Craps - Locate a **cold craps table (quiet and losses happening)**. Bet **2 units on don't pass**.
Directive #276: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.
Directive #277: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**.
Directive #278: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**.
Directive #279: Break Actions - Stand near a high-stakes table and **watch quietly for 10 minutes before continuing your own gambling**.
Directive #280: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #281: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.
Directive #282: Break Actions - Find the **nearest bar** and order a **local beer**. Sip it slowly while watching a game.
Directive #283: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.
Directive #284: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #285: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.
Directive #286: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #287: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy.
Directive #288: Break Actions - Stand near a high-stakes table and **watch quietly for 10 minutes before continuing your own gambling**.
Directive #289: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #290: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #291: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #292: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.
Directive #293: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.
Directive #294: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing.
Directive #295: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #296: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**.
Directive #297: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #298: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**.
Directive #299: Break Actions - Grab a **complimentary coffee or tea** and sip it while standing near a lively table.
Directive #300: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #301: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win.
Directive #302: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #303: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #304: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy.
Directive #305: Break Actions - Find the **nearest bar** and order a **local beer**. Sip it slowly while watching a game.
Directive #306: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**.
Directive #307: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.
Directive #308: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.
Directive #309: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**.
Directive #310: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.
Directive #311: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.
Directive #312: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.
Directive #313: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.
Directive #314: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy.
Directive #315: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win.
Directive #316: Craps - Find a **hot craps table (lots of cheering)** and bet **3 units on the pass line**.
Directive #317: Break Actions - Stand near a high-stakes table and **watch quietly for 10 minutes before continuing your own gambling**.
Directive #318: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.
Directive #319: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**.
Directive #320: Break Actions - Take a **quick walk to the nearest drinking fountain** and take a sip before returning.
Directive #321: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #322: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #323: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #324: Break Actions - Go to the **nearest bartender** and ask them to **make you their best drink**.
Directive #325: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.
Directive #326: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #327: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #328: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #329: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #330: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win.
Directive #331: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #332: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.
Directive #333: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.
Directive #334: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #335: Break Actions - Find a **TV screen showing live sports** and stand there for 10 minutes before playing again.
Directive #336: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.
Directive #337: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #338: Break Actions - Find the **nearest bar** and order a **local beer**. Sip it slowly while watching a game.
Directive #339: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.
Directive #340: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing.
Directive #341: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #342: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #343: Craps - Locate a **cold craps table (quiet and losses happening)**. Bet **2 units on don't pass**.
Directive #344: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.
Directive #345: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #346: Craps - Find a **hot craps table (lots of cheering)** and bet **3 units on the pass line**.
Directive #347: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**.
Directive #348: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #349: Break Actions - Find a **casino promotional booth** and ask about any deals or giveaways.
Directive #350: Craps - Place a **come bet** only after the shooter **rolls at least one point**.
Directive #351: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #352: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #353: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #354: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #355: Break Actions - Take a **deep breath, relax, and count your cash** before placing your next bet.
Directive #356: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #357: Break Actions - Walk around the **casino floor for exactly 5 minutes** before placing your next bet.
Directive #358: Break Actions - Find a **bar and order a random drink** from the menu without looking.
Directive #359: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #360: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #361: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #362: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.
Directive #363: Break Actions - Go to the **casino’s ATM or cash-out area** and count your winnings or losses before continuing.
Directive #364: Craps - Place a **come bet** only after the shooter **rolls at least one point**.
Directive #365: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.
Directive #366: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.
Directive #367: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**.
Directive #368: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**.
Directive #369: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #370: Break Actions - Take a **deep breath, relax, and count your cash** before placing your next bet.
Directive #371: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #372: Break Actions - Take a **5-minute phone break** outside before going back inside to play.
Directive #373: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.
Directive #374: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win.
Directive #375: Break Actions - Take a **deep breath, relax, and count your cash** before placing your next bet.
Directive #376: Break Actions - Stop and **watch a game you’ve never played before for 5 minutes**, then decide if you want to try it.
Directive #377: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #378: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.
Directive #379: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #380: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.
Directive #381: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #382: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #383: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #384: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.
Directive #385: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win.
Directive #386: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.
Directive #387: Craps - Locate a **cold craps table (quiet and losses happening)**. Bet **2 units on don't pass**.
Directive #388: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing.
Directive #389: Break Actions - Take a **bathroom break** and wash your hands before returning to the tables.
Directive #390: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win.
Directive #391: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #392: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**.
Directive #393: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.
Directive #394: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.
Directive #395: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.
Directive #396: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #397: Craps - If you see a player **pressing their bets aggressively**, match their come bet for one roll.
Directive #398: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #399: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.
Directive #400: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy.
Directive #401: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #402: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.
Directive #403: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.
Directive #404: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy.
Directive #405: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.
Directive #406: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #407: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.
Directive #408: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.
Directive #409: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**.
Directive #410: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**.
Directive #411: Break Actions - Walk to the **nearest bar** and order a **shot of tequila**. Take it immediately.
Directive #412: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**.
Directive #413: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**.
Directive #414: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #415: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.
Directive #416: Craps - Find a **hot craps table (lots of cheering)** and bet **3 units on the pass line**.
Directive #417: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**.
Directive #418: Break Actions - Walk to the **nearest food stand and grab a snack** before returning.
Directive #419: Craps - If you see a player **pressing their bets aggressively**, match their come bet for one roll.
Directive #420: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.
Directive #421: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #422: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.
Directive #423: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.
Directive #424: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.
Directive #425: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.
Directive #426: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #427: Break Actions - Walk to the **casino floor's self-serve drink station** and grab a **free soda**.
Directive #428: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy.
Directive #429: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #430: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy.
Directive #431: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing.
Directive #432: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.
Directive #433: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.
Directive #434: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #435: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.
Directive #436: Craps - Find a **hot craps table (lots of cheering)** and bet **3 units on the pass line**.
Directive #437: Craps - Locate a **cold craps table (quiet and losses happening)**. Bet **2 units on don't pass**.
Directive #438: Craps - Bet **4 units on the pass line** if the **last shooter hit two points in a row**.
Directive #439: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing.
Directive #440: Craps - Locate a **cold craps table (quiet and losses happening)**. Bet **2 units on don't pass**.
Directive #441: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #442: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #443: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**.
Directive #444: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #445: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**.
Directive #446: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**.
Directive #447: Break Actions - Find a **slot machine near a bar** and **sit there with a drink without playing**.
Directive #448: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.
Directive #449: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.
Directive #450: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #451: Break Actions - Go to the **casino's sports bar** and **watch a game for 10 minutes before returning**.
Directive #452: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #453: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.
Directive #454: Break Actions - Stand near a high-stakes table and **watch quietly for 10 minutes before continuing your own gambling**.
Directive #455: Break Actions - Find a **TV screen showing live sports** and stand there for 10 minutes before playing again.
Directive #456: Craps - If you see a player **pressing their bets aggressively**, match their come bet for one roll.
Directive #457: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #458: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.
Directive #459: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #460: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #461: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #462: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #463: Break Actions - Find a **casino promotional booth** and ask about any deals or giveaways.
Directive #464: Break Actions - Stand near a high-stakes table and **watch quietly for 10 minutes before continuing your own gambling**.
Directive #465: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.
Directive #466: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #467: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #468: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**.
Directive #469: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #470: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #471: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win.
Directive #472: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #473: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing.
Directive #474: Craps - Place a **come bet** only after the shooter **rolls at least one point**.
Directive #475: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #476: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #477: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #478: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.
Directive #479: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.
Directive #480: Break Actions - Find a **casino promotional booth** and ask about any deals or giveaways.
Directive #481: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.
Directive #482: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #483: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.
Directive #484: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.
Directive #485: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win.
Directive #486: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**.
Directive #487: Break Actions - Find a **casino lounge** and **sit for 15 minutes** while sipping a drink.
Directive #488: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #489: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.
Directive #490: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.
Directive #491: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**.
Directive #492: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #493: Break Actions - Find a **slot machine near a bar** and **sit there with a drink without playing**.
Directive #494: Break Actions - Find a **casino promotional booth** and ask about any deals or giveaways.
Directive #495: Craps - Bet **4 units on the pass line** if the **last shooter hit two points in a row**.
Directive #496: Break Actions - Stop and **watch a game you’ve never played before for 5 minutes**, then decide if you want to try it.
Directive #497: Craps - Bet on the **field bet** only if **the last two rolls missed field numbers**.
Directive #498: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #499: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #500: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win.
Directive #501: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**.
Directive #502: Break Actions - Find a **bar and order a random drink** from the menu without looking.
Directive #503: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #504: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #505: Break Actions - Take a **quick walk to the nearest drinking fountain** and take a sip before returning.
Directive #506: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #507: Break Actions - Walk to the **bar closest to the high-limit area** and order an **Old Fashioned**.
Directive #508: Craps - If you see a player **pressing their bets aggressively**, match their come bet for one roll.
Directive #509: Break Actions - Take a **deep breath, relax, and count your cash** before placing your next bet.
Directive #510: Break Actions - Walk to the **casino floor's self-serve drink station** and grab a **free soda**.
Directive #511: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.
Directive #512: Break Actions - Take a **quick walk to the nearest drinking fountain** and take a sip before returning.
Directive #513: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**.
Directive #514: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #515: Craps - Find a **hot craps table (lots of cheering)** and bet **3 units on the pass line**.
Directive #516: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**.
Directive #517: Break Actions - Walk to the **VIP section and pretend to belong there** for 5 minutes before returning.
Directive #518: Break Actions - Walk to the **closest cocktail waitress** and order a **free casino drink**.
Directive #519: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.
Directive #520: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.
Directive #521: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #522: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.
Directive #523: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.
Directive #524: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.
Directive #525: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #526: Break Actions - Find a **casino promotional booth** and ask about any deals or giveaways.
Directive #527: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.
Directive #528: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #529: Break Actions - Stop and **watch a game you’ve never played before for 5 minutes**, then decide if you want to try it.
Directive #530: Break Actions - Find a **bar and order a random drink** from the menu without looking.
Directive #531: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #532: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #533: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.
Directive #534: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #535: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #536: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**.
Directive #537: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #538: Break Actions - Ask a **pit boss what table is the hottest**, then walk to it and observe before betting.
Directive #539: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #540: Break Actions - Walk to the **nearest bar** and order a **shot of tequila**. Take it immediately.
Directive #541: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing.
Directive #542: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.
Directive #543: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.
Directive #544: Break Actions - Take a **bathroom break** and wash your hands before returning to the tables.
Directive #545: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #546: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing.
Directive #547: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**.
Directive #548: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #549: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing.
Directive #550: Break Actions - Take a **10-minute break and scroll through social media** before playing again.
Directive #551: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.
Directive #552: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.
Directive #553: Craps - Find a **table with a new shooter** and bet **the table minimum on pass line first, then adjust strategy**.
Directive #554: Break Actions - Go to the **casino's sports bar** and **watch a game for 10 minutes before returning**.
Directive #555: Break Actions - Walk to the **VIP section and pretend to belong there** for 5 minutes before returning.
Directive #556: Break Actions - Find a **comfortable chair in the lounge** and **sit for 10 minutes** before playing again.
Directive #557: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #558: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #559: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #560: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.
Directive #561: Craps - Find a **table with a new shooter** and bet **the table minimum on pass line first, then adjust strategy**.
Directive #562: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #563: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**.
Directive #564: Break Actions - Grab a **complimentary coffee or tea** and sip it while standing near a lively table.
Directive #565: Break Actions - Walk to the **closest cocktail waitress** and order a **free casino drink**.
Directive #566: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.
Directive #567: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy.
Directive #568: Craps - Place a **come bet** only after the shooter **rolls at least one point**.
Directive #569: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.
Directive #570: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.
Directive #571: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #572: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.
Directive #573: Break Actions - Take a **5-minute phone break** outside before going back inside to play.
Directive #574: Break Actions - Head to the **casino gift shop** and buy something under $10 before going back to play.
Directive #575: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing.
Directive #576: Break Actions - Find a **casino lounge** and **sit for 15 minutes** while sipping a drink.
Directive #577: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #578: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #579: Break Actions - Walk around the **casino floor for exactly 5 minutes** before placing your next bet.
Directive #580: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #581: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy.
Directive #582: Break Actions - Take a **quick walk to the nearest drinking fountain** and take a sip before returning.
Directive #583: Break Actions - Stand near a high-stakes table and **watch quietly for 10 minutes before continuing your own gambling**.
Directive #584: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**.
Directive #585: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #586: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #587: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #588: Craps - Locate a **cold craps table (quiet and losses happening)**. Bet **2 units on don't pass**.
Directive #589: Break Actions - Find the **nearest bar** and order a **local beer**. Sip it slowly while watching a game.
Directive #590: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**.
Directive #591: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**.
Directive #592: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.
Directive #593: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #594: Break Actions - Go to the **casino’s ATM or cash-out area** and count your winnings or losses before continuing.
Directive #595: Craps - Look for a table where **the last roll was a 7**. Bet **small on pass line and increase if you win**.
Directive #596: Break Actions - Walk to the **bar closest to the high-limit area** and order an **Old Fashioned**.
Directive #597: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.
Directive #598: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**.
Directive #599: Craps - Locate a **cold craps table (quiet and losses happening)**. Bet **2 units on don't pass**.
Directive #600: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.
Directive #601: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #602: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.
Directive #603: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #604: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #605: Break Actions - Stop and **watch a game you’ve never played before for 5 minutes**, then decide if you want to try it.
Directive #606: Break Actions - Stand near a high-stakes table and **watch quietly for 10 minutes before continuing your own gambling**.
Directive #607: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win.
Directive #608: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #609: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.
Directive #610: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #611: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.
Directive #612: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing.
Directive #613: Break Actions - Go to the **casino's sports bar** and **watch a game for 10 minutes before returning**.
Directive #614: Break Actions - Walk around the **casino floor for exactly 5 minutes** before placing your next bet.
Directive #615: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #616: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.
Directive #617: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #618: Craps - If you see a player **pressing their bets aggressively**, match their come bet for one roll.
Directive #619: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.
Directive #620: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.
Directive #621: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #622: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #623: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #624: Break Actions - Walk to the **casino floor's self-serve drink station** and grab a **free soda**.
Directive #625: Break Actions - Take a **bathroom break** and wash your hands before returning to the tables.
Directive #626: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #627: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #628: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.
Directive #629: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win.
Directive #630: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #631: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.
Directive #632: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing.
Directive #633: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #634: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #635: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #636: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.
Directive #637: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #638: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #639: Break Actions - Walk to the **bar closest to the high-limit area** and order an **Old Fashioned**.
Directive #640: Break Actions - Walk to the **bar closest to the high-limit area** and order an **Old Fashioned**.
Directive #641: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #642: Craps - Locate a **cold craps table (quiet and losses happening)**. Bet **2 units on don't pass**.
Directive #643: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #644: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.
Directive #645: Craps - Bet **4 units on the pass line** if the **last shooter hit two points in a row**.
Directive #646: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #647: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #648: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #649: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.
Directive #650: Break Actions - Walk to the **casino floor's self-serve drink station** and grab a **free soda**.
Directive #651: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.
Directive #652: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.
Directive #653: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.
Directive #654: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #655: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.
Directive #656: Break Actions - Take a **5-minute phone break** outside before going back inside to play.
Directive #657: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.
Directive #658: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.
Directive #659: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing.
Directive #660: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #661: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #662: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #663: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing.
Directive #664: Break Actions - Walk to the **closest cocktail waitress** and order a **free casino drink**.
Directive #665: Break Actions - Walk to the **closest cocktail waitress** and order a **free casino drink**.
Directive #666: Craps - Bet **4 units on the pass line** if the **last shooter hit two points in a row**.
Directive #667: Break Actions - Grab a **complimentary coffee or tea** and sip it while standing near a lively table.
Directive #668: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.
Directive #669: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**.
Directive #670: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.
Directive #671: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #672: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.
Directive #673: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.
Directive #674: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy.
Directive #675: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy.
Directive #676: Craps - Bet on the **field bet** only if **the last two rolls missed field numbers**.
Directive #677: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #678: Break Actions - Find a **casino lounge** and **sit for 15 minutes** while sipping a drink.
Directive #679: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.
Directive #680: Break Actions - Ask a **pit boss what table is the hottest**, then walk to it and observe before betting.
Directive #681: Craps - Find a **hot craps table (lots of cheering)** and bet **3 units on the pass line**.
Directive #682: Break Actions - Grab a **complimentary coffee or tea** and sip it while standing near a lively table.
Directive #683: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**.
Directive #684: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #685: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy.
Directive #686: Break Actions - Take a **5-minute phone break** outside before going back inside to play.
Directive #687: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #688: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.
Directive #689: Break Actions - Walk to the **bar closest to the high-limit area** and order an **Old Fashioned**.
Directive #690: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #691: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.
Directive #692: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #693: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.
Directive #694: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.
Directive #695: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.
Directive #696: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**.
Directive #697: Break Actions - Take a **casual walk through the high-roller section** without placing a bet.
Directive #698: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**.
Directive #699: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #700: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.
Directive #701: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**.
Directive #702: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #703: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #704: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #705: Break Actions - Take a **quick walk to the nearest drinking fountain** and take a sip before returning.
Directive #706: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #707: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #708: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #709: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.
Directive #710: Break Actions - Take a **deep breath, relax, and count your cash** before placing your next bet.
Directive #711: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.
Directive #712: Break Actions - Take a **casual walk through the high-roller section** without placing a bet.
Directive #713: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.
Directive #714: Break Actions - Take a **5-minute phone break** outside before going back inside to play.
Directive #715: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #716: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #717: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.
Directive #718: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**.
Directive #719: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #720: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #721: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #722: Craps - Find a **table with a new shooter** and bet **the table minimum on pass line first, then adjust strategy**.
Directive #723: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.
Directive #724: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #725: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #726: Break Actions - Find a **comfortable chair in the lounge** and **sit for 10 minutes** before playing again.
Directive #727: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.
Directive #728: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #729: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**.
Directive #730: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**.
Directive #731: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.
Directive #732: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.
Directive #733: Break Actions - Walk to the **casino floor's self-serve drink station** and grab a **free soda**.
Directive #734: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #735: Break Actions - Take a **10-minute break and scroll through social media** before playing again.
Directive #736: Craps - Bet on the **field bet** only if **the last two rolls missed field numbers**.
Directive #737: Break Actions - Find a **slot machine near a bar** and **sit there with a drink without playing**.
Directive #738: Break Actions - Find the **nearest bar** and order a **local beer**. Sip it slowly while watching a game.
Directive #739: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #740: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #741: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.
Directive #742: Break Actions - Take a **5-minute phone break** outside before going back inside to play.
Directive #743: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.
Directive #744: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**.
Directive #745: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.
Directive #746: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #747: Break Actions - Go outside and **breathe fresh air for at least 5 minutes**.
Directive #748: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing.
Directive #749: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.
Directive #750: Break Actions - Find a **casino lounge** and **sit for 15 minutes** while sipping a drink.
Directive #751: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #752: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.
Directive #753: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy.
Directive #754: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #755: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.
Directive #756: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.
Directive #757: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.
Directive #758: Craps - Find a **hot craps table (lots of cheering)** and bet **3 units on the pass line**.
Directive #759: Break Actions - Stop and **watch a game you’ve never played before for 5 minutes**, then decide if you want to try it.
Directive #760: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.
Directive #761: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.
Directive #762: Craps - Look for a table where **the last roll was a 7**. Bet **small on pass line and increase if you win**.
Directive #763: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.
Directive #764: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #765: Break Actions - Find a **casino promotional booth** and ask about any deals or giveaways.
Directive #766: Break Actions - Walk around the **casino floor for exactly 5 minutes** before placing your next bet.
Directive #767: Craps - Bet **4 units on the pass line** if the **last shooter hit two points in a row**.
Directive #768: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #769: Break Actions - Take a **bathroom break** and wash your hands before returning to the tables.
Directive #770: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #771: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.
Directive #772: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #773: Break Actions - Find a **comfortable chair in the lounge** and **sit for 10 minutes** before playing again.
Directive #774: Break Actions - Walk to the **closest cocktail waitress** and order a **free casino drink**.
Directive #775: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #776: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #777: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #778: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.
Directive #779: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.
Directive #780: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.
Directive #781: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing.
Directive #782: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #783: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.
Directive #784: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #785: Break Actions - Walk to the **bar closest to the high-limit area** and order an **Old Fashioned**.
Directive #786: Break Actions - Go to the **nearest bartender** and ask them to **make you their best drink**.
Directive #787: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #788: Craps - Find a **hot craps table (lots of cheering)** and bet **3 units on the pass line**.
Directive #789: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.
Directive #790: Break Actions - Take a **10-minute break and scroll through social media** before playing again.
Directive #791: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #792: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #793: Break Actions - Take a **deep breath, relax, and count your cash** before placing your next bet.
Directive #794: Break Actions - Walk to the **nearest bar** and order a **shot of tequila**. Take it immediately.
Directive #795: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #796: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.
Directive #797: Break Actions - Find the **nearest bar** and order a **local beer**. Sip it slowly while watching a game.
Directive #798: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #799: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**.
Directive #800: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #801: Break Actions - Find a **slot machine near a bar** and **sit there with a drink without playing**.
Directive #802: Break Actions - Find a **comfortable chair in the lounge** and **sit for 10 minutes** before playing again.
Directive #803: Craps - Look for a table where **the last roll was a 7**. Bet **small on pass line and increase if you win**.
Directive #804: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.
Directive #805: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.
Directive #806: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #807: Break Actions - Walk to the **bar closest to the high-limit area** and order an **Old Fashioned**.
Directive #808: Craps - Bet **4 units on the pass line** if the **last shooter hit two points in a row**.
Directive #809: Craps - Look for a table where **the last roll was a 7**. Bet **small on pass line and increase if you win**.
Directive #810: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #811: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #812: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #813: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**.
Directive #814: Craps - Bet **4 units on the pass line** if the **last shooter hit two points in a row**.
Directive #815: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.
Directive #816: Break Actions - Go to the **casino's sports bar** and **watch a game for 10 minutes before returning**.
Directive #817: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.
Directive #818: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**.
Directive #819: Break Actions - Go to the **casino's sports bar** and **watch a game for 10 minutes before returning**.
Directive #820: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #821: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.
Directive #822: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #823: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #824: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**.
Directive #825: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #826: Break Actions - Find a **casino promotional booth** and ask about any deals or giveaways.
Directive #827: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**.
Directive #828: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #829: Break Actions - Walk to the **bar closest to the high-limit area** and order an **Old Fashioned**.
Directive #830: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #831: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #832: Break Actions - Walk to the **casino floor's self-serve drink station** and grab a **free soda**.
Directive #833: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #834: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy.
Directive #835: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #836: Break Actions - Find a **comfortable chair in the lounge** and **sit for 10 minutes** before playing again.
Directive #837: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.
Directive #838: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.
Directive #839: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #840: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**.
Directive #841: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #842: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #843: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #844: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #845: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #846: Break Actions - Walk around the **casino floor for exactly 5 minutes** before placing your next bet.
Directive #847: Craps - Place a **come bet** only after the shooter **rolls at least one point**.
Directive #848: Break Actions - Find the **nearest bar** and order a **local beer**. Sip it slowly while watching a game.
Directive #849: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.
Directive #850: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #851: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #852: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #853: Break Actions - Take a **10-minute break and scroll through social media** before playing again.
Directive #854: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.
Directive #855: Craps - Bet on the **field bet** only if **the last two rolls missed field numbers**.
Directive #856: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #857: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #858: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**.
Directive #859: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #860: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #861: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #862: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.
Directive #863: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.
Directive #864: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #865: Blackjack - If the dealer is **showing a 5 or 6**, double down on **11** no matter what.
Directive #866: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #867: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #868: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #869: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #870: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #871: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.
Directive #872: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #873: Break Actions - Take a **10-minute break and scroll through social media** before playing again.
Directive #874: Craps - Find a **table with a new shooter** and bet **the table minimum on pass line first, then adjust strategy**.
Directive #875: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #876: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #877: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.
Directive #878: Break Actions - Walk to the **nearest food stand and grab a snack** before returning.
Directive #879: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.
Directive #880: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.
Directive #881: Break Actions - Take a **deep breath, relax, and count your cash** before placing your next bet.
Directive #882: Break Actions - Take a **casual walk through the high-roller section** without placing a bet.
Directive #883: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.
Directive #884: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.
Directive #885: Slots - Locate a **loud slot machine with flashing lights**. Bet **max for exactly 3 spins**.
Directive #886: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.
Directive #887: Break Actions - Take a **10-minute break and scroll through social media** before playing again.
Directive #888: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**.
Directive #889: Break Actions - Find a **TV screen showing live sports** and stand there for 10 minutes before playing again.
Directive #890: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.
Directive #891: Break Actions - Find the **nearest bar** and order a **local beer**. Sip it slowly while watching a game.
Directive #892: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**.
Directive #893: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**.
Directive #894: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #895: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #896: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #897: Craps - Find a **table with a new shooter** and bet **the table minimum on pass line first, then adjust strategy**.
Directive #898: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #899: Break Actions - Take a **10-minute break and scroll through social media** before playing again.
Directive #900: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.
Directive #901: Blackjack - Sit at a blackjack table with a **minimum bet of $15 or higher**. Bet conservatively for 3 rounds before increasing.
Directive #902: Break Actions - Find a **casino lounge** and **sit for 15 minutes** while sipping a drink.
Directive #903: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.
Directive #904: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**.
Directive #905: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #906: Break Actions - Take a **casual walk through the high-roller section** without placing a bet.
Directive #907: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #908: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #909: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #910: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #911: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**.
Directive #912: Break Actions - Take a **quick walk to the nearest drinking fountain** and take a sip before returning.
Directive #913: Craps - Bet on the **field bet** only if **the last two rolls missed field numbers**.
Directive #914: Break Actions - Take a **bathroom break** and wash your hands before returning to the tables.
Directive #915: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.
Directive #916: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #917: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #918: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win.
Directive #919: Blackjack - Find a **blackjack table near a VIP area** and buy in for an odd amount ($27, $33, etc.) just for luck.
Directive #920: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**.
Directive #921: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #922: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #923: Break Actions - Find a **casino promotional booth** and ask about any deals or giveaways.
Directive #924: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #925: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #926: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #927: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #928: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.
Directive #929: Blackjack - Split **8s and Aces** at the next available blackjack table, no matter the dealer's card.
Directive #930: Break Actions - Walk to the **nearest food stand and grab a snack** before returning.
Directive #931: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #932: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.
Directive #933: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.
Directive #934: Craps - Find a **hot craps table (lots of cheering)** and bet **3 units on the pass line**.
Directive #935: Break Actions - Walk to the **closest cocktail waitress** and order a **free casino drink**.
Directive #936: Craps - If you see a player **pressing their bets aggressively**, match their come bet for one roll.
Directive #937: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #938: Slots - Locate an **Egyptian-themed slot machine** and play **10 spins at minimum bet** before deciding to increase.
Directive #939: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #940: Break Actions - Take a **bathroom break** and wash your hands before returning to the tables.
Directive #941: Break Actions - Walk to the **VIP section and pretend to belong there** for 5 minutes before returning.
Directive #942: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #943: Break Actions - Walk to the **bar closest to the high-limit area** and order an **Old Fashioned**.
Directive #944: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #945: Break Actions - Take a **deep breath, relax, and count your cash** before placing your next bet.
Directive #946: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.
Directive #947: Break Actions - Walk around the **casino floor for exactly 5 minutes** before placing your next bet.
Directive #948: Blackjack - If the dealer **pulls three face cards in a row**, lower your bet for the next hand.
Directive #949: Slots - Look for a **slot machine where someone just walked away after a long session**. Bet **max for 5 spins**.
Directive #950: Break Actions - Find a **slot machine near a bar** and **sit there with a drink without playing**.
Directive #951: Roulette - Find a table with a **digital history board**. Bet on the dozen that appeared the least in the last 20 spins.
Directive #952: Roulette - Locate the **nearest roulette table with an empty seat** and bet 2 units on a **street bet (covering 3 numbers)**.
Directive #953: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #954: Roulette - Find the **closest, loudest roulette table** and bet 3 units on the outside - 1-18.
Directive #955: Break Actions - Walk to the **casino floor's self-serve drink station** and grab a **free soda**.
Directive #956: Break Actions - Find a **slot machine near a bar** and **sit there with a drink without playing**.
Directive #957: Craps - Bet **4 units on the pass line** if the **last shooter hit two points in a row**.
Directive #958: Roulette - Walk to a **European roulette table (single zero)** and place 3 units on the **even money bet** with the longest losing streak.
Directive #959: Break Actions - Find a **bar and order a random drink** from the menu without looking.
Directive #960: Break Actions - Stop and **watch a game you’ve never played before for 5 minutes**, then decide if you want to try it.
Directive #961: Slots - Walk to the **closest slot machine with an animal theme** and bet **max bet for 3 spins**.
Directive #962: Break Actions - Take a **deep breath, relax, and count your cash** before placing your next bet.
Directive #963: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.
Directive #964: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #965: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.
Directive #966: Blackjack - Find a **blackjack table where the dealer just got a blackjack**. Bet 3 units and follow basic strategy.
Directive #967: Break Actions - Find a **TV screen showing live sports** and stand there for 10 minutes before playing again.
Directive #968: Slots - Walk to the **nearest progressive jackpot slot**. Bet **2 units per spin for 10 spins**.
Directive #969: Roulette - Find a roulette table **in a high-traffic area** and bet 1 unit on **two adjacent single numbers**.
Directive #970: Blackjack - Walk to the **nearest full blackjack table** and bet **1 unit on the first hand** to feel out the dealer.
Directive #971: Break Actions - Take a **quick walk to the nearest drinking fountain** and take a sip before returning.
Directive #972: Break Actions - Take a **5-minute phone break** outside before going back inside to play.
Directive #973: Break Actions - Go to the **nearest bartender** and ask them to **make you their best drink**.
Directive #974: Craps - Place a **come bet** only after the shooter **rolls at least one point**.
Directive #975: Slots - Find a **Wheel of Fortune slot**. Spin **exactly 7 times** at minimum bet and then move if no win.
Directive #976: Roulette - Locate a table where **the last five spins were red**. Bet **4 units on black**.
Directive #977: Craps - Bet on the **field bet** only if **the last two rolls missed field numbers**.
Directive #978: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #979: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.
Directive #980: Craps - If you see a player **pressing their bets aggressively**, match their come bet for one roll.
Directive #981: Slots - Find a **penny slot machine with a high volatility rating**. Bet **5 spins at half-max bet**.
Directive #982: Slots - Find the **nearest slot machine with a jackpot over $100,000** and bet **min for 15 spins**.
Directive #983: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #984: Break Actions - Take a **10-minute break and scroll through social media** before playing again.
Directive #985: Break Actions - Take a **10-minute break and scroll through social media** before playing again.
Directive #986: Blackjack - Locate a **table with a dealer showing a 6 as their upcard**. Bet **2 units** and play conservatively.
Directive #987: Roulette - Bet **3 units on black** at a table where the last spin was **green (0 or 00)**.
Directive #988: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.
Directive #989: Roulette - Find a table where the **last three numbers were all even**. Bet 3 units on odd.
Directive #990: Roulette - If you see a table with **a recent streak of the same color** (4 or more), bet **opposite for 2 rounds**.
Directive #991: Slots - Find a slot **near the cashier** and bet **min for 10 spins, then increase to max for 3 spins**.
Directive #992: Break Actions - Head to the **casino gift shop** and buy something under $10 before going back to play.
Directive #993: Blackjack - Find a **blackjack table where players seem happy** and bet **3 units on your first hand**.
Directive #994: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.
Directive #995: Craps - Find a **table with at least one high roller** and bet the same amount as their first roll.
Directive #996: Craps - Find a **hot craps table (lots of cheering)** and bet **3 units on the pass line**.
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

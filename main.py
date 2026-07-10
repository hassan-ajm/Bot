import time
import sys
from javascript import require, On

mineflayer = require('mineflayer')

print("=== DEPLOYING MINECRAFT BOT ===", flush=True)

try:
    bot = mineflayer.createBot({
        'host': 'your.server.ip',       # <-- Double check this is correct!
        'port': 25565,
        'username': 'YourMicrosoftEmail@gmail.com',
        'auth': 'microsoft'
    })
    print("Bot object created successfully. Authenticating...", flush=True)
except Exception as e:
    print(f"Failed to initialize bot constructor: {e}", flush=True)

@On(bot, 'login')
def handle_login(*args):
    print("Bot successfully logged into the proxy cluster network!", flush=True)

@On(bot, 'spawn')
def handle_spawn(*args):
    print("Bot spawned into Lobby instance. Waiting 5 seconds...", flush=True)
    time.sleep(5)
    
    try:
        print("Attempting to select hotbar slot 0...", flush=True)
        bot.setQuickBarSlot(0)
        time.sleep(1)
        print("Attempting to right-click item...", flush=True)
        bot.activateItem()
        print("Item activated. Awaiting inventory chest menu window...", flush=True)
    except Exception as e:
        print(f"Lobby navigation error: {e}", flush=True)

@On(bot, 'windowOpen')
def handle_window(window, *args):
    print(f"Inventory menu detected! Title: {window.title}", flush=True)
    time.sleep(2) 
    
    survival_slot = 15 
    try:
        print(f"Clicking custom survival portal slot: {survival_slot}", flush=True)
        bot.clickWindow(survival_slot, 0, 0)
        print("Click sent! Checking if transferred to survival...", flush=True)
    except Exception as e:
        print(f"Failed to execute menu click: {e}", flush=True)

@On(bot, 'error')
def handle_error(err, *args):
    print(f"Mineflayer Core Error encountered: {err}", flush=True)

@On(bot, 'kicked')
def handle_kick(reason, loggedIn, *args):
    print(f"Bot was kicked from the server. Reason: {reason}", flush=True)

# Keep process alive
try:
    while True:
        time.sleep(60)
        if not bot.currentWindow:
            try:
                bot.setControlState('jump', True)
                bot.setControlState('jump', False)
            except:
                pass
except KeyboardInterrupt:
    print("Process terminated manually.", flush=True)
    sys.exit()

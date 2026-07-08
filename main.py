import time
import sys
from javascript import require, On

mineflayer = require('mineflayer')

print("Starting Minecraft Bot on GitHub Actions...")
bot = mineflayer.createBot({
    'host': 'play.legocraft.net',       # <-- Replace with your server IP
    'port': 25565,
    'username': 'craftmeplz8@gmail.com', # <-- Your premium email
    'auth': 'microsoft'
})

@On(bot, 'spawn')
def handle_spawn(*args):
    print("Bot spawned in Lobby. Waiting 5 seconds...")
    time.sleep(5)
    
    try:
        bot.setQuickBarSlot(0)
        print("Holding lobby item...")
        time.sleep(1)
        bot.activateItem()
        print("Opened menu. Waiting 2 seconds...")
    except Exception as e:
        print(f"Error: {e}")

@On(bot, 'windowOpen')
def handle_window(window, *args):
    print(f"Menu opened: {window.title}")
    time.sleep(2) 
    
    survival_slot = 15 # Row 2, Slot 7
    try:
        print(f"Clicking slot {survival_slot}...")
        bot.clickWindow(survival_slot, 0, 0)
        print("Transferred to survival! Standing AFK now...")
    except Exception as e:
        print(f"Failed to click: {e}")

# Simple loop to keep the script running on the cloud server
try:
    while True:
        time.sleep(60)
        if not bot.currentWindow:
            bot.setControlState('jump', True)
            bot.setControlState('jump', False)
except KeyboardInterrupt:
    print("Stopping bot.")
    sys.exit()

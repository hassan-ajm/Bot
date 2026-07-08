import os
import threading
import time
from flask import Flask
from javascript import require, On

app = Flask(__name__)

@app.route('/')
def home():
    return "AFK Bot is running!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

mineflayer = require('mineflayer')

def run_bot():
    print("Starting Minecraft Bot with Microsoft Auth...")
    bot = mineflayer.createBot({
        'host': 'play.legocraft.net',       # <-- Replace with your server IP
        'port': 25565,
        'username': 'craftmeplz8@gmail.com', # <-- Your premium email
        'auth': 'microsoft'
    })

    @On(bot, 'spawn')
    def handle_spawn(*args):
        print("Bot spawned in Lobby. Waiting 5 seconds for world to load...")
        time.sleep(5)
        
        # 1. Equip the item in Hotbar Slot 0 (First slot)
        try:
            bot.setQuickBarSlot(0)
            print("Holding lobby item...")
            time.sleep(1)
            
            # Right-click the air/item to open the proxy menu
            bot.activateItem()
            print("Right-clicked item. Waiting for menu to open...")
        except Exception as e:
            print(f"Error using hotbar item: {e}")

    @On(bot, 'windowOpen')
    def handle_window(window, *args):
        print(f"Menu opened: {window.title}")
        time.sleep(2) # Give it a second to render slots safely
        
        # In Minecraft code, a single chest row is 9 slots. 
        # Row 1 is slots 0-8. 
        # Row 2, Slot 7 is absolute Slot ID 15.
        survival_slot = 15 
        
        try:
            print(f"Clicking slot {survival_slot} for Survival...")
            bot.clickWindow(survival_slot, 0, 0)
            print("Successfully clicked! Transferring to survival...")
        except Exception as e:
            print(f"Failed to click menu slot: {e}")

    # Anti-AFK Loop running in the background after transfer
    def anti_afk():
        while True:
            time.sleep(60)
            try:
                # Only try to jump if we aren't in a menu window anymore
                if not bot.currentWindow:
                    bot.setControlState('jump', True)
                    bot.setControlState('jump', False)
            except:
                pass

    threading.Thread(target=anti_afk, daemon=True).start()

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    run_bot()
import os
import discord
import asyncio
from flask import Flask
from threading import Thread

# --- Flask server to stay alive ---
app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_web).start()

# --- Discord client setup ---
TOKEN = os.getenv("DISCORD_TOKEN")
client = discord.Client()

# --- Dynamic collection setup ---
raw_collection = os.getenv("COLLECTION", "")
poke_triggers = [poke.strip() for poke in raw_collection.split(",") if poke.strip()]
response_prefix = "<@716390085896962058> c "

@client.event
async def on_ready():
    print("✅ Selfbot is running in invisible mode")
    await client.change_presence(status=discord.Status.invisible)

@client.event
async def on_message(message):
    # Only respond to messages from app ID 854233015475109888
    if message.author.id != 854233015475109888:
        return
    
    content = message.content.strip()
    
    for trigger in poke_triggers:
        if content.startswith(trigger):
            try:
                poke_name = trigger.replace(":", "")
                response = f"{response_prefix}{poke_name}"
                
                # Wait 3 seconds before sending the response
                print(f"⏳ Collection detected: {poke_name}. Waiting 3 seconds...")
                await asyncio.sleep(3)
                
                await message.channel.send(response)
                print(f"✅ Sent after delay: {response}")
            except Exception as e:
                print(f"❌ Error sending response for {poke_name}: {e}")
            break

client.run(TOKEN)

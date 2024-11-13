# I cannot take credit for a lot in this program, some was taken from this link: https://www.geeksforgeeks.org/python-using-pil-imagegrab-and-pytesseract/
# GitHub copilot was also used heavily.

# This will only work with OP Autoclicker for Windows.
# Once you run the code, set your autoclicker delay to 2.7 seconds, and place it over the top right of the 'Farm' button.

# Main difference between this and the 'main' branch is that this one creates a bot that can be used to kill the script if needed.
# I will not offer support for this branch.

import discord
from discord.ext import commands
import asyncio
import os
import signal
import threading

# Your existing imports
import numpy as nm
import time
import pytesseract
import cv2
from PIL import ImageGrab
import pyautogui
import re


# Discord bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
botToken = "REPLACE THIS WITH YOUR BOT TOKEN"

# Function to kill the script and the task "AutoClicker.exe"
def kill_script():
    # Kill the AutoClicker task and the current script
    os.system("taskkill /f /im AutoClicker.exe")
    os.kill(os.getpid(), signal.SIGTERM)


# Slash command to bring up an embed with a button to kill the script
@bot.tree.command(name="access", description="Access control for the script")
async def access(interaction: discord.Interaction):
    embed = discord.Embed(title="Control Panel", description="Click the button below to kill the script.", color=0x00ff00)
    button = discord.ui.Button(label="Kill Script", style=discord.ButtonStyle.danger)

    async def button_callback(interaction: discord.Interaction):
        await interaction.response.send_message("Killing the script...", ephemeral=True)
        kill_script()

    button.callback = button_callback
    view = discord.ui.View()
    view.add_item(button)
    await interaction.response.send_message(embed=embed, view=view)

# When the bot starts up, print the following to console.
@bot.event
async def on_ready():
    print("Bot is ready")
    print(discord.__version__)
    await bot.tree.sync(guild=None)  # Sync commands globally

# Start the bot
async def main():
    async with bot:
        await bot.start(botToken)

# Your existing function
def imToString():
    # Path of tesseract executable 
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    while True:
        # ImageGrab-To capture the screen image in a loop.  
        # Bbox used to capture a specific area.
        cap = ImageGrab.grab(bbox=(612, 967, 1450, 1226))
        # You most likely WILL have to change this value to fit your screen resolution, I have a 2560x1440 monitor so this is the value I used.
        # I used this program: https://sourceforge.net/projects/mpos/
  
        # Converted the image to monochrome for it to be easily  
        # read by the OCR and obtained the output String. 
        tesstr = pytesseract.image_to_string(
            cv2.cvtColor(nm.array(cap), cv2.COLOR_BGR2GRAY),
            lang='eng')
        print(tesstr)
        # Extract the code after "to continue playing:"
        if "to continue playing:" in tesstr:
            match = re.search('to continue playing: (\w+)', tesstr)
            if match:
                code = match.group(1)
                # Sends the /verify command to auto verify you
                pyautogui.typewrite(f"/verify {code}")
                pyautogui.press("enter")
                time.sleep(2)
                pyautogui.press("enter")
                time.sleep(2)
        if "Dismiss message" in tesstr:
            # Find the location of the "Dismiss message" text on the screen
            dismiss_location = pyautogui.locateCenterOnScreen("dismiss_message.png", confidence=0.8)
            if dismiss_location:
                # Click on the "Dismiss message" text
                pyautogui.click(dismiss_location)
                time.sleep(2)
                # Teleport the mouse to coordinates 816, 1144. These are the coordinates of the "Farm" button, and will have to change depending on your screen resolution.
                pyautogui.moveTo(816, 1144)

# Run the bot and the script
def run_bot():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot is shutting down...")
        asyncio.run(bot.close())

def run_imToString():
    imToString()

# Start the bot in a separate thread
bot_thread = threading.Thread(target=run_bot)
bot_thread.start()

# Run the imToString function
run_imToString()

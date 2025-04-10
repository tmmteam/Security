from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import time

# ----------- Bot Config -------------
API_ID = 22243185
API_HASH = "39d926a67155f59b722db787a23893ac"
BOT_TOKEN = "7018151520:AAFUQvBVucwn74A1dQFRjRpCkn8fSgjD9fA"
OWNER_ID = 5311223486

app = Client("GroupSecurityBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ----------- Banned Words & Links -------------
ABUSE_WORDS = ["cp", "ncert", "physics wallah", "aakash", "byjus", "dick", "madarchod", "bsdk", "sex", "asshole", "lund", "randi", "lode"]

def contains_link(text):
    return any(x in text for x in ["http://", "https://", "t.me", "www."])

# ----------- Start Command -------------
@app.on_message(filters.command("start"))
async def start(client, message):
    buttons = [
        [InlineKeyboardButton("👑 Owner", url="https://t.me/moh_maya_official"),
         InlineKeyboardButton("📢 Update", url="https://t.me/otploothub")],
        [InlineKeyboardButton("➕ Add to Group", url=f"https://t.me/{(await client.get_me()).username}?startgroup=true")]
    ]
    await message.reply_photo(
        photo="https://graph.org/file/e7d8fcbcd6b0ba2b334d5-431de28784638bf363.jpg",
        caption=(
            "🤖 𝖦𝗋𝗈𝗎𝗉 𝖲𝖾𝖼𝗎𝗋𝗂𝗍𝗒 𝖱𝗈𝖻𝗈𝗍 🛡️\n\n"
            "Welcome to GroupSecurityRobot, your vigilant guardian in this Telegram space!
Our mission is to ensure a secure and pleasant environment for everyone.
From copyright protection to maintaining decorum, we've got it covered.
Feel free to report any concerns, and let's work together to make this community thrive! 🤝🔐"
        ),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ----------- Ping Command -------------
@app.on_message(filters.command("ping"))
async def ping(_, message):
    start = time.time()
    m = await message.reply("Pinging...")
    end = time.time()
    await m.edit(f"Pong! {round((end - start) * 1000)} ms")

# ----------- Notify When Bot Added to Group -------------
@app.on_chat_member_updated()
async def joined_group(client, member):
    if member.new_chat_member.user.id == (await client.get_me()).id:
        await client.send_message(OWNER_ID, f"✅ Bot added to group: {member.chat.title} ({member.chat.id})")

# ----------- Monitor Group Messages -------------
@app.on_message(filters.group & filters.text)
async def monitor_messages(client, message: Message):
    text = message.text.lower()
    user_mention = message.from_user.mention

    if contains_link(text):
        await message.delete()
        await message.reply(f"{user_mention} Don't send links here ❌")

    elif len(text.split()) > 250:
        await message.delete()
        await message.reply(f"{user_mention} More than 250 words not allowed ⚠️")

    elif any(bad in text for bad in ABUSE_WORDS):
        await message.delete()
        await message.reply(f"{user_mention} Abuse mat karo yaha 😡")

# ----------- Delete Edited Messages -------------
@app.on_edited_message(filters.group)
async def edited_message_check(client, message):
    try:
        await message.delete()
        await message.reply(f"{message.from_user.mention} Edited messages not allowed!")
    except Exception as e:
        print("Error deleting edited message:", e)

# ----------- Block All Document Files -------------
@app.on_message(filters.group & filters.document)
async def block_documents(client, message):
    try:
        await message.delete()
        await message.reply(f"{message.from_user.mention} File not allowed.")
    except Exception as e:
        print(f"Error deleting document: {e}")

# ----------- Also Delete Edited Documents -------------
@app.on_edited_message(filters.group & filters.document)
async def edited_documents(client, message):
    try:
        await message.delete()
        await message.reply(f"{message.from_user.mention} Edited file not allowed.")
    except Exception as e:
        print(f"Error deleting edited document: {e}")

# ----------- Run the Bot -------------
print("Bot is running...")
app.run()

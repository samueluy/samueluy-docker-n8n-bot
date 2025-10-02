import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import MessageHandler, filters

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 📌 Links to your platforms
GITHUB_LINK = "https://github.com/samueluy/sql-basics-2025"
TIKTOK_LINK = "https://www.tiktok.com/@samueluyyt"
YOUTUBE_LINK = "https://www.youtube.com/samueluy"
LINKEDIN_LINK = "https://www.linkedin.com/in/samueluy/"

# 🔘 Reusable button layout
# Main keyboard: SQL Basics, Links, About, Help
MAIN_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("📘 SQL Basics", url=GITHUB_LINK)],
    [InlineKeyboardButton("🔗 Links", callback_data="show_links")],
    [InlineKeyboardButton("ℹ️ About", callback_data="about")],
    [InlineKeyboardButton("❓ Help", callback_data="help")],
])

# Links keyboard: TikTok, YouTube, LinkedIn
LINKS_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("🎵 TikTok", url=TIKTOK_LINK)],
    [InlineKeyboardButton("🎥 YouTube", url=YOUTUBE_LINK)],
    [InlineKeyboardButton("💼 LinkedIn", url=LINKEDIN_LINK)],
    [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")],
])

# On join handler
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(
            f"👋 Welcome, {member.full_name}!\n\n"
            "💡 Here's something to get you started:\n"
            "• <b>SQL Basics Scripts</b>: https://github.com/samueluy/sql-basics-2025\n"
            "• 📥 More freebies coming soon in this channel!\n\n"
            "Tap /start anytime to access the full menu.",
            reply_markup=MAIN_KEYBOARD,
            parse_mode="HTML"
        )

# 🧠 Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to the channel toolkit!\nClick a button below to explore 👇",
        reply_markup=MAIN_KEYBOARD
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message or update.callback_query.message
    await message.reply_text(
        "<b>❓ Help Guide</b>\n\n"
        "Here are a few commands to get you started:\n\n"
        "👉 /start — Show main menu\n"
        "👉 /links — View all my social & content links\n"
        "👉 /sqlbasics — Go directly to the SQL practice repo\n"
        "👉 /about — Learn more about what I do\n\n"
        "Use the buttons for easier navigation.\n\n"
        "Let’s build and grow together 🚀",
        parse_mode="HTML"
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message or update.callback_query.message
    await message.reply_text(
        "<b>👋 About Me</b>\n\n"
        "I’m <b>Sam</b> — a data engineer and content creator.\n\n"
        "Join a community of <b>builders, dreamers, and self-starters</b> as I share:\n"
        "📈 Productivity, digital systems, & self-growth\n"
        "🧠 Learn programming and digital tools\n\n"
        "For those who want to be more than average.\n\n"
        "🔗 Explore more using /links or visit my GitHub for projects like SQL Basics!",
        parse_mode="HTML"
    )


# Callback query handler for inline buttons
from telegram.ext import CallbackQueryHandler

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "show_links":
        await query.edit_message_text(
            "🔗 Explore my content through the buttons below:",
            reply_markup=LINKS_KEYBOARD
        )
    elif query.data == "back_to_main":
        await query.edit_message_text(
            "👋 Welcome to the channel toolkit!\nClick a button below to explore 👇",
            reply_markup=MAIN_KEYBOARD
        )
    elif query.data == "about":
        await about(update, context)
    elif query.data == "help":
        await help_command(update, context)

# 🛠 App Setup
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("about", about))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

print("🤖 Bot is running with button support...")
app.run_polling()

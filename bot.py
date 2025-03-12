import telebot
from telebot import types
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables
TOKEN = os.getenv('BOT_TOKEN', '7322761418:AAHPd0ft2xRClfHBRZ2pmEmPEhBRkisNWrw')
ADMIN_ID = os.getenv('ADMIN_ID', '7053349365')

bot = telebot.TeleBot(TOKEN)

# Start komandasi uchun
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    contact_btn = types.KeyboardButton('📝 Leave Message')
    portfolio_btn = types.KeyboardButton('🌐 Portfolio Website')
    about_btn = types.KeyboardButton('ℹ️ About Me')
    
    markup.add(portfolio_btn)
    markup.add(contact_btn, about_btn)
    
    welcome_text = f"""
⭐ *Welcome to My Portfolio Bot* ⭐

Hello [*{user.first_name}*](tg://user?id={user.id}) 👋

I'm glad to see you here\. You can:

📌 Visit my portfolio website
📝 Send me a message
ℹ️ Learn more about my work

Choose an option below 👇
"""
    
    bot.send_message(message.chat.id, welcome_text, parse_mode='MarkdownV2', reply_markup=markup)

# Portfolio website havolasi
@bot.message_handler(func=lambda message: message.text == '🌐 Portfolio Website')
def portfolio_link(message):
    markup = types.InlineKeyboardMarkup()
    portfolio_button = types.InlineKeyboardButton(
        text="Visit Portfolio", 
        url="https://t.me/komilovITbot/earth"
    )
    markup.add(portfolio_button)
    bot.reply_to(message, "Check out my portfolio website! 🚀", reply_markup=markup)

# About me ma'lumoti
@bot.message_handler(func=lambda message: message.text == 'ℹ️ About Me')
def about_me(message):
    about_text = """
🎯 <b>Front-end Developer</b>
<pre title="Technical Skills">
<b>Technical Skills:</b>

└─ 💻 Core:
|    ├─ HTML5
|    ├─ CSS3
|    └─ JavaScript
|
└─ 🛠 Frameworks:
|    ├─ React.js (soon)
|    └─ Next.js (soon)
|
└─ 📱 Expertise:
|    ├─ Responsive Design
|    ├─ UI/UX Development
|    ├─ Interactive Animations
|    └─ Clean Code
</pre>

<b>Let's create something amazing together!</b> ✨
"""
    bot.reply_to(message, about_text, parse_mode='HTML')

# Xabar qoldirish
@bot.message_handler(func=lambda message: message.text == '📝 Leave Message')
def ask_message(message):
    msg = bot.reply_to(message, """
✍️ *Please write your message:*

I'll receive your message directly and respond as soon as possible.
    """, parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_message)

def process_message(message):
    user = message.from_user
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Admin uchun xabar formati
    admin_message = f"""
📨 <b>New Message Received!</b>

👤 From: <a href="tg://user?id={user.id}">{user.first_name}</a>
💠 ID: <code>{user.id}</code>
🔗 Username: @{user.username}
🕒 Time: <code>{timestamp}</code>

💬 <b>Message:</b>
<pre>{message.text}</pre>
"""
    
    # Adminga xabarni yuborish
    bot.send_message(ADMIN_ID, admin_message, parse_mode='HTML')
    
    # Foydalanuvchiga tasdiqlash xabari
    thank_you = "Thank you! Your message has been sent. I'll get back to you soon! 🙂"
    bot.reply_to(message, thank_you)

# Botni ishga tushirish
if __name__ == "__main__":
    print("Bot started...")
    bot.polling(none_stop=True)

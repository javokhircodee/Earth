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
    
    markup.add( portfolio_btn)
    markup.add(contact_btn, about_btn)
    
    welcome_text = f"Hello {user.first_name}! 👋\n\n" \
                   "Welcome to my portfolio bot. Here you can:\n" \
                   "• Leave me a message\n" \
                   "• Visit my portfolio website\n" \
                   "• Learn more about me and my work"
    
    bot.reply_to(message, welcome_text, reply_markup=markup)

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
🎯 Front-end Developer

Skills:
• HTML5, CSS3, JavaScript
• React, Next.js
• Responsive Design
• UI/UX Development
• Interactive Animations
• Clean Code

Let's create something amazing together! 
    """
    bot.reply_to(message, about_text)

# Xabar qoldirish
@bot.message_handler(func=lambda message: message.text == '📝 Leave Message')
def ask_message(message):
    msg = bot.reply_to(message, "Please write your message:")
    bot.register_next_step_handler(msg, process_message)

def process_message(message):
    user = message.from_user
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Admin uchun xabar formati
    admin_message = f"New message!\n\n" \
                    f"From: {user.first_name} ({user.id})\n" \
                    f"Username: @{user.username}\n" \
                    f"Time: {timestamp}\n\n" \
                    f"Message: {message.text}"
    
    # Adminga xabarni yuborish
    bot.send_message(ADMIN_ID, admin_message)
    
    # Foydalanuvchiga tasdiqlash xabari
    thank_you = "Thank you! Your message has been sent. I'll get back to you soon! 🙂"
    bot.reply_to(message, thank_you)

# Botni ishga tushirish
if __name__ == "__main__":
    print("Bot started...")
    bot.polling(none_stop=True)

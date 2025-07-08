from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

BOT_TOKEN = "7685546954:AAGRrliSFDU0lwQR-xmxLi7zFjo3DbQ50Ow"
ADMIN_ID = 6059547931

products = {
    "💵100+5 gold - 10.000 uzs": ("100+5 gold", "10.000 uzs"),
    "💵300+20 gold - 30.000 uzs": ("300+20 gold", "30.000 uzs"),
    "💵500+40 gold - 50.000 uzs": ("500+40 gold", "50.000 uzs"),
    "💵1000+100 gold - 100.000 uzs": ("1000+100 gold", "100.000 uzs"),
    "💵3000+260 gold - 300.000 uzs": ("3000+260 gold", "300.000 uzs"),
    "💵5000+800 gold - 500.000 uzs": ("5000+800 gold", "500.000 uzs"),
    "🎁Pass elite - 40.000 uzs": ("Pass elite", "40.000 uzs"),
    "🎁Pass premium - 95.000 uzs": ("Pass premium", "95.000 uzs"),
    "⏫LEVEL UP PASS - 25.000 uzs": ("LEVEL UP PASS", "25.000 uzs"),
    "Ultra Qurol Ceysi - 7.500 uzs": ("Ultra Qurol Ceysi", "7.500 uzs"),
}

user_orders = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[InlineKeyboardButton(text=p, callback_data=p)] for p in products.keys()]
    await update.message.reply_text("NRAXLAR : ✅", reply_markup=InlineKeyboardMarkup(buttons))

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    product = query.data
    context.user_data["product"] = product
    await query.message.reply_text("🆔ID Yuboring‼️ (faqat raqam)")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text("❌ Iltimos, ID faqat raqamlardan iborat bo‘lishi kerak.")
        return

    product = context.user_data.get("product")
    if not product:
        await update.message.reply_text("Iltimos, avval narxni tanlang.")
        return

    game_id = text
    gold, price = products[product]
    context.user_data["game_id"] = game_id

    msg = f"""💠 Buyurtma tafsilotlari:
GOLD: {gold}
ID: {game_id}
TO‘LOV: {price}

💳5614684900089135
👤N.Muborak
📱+998.99.546.74.10

‼️Iltimos belgilangan summadan kam summa yubormang va komissiya ham esdan chiqmasin‼️
Aks holda buyurtma bajarilmasligi mumkin‼️

To‘lov amalga oshganini isbotlovchi chek (1ta rasm shaklida) yuborish esdan chiqmasin ‼️
"""
    await update.message.reply_text(msg)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    product = context.user_data.get("product")
    game_id = context.user_data.get("game_id")

    if not product or not game_id:
        await update.message.reply_text("Iltimos avval buyurtmani to‘liq kiriting.")
        return

    gold, _ = products[product]
    order_id = len(user_orders) + 1
    user_orders[order_id] = (user.username, gold, game_id)

    msg = f"""✅ Yangi buyurtma:

User name: @{user.username}
GOLD: {gold}
ID: {game_id}
Buyurtma raqami: #{order_id}
"""
    await context.bot.send_message(chat_id=ADMIN_ID, text=msg)
    await context.bot.send_photo(chat_id=ADMIN_ID, photo=update.message.photo[-1].file_id)

    await update.message.reply_text("✅ Buyurtmangiz qabul qilindi! Tez orada admin siz bilan bog‘lanadi.")

    buttons = [[InlineKeyboardButton(text=p, callback_data=p)] for p in products.keys()]
    await update.message.reply_text("Yana buyurtma berish uchun narxni tanlang 👇", reply_markup=InlineKeyboardMarkup(buttons))

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("🤖 Bot ishga tushdi...")
    app.run_polling()
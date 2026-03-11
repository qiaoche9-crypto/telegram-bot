from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8650831871:AAEHyD85CTuSmMvM12RelKKhYjM7uWeHaKo"
ADMIN_ID = 7610608498

msg_user = {}

async def forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id

    if user.username:
        username = "@" + user.username
    else:
        username = user.first_name

    # 转发用户消息
    sent = await context.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=update.message.chat_id,
        message_id=update.message.message_id
    )

    # 记录消息对应用户
    msg_user[sent.message_id] = user_id


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id != ADMIN_ID:
        return

    if update.message.reply_to_message:
        reply_id = update.message.reply_to_message.message_id

        if reply_id in msg_user:
            user_id = msg_user[reply_id]

            await context.bot.copy_message(
                chat_id=user_id,
                from_chat_id=ADMIN_ID,
                message_id=update.message.message_id
            )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(~filters.Chat(ADMIN_ID), forward))
app.add_handler(MessageHandler(filters.Chat(ADMIN_ID), reply))

app.run_polling()
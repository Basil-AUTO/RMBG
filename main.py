
import os
from rembg import remove
from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler,ContextTypes, MessageHandler, filters
# import asyncio

# Update(
#     message=Message(channel_chat_created=False, 
#                     chat=Chat(first_name='Basil', id=5089134456, last_name='S. Elbalaawi', type=<ChatType.PRIVATE>, username='CiscoManForce'),
#                     date=datetime.datetime(2024, 12, 1, 8, 31, 49, tzinfo=datetime.timezone.utc),
#                     delete_chat_photo=False,
#                     from_user=User(first_name='Basil', id=5089134456, is_bot=False, language_code='en', last_name='S. Elbalaawi', username='CiscoManForce'),
#                     group_chat_created=False, message_id=10, supergroup_chat_created=False, text='hello'),
#     update_id=273632054)

TOKEN= "7917835521:AAFOSNTIcFfYy27rlXrvVIpitoURBPx4aD0"
# async def main():
    # bot =telegram.Bot(TOKEN)
    # async with bot:
    #     update= (await bot.get_updates())[-1]
    #     chat_id= update.message.chat.id
    #     user_name= update.message.from_user.first_name
    #     await bot.send_message(text=f" hi {user_name}, how can i help you", chat_id=chat_id)
    
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE ):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi i am a backgroud removal bot, if you want to start click on /start ")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE ):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="To remove the backgroud , please send image ")
async def process_image(photo_name:str):
    name, _ = os.path.splitext(photo_name)
    output_photo_path = f"./processed/{name}.png"
    input = Image.open(f"./temp/{photo_name}")
    output= remove(input)
    output.save(output_photo_path)
    os.remove(f"./temp/{photo_name}")
    return output_photo_path
    
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE ):
    if filters.PHOTO.check_update(update):
        file_id = update.message.photo[-1].file_id
        unique_file_id = update.message.photo[-1].file_unique_id    
        photo_name = f"{unique_file_id}.jpg"
    elif filters.Document.IMAGE:
        file_id = update.message.document.file_id
        _, f_ext = os.path.splitext(update.message.document.file_name)
        unique_file_id = update.message.document.file_unique_id
        photo_name = f"{unique_file_id}.{f_ext}"
        
    photo_file= await context.bot.get_file(file_id)
    await photo_file.download_to_drive(custom_path=f"./temp/{photo_name}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=" we are proccessing your requist, please wait....")
    processed_image= await process_image(photo_name)
    await context.bot.send_document(chat_id= update.effective_chat.id, document=processed_image)
    os.remove(processed_image)
    
    
    
if __name__== '__main__':
    # asyncio.run(main())
    application= ApplicationBuilder().token(TOKEN).build()

    # Command Handllers
    help_handler= CommandHandler("help", help)
    start_handler= CommandHandler("start", start)
    message_handler= MessageHandler(filters.PHOTO | filters.Document.IMAGE , handle_message)
    
    # Register the handler commands to the appliction 
    application.add_handler(help_handler)
    application.add_handler(start_handler)
    application.add_handler(message_handler)
    
    
    application.run_polling()
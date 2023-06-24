import logging 
from aiogram import Bot, Dispatcher, executor, types
from routes.user_routes import create_user,get_one_user,create_user_page
from models.user_model import User

API_TOKEN = '6225207824:AAFPgfg9U0vJd40JBfcOmPgYg7xpGEnhBMc'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def webAppKeyboard(user_id:str=None): #создание клавиатуры с webapp кнопкой
   keyboard = types.ReplyKeyboardMarkup(row_width=1) #создаем клавиатуру
   webAppTest = types.WebAppInfo(url=f"https://anh2o.github.io/{user_id}.html") #создаем webappinfo - формат хранения url
   one_butt = types.KeyboardButton(text="Тестовая страница", web_app=webAppTest) #создаем кнопку типа webapp
   keyboard.add(one_butt) #добавляем кнопки в клавиатуру
   return keyboard #возвращаем клавиатуру

def webAppKeyboardInline(): #создание inline-клавиатуры с webapp кнопкой
   keyboard = types.InlineKeyboardMarkup(row_width=1) #создаем клавиатуру inline
   webApp = types.WebAppInfo("https://telegram.mihailgok.ru") #создаем webappinfo - формат хранения url
   one = types.InlineKeyboardButton(text="Веб приложение", web_app=webApp) #создаем кнопку типа webapp
   keyboard.add(one) #добавляем кнопку в клавиатуру

   return keyboard #возвращаем клавиатуру


@dp.message_handler(commands=['start']) #обрабатываем команду старт
async def start_fun(message):
   if (await get_one_user(message.from_user.id))["data"]==[]:
    
    await create_user(user)
   user = User(name=message.from_user.first_name,tgid=message.from_user.id,pay_state='0')
   await create_user_page(user)
   await bot.send_message(message.from_user.id, 'Привет', parse_mode="Markdown", reply_markup=webAppKeyboard(user_id=message.from_user.id))
   
@dp.message_handler(content_types="text")
def new_mes(message):
   start_fun(message)


@dp.message_handler(content_types="web_app_data") #получаем отправленные данные 
async def answer(webAppMes):
   print(webAppMes) #вся информация о сообщении
   print(webAppMes.web_app_data.data) #конкретно то что мы передали в бота
   await bot.send_message(webAppMes.chat.id, f"получили инофрмацию из веб-приложения: {webAppMes.web_app_data.data}") 
   #отправляем сообщение в ответ на отправку данных из веб-приложения 

if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)
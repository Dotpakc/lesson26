from os import listdir, path



def get_keyboard_from_path(sources):
    # categ_keyboard = types.InlineKeyboardMarkup()
    
    if path.exists(sources):
            list_categ = listdir(sources)
               
    for dir in list_categ:
            print(dir)
            # button = types.InlineKeyboardButton(dir, callback_data=dir)
            # categ_keyboard.add(button)
    

get_keyboard_from_path('shop/course')
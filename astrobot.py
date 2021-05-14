#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]

## Use your own token that @BotFather gave you (DO NOT SHARE IT WITH ANYONE AS THEY WILL BE ABLE TO CONTROL THE BOT)
TOKEN = ''

# Libraries for random numbers and image processing
from PIL import Image, ImageFont,ImageDraw , ImageChops
import random
import string
from io import BytesIO
import requests

## Function to generate the card, the astrobingocard must be on the same folder 
def generateCard(user):
    randomArray = random.sample(range(1,60),24)
    bio = BytesIO()
    bio.name = '{0}.png'.format(random.choice(string.ascii_lowercase) for i in range(1,10)) 
    with Image.open('AstroBingoCard.png') as img:
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial",  32)
        #DRAW A RECTANGLE FROM X=500,Y=9210 TO X=980,Y=980
        draw.rectangle(((500,920),(980,980)), fill="black")
        #WRITE THE USER NAME INTO THE RECTANGLE
        draw.text((500,920), '@{0}'.format(user), (255,255,0) ,font=ImageFont.truetype("arial",  44) )
        #ROW 1
        draw.text((455,365), str(randomArray[0]),font=font)
        draw.text((555,365), str(randomArray[1]),font=font)
        draw.text((655,365), str(randomArray[2]),font=font)
        draw.text((755,365), str(randomArray[3]),font=font)
        draw.text((855,365), str(randomArray[4]),font=font)
        #ROW 2
        draw.text((455,460), str(randomArray[5]),font=font)
        draw.text((555,460), str(randomArray[6]),font=font)
        draw.text((655,460), str(randomArray[7]),font=font)
        draw.text((755,460), str(randomArray[8]),font=font)
        draw.text((855,460), str(randomArray[9]),font=font)
        #ROW 3 - BE AWARE OF THE JOKER
        draw.text((455,550), str(randomArray[10]),font=font)
        draw.text((555,550), str(randomArray[11]),font=font)
        #draw.text((655,550), str(randomArray[0]),font=font) #JOKER
        draw.text((755,550), str(randomArray[12]),font=font)
        draw.text((855,550), str(randomArray[13]),font=font)
        #ROW 4
        draw.text((455,650), str(randomArray[14]),font=font)
        draw.text((555,650), str(randomArray[15]),font=font)
        draw.text((655,650), str(randomArray[16]),font=font)
        draw.text((755,650), str(randomArray[17]),font=font)
        draw.text((855,650), str(randomArray[18]),font=font)
        #ROW 5
        draw.text((455,750), str(randomArray[19]),font=font)
        draw.text((555,750), str(randomArray[20]),font=font)
        draw.text((655,750), str(randomArray[21]),font=font)
        draw.text((755,750), str(randomArray[22]),font=font)
        draw.text((855,750), str(randomArray[23]),font=font)

        img.save(bio, 'PNG')
    return bio




# Telegram libraries
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext



def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi astronauts!')

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help astronauts im running out of oxygen!')

def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)

def price(update: Update, context: CallbackContext) -> None:
    r = requests.get('https://api.coingecko.com/api/v3/coins/astronaut')
    update.message.reply_text('Naut price: {0}$'.format(r.json()['market_data']['current_price']['usd']))

def card(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    if(user.username):
         bio = generateCard(user.username)
    elif(not user.username):
         bio = generateCard(user.first_name)
    bio.seek(0)
    update.message.reply_photo(bio)



def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("card", card))
    dispatcher.add_handler(CommandHandler("price", price))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
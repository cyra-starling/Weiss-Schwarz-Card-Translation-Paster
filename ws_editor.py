from PIL import Image, ImageDraw, ImageFont
from math import ceil
import numpy as np
import csv
import textwrap
import os, sys

normalPos = (18, 560)
climaxPos = (18, 400)
normalCharLimit = 70
climaxCharLimit = 80
fontSize = 16
wrapGap = 3
lineGap = 10
outputPath = "./output/"
sheetOutputPath = "./cardsheets/"
wsCardWidth = 460
wsCardHeight = 641

font = ImageFont.truetype("./SpaceMonoRegular-JRrmm.ttf")

# Expected Input
# <path to image folders> <path to csv file> <path to card backing> <card sheets name>
# CSV format: [CardNumber] [Climax] [Text]

# ----- Prep output folder
if not os.path.exists(outputPath):
    os.mkdir(outputPath)
if not os.path.exists(sheetOutputPath):
    os.mkdir(sheetOutputPath)

# ----- Get the input dir & get list of images
inputPath = os.path.abspath(sys.argv[1])
if not os.path.exists(inputPath):
    print("Input path doesnt exists")
    sys.exit()

imageNames = os.listdir(inputPath)
imagePaths = []
outputImagePaths = []

for file in imageNames:
    if ".png" in file:
        imagePaths.append(os.path.join(inputPath, file))

# ----- Read CSV file for the text
cardText = {}
with open(sys.argv[2], "r") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        cardNum = row.pop("CardNumber")
        cardText[cardNum] = row


# ----- Start processing translation pasting
for cardIndex in range(len(imagePaths)):
    # Match Name!
    # Variations: R S SP SSP, but as long as dict has smth that is a substr of the curr name, shld be gucci
    cardName = imageNames[cardIndex]
    text = ""
    climax = ""


    for keyName in cardText.keys():
        nameFormatted = keyName.replace("/", "_").replace("-", "_").lower()
        if nameFormatted in cardName:
            text = cardText[keyName]["Text"]
            climax = cardText[keyName]["Climax"]

    if not climax:
        print("ERROR: " + cardName)
        # continue
        sys.exit()

    pos = climaxPos if "Y" in climax else normalPos
    charLimit = climaxCharLimit if "Y" in climax else normalCharLimit

    image = Image.open(imagePaths[cardIndex])
    image = image.convert("RGBA")
    width, height = image.size 
    draw = ImageDraw.Draw(image)

    split_text = reversed(text.splitlines())

    count = 0
    lineCount = 0

    for text_line in split_text:
        wrapped_text = reversed(textwrap.wrap(text_line, charLimit))
        for wrapped_line in wrapped_text:
            # draw text here
            w = draw.textlength(wrapped_line, font=font, font_size=fontSize)
            y = pos[1] - (count * (fontSize + wrapGap)) - (lineCount * lineGap)
            x = pos[0]

            draw.rectangle([(x - 5,  y - fontSize - wrapGap), (x + w + 5, y)], fill="white")
            draw.text((x, y), wrapped_line, fill="black", font=font, font_size=fontSize, anchor="lb")
            count+=1
        lineCount+=1

    print("Saving card #"+str(cardIndex))
    image.save(outputPath+imageNames[cardIndex], optimize=True)
    outputImagePaths.append(outputPath+imageNames[cardIndex])


# ----- Get card backing path
cardBackPath = sys.argv[3]
if not os.path.exists(cardBackPath):
    print("Card backing path doesnt exists")
    sys.exit()

# ----- Get card sheet name
cardSheetName = sys.argv[4]
if not cardSheetName:
    cardSheetName = "WS_CARDSHEET_"

# ----- Start making card sheets
# 1 sheet has 69 cards max, 70th card is card back image
numberOfSheets = 0
if (len(outputImagePaths) % 69) > 0:
    numberOfSheets = ceil(len(outputImagePaths) / 69)
else:
    numberOfSheets = len(outputImagePaths) / 69

print(len(outputImagePaths))

if numberOfSheets > 0:
    for sheet in range(numberOfSheets):
        cardsheet = Image.new('RGBA', (10*wsCardWidth, 7*wsCardHeight))
        print(cardsheet.height)
        cardInSheet = 0
        row = 0
        for card in range(len(outputImagePaths)):
        # for card in range(2):
            cardInSheet += 1
            cardToPaste = Image.open(outputImagePaths[card])
            
            if cardToPaste.width > cardToPaste.height:
                # means its CX cards (Landscape cards), rotate first
                cardToPaste = cardToPaste.transpose(method=Image.Transpose.ROTATE_270)

            cardsheet.paste(cardToPaste, ((card % 10)*wsCardWidth, row*wsCardHeight))
            if cardInSheet % 10 == 0:
                row += 1

            if cardInSheet == 69:
                cardsheet.paste(Image.open(cardBackPath), (9*wsCardWidth, 6*wsCardHeight))
                break

        if cardInSheet < 69:
                cardsheet.paste(Image.open(cardBackPath), (9*wsCardWidth, 6*wsCardHeight))

        print(sheetOutputPath+cardSheetName+str(sheet)+".png")
        cardsheet.save(sheetOutputPath+cardSheetName+str(sheet)+".png", optimize=True)

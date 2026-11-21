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
outputPath = "./cards/"
outputCXPath = "./climaxCards/"
sheetOutputPath = "./cardsheets/"
wsCardWidth = 460
wsCardHeight = 641

font = ImageFont.truetype("./SpaceMonoRegular-JRrmm.ttf")

# Expected Input
# <path to image folders> <path to csv file> <path to card backing>
# CSV format: [CardNumber] [Climax] [Text]

def generate_card_sheets(inputImages, outPath, outputName):
    numberOfSheets = 0
    if (len(inputImages) % 69) > 0:
        numberOfSheets = ceil(len(inputImages) / 69)
    else:
        numberOfSheets = int(len(inputImages) / 69)

    if numberOfSheets > 0:
        card = 0
        for sheet in range(numberOfSheets):
            cardsheet = Image.new('RGBA', (10*wsCardWidth, 7*wsCardHeight))
            row = 0
            for i in range(70):
                if card >= len(inputImages):
                    break

                cardToPaste = Image.open(inputImages[card])

                # rotate CX cards first
                if cardToPaste.width > cardToPaste.height:
                    cardToPaste = cardToPaste.transpose(method=Image.Transpose.ROTATE_270)

                if (i > 0) and (i % 10 == 0):
                    row += 1

                cardsheet.paste(cardToPaste, ((card % 10)*wsCardWidth, row*wsCardHeight))

                card += 1

            cardsheet.paste(Image.open(cardBackPath), (9*wsCardWidth, 6*wsCardHeight))

            print(outPath+outputName+str(sheet)+".png")
            cardsheet.save(outPath+outputName+str(sheet)+".png", optimize=True)


# ----- Prep output folder
if not os.path.exists(outputPath):
    os.mkdir(outputPath)
if not os.path.exists(outputCXPath):
    os.mkdir(outputCXPath)
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

    
    if climax == "Y":
        image.save(outputCXPath+imageNames[cardIndex], optimize=True)
    else:
        image.save(outputPath+imageNames[cardIndex], optimize=True)


# ----- Get card backing path
cardBackPath = sys.argv[3]
if not os.path.exists(cardBackPath):
    print("Card backing path doesnt exists")
    sys.exit()

# ----- Start making card sheets
cxImageNames = os.listdir(outputCXPath)
outputImageNames = os.listdir(outputPath)
cxImagePaths = []
outputImagePaths = []

for file in cxImageNames:
    if ".png" in file:
        cxImagePaths.append(os.path.join(outputCXPath, file))

generate_card_sheets(cxImagePaths, sheetOutputPath, "WS_CARDSHEET_CX_")

for file in outputImageNames:
    if ".png" in file:
        outputImagePaths.append(os.path.join(outputPath, file))

generate_card_sheets(outputImagePaths, sheetOutputPath, "WS_CARDSHEET_")
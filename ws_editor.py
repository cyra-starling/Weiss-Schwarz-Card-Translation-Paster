from PIL import Image, ImageDraw, ImageFont
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

font = ImageFont.truetype("./SpaceMonoRegular-JRrmm.ttf")

# Expected Input
# <path to image folders> <csv file> <card number>
# Card number format: GBF-S134
# CSV format: [CardNumber] [Climax] [Text]

# ----- Prep output folder
if not os.path.exists(outputPath):
    os.mkdir(outputPath)

# ----- Get the input dir & get list of images
inputPath = os.path.abspath(sys.argv[1])
if not os.path.exists(inputPath):
    sys.exit()

imageNames = os.listdir(inputPath)
imagePaths = []

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


# ----- Start processing
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

    image.save(outputPath+imageNames[cardIndex], optimize=True)
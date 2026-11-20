# WS Card Translation Paster
This is just a personal script to paste card translation onto card images because I play JP decks with not enough JP language skills~

It's here to be saved online mainly!

> Update 21/11/26
> I had to update my card translations, so I decided to add the card sheet making here too because I'm lazy to use the card sheet tool TTS gave. Hardcoded the card size from the images i dl-ed sooo yeah rmb that if i ever get different size images!

For future me on how to use:
`./GBF/` - Folder for all card images
`GBF-text.csv` - `CardNumber`, `Climax`, and `Text` are the collumns
```
python3 ws_editor.py  ./GBF/ ./GBF-text.csv ./ws-card-back.png <cardsheet_file_name>
```

### Requirements..
PIL, Numpy

### Credits?
Utilized free monospace font Space Mono (file not included!), "calculations" (more like estimations) are determined with this font, changing font probably means have to readjust the anchor for the text.
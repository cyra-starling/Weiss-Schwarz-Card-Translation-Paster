# WS Card Translation Paster
This is just a personal script to paste card translation onto card images because I play JP decks with not enough JP language skills~

It's here to be saved online mainly!

> Update 21/11/26
> I had to update my card translations, so I decided to add the card sheet making here too because I'm lazy to use the card sheet tool TTS gave. Hardcoded the card size from the images i dl-ed sooo yeah rmb that if i ever get different size images!

> Update 22/11/26
> Lesson learnt, don't code at 3am or so probably, IDK what I was thinking while i wrote it and it was horrible LMFAO but anyways I fixed it. I also split CX card sheets & Normal card sheets. This is so that when you import custom deck into TTS, you can mark CX cards as sideways so when you press ALT to inspect/zoom, it will show correctly! 

For future me on how to use:
`./GBF/` - Folder for all card images
`GBF-text.csv` - `CardNumber`, `Climax`, and `Text` are the collumns
```
python3 ws_editor.py  ./GBF/ ./GBF-text.csv ./ws-card-back.png
```

### Requirements..
PIL, Numpy

### Credits?
Utilized free monospace font Space Mono (file not included!), "calculations" (more like estimations) are determined with this font, changing font probably means have to readjust the anchor for the text.
from borb.pdf import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from decimal import Decimal
from borb.pdf.canvas.layout.image.image import Image

from borb.pdf import FixedColumnWidthTable
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from pathlib import Path

from borb.pdf import HexColor

from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont

from borb.pdf.canvas.font.font import Font
from borb.pdf import Alignment
from borb.pdf import TableCell

import pandas as pd

imgAttrib = 'image: Flaticon.com'

font_path: Path = Path('./Fonts/Everson Mono.ttf')
custom_font: Font = TrueTypeFont.true_type_font_from_file(font_path)

def generateReport(db, playerName):

    players = db['player']
    country = db['country']
    profiles = db['playerProfile']

    pdf = Document()
    page = Page()

    pdf.add_page(page)

    layout = SingleColumnLayout(page)

    layout.add(    
        Image(
            Path('./Assets/strategy.png'),        
        width=Decimal(128),        
        height=Decimal(128), horizontal_alignment=Alignment.CENTERED)
        )

    layout.add(Paragraph('Gambit Chess Tournament Report', font_size=22, font=custom_font, horizontal_alignment=Alignment.CENTERED))

    player = players.find_one({"Player_Name": playerName})

    playerID = player['Player_ID']
    playerCountry = player['Country_ID']    
    countryNow = country.find_one({"Country_ID": playerCountry})
    countryName =countryNow['Country_Name']
    playerDOB = player['Date_of_Birth']
    gender = player['Gender']
    playerRating = player['Player_Rating']
    fide = player['FIDE_Percentile']
    prof = profiles.find({"Player_ID": playerID})

    layout.add(Paragraph(''))
    layout.add(Paragraph(''))
    layout.add(Paragraph(''))

    layout.add(Paragraph('Player Name: ' + playerName, font_size=14, font=custom_font))
    layout.add(Paragraph('License: ' + playerID, font_size=12, font=custom_font))
    layout.add(Paragraph('Date of Birth: ' + playerDOB, font_size=14, font=custom_font))
    layout.add(Paragraph('Gender: ' + gender, font_size=14, font=custom_font))
    layout.add(Paragraph('Rating: ' + str(playerRating), font_size=12, font=custom_font))
    layout.add(Paragraph('FIDE Percentile: ' + str(fide), font_size=14, font=custom_font))
    layout.add(Paragraph('Country: ' + countryName, font_size=14, font=custom_font))
    layout.add(Paragraph(''))


    prof = pd.DataFrame(list(prof))

    if (len(prof)>0):
        page2 = Page()

        pdf.add_page(page2)

        layout2 = SingleColumnLayout(page2)

        layout2.add(Paragraph('Achievements', font_size=12, font=custom_font))
        prof = prof[prof['Achievements'].astype(str) != 'nan']

        table = FixedColumnWidthTable(number_of_rows=len(prof) + 1, number_of_columns=3)

        odd_color = HexColor("BBBBBB")
        even_color = HexColor("FFFFFF")

        table.add(TableCell(Paragraph('Achievement', font_size=12, font=custom_font), background_color=odd_color, padding_top=Decimal(5), padding_left=Decimal(5)))
        table.add(TableCell(Paragraph('Year', font_size=12, font=custom_font), background_color=odd_color, padding_top=Decimal(5), padding_left=Decimal(5)))
        table.add(TableCell(Paragraph('Coach', font_size=12, font=custom_font), background_color=odd_color, padding_top=Decimal(5), padding_left=Decimal(5)))
            
        for i in range(len(prof)):
            c = even_color if i % 2 == 0 else odd_color
            row = prof.iloc[i]
            table.add(TableCell(Paragraph(row['Achievements'][:-3], font_size=10, font=custom_font), background_color=c, padding_top=Decimal(5), padding_left=Decimal(5)))
            table.add(TableCell(Paragraph(str(row['Year']), font_size=10, font=custom_font), background_color=c, padding_top=Decimal(5), padding_left=Decimal(5)))
            table.add(TableCell(Paragraph(row['CoachName'], font_size=10, font=custom_font), background_color=c, padding_top=Decimal(5), padding_left=Decimal(5)))

        
        layout2.add(table)
    
    with open('./Outs/playerReport.pdf', 'wb') as pdfOut:
        PDF.dumps(pdfOut, pdf)

    return
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

def generateReport(db, tournName):

    tournaments = db['tournament']
    players = db['player']
    country = db['country']
    matches = db['match']
    arbiters = db['arbiter']
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

    tournament = tournaments.find_one({"Tournament_Name": tournName})
    tournamentID = tournaments['Tournament_ID']
    matchesTourn = matches.find({'Tournament_ID' : tournamentID})
    matchesTourn = pd.DataFrame(list(matchesTourn))

    tournName = tournament['Tournament_Name']
    startDate = tournament['Start_Date']
    endDate = tournament['End_Date']
    winner = tournament['Winner']
    loc = tournament['Location']
    countryNow = country.find_one({'Country_ID' : tournament['Country']})
    countryName = countryNow['Country_Name']

    layout.add(Paragraph(''))
    layout.add(Paragraph(''))
    layout.add(Paragraph(''))
    layout.add(Paragraph(''))

    layout.add(Paragraph('Tournament Name: ' + tournName, font_size=14, font=custom_font))
    layout.add(Paragraph('Start Date: ' + startDate, font_size=14, font=custom_font))
    layout.add(Paragraph('End Date: ' + endDate, font_size=14, font=custom_font))
    layout.add(Paragraph('Location: ' + loc, font_size=14, font=custom_font))
    layout.add(Paragraph('Country: ' + countryName, font_size=14, font=custom_font))

    page2 = Page()

    pdf.add_page(page2)

    layout2 = SingleColumnLayout(page2)

    layout2.add(Paragraph('Host', font_size=12, font=custom_font))
    layout2.add(Paragraph('Country: ' + countryName, font_size=12, font=custom_font))
    layout2.add(Paragraph('Organization: ' + countryNow['Chess_Org'], font_size=12, font=custom_font))
    layout2.add(Paragraph('International License: ' + countryNow['Org_License'], font_size=12, font=custom_font))
    layout2.add(Paragraph('President: ' + countryNow['Org_President'], font_size=12, font=custom_font))
    layout2.add(Paragraph(''))

    winnerNow = players.find_one({'Player_ID' : winner})

    layout2.add(Paragraph('Winner', font_size=12, font=custom_font))
    layout2.add(Paragraph('License: ' + winner, font_size=12, font=custom_font))
    layout2.add(Paragraph('Name: ' + winnerNow['Player_Name'], font_size=12, font=custom_font))
    layout2.add(Paragraph('Country: ' + country.find_one({'Country_ID' : winnerNow['Country']})['Country_Name'], font_size=12, font=custom_font))
    layout2.add(Paragraph('Date of Birth: ' + str(winnerNow['DOB']), font_size=12, font=custom_font))
    layout2.add(Paragraph('Rating: ' + str(winnerNow['Player_Rating']), font_size=12, font=custom_font))
    layout2.add(Paragraph('FIDE Percentile: ' + str(winnerNow['FIDE_Percentile']), font_size=12, font=custom_font))
    layout2.add(Paragraph(''))
    layout2.add(Paragraph('Achievements', font_size=12, font=custom_font))

    prof = profiles.find({'Player_ID' : winner})
    prof = pd.DataFrame(list(prof))
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

    layout2.add(Paragraph(''))
    layout2.add(Paragraph(''))

    w = HexColor("FBEB70")

    columns = ['Match ID', 'Player White', 'Player Black', 'Arbiter', 'Round']

    def createTable(data):
        table = FixedColumnWidthTable(number_of_rows=len(data) + 1, number_of_columns=len(columns))

        for column in columns:
            table.add(TableCell(Paragraph(column, font_size=12, font=custom_font), background_color=odd_color, padding_top=Decimal(5), padding_left=Decimal(5)))

        for i in range(len(data)):
            c = even_color if i % 2 == 0 else odd_color
            row = data.iloc[i]

            table.add(TableCell(Paragraph(str(row['Match_ID']), font_size=8, font=custom_font), background_color=c, padding_top=Decimal(5), padding_left=Decimal(5)))

            if row['Player_Black'] == row['Winner']:
                table.add(TableCell(Paragraph(row['Player_White'], font_size=8, font=custom_font), background_color=c, padding_top=Decimal(5), padding_left=Decimal(5)))
                table.add(TableCell(Paragraph(row['Player_Black'], font_size=8, font=custom_font), background_color=w, padding_top=Decimal(5), padding_left=Decimal(5)))
            elif row['Player_White'] == row['Winner']:
                table.add(TableCell(Paragraph(row['Player_White'], font_size=8, font=custom_font), background_color=w, padding_top=Decimal(5), padding_left=Decimal(5)))
                table.add(TableCell(Paragraph(row['Player_Black'], font_size=8, font=custom_font), background_color=c, padding_top=Decimal(5), padding_left=Decimal(5)))

            table.add(TableCell(Paragraph(row['Arbiter'], font_size=8, font=custom_font), background_color=c, padding_top=Decimal(5), padding_left=Decimal(5)))
            table.add(TableCell(Paragraph(str(row['Round']), font_size=8, font=custom_font), background_color=c, padding_top=Decimal(5), padding_left=Decimal(5)))

        return table

    def below32():
        page3 = Page()

        pdf.add_page(page3)

        layout3 = SingleColumnLayout(page3)

        layout3.add(Paragraph('Matches', font_size=14, font=custom_font))

        layout3.add(createTable(matchesTourn))

        layout3.add(Paragraph(''))
        layout3.add(Paragraph('Note: Winner of match is highlighted', font_size=6, font=custom_font))
        layout3.add(Paragraph('All IDs can be referenced in the appendix', font_size=6, font=custom_font))

    def above32():
        page3 = Page()

        pdf.add_page(page3)

        layout3 = SingleColumnLayout(page3)

        layout3.add(Paragraph('Matches', font_size=14, font=custom_font))

        layout3.add(createTable(matchesTourn.iloc[:32]))

        pageT = Page()

        pdf.add_page(pageT)

        layoutT = SingleColumnLayout(pageT)

        layoutT.add(Paragraph('Matches - Contd.', font_size=14, font=custom_font))
        
        layoutT.add(createTable(matchesTourn.iloc[32:].reset_index(drop=True)))

        layoutT.add(Paragraph('Note: Winner of match is highlighted', font_size=6, font=custom_font))

    if len(matchesTourn) > 32:
        above32()
    else:
        below32()

    with open('./Outs/tournReport.pdf', 'wb') as pdfOut:
        PDF.dumps(pdfOut, pdf)

    return
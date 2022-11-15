from borb.pdf import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from decimal import Decimal
from borb.pdf.canvas.layout.image.image import Image

from borb.pdf.canvas.layout.text.paragraph import Paragraph
from pathlib import Path

from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont

from borb.pdf.canvas.font.font import Font
from borb.pdf import Alignment
from borb.pdf.page.page_size import PageSize

import pandas as pd
import chess
import chess.svg

from cairosvg import svg2pdf
import typing

imgAttrib = 'image: Flaticon.com'

font_path: Path = Path('./Fonts/Everson Mono.ttf')
custom_font: Font = TrueTypeFont.true_type_font_from_file(font_path)

def generateReport(db, matchID):

    tournaments = db['tournament']
    players = db['player']
    matches = db['match']
    arbiters = db['arbiter']
    movesDB = db['moves']

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

    match = matches.find_one({"Match_ID": matchID})
    tournament = tournaments.find_one({"Tournament_ID": match['Tournament_ID']})

    tournName = tournament['Tournament_Name']
    startDate = tournament['Start_Date']
    endDate = tournament['End_Date']
    roundNum = match['Round']
    matchType = match['Match_Type']

    playerWhite = players.find_one({"Player_ID": match['Player_White']})
    nameWhite = playerWhite['Player_Name']
    playerBlack = players.find_one({"Player_ID": match['Player_Black']})
    nameBlack = playerBlack['Player_Name']

    winner = match['Winner']

    arbiterID = match['Arbiter_ID']
    nameArbiter = arbiters.find_one({"Arbiter_ID": arbiterID})['Arbiter_Name']

    layout.add(Paragraph('Tournament Name: ' + tournName, font_size=10, font=custom_font))
    layout.add(Paragraph('Start Date: ' + startDate, font_size=10, font=custom_font))
    layout.add(Paragraph('End Date: ' + endDate, font_size=10, font=custom_font))
    layout.add(Paragraph('Match: ' + matchID, font_size=10, font=custom_font))
    layout.add(Paragraph('Round Number: ' + str(roundNum), font_size=10, font=custom_font))
    layout.add(Paragraph('Match Type: ' + matchType, font_size=10, font=custom_font))
    layout.add(Paragraph('Arbiter: ' + nameArbiter + ' - ' + arbiterID, font_size=10, font=custom_font))

    layout.add(Paragraph(''))

    layout.add(Paragraph('Player White: ' + nameWhite + ' - ' + playerWhite['Player_ID'], font_size=10, font=custom_font))
    layout.add(Paragraph('Player Black: ' + nameBlack + ' - ' + playerBlack['Player_ID'], font_size=10, font=custom_font))
    layout.add(Paragraph('Winner: ' + winner, font_size=10, font=custom_font))

    moves = movesDB.find({"Match_ID": matchID})

    moves = pd.DataFrame(list(moves))

    board = chess.Board()

    for move in moves['Move']:

        board.push_san(move)

        svg = chess.svg.board(board=board, size=600, lastmove=board.peek())

        svg2pdf(bytestring=svg,write_to='./Assets/Renders/output.pdf', output_height=float(PageSize.A4_PORTRAIT.value[1]), output_width=float(PageSize.A4_PORTRAIT.value[0]), parent_height=float(PageSize.A4_PORTRAIT.value[1]), parent_width=float(PageSize.A4_PORTRAIT.value[0]))

        pdf2: typing.Optional[Document] = Document()

        with open("./Assets/Renders/output.pdf", "rb") as pdf_file_handle:
            pdf2 = PDF.loads(pdf_file_handle)

        pdf.add_document(pdf2)

    with open('./Outs/matchReport.pdf', 'wb') as pdfOut:
        PDF.dumps(pdfOut, pdf)

    return
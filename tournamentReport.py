from pymongo import MongoClient
import pymongo
import pandas as pd
import json

import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(f"mongodb+srv://orectique:{os.getenv('DB_P')}@orectique.ixj7l.mongodb.net/?retryWrites=true&w=majority")

db = client['chessOlympiad']

def generateReport(tournName):
    return
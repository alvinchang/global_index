
"""
The main 'geoname' table has the following fields :
---------------------------------------------------
geonameid         : integer id of record in geonames database
name              : name of geographical point (utf8) varchar(200)
asciiname         : name of geographical point in plain ascii characters, varchar(200)
alternatenames    : alternatenames, comma separated, ascii names automatically transliterated, convenience attribute from alternatename table, varchar(10000)
latitude          : latitude in decimal degrees (wgs84)
longitude         : longitude in decimal degrees (wgs84)
feature class     : see http://www.geonames.org/export/codes.html, char(1)
feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
country code      : ISO-3166 2-letter country code, 2 characters
cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 200 characters
admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80)
admin3 code       : code for third level administrative division, varchar(20)
admin4 code       : code for fourth level administrative division, varchar(20)
population        : bigint (8 byte int)
elevation         : in meters, integer
dem               : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
timezone          : the iana timezone id (see file timeZone.txt) varchar(40)
modification date : date of last modification in yyyy-MM-dd format

"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, BIGINT, DATE, FLOAT

db = SQLAlchemy()


class Cities(db.Model):
    # Using floats instead of Decimals as they are not supported by sqlite3
    # Also sqlite3 dates needs a python date (cant be a string)
    __tablename__ = 'Geonames'

    geonameid = Column(Integer, primary_key=True)
    name = Column(String(200))
    asciiname = Column(String(200))
    alternatenames = Column(String(10000))
    latitude = Column(FLOAT)
    longitude = Column(FLOAT)
    feature_class = Column(String(1))
    feature_code = Column(String(10))
    country_code = Column(String(2))
    cc2 = Column(String(200))
    admin1_code = Column(String(20))
    admin2_code = Column(String(80))
    admin3_code = Column(String(20))
    admin4_code = Column(String(20))
    population = Column(BIGINT)
    elevation = Column(Integer)
    dem = Column(Integer)
    timezone = Column(String(40))
    modification_date = Column(DATE)


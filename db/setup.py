
from datetime import datetime
from pathlib import Path
import os
import csv

from sqlalchemy.exc import SQLAlchemyError

from db.common import db_session
from db.models import db, Cities


class GeonamesCsvHeadersIndices:
    GEONAMEID = 0
    NAME = 1
    ASCIINAME = 2
    ALTERNATENAMES = 3
    LATITUDE = 4
    LONGITUDE = 5
    FEATURE_CLASS = 6
    FEATURE_CODE = 7
    COUNTRY_CODE = 8
    CC2 = 9
    ADMIN1_CODE = 10
    ADMIN2_CODE = 11
    ADMIN3_CODE = 12
    ADMIN4_CODE = 13
    POPULATION = 14
    ELEVATION = 15
    DEM = 16
    TIMEZONE = 17
    MODIFICATION_DATE = 18


class Date:
    DATEISO8601_FORMAT = "%Y-%m-%d"


def load_db(file_location: str):
    """
    Loads the specified file at `file_location` into our database.
    :return:
    """
    with open(file_location, 'r') as f:

        csv_reader = csv.reader(f, delimiter='\t')

        all_sqlalchemy_objs = []
        for line in csv_reader:
            geoname_db_obj = Cities(
                geonameid=line[GeonamesCsvHeadersIndices.GEONAMEID],
                name=line[GeonamesCsvHeadersIndices.NAME],
                asciiname=line[GeonamesCsvHeadersIndices.ASCIINAME],
                alternatenames=line[GeonamesCsvHeadersIndices.ALTERNATENAMES],
                latitude=line[GeonamesCsvHeadersIndices.LATITUDE],
                longitude=line[GeonamesCsvHeadersIndices.LONGITUDE],
                feature_class=line[GeonamesCsvHeadersIndices.FEATURE_CLASS],
                feature_code=line[GeonamesCsvHeadersIndices.FEATURE_CODE],
                country_code=line[GeonamesCsvHeadersIndices.COUNTRY_CODE],
                cc2=line[GeonamesCsvHeadersIndices.CC2],
                admin1_code=line[GeonamesCsvHeadersIndices.ADMIN1_CODE],
                admin2_code=line[GeonamesCsvHeadersIndices.ADMIN2_CODE],
                admin3_code=line[GeonamesCsvHeadersIndices.ADMIN3_CODE],
                admin4_code=line[GeonamesCsvHeadersIndices.ADMIN4_CODE],
                population=line[GeonamesCsvHeadersIndices.POPULATION],
                elevation=line[GeonamesCsvHeadersIndices.ELEVATION],
                dem=line[GeonamesCsvHeadersIndices.DEM],
                timezone=line[GeonamesCsvHeadersIndices.TIMEZONE],
                modification_date=datetime.strptime(line[GeonamesCsvHeadersIndices.MODIFICATION_DATE],
                                                    Date.DATEISO8601_FORMAT).date()
                )

            all_sqlalchemy_objs.append(geoname_db_obj)

        with db_session() as session:

            print("Adding {} objs".format(len(all_sqlalchemy_objs)))
            session.add_all(all_sqlalchemy_objs)
from db.common import db_session
from db.models import Cities


class CityMissingError(ValueError):

    def __init__(self, msg):
        super().__init__(msg)


class CityService:

    @staticmethod
    def _get_pythagorean_distance(initial_lat: float, initial_long: float, target_lat: float, target_long: float) \
            -> float:
        """
        Computes the Pythagorean distance between two points (`initial_lat`, `initial_long`) and (`target_lat`,
        `target_long`) and is used to determine proximity between two cities.

        :param initial_lat: the latitude of the initial city
        :param initial_long: the longitude of the initial city
        :param target_lat: the latitude of the target city
        :param target_long: the longitude of the target city

        :return: the pythagorean distance between the two cities
        :rtype: float
        """
        return ((target_lat - initial_lat) ** 2 + (target_long - initial_long) ** 2) ** .5

    @staticmethod
    def get_closest_city_names_by_proximity(city_id: int, top_k: int, country_restriction: str):
        """
        Gets a list of city names and their ids that are closest to a `city_id`, bounded by `closest_k` and filtered by an
        optional `country_restriction`.

        :param city_id: the city id to base proximity off of
        :param top_k: the number of results to limit by
        :param country_restriction: (optional) a country code (ex. 'US') restriction to apply

        :return: a list of city names and ids that represent the `closest_k` city_names with a `country_restriction` applied
        (if specified), with respect to the latitude and longitude of the given `city_id`
        :raises: CityMissingError (if `city_id` was not found)
        """

        with db_session() as session:
            # First find if the `city_id` is within our database, raise error if its not found.
            city_result = session.query(Cities).filter(Cities.geonameid == city_id).all()
            if not city_result:
                raise CityMissingError("Did not find city_id={}".format(city_id))

            city = city_result[0]

            base_query = session.query(Cities)

            # Apply any country restriction (if specified)
            if country_restriction:
                base_query = base_query.filter(Cities.country_code == country_restriction)

            # Fetch all results, and sort by their pythagorean distance to our `city_id`
            # Note: This is slow, it would be better to do it in the sqlalchemy call and limit results.
            results = base_query.all()

            sorted_results = sorted(results, key=lambda x: CityService._get_pythagorean_distance(
                city.latitude, city.longitude, x.latitude, x.longitude
            ))

            return [[res.name, res.geonameid] for res in sorted_results[0:top_k]]

    @staticmethod
    def get_cities_by_lexicography(city_name_match_str: str, top_k: int, country_restriction=None):
        """
        Gets a list of city names by lexicographical name matching based on `city_name_match_str', limiting results
        by `top_k` and an optional `country_restriction` parameter, ordered alphabetically.

        :param city_name_match_str: the string to match a city's ascii name by, if multiple words are specified then
        they will be treated independently.
        :param top_k: the number of results to return. If top_k is not specified it will default to 100.
        :param country_restriction: (optional) a country code (ex. 'US') restriction to apply
        :return: a list of city names that represent the `top_k` cities that match the `city_name_match_str` with the
        optional `country_restriction` parameter applied (if specified)
        """

        # Set app default for top_k for lexicographical API if not set.
        top_k_default = top_k if not top_k else 100

        with db_session() as session:

            base_query = session.query(Cities)

            match_word_list = city_name_match_str.split(" ")
            # Construct our ilike filter clause based on the `match_word_list` to match independently on each word
            # with respect to order.
            name_match_filter_sql = "%%" + "%% %%".join(match_word_list) + "%%"

            # Apply any country restriction (if specified)
            if country_restriction:
                base_query = base_query.filter(Cities.country_code == country_restriction)

            name_match_filter_clause = Cities.asciiname.ilike(name_match_filter_sql)

            results = base_query.filter(name_match_filter_clause).order_by(Cities.asciiname.asc()).all()

            return [[res.name, res.geonameid] for res in results[0:top_k_default]]
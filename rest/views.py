from flask import Blueprint, request
from flask.json import jsonify

from services.city_service import CityService, CityMissingError

city_blueprints = Blueprint(__name__, "cities")


class CityViewConstants:
    TOP_K_CLOSEST = "top_k_closest"
    TOP_K = "top_k"
    COUNTRY_RESTRICTION = "country_restriction"
    CITY_NAME_MATCH_STR = "city_name_match_str"
    CLOSEST_CITIES_BY_PROXIMITY = "closest_cities_by_proximity"
    CLOSEST_CITIES_BY_LEXICOGRAPHY = "closest_cities_by_lexicography"
    CITY_ID = "city_id"


class RestMessageConstants:
    ERROR_MSG = "error_msg"


@city_blueprints.route('/proximity', methods=['GET'])
def get_closest_city_names_by_proximity():
    """
    REST method route for proximity API

    """
    try:

        top_k = request.args.get(CityViewConstants.TOP_K, type=int)
        if top_k is None:
            raise ValueError("Could not find `top_k` parameter")

        city_id = request.args.get(CityViewConstants.CITY_ID, type=int)
        if city_id is None:
            raise ValueError("Could not find `city_id` parameter")

        country_restriction = request.args.get(CityViewConstants.COUNTRY_RESTRICTION)

        closest_city_names = CityService.get_closest_city_names_by_proximity(city_id,
                                                                             top_k=top_k,
                                                                             country_restriction=country_restriction)
        return jsonify({
            CityViewConstants.CLOSEST_CITIES_BY_PROXIMITY: closest_city_names
        }), 200

    except CityMissingError as e:
        return jsonify(
            {RestMessageConstants.ERROR_MSG: str(e)}
        ), 404

    except Exception as e:
        return jsonify(
            {RestMessageConstants.ERROR_MSG: str(e)}
        ), 500


@city_blueprints.route('/lexicographical', methods=['GET'])
def get_city_names_by_lexicography():
    """
    REST method route for lexicographical API

    """
    try:
        city_name_match_str = request.args.get(CityViewConstants.CITY_NAME_MATCH_STR)

        top_k = request.args.get(CityViewConstants.TOP_K, type=int)

        country_restriction = request.args.get(CityViewConstants.COUNTRY_RESTRICTION)

        matched_cities = CityService.get_cities_by_lexicography(city_name_match_str, top_k, country_restriction)

        return jsonify({
            CityViewConstants.CLOSEST_CITIES_BY_LEXICOGRAPHY: matched_cities
        }), 200

    except CityMissingError as e:
        return jsonify(
            {RestMessageConstants.ERROR_MSG: str(e)}
        ), 404

    except Exception as e:
        return jsonify(
            {RestMessageConstants.ERROR_MSG: str(e)}
        ), 500

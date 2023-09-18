"""execute each exercise or correction for TP1"""
import sys
import requests


from datetime import datetime
from collections import defaultdict
from common.file_utils import dump_json, load_json
from common.default import (
    TP1_PROBES_PATH,
    TP1_ANCHORS_PATH,
    TP1_RESULTS_PATH,
    TP1_DATASET_PATH,
)

from settings.logger_config import logger

from ripe.utils import (
    get_date_from_timestamp,
    get_timestamp_from_date,
    get_date_from_str,
)
from ripe.ripe_atlas_api import get_atlas_anchors, get_atlas_probes


def exo1() -> dict:
    """
    retrieve a measurement using RIPE Atlas API, using a measurement uuid

    hints: requests package import
    """
    measurement_id = 38333397
    base_url = None

    if not base_url:
        raise RuntimeError("url empty")

    else:
        ####################################################################
        # TODO: make an http request to RIPE API (using requests package)  #
        # to get measurement with measurement id : 38333397                #
        ####################################################################
        response = None
        pass

    logger.info(f"response: {response}")


def exo2() -> dict:
    """retrieve measurement results"""
    measurement_id = 38333397
    base_url = None

    if not base_url:
        raise RuntimeError("url empty")

    else:
        ####################################################################
        # TODO: make an http request to RIPE API (using requests package)  #
        # to get measurement with measurement id : 38333397                #
        ####################################################################
        response = None
        pass

    logger.info(f"response: {response}")


def exo3() -> None:
    """
    download and save all anchors and all probes
    hints: methods get_atlas_probes / get_atlas_anchors
    """

    ####################################################################
    # TODO: download probes                                            #
    ####################################################################
    probes: list = None

    try:
        assert len(probes) > 1
        logger.info(f"retrieved {len(probes)} probes")
    except AssertionError:
        logger.error(f"No probes were downloaded")
        sys.exit(1)

    ####################################################################
    # TODO: download anchors                                           #
    ####################################################################
    anchors: list = None

    try:
        assert len(anchors) > 1
        logger.info(f"retrieved {len(anchors)} probes")
    except AssertionError:
        logger.error(f"No anchors were downloaded")
        sys.exit(1)

    ####################################################################
    # TODO: upload your files into the right directory                 #
    ####################################################################

    return probes, anchors


def exo4(country_codes: list) -> list:
    """write a function that get all probes and anchors
    located in one of the country listed
    """

    ####################################################################
    # TODO: From the set downloaded in exo2, retrieve all servers      #
    # located in Ukraine and Russia                                    #
    ####################################################################
    candidates: str = None

    if not candidates:
        raise RuntimeError(
            "There is at least one probes/anchor in Ukraine and/or Russia"
        )

    return candidates


def exo5(targets: list, start_time: str, stop_time: str) -> list:
    """from a list of probes retrieve a list of measurement results
    hints: check RIPE API parameter start_time__gte and start_time__lte
    """
    ####################################################################
    # TODO: From the list of servers we found in exo2, get their       #
    # measurement results                                              #
    # located in Ukraine and Russia                                    #
    ####################################################################
    measurements: list = None
    base_url: str = None

    if not base_url:
        raise RuntimeError("You must provide an url for this exo")

    if not measurements:
        raise RuntimeError("failed exo 4, you must retrieve measurements")
    else:
        logger.info("retrieved some measurements")

    return measurements


def exo6(event_date: str) -> dict:
    """From a list of measurements, get one 'old' and one 'new' measurement
    the idea is to have a reference measurement we can compare with another after an event
    """
    ####################################################################
    # TODO: From a list of measurements,                               #
    # get one 'old' and one 'new' measurement                          #
    # the idea is to have a reference measurement                      #
    # we can compare with another after an event                       #
    ####################################################################
    measurement_dataset: list = load_json(TP1_RESULTS_PATH / "results_exo4.json")
    analysis_dataset = defaultdict(dict)
    event_time = get_date_from_str(event_date)

    if analysis_dataset:
        raise RuntimeError("Failed at exo 5, you must return at least two measurements")

    return analysis_dataset


def exo7() -> None:
    """get measurement results for each pair of measurement and compare them"""
    ####################################################################
    # TODO: From a dataset of measurements pair (reference/after),     #
    # retrieve results, and compare each pair                          #
    ####################################################################
    analysis_dataset: dict = load_json(TP1_DATASET_PATH / "analysis.json")


if __name__ == "__main__":
    # comment methods you do not want to exec
    # (or uncomment otherwise)

    exo1()

    exo2()

    exo3()

    country_codes = ["RU"]
    exo4(country_codes)

    start_time = "01/01/2022 00:00:00"
    stop_time = "01/03/2022 00:00:00"
    exo5()

    event_date = "20/02/2022 00:00:00"
    exo6(event_date)

    exo7()

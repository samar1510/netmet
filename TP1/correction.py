"""execute each exercise or correction for TP1"""
import sys
import requests

from tqdm import tqdm
from collections import defaultdict
from common.file_utils import dump_json, load_json, dump_pickle, load_pickle
from common.default import (
    TP1_PROBES_PATH,
    TP1_ANCHORS_PATH,
    TP1_RESULTS_PATH,
    TP1_DATASET_PATH,
)

from common.logger_config import logger

from common.ripe.utils import (
    print_traceroute,
    get_date_from_timestamp,
    get_timestamp_from_date,
    get_date_from_str,
)
from common.ripe.ripe_atlas_api import (
    get_atlas_anchors,
    get_atlas_probes,
    get_all_results_from_request,
)


def exo1() -> dict:
    """retrieve a measurement using RIPE Atlas API, using a measurement uuid"""
    measurement_id = 38333397
    base_url = "https://atlas.ripe.net/api/v2/measurements"

    if not base_url:
        raise RuntimeError("url missing")
    else:
        ####################################################################
        # TODO: make an http request to RIPE API (using requests package)  #
        # to get measurement with measurement id : 38333397                #
        ####################################################################
        response = requests.get(f"{base_url}/{measurement_id}/").json()

    logger.info(f"response: {response}")


def exo2() -> dict:
    """retrieve measurement results"""
    measurement_id = 38333397
    base_url = "https://atlas.ripe.net/api/v2/measurements"

    if not base_url:
        raise RuntimeError("url missing")
    else:
        ####################################################################
        # TODO: make an http request to RIPE API (using requests package)  #
        # hints: check API ref to get specific measurement result          #
        ####################################################################
        results = requests.get(f"{base_url}/{measurement_id}/results").json()[0]

    logger.info(f"response: {results}")
    logger.info(f"measurement source : {results['from']}")
    logger.info(f"measurement type   : {results['type']}")

    # this measurement is a traceroute
    traceroute_results = results["result"]

    print_traceroute(traceroute_results)


def exo3() -> None:
    """
    download and save all anchors and all probes
    hints: methods get_atlas_probes / get_atlas_anchors
    """

    ####################################################################
    # TODO: download probes                                            #
    ####################################################################
    probes: list = None
    probes, _, _ = get_atlas_probes()

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
    anchors, _, _ = get_atlas_anchors()

    try:
        assert len(anchors) > 1
        logger.info(f"retrieved {len(anchors)} probes")
    except AssertionError:
        logger.error(f"No anchors were downloaded")
        sys.exit(1)

    ####################################################################
    # TODO: upload your files into the right directory                 #
    ####################################################################
    dump_json(probes, TP1_PROBES_PATH)
    logger.info("probes successfully saved")

    dump_json(anchors, TP1_ANCHORS_PATH)
    logger.info("anchors successfully saved")

    return probes, anchors


def exo4(country_codes: list) -> None:
    """write a function that get all probes and anchors
    located in one of the country listed
    """

    ####################################################################
    # TODO: From the set downloaded in exo2, retrieve all servers      #
    # located in Ukraine and Russia                                    #
    ####################################################################
    candidates: list = []

    anchors: list = load_json(TP1_ANCHORS_PATH)

    for probe in anchors:
        if probe["country_code"] in country_codes:
            candidates.append(probe)

    if not candidates:
        raise RuntimeError(
            "Failed exo 2: There is at least one probes/anchor in Ukraine and/or Russia"
        )
    else:
        logger.info(f"retrieved {len(candidates)} in country codes: {country_codes}")

    return candidates


def exo5(targets: list, start_time: str, stop_time: str, measurement_type: str) -> dict:
    """get all measurements towards a list of targets,
    performed within a given time interval
    and for a specific measurement type
    """

    target_measurements = defaultdict(list)
    base_url: str = "https://atlas.ripe.net/api/v2/measurements/"

    start_time = get_timestamp_from_date(start_time)
    stop_time = get_timestamp_from_date(stop_time)

    for target in tqdm(targets):
        target_ip = target["address_v4"]

        params = {
            "target_ip": target_ip,
            "start_time__gte": start_time,
            "start_time__lte": stop_time,
            "type": measurement_type,
        }

        for measurement in get_all_results_from_request(url=base_url, params=params):
            if "results" in measurement:
                target_measurements[target_ip].append(measurement)

    if not base_url:
        raise RuntimeError("You must provide an url for this exo")

    if not target_measurements:
        raise RuntimeError("failed exo 4, you must retrieve measurements")
    else:
        logger.info("retrieved some measurements")

    # save all results
    dump_pickle(target_measurements, TP1_RESULTS_PATH / "results_exo5.pickle")

    return target_measurements


def exo6(vps: list) -> dict:
    """get all results for each measurement"""
    event_related_measurements = defaultdict(list)
    vps_src_list = [vp["address_v4"] for vp in vps]

    target_measurements: dict = load_pickle(TP1_RESULTS_PATH / "results_exo5.pickle")

    for target_ip, measurements in tqdm(target_measurements.items()):
        for measurement in measurements:
            for result in measurement["results"]:
                result_url = result["result"]

                measurement_results = requests.get(result_url).json()

                for measurement_result in measurement_results:
                    src_addr = measurement_result["src_addr"]

                    if src_addr in vps_src_list:
                        # save measurement and measurement results
                        event_related_measurements[(target_ip, src_addr)].append(
                            measurement_result  # we keep the whole measurement so we have its end time and creation time
                        )

                        # save partial results as connection might brake
                        dump_pickle(
                            event_related_measurements,
                            TP1_RESULTS_PATH / "results_exo5.pickle",
                        )
    return event_related_measurements


def exo7(event_date: str) -> None:
    """From a list of measurements, get one 'old' and one 'new' measurement
    the idea is to have a reference measurement we can compare with another after an event
    """
    ####################################################################
    # TODO: From a list of measurements,                               #
    # get one 'old' and one 'new' measurement                          #
    # the idea is to have a reference measurement                      #
    # we can compare with another after an event                       #
    ####################################################################
    measurement_dataset: dict = load_pickle(TP1_RESULTS_PATH / "results_exo5.pickle")
    analysis_dataset = defaultdict(dict)
    event_time = get_date_from_str(event_date)

    for src_dst_pair, measurement_list in measurement_dataset.items():
        m_before: dict = {}
        m_after: dict = {}

        target_ip = src_dst_pair[0]
        vp_ip = src_dst_pair[1]

        # we need at least two measurements
        if len(measurement_list) > 1:
            # order by end time
            ordered_measurements = sorted(measurement_list, key=lambda x: x["endtime"])

            # get the oldest measurement as reference
            m_before = ordered_measurements[0]

            # get the last measurement made
            m_after = ordered_measurements[-1]

            # save one pair of measurements per target
            if m_before and m_after:
                logger.info(
                    f"""
                    target ip: {target_ip} | vp ip: {vp_ip}
                    measurement before event end time: {get_date_from_timestamp(m_before['endtime'])} \
                    measurement after event end time: {get_date_from_timestamp(m_after['endtime'])}
                    """
                )

                analysis_dataset[(target_ip, vp_ip)]["m_before"] = m_before
                analysis_dataset[(target_ip, vp_ip)]["m_after"] = m_after

    if not analysis_dataset:
        raise RuntimeError("Failed at exo 5, you must return at least two measurements")

    dump_pickle(analysis_dataset, TP1_DATASET_PATH / "analysis.pickle")

    return analysis_dataset


def exo8() -> None:
    """retrieve measurement result"""
    ####################################################################
    # TODO: write a method with a measurement description as input     #
    # and output the its results.                                      #
    # hints: in measurement description you have a results url         #
    ####################################################################
    analysis_dataset: dict = load_pickle(TP1_DATASET_PATH / "analysis.pickle")

    for src_dst_pair in analysis_dataset:
        target_ip, vp_ip = src_dst_pair

        logger.info(
            f"""
            ##################################################################################################################
            # Analyzing results for target_ip: {target_ip} | vp_ip: {vp_ip}                                                  
            ##################################################################################################################
            """
        )

        traceroute_before = analysis_dataset[src_dst_pair]["m_before"]
        traceroute_after = analysis_dataset[src_dst_pair]["m_after"]

        logger.info(
            f"""
            #########################################################
            # TRACEROUTE BEFORE EVENT                               #
            #########################################################
            """
        )
        print_traceroute(traceroute_before["result"])

        logger.info(
            f"""
            #########################################################
            # TRACEROUTE AFTER EVENT                                #
            #########################################################
            """
        )
        print_traceroute(traceroute_after["result"])


if __name__ == "__main__":
    # EXO 1
    # exo1()

    # EXO2
    # exo2()

    # # EXO 3
    # probes, anchors = exo3()

    # EXO 4
    # country_codes = ["UA", "RU"]
    # country_filtered_anchors = exo4(country_codes)

    # # # # # EXO 5
    # start_time = "01/01/2022 00:00:00"
    # stop_time = "01/05/2022 00:00:00"
    # measurement_type = "traceroute"
    # targets = load_json(TP1_DATASET_PATH / "ru_targets.json")
    # vps = load_json(TP1_DATASET_PATH / "ua_vps.json")

    # exo5(targets, start_time, stop_time, measurement_type)

    # exo6(vps)

    # # EXO 6
    event_date = "20/02/2022 00:00:00"
    exo7(event_date)

    # EXO 7
    exo8()

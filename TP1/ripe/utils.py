"""useful functions for working with response from RIPE Atlas"""
import time

from numpy import mean
from datetime import datetime

from settings.logger_config import logger


def print_traceroute(traceroute_results: list) -> None:
    """print traceroute result nicely"""
    logger.info(f"TTL | results | rtt")

    for hop_results in traceroute_results:
        # get results metrics
        ttl = hop_results["hop"]
        response = ""
        rtts = []
        for result in hop_results["result"]:
            if "from" in result:
                response += " " + result["from"]
                rtts.append(result["rtt"])
            else:
                response += " *"

        # in case we only have stars (no answers)
        rtt = None
        if rtts:
            rtt = mean(rtts)

        # print metrics
        logger.info(f"{ttl} , {response} , {rtt}")


def get_date_from_str(date: str) -> datetime.date:
    """get datetime object from str var"""
    return datetime.strptime(date, "%d/%m/%Y %H:%M:%S")


def get_date_from_timestamp(timestamp: str) -> datetime.date:
    """return a datetime from a timestamp"""
    return datetime.fromtimestamp(timestamp)


def get_timestamp_from_date(date: datetime | str) -> str:
    """from a datetime format return unix timestamp"""
    if type(date) is str:
        date = datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
    return int(time.mktime(date.timetuple()))


if __name__ == "__main__":
    start_time = datetime(2022, 2, 19)
    end_time = datetime(2022, 2, 25)

    start_time = get_timestamp_from_date(start_time)
    end_time = get_timestamp_from_date(end_time)

    print(start_time)
    print(end_time)

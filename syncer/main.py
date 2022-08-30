import re
from typing import TextIO, Tuple

import requests
import yaml
from ics import Calendar, Event


class ParseCalendarListError(Exception):
    pass


class DowloadCalendarError(Exception):
    pass


def parseCalendarsFile(calendarsFile: TextIO) -> list[Tuple[str, str]]:
    """Parse the yaml imput from a file and construct the list of all
    the calendars' name and url.

    Args:
        calendarsFile (TextIO): The calendars file

    Returns:
        list[Tuple[str, str]]: A list of the calendars' name and url. 
    """
    calendarsList = yaml.safe_load(calendarsFile)
    calendarsList = [(calendar['name'], calendar['url'])
                     for calendar in calendarsList]
    return calendarsList


def getCalendarsListFromFile(calendarsPath: str) -> list[Tuple[str, str]]:
    """Read a YAML file with all the calendars and return a list of
    the calendars' name and url.

    Args:
        calendarsPath (str): The path of the YAML file containing the calendars list.

    Returns:
        list[Tuple[str, str]]: A list of the calendars' name and url.
    """

    try:
        with open(calendarsPath) as calendarsFile:
            return parseCalendarsFile(calendarsFile)
    except Exception:
        raise ParseCalendarListError()


def updateSyncLastStartTime() -> None:
    # TODO
    pass


def updateSyncLastEndTime() -> None:
    # TODO
    pass


def dowloadCalendar(url: str) -> str:
    """Dowload a calendar from is url.

    Args:
        url (str): The calendar's url.

    Returns:
        str: The isc file correspondaing to the calendar.
    """
    response = requests.get(url)
    if not response.ok:
        raise DowloadCalendarError()

    return response.text


def getAllCalendars(calendarsPath: str) -> list[Tuple[str, str]]:
    """Get all ics files for the calendars in the calendars list.

    Args:
        calendarListPath (str): The path to the calendar list.

    Returns:
        list[str]: A list of all calendars' name and ics files.
    """
    calendars = getCalendarsListFromFile(calendarsPath)
    return [(name, dowloadCalendar(url)) for name, url in calendars]


def getCleanName(event: Event) -> str:
    name = event.name.split(' - ')
    return name[1] if len(name) > 1 else name[0]


def getType(description: str) -> str:
    if description:
        matches = re.findall(r'type.*\n', description.lower())
        if matches:
            return matches[0].split(':')[1].strip()


def parseEvent(event: Event) -> None:
    # print(event.name, '\n'*3)
    pass


def syncCalendar(calendarName: str, calendarICS: str) -> None:
    calendar = Calendar(calendarICS)


def sync(calendarsListPath: str = 'calendars.yml') -> None:
    updateSyncLastStartTime()

    calendarsICS = getAllCalendars(calendarsListPath)

    for calendarName, calendarICS in calendarsICS:
        syncCalendar(calendarName, calendarICS)

    updateSyncLastEndTime()


if __name__ == '__main__':
    sync()

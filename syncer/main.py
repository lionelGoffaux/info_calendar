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


def getCleanName(eventName: str) -> str:
    """Clean the name of an event.

    Args:
        eventName (str): The name of the event.

    Returns:
        str: The clean name of the event.
    """
    name = eventName.split(' - ')
    return name[1] if len(name) > 1 else name[0]


def getType(description: str) -> str|None:
    """Get the type of the event from its description.

    Args:
        description (str): The description of the event.

    Returns:
        str|None: The type of the event or None if the event has no type.
    """
    if description:
        matches = re.findall(r'type.*\n', description.lower())
        if matches:
            return matches[0].split(':')[1].strip()
        
        
def parseEvent(event: Event, result: dict[str, Calendar]) -> None:
    """Parse an event and add it to the result dictionary.

    Args:
        event (Event): The event to parse.
        result (dict[str, Calendar]): The result dictionary.
    """
    event.name = getCleanName(event.name)
    result.get(event.name, Calendar()).events.add(event)
    
    event_type = getType(event.description) if event.description else None

    if event_type:
        result.get(f'{event.name}/{event_type}', Calendar()).events.add(event)
        
        
def parseCalendar(calendarName: str, calendar: Calendar) -> dict[str, Calendar]:
    """Parse a calendar and return a dictionary of the different calendars 
    one for each course and one for each type of event of a same course.

    Args:
        calendarName (str): The name of the calendar.
        calendar (Calendar): The calendar to parse.

    Returns:
        dict[str, Calendar]: The result calendars and their keys.
    """
    result = {}
    
    for event in calendar.events:
        parseEvent(event, result)

    return result


def syncCalendar(calendarName: str, calendarICS: str) -> None:
    calendar = Calendar(calendarICS)
    
    parsed_calendars = parseCalendar(calendarName, calendar)
    
    #TODO: save the calendars in the database


def sync(calendarsListPath: str = 'calendars.yml') -> None:
    #TODO: capture and log the exceptions
    updateSyncLastStartTime()

    calendarsICS = getAllCalendars(calendarsListPath)

    for calendarName, calendarICS in calendarsICS:
        syncCalendar(calendarName, calendarICS)

    updateSyncLastEndTime()


if __name__ == '__main__':
    #TODO: run the sync function on a regular basis (using scheduler)
    sync()

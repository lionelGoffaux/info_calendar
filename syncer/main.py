import asyncio
import re
import logging
from typing import TextIO

import httpx
import yaml
import schedule
from ics import Calendar
from ics.event import Event


class ParseCalendarListError(Exception):
    pass


class DownloadCalendarError(Exception):
    pass


def parse_calendars_file(calendars_file: TextIO) -> list[tuple[str, str]]:
    """Parse the yaml input from a file and construct the list of all
    the calendars' name and url.

    Args:
        calendars_file (TextIO): The calendars file

    Returns:
        list[tuple[str, str]]: A list of the calendars' name and url. 
    """
    calendars_list = yaml.safe_load(calendars_file)
    calendars_list = [(calendar['name'], calendar['url'])
                      for calendar in calendars_list]
    return calendars_list


def get_calendars_list_from_file(calendars_path: str) -> list[tuple[str, str]]:
    """Read a YAML file with all the calendars and return a list of
    the calendars' name and url.

    Args:
        calendars_path (str): The path of the YAML file containing the calendars list.

    Returns:
        list[tuple[str, str]]: A list of the calendars' name and url.
    """

    try:
        with open(calendars_path) as calendarsFile:
            return parse_calendars_file(calendarsFile)
    except Exception:
        raise ParseCalendarListError()


def update_sync_last_start_time():
    # TODO
    logging.info(f'a synchronization started at')


def update_sync_last_end_time():
    # TODO
    logging.info(f'a synchronization ended at')


async def download_calendar(client: httpx.AsyncClient, url: str) -> str:
    """Download a calendar from is url.

    Args:
        client (httpx.AsyncClient): The client to use to download the calendar.
        url (str): The calendar's url.

    Returns:
        str: The isc file corresponding to the calendar.
    """
    try:
        response = await client.get(url)
    except (httpx.ConnectTimeout, httpx.ConnectError):
        raise DownloadCalendarError()

    if not response.status_code == 200:
        raise DownloadCalendarError()

    logging.info(f"successfully download calendar at {url}")
    return response.text


async def get_all_calendars(calendars_path: str) -> list[tuple[str, str]]:
    """Get all ics files for the calendars in the calendars list.

    Args:
        calendars_path (str): The path to the calendar list.

    Returns:
        list[tuple[str, str]]: A list of all calendars' name and ics files.
    """
    async with httpx.AsyncClient() as client:
        calendars_list = get_calendars_list_from_file(calendars_path)
        calendars_ics = await download_all_calendars(calendars_list, client)
        calendars = [(name, calendar) for (name, _), calendar in zip(calendars_list, calendars_ics)]
        return calendars


async def download_all_calendars(calendars_list, client):
    tasks = []
    for _, calendarURL in calendars_list:
        tasks.append(asyncio.create_task(download_calendar(client, calendarURL)))
    calendars = await asyncio.gather(*tasks)
    return calendars


def get_clean_name(event_name: str) -> str:
    """Clean the name of an event.

    Args:
        event_name (str): The name of the event.

    Returns:
        str: The clean name of the event.
    """
    name = event_name.split(' - ')
    name = name[1] if len(name) > 1 else name[0]
    return name


def get_type(event: Event) -> str | None:
    """Get the type of the event from its description.

    Args:
        event (Event): The event.

    Returns:
        str|None: The type of the event or None if the event has no type.
    """
    if event.description:
        matches = re.findall(r'type.*\n', event.description.lower())
        if matches:
            return matches[0].split(':')[1].strip()


def is_canceled(event: Event) -> bool:
    return event.name and "annulé" in event.name.lower()


def set_proper_event_name(event: Event):
    """Set a proper name for a event.

    Args:
        event (Event):  The event.
    """
    event.name = get_clean_name(event.name)
    if is_canceled(event):
        event.name = '[annulé] ' + event.name


def add_event_to_courses_calendars(event, courses_calendars):
    """Add an event to its courses calendars.

    Args:
        event (Event):
        courses_calendars (dict[str, Calendar]): The courses calendars
    """
    courses_calendars.get(event.name, Calendar()).events.add(event)

    event_type = get_type(event)
    if event_type:
        courses_calendars.get(f'{event.name}/{event_type}', Calendar()).events.add(event)


def split_into_courses_calendars(calendar: Calendar) -> dict[str, Calendar]:
    """Split a calendar into a calendar into multiple calendars one for each course.

    Args:
        calendar (Calendar): The calendar to parse.

    Returns:
        dict[str, Calendar]: The courses_calendar calendars and their keys.
    """
    courses_calendars = {}
    for event in calendar.events:
        set_proper_event_name(event)
        add_event_to_courses_calendars(event, courses_calendars)

    return courses_calendars


def sync_calendar(calendar_name: str, calendar_ics: str) -> None:
    calendar = Calendar(calendar_ics)

    parsed_calendars = split_into_courses_calendars(calendar)

    # TODO: save the calendars in the database


async def sync_all_calendars(calendars_ics):
    for calendar_name, calendar_ics in calendars_ics:
        sync_calendar(calendar_name, calendar_ics)
        logging.info(f"successfully sync {calendar_name}")


async def sync(calendars_list_path: str = 'calendars.yml'):
    update_sync_last_start_time()

    calendars_ics = await get_all_calendars(calendars_list_path)
    await sync_all_calendars(calendars_ics)

    update_sync_last_end_time()


def sync_job():
    """
    Launch the sync and handle the possible errors.
    """
    try:
        asyncio.run(sync())
    except DownloadCalendarError:
        logging.error('an error occur during the download of the calendars')
    except ParseCalendarListError:
        logging.error('an error occur during the parsing of the calendars list')


def main():
    set_logging_config()

    schedule.every(15).minutes.do(sync_job)

    while True:
        schedule.run_pending()


def set_logging_config():
    log_format = '[%(levelname)s] %(asctime)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)


if __name__ == '__main__':
    main()

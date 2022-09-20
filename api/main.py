import base64
import logging

import redis
from flask import Flask, request, jsonify

app = Flask(__name__)
redis = redis.Redis(host='redis')


def decode_set(encoded_set: set) -> set:
    """Decode a set of bytes to a set of str.

    Args:
        encoded_set(set): The set to decode.

    Returns:
        set: The decoded set.
    """
    return {item.decode('utf-8') for item in encoded_set}


@app.route("/api/courses/<calendar_name>/<course_name>")
def list_course_type(calendar_name, course_name):
    """List all course types of a course.
    Args:
        calendar_name(str): The calendar's name.
        course_name(str): The course's name.
    """
    course_types = redis.smembers(f'coursesList/{calendar_name}/{course_name}')
    if not course_types:
        return jsonify({'error': 'course not found'}), 404

    course_types_list = list(decode_set(course_types))
    course_types_list.sort()

    return jsonify(course_types_list)


@app.route("/api/courses/<calendar_name>")
def list_calendar_courses(calendar_name: str):
    """List all courses in a calendar.

    Args:
        calendar_name(str): The calendar's name.
    """

    courses = redis.smembers(f'coursesList/{calendar_name}')
    if not courses:
        return jsonify({'error': 'calendar not found'}), 404

    courses_list = list(decode_set(courses))
    courses_list.sort()

    return jsonify(courses_list)


@app.route("/api/list_calendars")
def list_calendars():
    """Return the list of all the calendar."""
    calendars = redis.smembers("calendars")
    if calendars is None:
        return "Not Found", 404

    calendars_list = list(decode_set(calendars))
    calendars_list.sort()

    return jsonify(calendars_list)


@app.route("/api/update_info")
def update_info():
    """Return the last update start time and the last update end time."""
    return jsonify({
        'updateStart': redis.get('updateStart').decode(),
        'updateEnd': redis.get('updateEnd').decode()
    })


@app.route("/calendar.ics")
def calendar():
    """Return the calendar in the ics format using the courses list in parameter.
    The list is a JSON list in base64 of the courses' name.
    Examples:
        - http://localhost/calendar.ics?courses=WyJiYWMxL2Jpb2xvZ3kvdHAiLCAibWExL21hdGhzIl0= -> ["bac1/biology/tp", "ma1/maths"]
    """
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

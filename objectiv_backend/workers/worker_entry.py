"""
Copyright 2021 Objectiv B.V.
"""
import time
from typing import List, Tuple

from objectiv_backend.schema.validate_events import validate_event_adheres_to_schema, validate_event_time, EventError
from objectiv_backend.common.types import EventDataList


def process_events_entry(events: EventDataList, current_millis: int = 0) -> \
        Tuple[EventDataList, EventDataList, List[EventError]]:
    """
    Split event list on events that pass validation and those that don't

    :param events: List of events. validate_structure_event_list() must pass on this list.
    :param current_millis: (current) timestamp to compare events with
    :return: tuple with three lists. Both event lists have the hydrated types.
        1) ok events: events that passed validation
        2) not-ok events: events that didn't pass validation
        3) list of errors per event
    """
    ok_events: EventDataList = []
    nok_events: EventDataList = []
    event_errors = []

    if current_millis == 0:
        current_millis = round(time.time() * 1000)

    for event in events:

        error_info = \
            validate_event_adheres_to_schema(event=event) + \
            validate_event_time(event=event, current_millis=current_millis)

        if error_info:
            print(f"error, event_id: {event['id']}, errors: {[ei.info for ei in error_info]}")
            nok_events.append(event)
            event_errors.append(EventError(event_id=event['id'], error_info=error_info))
        else:
            ok_events.append(event)
    return ok_events, nok_events, event_errors



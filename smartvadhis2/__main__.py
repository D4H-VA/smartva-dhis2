#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from logzero import logger

from .core.config import setup as setup_with_config
from .core.helpers import read_csv, parse_args
from .core.verbalautopsy import Event, verbal_autopsy_factory
from .core.exceptions.base import SmartVADHIS2Exception
from .core.exceptions.errors import ImportException, DuplicateEventImportError


def smartva_to_dhis2(db, dhis, smartva_file):
    if smartva_file:
        for i, record in enumerate(read_csv(smartva_file), 1):
            logger.info("{0} ROW NUMBER: {1} {0}".format('----------', i))
            va, exceptions, warnings = verbal_autopsy_factory(record)
            if warnings:
                [logger.warn("{} for record {}".format(warning, record)) for warning in warnings]
            if not exceptions:
                event = Event(va)
                try:
                    dhis.is_duplicate(va.sid)
                except DuplicateEventImportError as e:
                    logger.exception(e)
                    db.write_errors(va, e)
                else:
                    try:
                        dhis.post_event(event.payload)
                    except ImportException as e:
                        logger.exception("{}\nfor payload {}".format(e, event.payload))
                        db.write_errors(va, [e])
            else:
                [logger.exception("{} for record {}".format(exception, record)) for exception in exceptions]
                db.write_errors(va, exceptions)


def run(arguments):
    dhis, briefcase, smartva, db = setup_with_config()

    smartva_file = None
    if arguments.briefcase_file:
        smartva_file = smartva.run(arguments.briefcase_file, manual=True)
    else:
        briefcase_file = briefcase.download_briefcases(arguments.all)
        if briefcase_file:
            smartva_file = smartva.run(briefcase_file)
        else:
            logger.warning("No new briefcases downloaded")

    smartva_to_dhis2(db, dhis, smartva_file)


def main():
    try:
        args = parse_args(sys.argv[1:])
        run(args)
    except KeyboardInterrupt:
        logger.warning("Aborted!")
    except Exception as e:
        raise SmartVADHIS2Exception(e)


if __name__ == '__main__':
    main()
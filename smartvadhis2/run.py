import argparse
import sys
from datetime import datetime, timedelta
import os

from logzero import logger
from apscheduler.schedulers.blocking import BlockingScheduler


from .core.config import setup as setup_with_config, DatabaseConfig
from .core.helpers import read_csv, is_non_zero_file, get_timewindow
from .core.verbalautopsy import Event, verbal_autopsy_factory
from .core.exceptions.base import SmartVADHIS2Exception, NoODKDataException
from .core.exceptions.errors import ImportException, DuplicateEventImportError


def _parse_args(args=sys.argv[1:]):
    """Parse arguments"""
    parser = argparse.ArgumentParser(usage='%(prog)s', description=u"Run SmartVA and import to DHIS2")

    group = parser.add_mutually_exclusive_group()

    group.add_argument(u'--manual',
                       dest='manual',
                       action='store',
                       required=False,
                       help=u"Skip download of briefcase file, provide local file path instead"
                       )

    group.add_argument(u'--all',
                       dest='all',
                       action='store_true',
                       default=False,
                       required=False,
                       help=u"Pull all briefcases instead of relative time window"
                       )

    arguments = parser.parse_args(args)
    if arguments.manual and not os.path.exists(arguments.manual):
        raise FileNotFoundError(u"Briefcase file does not exist: {}".format(arguments.manual))
    return arguments


def _schedule():
    """
    Background scheduler that runs forever, schedules to (other) SQLite database
    """
    scheduler = BlockingScheduler()
    url = r'sqlite:///{}'.format(os.path.join(DatabaseConfig.database_dir, 'scheduling.db'))
    scheduler.add_jobstore('sqlalchemy', url=url)
    SECONDS = 30
    scheduler.add_job(_run,
                      'interval',
                      seconds=SECONDS,
                      args=[False, False],
                      replace_existing=True,
                      id='smartvadhis2runner')
    logger.info("Started scheduling every {} seconds".format(SECONDS))
    scheduler.start()


def _run(manual, download_all):
    """
    Method with the application logic.
    """
    dhis, briefcase, smartva, db = setup_with_config()

    new_data = False
    if manual:
        smartva_file = smartva.run(manual, manual=True)
    else:
        briefcase_file = briefcase.download_briefcases(download_all)
        smartva_file = None
        if is_non_zero_file(briefcase_file):
            try:
                smartva_file = smartva.run(briefcase_file)
            except NoODKDataException:
                pass
            else:
                new_data = True
        else:
            logger.debug("briefcase file is empty: {}".format(briefcase_file))

    if new_data:
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
                    db.write_errors(record, e)
                else:
                    try:
                        dhis.post_event(event.payload)
                    except ImportException as e:
                        logger.exception("{}\nfor payload {}".format(e, event.payload))
                        db.write_errors(record, [e])
            else:
                [logger.exception("{} for record {}".format(exception, record)) for exception in exceptions]
                db.write_errors(record, exceptions)
    else:
        logger.warn("No new data to process in time window {} - {}".format(*get_timewindow()))


def launch():
    try:
        opts = _parse_args()
        if not any([opts.manual, opts.all]):
            try:
                _schedule()
            except (KeyboardInterrupt, SystemExit):
                pass
        else:
            _run(manual=opts.manual, download_all=opts.all)
    except KeyboardInterrupt:
        logger.warning("Aborted!")
    except Exception as e:
        raise SmartVADHIS2Exception(e)

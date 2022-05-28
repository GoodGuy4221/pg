import logging

logging.basicConfig(
    filename='test.log',
    format='%(levelname)s %(asctime)s %(message)s',
    level=logging.WARNING,
)

LOG = logging.getLogger()

LOG.warning('hello')
LOG.info('info')

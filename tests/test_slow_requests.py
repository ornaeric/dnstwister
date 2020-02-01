import datetime

import dnstwister.tools
from dnstwister.core.domain import Domain


def test_large_domain_is_reasonable_in_performance():
    """Looooong domain names highlighted that the idna decoding is slooooow.

    This is a basic benchmark for performance, based on a bot's behaviour
    recently.
    """
    domain = 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz.zzzzzzzzzzzzzzzzzzzzzzzzzppieo.com'

    start = datetime.datetime.now()

    dnstwister.tools.fuzzy_domains(Domain(domain))

    duration = (datetime.datetime.now() - start).total_seconds()

    assert duration < 10, 'duration too long: {} secs'.format(duration)

    print('Long domain name fuzzed in: {} seconds'.format(duration))

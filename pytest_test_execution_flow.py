import pytest


MARKS = {
    'skip_all_after_this_fail': pytest.skip,
    'fail_all_after_this_fail': pytest.fail,
}


def pytest_addoption(parser):
    parser.addini(
        'run_at_start',
        type='args',
        help='These tests will be launched at the beginning of the session.'
    )

    parser.addini(
        'run_at_end',
        type='args',
        help='These tests will be launched at the ending of the session.'
    )


def pytest_configure(config):
    for mark in MARKS:
        config.addinivalue_line('markers', mark)
    run_at_start = config.getini('run_at_start')
    run_at_end = config.getini('run_at_end')
    config.sequence_manager = SequenceManager(run_at_start, run_at_end)
    config.pluginmanager.register(config.sequence_manager)


def pytest_unconfigure(config):
    sequence_manager = getattr(config, 'sequence_manager', None)
    if sequence_manager:
        config.pluginmanager.unregister(config.sequence_manager)
        del config.sequence_manager


class SequenceManager:
    def __init__(self, run_at_start, run_at_end):
        self.action = None
        self.reason = None
        self.run_at_start = run_at_start
        self.run_at_end = [i for i in run_at_end if i not in run_at_start]

    def pytest_collection_modifyitems(self, session, config, items):
        _items = items[:]
        nose, tail = [], []
        for test_name in self.run_at_start:
            for k in _items:
                if k.name == test_name:
                    _items.remove(k)
                    nose.append(k)
        for test_name in self.run_at_end:
            for k in _items:
                if k.name == test_name:
                    _items.remove(k)
                    tail.append(k)
        items[:] = nose + _items + tail

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        res = outcome.get_result()
        if res.when == 'call':
            if res.outcome == 'failed' and not self.action:
                for mark, action in MARKS.items():
                    if item.get_closest_marker(mark):
                        self.action = action
                        self.reason = action.__name__
                        break

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_call(self, item):
        if self.action:
            msg = 'This test {0}ed because test - {1} was failed!'.format(self.reason, item.name)
            self.action(msg)

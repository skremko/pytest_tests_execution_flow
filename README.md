

pytest-tests-execution-flow
==============================================================================

pytest-tests-execution-flow is a plugin for pytest, which allows to set tests that
must be started at the beginning and end of the session. The plugin also provides two marks
`skip_all_after_this_fail` and `fail_all_after_this_fail`, which allows you to skip\fail
next tests if the marked tests fail.

Requirements
==============================================================================

You will need the following prerequisites in order to use pytest-tests-execution-flow:

- Python 2.7, 3.6
- Pytest 4.1.0 or higher

Installation
==============================================================================
Install the plugin with::

    pip install pytest-tests-execution-flow

Usage
==============================================================================
Prepare the config file :code:`pytest.ini` in root directory of tests

Example of `pytest.ini`:

    [pytest]
    run_at_start=
        test_5
        test_4 
    run_at_end=
        test_1
        test_2 

If same test name exist at both parameters it will be run at start.

""" Tests for calculations

"""
import os
import pytest
from aiida.utils.fixtures import fixture_manager
import {{cookiecutter.module_name}}.tests as tests


@pytest.fixture(scope='session')
def aiida_profile():
    """setup a test profile for the duration of the tests"""
    with fixture_manager() as fixture_mgr:
        yield fixture_mgr


@pytest.fixture(scope='function')
def new_database(aiida_profile):
    """clear the database after each test"""
    yield
    aiida_profile.reset_db()


def test_submit(new_database):        
    # Set up code, if it does not exist
    code = tests.get_code(entry_point='{{cookiecutter.entry_point_prefix}}')

    from aiida.orm.data.singlefile import SinglefileData

    # Prepare input parameters
    from aiida.orm import DataFactory
    DiffParameters = DataFactory('{{cookiecutter.entry_point_prefix}}')
    parameters = DiffParameters({'ignore-case': True})

    file1 = SinglefileData(file=os.path.join(tests.TEST_DIR, 'file1.txt'))
    file2 = SinglefileData(file=os.path.join(tests.TEST_DIR, 'file2.txt'))

    # set up calculation
    calc = code.new_calc()
    calc.label = "{{cookiecutter.module_name}} test"
    calc.description = "Test job submission with the {{cookiecutter.module_name}} plugin"
    calc.set_max_wallclock_seconds(30)
    calc.set_withmpi(False)
    calc.set_resources({"num_machines": 1, "num_mpiprocs_per_machine": 1})

    calc.use_parameters(parameters)
    calc.use_file1(file1)
    calc.use_file2(file2)

    calc.store_all()
    calc.submit()
    print("submitted calculation; calc=Calculation(uuid='{}') # ID={}"\
            .format(calc.uuid,calc.dbnode.pk))

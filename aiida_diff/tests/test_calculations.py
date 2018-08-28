""" Tests for calculations

"""
import os
import aiida_diff.tests as tests


def test_submit(new_database):
    """test submission of code"""
    from aiida.orm.data.singlefile import SinglefileData
    from aiida.common.folders import SandboxFolder

    # Set up code, if it does not exist
    code = tests.get_code(entry_point='diff')

    # Prepare input parameters
    from aiida.orm import DataFactory
    DiffParameters = DataFactory('diff')
    parameters = DiffParameters({'ignore-case': True})

    file1 = SinglefileData(file=os.path.join(tests.TEST_DIR, 'file1.txt'))
    file2 = SinglefileData(file=os.path.join(tests.TEST_DIR, 'file2.txt'))

    # set up calculation
    calc = code.new_calc()
    # calc.label = "aiida_diff test"
    # calc.description = "Test job submission with the aiida_diff plugin"
    # calc.set_max_wallclock_seconds(30)
    calc.set_withmpi(False)
    calc.set_resources({"num_machines": 1, "num_mpiprocs_per_machine": 1})

    calc.use_parameters(parameters)
    calc.use_file1(file1)
    calc.use_file2(file2)

    calc.store_all()

    # output input files and scripts to temporary folder
    with SandboxFolder() as folder:
        subfolder, script_filename = calc.submit_test(folder=folder)
        print("inputs created successfully at {}".format(subfolder.abspath))
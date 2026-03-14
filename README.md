# Modelling the Motion of a Spinning Cricket Ball

This codebase was created as part of my Mathematics MMath dissertation.

## Non-technical Information

Go to the 'test' folder, then go to the 'test_results' folder. Go to any test case foler - e.g. 'Default_leg_spin' - where you can find '.txt. files with numerical data, '.png' files each with a 2D and 3D visualisation of the ball's trajectory, and '.gif' files each with a video simulation from different viewpoints from the field.

## Technical Information

### Viewing results

Navigate to 'test/test_results'. Plots, data and simulations can be found inside each test case directory.

### Usage / Reproduce test results

Run:

To generate constant values which will be used by all scripts,
'cd src'
'python3 gen_constants.py'

To generate test case parameter sets which will be used by plotting and simulating scripts,
'cd ../test'
'python3 gen_test_cases.py'

To execute the model and produce trajectory plots for all test cases,
'python3 run_plots_for_all_tests.py' 
or alternatively 'python3 ../src/plots3D.py <test case number> <debug mode>' for each test case (specified by number) where debug mode is 0 (off) or 1 (on)
Also, 'python3 collate_plots.py <common test case name> <comma-separated values>' and 'python3 summary_file_regen.py' can be run to generate or re-generate data if required.

To produce a simulation from all viewpoints for each test case,
'python3 run_sim_for_all_tests.py' ensuring all simulations close once completed (IMPORTANT: Python may need to be quit manually)
or alternatively 'python3 ../src/sim3D.py <test case number> <viewpoint>' for each test case (specified by number) where viewpoint can be one of ["diagonal", "sideon", "bowler", "top-down", "umpire", "batter", "wicket-keeper"] without quotes

### Trouble shooting

Files 'src/constants.txt' and 'test/test_cases.txt' must exist and be populated for model execution and plot production (i.e. to run 'plots3D.py'). 
File '<test case name>/plot3D_output.txt' must exist and be populated for simulation generation (i.e. to run 'sim3D.py').

Scripts 'run_plots_for_all_tests.py' and 'run_sim_for_all_tests.py' execute the smaller scripts 'plots3D.py', 'sim3D.py', 'collate_plots.py' so inspection of the code in the former two scripts can help with running the latter three scripts successfully.
This projects contains multiple scripts that process events from an HDF5 file.

# Plotting relevant scripts

## recover_current.py
Recovers the actual current (measured_current = 0.5 * real_current)

## modify_csvs.py
Calculates additional things and adds them to the CSVs (creates a copy of the original and puts the new ones into a separate directory)

## scatter_plots.py
Creates scatter plots that can be opened in a browser

# DTW analysis relevant scripts

## trim_events.py
Trims the events based off of where they actually start and finish. Also calculates some other parameters and writes everything into a new CSV.

## dtw_analysis.py
Performs DTW analysis on the trimmed events and plots the result.

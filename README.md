This projects contains multiple scripts that process events from an HDF5 file.

# recover_current.py
Recovers the actual current (measured_current = 0.5 * real_current)

# trim_events.py
Trims the events based off of where they actually start and finish. Also calculates some other parameters and writes everything into a new CSV.

# dtw_analysis.py
Performs DTW analysis on the trimmed events and plots the result.

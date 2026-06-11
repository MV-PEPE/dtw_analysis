"""
Separate Interactive Histograms
---------------------------------
Loads event metadata from all CSVs in data_with_real_current and
data_with_recovered_current, groups them by folder prefix, and
generates two interactive histogram figures (count vs. resistance
and count vs. dwell time) with a separate subplot per group.

Requirements:
    pip install pandas plotly
"""

import pandas as pd                      # for loading and combining CSV metadata
import plotly.graph_objects as go        # for building interactive histograms
from plotly.subplots import make_subplots  # for creating subplot grids
import plotly.io as pio                  # for saving interactive HTML files
from pathlib import Path                 # for navigating the folder structure
import math                              # for computing subplot grid dimensions

# ── Configuration ─────────────────────────────────────────────────────────────

DATA_DIRS = [
    Path("data/data_for_plots/data_with_real_current"),       # directory with real current data
    Path("data/data_for_plots/data_with_recovered_current"),  # directory with recovered current data
]

GROUPS = {
    "aLA_holo_1": "aLA holo 1",  # group display names
    "BSA_1":      "BSA 1",
    "BSA_2":      "BSA 2",
    "BSA_3":      "BSA 3",
    "aLA_apo_1":  "aLA apo 1",
    "aLA_holo_2": "aLA holo 2",
}

COLORS = {
    "aLA_holo_1": "#e6194b",  # red
    "BSA_1":      "#3cb44b",  # green
    "BSA_2":      "#4363d8",  # blue
    "BSA_3":      "#f58231",  # orange
    "aLA_apo_1":  "#911eb4",  # purple
    "aLA_holo_2": "#42d4f4",  # cyan
}

OUTPUT_DIR = Path("histograms/histograms_separate")  # directory to save the output HTML files

# ── Load and group CSVs ────────────────────────────────────────────────────────

group_data = {g: [] for g in GROUPS}  # dictionary to collect dataframes per group

for data_dir in DATA_DIRS:                               # loop over both data directories
    for csv_path in data_dir.rglob("*.csv"):             # recursively find all CSV files
        folder_name = csv_path.parent.name               # get the subfolder name
        for prefix in GROUPS:                            # check which group this folder belongs to
            if folder_name.startswith(prefix):           # match folder name to group prefix
                df = pd.read_csv(csv_path)               # load the CSV
                df["group"] = prefix                     # tag each row with its group name
                group_data[prefix].append(df)            # add to the group's list
                break                                    # stop checking prefixes once matched

group_dfs = {}
for prefix, dfs in group_data.items():                   # loop over each group
    if dfs:                                              # only process groups that have data
        group_dfs[prefix] = pd.concat(dfs, ignore_index=True)  # combine all CSVs for this group
        print(f"Group '{prefix}': {len(group_dfs[prefix])} total events")
    else:
        print(f"Group '{prefix}': no data found")        # warn if a group has no data

# ── Plotting helper ────────────────────────────────────────────────────────────

OUTPUT_DIR.mkdir(exist_ok=True)  # create output directory if it doesn't exist

def make_separate_histograms(col_name, x_label, filename):
    """Create a figure with one subplot per group."""
    n_groups = len(group_dfs)                            # number of groups with data
    n_cols   = 2                                         # number of columns in subplot grid
    n_rows   = math.ceil(n_groups / n_cols)              # number of rows needed

    fig = make_subplots(
        rows=n_rows, cols=n_cols,                        # subplot grid dimensions
        subplot_titles=list(GROUPS[p] for p in group_dfs),  # title each subplot with group name
    )

    for i, (prefix, df) in enumerate(group_dfs.items()):
        row_idx = i // n_cols + 1  # row index for this subplot
        col_idx = i % n_cols + 1   # column index for this subplot

        fig.add_trace(
            go.Histogram(
                x=df[col_name],  # col_name is the function parameter
                name=GROUPS[prefix],                     # group display name for legend
                marker_color=COLORS[prefix],             # group color
                marker=dict(line=dict(width=2)),         # outline for step style
                xbins=dict(size=5),                      # fixed bin width of 5 MOhm for all groups
            ),
            row=row_idx, col=col_idx,                    # place in correct subplot position
        )

        fig.update_xaxes(title_text=x_label, row=row_idx, col=col_idx)
        fig.update_yaxes(title_text="Count",  row=row_idx, col=col_idx)

    fig.update_layout(
        showlegend=False,                                # hide legend since subplots have titles
        height=400 * n_rows,                            # scale figure height to number of rows
    )

    out_path = OUTPUT_DIR / filename                     # full output path
    pio.write_html(fig, str(out_path))                   # save interactive HTML file
    fig.show()                                           # open in browser
    print(f"Saved: {out_path}")                          # confirm the file was saved

# ── Generate histograms ────────────────────────────────────────────────────────

make_separate_histograms("resistance_MOhm", "R (MOhm)",        "separate_histograms_resistance.html")
make_separate_histograms("dwell_time_ms",   "Dwell Time (ms)", "separate_histograms_dwell_time.html")
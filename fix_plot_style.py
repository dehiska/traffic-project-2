"""Update the epistemic uncertainty dual-axis plot to match the lecture Pt3 style exactly."""
import json

path = r"C:\Users\owner\Downloads\Masters\Masters_Spring_2026\Advanced Deep Learning\Traffic Project 2\03_Advanced_Viz_and_Uncertainty.ipynb"

with open(path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# ── Update Cell 37: match the exact Pt3 Cell 78 lecture style ──
nb["cells"][37]["source"] = [
    "# == Dual-axis: Stress Test + Epistemic Uncertainty + Temperature Overlay ==\n",
    "# (Matching the exact lecture Pt3 Cell 78 style)\n",
    "\n",
    "fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 14))\n",
    "\n",
    "def plot_with_temp(ax, start, end, title,\n",
    "                   mu_base, low_base, high_base,\n",
    "                   mu_mod, low_mod, high_mod,\n",
    "                   mod_color, mod_label):\n",
    '    """Lecture-style dual-axis: Traffic + Temperature with MC Dropout CI."""\n',
    "    # Prepare primary data\n",
    "    t = test_window_df['timestamp'].iloc[start:end]\n",
    "    actual = y_test_true_inv[start:end]\n",
    "\n",
    "    # Get temperature in Fahrenheit for the lecture-style axis\n",
    "    if 'temp_c' in test_window_df.columns:\n",
    "        temp_c = test_window_df['temp_c'].iloc[start:end].values\n",
    "        temp_f = temp_c * 9/5 + 32  # convert C -> F for display\n",
    "    else:\n",
    "        temp_f = np.zeros(end - start)\n",
    "\n",
    "    # --- Secondary Axis for Temperature ---\n",
    "    ax_temp = ax.twinx()\n",
    "    ax_temp.plot(t, temp_f, color='gray', lw=1.5, ls=':',\n",
    "                 label='Outdoor Temp (\\u00b0F)')\n",
    "    ax_temp.set_ylabel('Temperature (\\u00b0F)', color='gray', fontsize=12)\n",
    "    ax_temp.tick_params(axis='y', labelcolor='gray')\n",
    "\n",
    "    # --- Primary Axis for Traffic ---\n",
    "    ax.plot(t, mu_base, label='Base Forecast (Mean)', color='C0', lw=2)\n",
    "    ax.fill_between(t, low_base, high_base, color='C0', alpha=0.2)\n",
    "\n",
    "    ax.plot(t, mu_mod, label=mod_label, color=mod_color, lw=2)\n",
    "    ax.fill_between(t, low_mod, high_mod, color=mod_color, alpha=0.15)\n",
    "\n",
    "    ax.plot(t, actual, color='black', linestyle='--', linewidth=3,\n",
    "            label='ACTUAL Traffic', alpha=0.7)\n",
    "\n",
    "    ax.set_title(title, fontsize=15, fontweight='bold')\n",
    "    ax.set_ylabel('Traffic Count (veh/hr)', fontsize=12)\n",
    "\n",
    "    # Merging legends from both axes (lecture style)\n",
    "    lines, labels = ax.get_legend_handles_labels()\n",
    "    lines2, labels2 = ax_temp.get_legend_handles_labels()\n",
    "    ax.legend(lines + lines2, labels + labels2, loc='upper left', ncol=3)\n",
    "    ax.grid(True, alpha=0.1)\n",
    "\n",
    "# Execute Plot 1: Hot Period (Summer)\n",
    "hot_time = test_window_df['timestamp'].iloc[h_idx] if h_idx < len(test_window_df) else 'N/A'\n",
    "plot_with_temp(ax1, h_start, h_end,\n",
    "               f'Summer: Heatwave Stress Test vs. Temp Signal ({hot_time})',\n",
    "               mu_h_base, lo_h_base, hi_h_base,\n",
    "               mu_h_hot, lo_h_hot, hi_h_hot,\n",
    "               'red', '+10\\u00b0F Forecast')\n",
    "\n",
    "# Execute Plot 2: Cold Period (Winter)\n",
    "cold_time = test_window_df['timestamp'].iloc[c_idx] if c_idx < len(test_window_df) else 'N/A'\n",
    "plot_with_temp(ax2, c_start, c_end,\n",
    "               f'Winter: Cold Snap Stress Test vs. Temp Signal ({cold_time})',\n",
    "               mu_c_base, lo_c_base, hi_c_base,\n",
    "               mu_c_cold, lo_c_cold, hi_c_cold,\n",
    "               'purple', '-10\\u00b0F Forecast')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.savefig(PROCESSED / 'viz_epistemic_with_temp.png', dpi=150, bbox_inches='tight')\n",
    "plt.show()\n",
]

with open(path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print("Cell 37 updated to match lecture Pt3 Cell 78 style.")

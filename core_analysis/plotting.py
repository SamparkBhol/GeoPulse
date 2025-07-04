import matplotlib.pyplot as plt
import io
import numpy as np
from matplotlib.colors import ListedColormap, BoundaryNorm
from typing import Dict
import tempfile
import rasterio
from rasterio.transform import from_bounds
import json
import leafmap.foliumap as leafmap

DW_CLASSES = {
    0: 'Water', 1: 'Trees', 2: 'Grass', 3: 'Flooded Vegetation', 4: 'Crops',
    5: 'Shrub & Scrub', 6: 'Built-up', 7: 'Bare Ground', 8: 'Snow & Ice'
}
VIS_CLASS_IDS = list(range(9))
VIS_PALETTE = [
    '#419bdf', '#397d49', '#88b053', '#7a87c6', '#e49635',
    '#dfc35a', '#c4281b', '#a59b8f', '#b39fe1'
]
cmap = ListedColormap(VIS_PALETTE)

def plot_land_cover_trends(df) -> bytes:
    """Plot land cover class percentage trends over time and return as PNG bytes."""
    class_colors = dict(zip(DW_CLASSES.values(), VIS_PALETTE))
    markers = ['o', 's', '^', 'v', 'D', 'P', '*', 'X', '>']
    fig, ax = plt.subplots(figsize=(14, 7))
    for i, class_name in enumerate(DW_CLASSES.values()):
        if class_name in df.columns:
            ax.plot(df.index, df[class_name], label=class_name, color=class_colors[class_name], marker=markers[i % len(markers)])
    ax.set(title="Land Cover Class Percentage Over Time", xlabel="Year", ylabel="Area (%)")
    ax.grid(True)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    plt.close(fig) # Close the figure to free memory
    buf.seek(0)
    return buf.getvalue()

def visualize_multiple_years(images_by_year: Dict[int, np.ndarray]) -> bytes:
    """Visualize land cover maps for multiple years and return as PNG bytes."""
    years = sorted(images_by_year)
    fig, axs = plt.subplots(2, 5, figsize=(20, 8))
    norm = BoundaryNorm(VIS_CLASS_IDS + [VIS_CLASS_IDS[-1] + 1], cmap.N)
    for ax, year in zip(axs.ravel(), years):
        im = ax.imshow(images_by_year[year], cmap=cmap, norm=norm)
        ax.set(title=str(year), xticks=[], yticks=[])
    for ax in axs.ravel()[len(years):]:
        ax.axis('off')
    cbar = fig.colorbar(im, ax=axs, ticks=VIS_CLASS_IDS, fraction=0.03, pad=0.01)
    cbar.ax.set_yticklabels(list(DW_CLASSES.values()))
    cbar.set_label("Land Cover Class", rotation=270, labelpad=15)
    fig.tight_layout(); plt.subplots_adjust(right=0.88)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    plt.close(fig) # Close the figure to free memory
    buf.seek(0)
    return buf.getvalue()

def show_overlay_on_map(image_array: np.ndarray, bbox) -> bytes:
    """Show a land cover overlay on a satellite map using leafmap and return as PNG bytes."""
    # For Vercel deployment, direct leafmap rendering to image is complex due to headless browser requirements.
    # Returning a placeholder image for now.
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.text(0.5, 0.5, "Map Placeholder (Interactive map requires frontend rendering)", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=12, wrap=True)
    ax.axis('off')
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()
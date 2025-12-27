#!/usr/bin/env python3
"""
Visualization script for the 1979 UK earthquake aftershock sequence.

This script creates:
1. Map plot showing aftershock locations
2. Depth profile cross-section
3. Time-magnitude distribution (seismicity rate)
4. Magnitude-frequency distribution (Gutenberg-Richter)

Requirements:
- pandas
- matplotlib
- cartopy (for map projections)
- numpy
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os
from datetime import datetime

# Try to import cartopy for mapping, but provide fallback
try:
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    CARTOPY_AVAILABLE = True
except ImportError:
    CARTOPY_AVAILABLE = False
    print("Warning: cartopy not available. Map plots will use simple scatter.")

def load_aftershock_data(filepath):
    """Load aftershock data from CSV file."""
    df = pd.read_csv(filepath, comment='#')
    # Convert date and time to datetime
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
    return df

def create_map_plot(df, output_path=None):
    """Create a map of aftershock locations."""
    fig = plt.figure(figsize=(12, 10))
    
    if CARTOPY_AVAILABLE:
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.set_extent([-3, 0, 53.5, 55.5], crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS, linestyle=':')
        ax.add_feature(cfeature.LAND, alpha=0.3)
        ax.add_feature(cfeature.OCEAN, alpha=0.3)
        ax.gridlines(draw_labels=True)
        title = '1979 UK Earthquake Aftershock Locations (Cartopy)'
    else:
        ax = plt.axes()
        title = '1979 UK Earthquake Aftershock Locations'
    
    # Color by depth
    scatter = ax.scatter(df['longitude'], df['latitude'], 
                         c=df['depth_km'], s=df['magnitude']**3 * 10,
                         alpha=0.7, cmap='viridis_r', edgecolor='k', linewidth=0.5)
    
    # Add colorbar
    plt.colorbar(scatter, ax=ax, label='Depth (km)')
    
    # Add magnitude legend
    magnitude_legend = [2, 3, 4]
    for mag in magnitude_legend:
        ax.scatter([], [], c='gray', s=mag**3 * 10, alpha=0.7,
                   label=f'M {mag}', edgecolor='k')
    
    ax.legend(title='Magnitude Scale', scatterpoints=1, frameon=True)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title(title)
    
    # Mark main shock
    main_shock = df[df['magnitude'] == df['magnitude'].max()].iloc[0]
    ax.scatter(main_shock['longitude'], main_shock['latitude'],
               s=400, marker='*', color='red', edgecolor='k', linewidth=1.5,
               label='Main shock (M {})'.format(main_shock['magnitude']))
    ax.legend()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Map plot saved to {output_path}")
    else:
        plt.show()

def create_depth_profile(df, output_path=None):
    """Create depth profile cross-section."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Depth vs longitude
    ax1.scatter(df['longitude'], df['depth_km'], c=df['magnitude'],
                s=df['magnitude']**2 * 20, alpha=0.7, cmap='hot_r', edgecolor='k')
    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Depth (km)')
    ax1.set_title('Depth-Longitude Cross-section')
    ax1.invert_yaxis()  # Depth increases downward
    ax1.grid(True, alpha=0.3)
    
    # Depth vs latitude
    ax2.scatter(df['latitude'], df['depth_km'], c=df['magnitude'],
                s=df['magnitude']**2 * 20, alpha=0.7, cmap='hot_r', edgecolor='k')
    ax2.set_xlabel('Latitude')
    ax2.set_ylabel('Depth (km)')
    ax2.set_title('Depth-Latitude Cross-section')
    ax2.invert_yaxis()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Depth profile saved to {output_path}")
    else:
        plt.show()

def create_time_series(df, output_path=None):
    """Create time-magnitude and seismicity rate plots."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Time-magnitude plot
    ax1.scatter(df['datetime'], df['magnitude'], c=df['depth_km'],
                s=df['magnitude']**2 * 15, alpha=0.7, cmap='coolwarm', edgecolor='k')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Magnitude')
    ax1.set_title('Aftershock Time-Magnitude Distribution')
    ax1.grid(True, alpha=0.3)
    
    # Seismicity rate (cumulative count)
    df_sorted = df.sort_values('datetime')
    df_sorted['cumulative_count'] = range(1, len(df_sorted) + 1)
    ax2.plot(df_sorted['datetime'], df_sorted['cumulative_count'], 'b-', linewidth=2)
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Cumulative Number of Aftershocks')
    ax2.set_title('Aftershock Cumulative Count')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Time series plot saved to {output_path}")
    else:
        plt.show()

def create_magnitude_frequency(df, output_path=None):
    """Create Gutenberg-Richter magnitude-frequency distribution."""
    magnitudes = df['magnitude'].values
    min_mag = np.floor(magnitudes.min())
    max_mag = np.ceil(magnitudes.max())
    bins = np.arange(min_mag - 0.5, max_mag + 0.5, 0.2)
    
    hist, bin_edges = np.histogram(magnitudes, bins=bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # Cumulative distribution
    cum_counts = np.cumsum(hist[::-1])[::-1]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Non-cumulative histogram
    ax1.bar(bin_centers, hist, width=0.15, alpha=0.7, color='steelblue')
    ax1.set_xlabel('Magnitude')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Magnitude-Frequency Histogram')
    ax1.grid(True, alpha=0.3)
    
    # Cumulative Gutenberg-Richter plot (log scale)
    ax2.semilogy(bin_centers, cum_counts, 'ro-', linewidth=2, markersize=8)
    ax2.set_xlabel('Magnitude')
    ax2.set_ylabel('Cumulative Frequency (log scale)')
    ax2.set_title('Gutenberg-Richter Cumulative Distribution')
    ax2.grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Magnitude-frequency plot saved to {output_path}")
    else:
        plt.show()

def main():
    parser = argparse.ArgumentParser(description='Visualize aftershock data.')
    parser.add_argument('data_file', help='Path to CSV file with aftershock data')
    parser.add_argument('--output_dir', default='./output',
                        help='Directory to save output plots (default: ./output)')
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Load data
    print(f"Loading data from {args.data_file}")
    df = load_aftershock_data(args.data_file)
    print(f"Loaded {len(df)} aftershocks")
    print(f"Time range: {df['datetime'].min()} to {df['datetime'].max()}")
    print(f"Magnitude range: {df['magnitude'].min()} to {df['magnitude'].max()}")
    
    # Generate plots
    create_map_plot(df, os.path.join(args.output_dir, 'aftershock_map.png'))
    create_depth_profile(df, os.path.join(args.output_dir, 'depth_profile.png'))
    create_time_series(df, os.path.join(args.output_dir, 'time_series.png'))
    create_magnitude_frequency(df, os.path.join(args.output_dir, 'magnitude_frequency.png'))
    
    print(f"\nAll plots saved to {args.output_dir}/")

if __name__ == '__main__':
    main()
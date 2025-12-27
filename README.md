# 1979 UK Earthquake Aftershocks Analysis

A GitHub-based collaborative workflow for analyzing the aftershock sequence of the 1979 earthquake in northern England and southern Scotland.

## Project Overview

This repository provides a systematic framework for documenting, analyzing, and visualizing aftershock data from the 1979 earthquake (also known as the "Bishop Auckland earthquake" or "1979 North England earthquake"). The earthquake occurred on 28 December 1979 with a magnitude of approximately 4.9 ML, causing significant ground shaking across northern England and southern Scotland.

The repository aims to:
- Standardize aftershock data entry (magnitude, location, timing, depth)
- Facilitate collaborative analysis using GitHub tools
- Integrate with existing seismological analysis tools
- Provide visualization scripts for the aftershock sequence
- Enable comparative analysis with other historical UK earthquakes

## Repository Structure

```
├── README.md                   # This file
├── data_templates/             # Standardized templates for data entry
│   ├── aftershock_data_template.csv
│   └── aftershock_data_schema.json
├── scripts/                    # Analysis and visualization scripts
│   ├── visualize_aftershocks.py
│   └── comparative_analysis.py
├── data/                       # Raw and processed aftershock data
├── docs/                       # Documentation and references
├── .github/                    # GitHub workflows and issue templates
└── LICENSE                     # License information
```

## Data Collection

The aftershock sequence following the 1979 earthquake was recorded by the UK seismic network. This repository includes:

1. **Primary Data**: The main shock parameters and aftershock catalog
2. **Template**: CSV template for consistent data entry
3. **Validation**: JSON schema to ensure data quality

## Analysis Methods

- **Seismogram Interpretation**: Analysis of magnetic tape recordings from the 1979 event
- **Magnitude Estimation**: Using both local magnitude (ML) and moment magnitude (Mw)
- **Location Determination**: Hypocentral location using phase picks and velocity models
- **Aftershock Pattern Analysis**: Spatial and temporal clustering analysis

## Collaborative Workflow

This project uses GitHub features to enable collaborative research:

1. **Issues**: Document questions about data interpretation and analysis methods
2. **Pull Requests**: Contribute data, scripts, and documentation
3. **Projects**: Track progress on different analysis components
4. **Actions**: Automated data validation and visualization

## Getting Started

1. Clone this repository: `git clone https://github.com/rognollbens/1979-UK-earthquake-aftershocks-analysis.git`
2. Review the data templates in `data_templates/`
3. Explore existing analysis scripts in `scripts/`
4. Check the open issues for ongoing discussions

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- UK Seismic Network and British Geological Survey for historical data
- Original researchers who documented the 1979 earthquake sequence
- GitHub for providing collaborative tools for scientific research
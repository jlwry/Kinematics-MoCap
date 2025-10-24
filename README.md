# Kinematics-MoCap

An educational tutorial on implementing calculating joint angles using the Grood & Suntay method, with specific focus on its applications to multi-segment foot models.

## Overview

This repository provides a complete walkthrough of multi-segment foot modeling, from loading motion capture data to calculating and visualizing tibia-hindfoot joint angles. 

<img width="540" height="540" alt="g_and_s" src="https://github.com/user-attachments/assets/3f8d17bc-3f18-4a81-847c-083d0bd6a8ee" />

## What's Included

- **Example Data**: Sample C3D files with marker trajectories for foot segments
- **Core Functions**: Modular Python functions for coordinate system construction and joint angle calculations
- **Sample Workflow**: Jupyter notebook with a literature review on multi-segment foot models, and working examples
- **Visualizations**: Tools to plot joint kinematics

## Background

### The Oxford Foot Model (OFM)

The Oxford Foot Model is a widely-used multi-segment foot model that divides the foot into four distinct rigid segments. This allows for more detailed analysis of foot motion compared to single-segment models, which is crucial for understanding pathological gait, foot dysfunction, and surgical outcomes.

**Key segments:**
- Tibia (shank)
- Hindfoot (calcaneus)
- Forefoot
- Hallux

### Grood & Suntay Joint Coordinate System

The Grood & Suntay (1983) method is the gold standard for describing 3D joint rotations in biomechanics. This approach:
- Defines joint angles relative to anatomically meaningful axes (e1, and e3)
- Provides clinically interpretable rotations (flexion/extension, ab/adduction, internal/external rotation)

## Getting Started

### Quick Start

Open the Jupyter notebook to view the example workflow. All functions can be analysed in 'utils.mocapfunctions.py'

## References

Grood, E. S., & Suntay, W. J. (1983). A Joint Coordinate System for the Clinical Description of Three-Dimensional Motions: Application to the Knee. Journal of Biomechanical Engineering, 105(2), 136–144. https://doi.org/10.1115/1.3138397

## Contributing

This is an educational resource. If you find errors, have suggestions for improvements, or want to add additional examples, please open an issue or submit a pull request.



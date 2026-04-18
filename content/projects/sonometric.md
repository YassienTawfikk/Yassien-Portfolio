---
title: SonoMetric
short_description: Medical-grade Pulsed Doppler Ultrasound simulation with a high-fidelity
  physics engine, real-time STFT spectral analysis, and laminar flow modeling.
overview_image_id: https://res.cloudinary.com/dzn4mqtzg/image/upload/v1766534803/SonoMetric_Poster_c5xwx2.png
year: '2025'
domain_id: biomedical_engineering
category_id: biomedical_signal_processing
github_link: https://github.com/YassienTawfikk/SonoMetric.git
video_demo: https://github.com/user-attachments/assets/092e29a9-f01c-4ec0-91c7-03a8c9e121d2
order: 1
tech_stack:
- Python
- PyQt5
- NumPy
- SciPy
- Multithreading
tags:
- Medical Imaging
- Ultrasound
- Doppler Simulation
- Signal Processing
- Physics Engine
- STFT
- Real-Time
highlights:
- Real-time physics engine simulating scatterer movement and RF signal backscattering.
- Laminar flow model implementing parabolic velocity profiles.
- Custom signal processing pipeline (STFT) for dynamic spectrogram visualization.
- Complex-valued I/Q signal generation to distinguish flow direction.
- Medically accurate configuration (5 MHz transducer, 1540 m/s speed of sound).
- Real-time quantitative velocity estimation and error tracking.
---

SonoMetric is a high-fidelity desktop application designed to simulate Pulsed Wave (PW) Doppler ultrasound signal acquisition and processing. It features a custom-built physics engine that models backscattered RF signals from scatterers moving within a laminar flow profile. The system processes these signals using a Short-Time Fourier Transform (STFT) pipeline to generate a dynamic spectrogram, mimicking clinical Spectral Doppler displays. With a focus on physical accuracy, it handles complex I/Q components to distinguish flow direction and provides real-time quantitative velocity metrics, making it a powerful tool for understanding medical imaging physics.

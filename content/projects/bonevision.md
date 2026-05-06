---
category_id: computer_vision_image_processing
domain_id: medical_imaging
github_link: https://github.com/YassienTawfikk/BoneVision-DX-ray.git
video_demo: https://github.com/user-attachments/assets/31cce0be-7b53-4689-9c1b-8fae2ceaed53
highlights:
- Dual-Energy X-Ray material decomposition simulation separating bone and soft tissue.
- Interactive visualization of Low-E and High-E projections using the Beer-Lambert law.
- Digital phantom library (Ribcage, Cylinder, Layers) at 512x512 resolution.
- Real-time quantitative evaluation metrics computing MAE, CNR, and SNR.
- Configurable degradation modeling dynamically injecting noise and scatter.
order: 3
overview_image_id: K837RwQv/Bone-Vision-Design.png
short_description: Advanced Python desktop application simulating dual-energy X-ray acquisition and performing mathematical material decomposition to visualize separate bone and soft-tissue maps.
tags:
- Medical Imaging
- PyQt5
- Dual-Energy X-Ray
- Signal Processing
- Material Decomposition
- Simulation
- Scientific Computing
- MVC Architecture
tech_stack:
- Python
- PyQt5
- NumPy
- SciPy
- Matplotlib
title: BoneVision DX-Ray
year: '2026'
---

BoneVision DX-Ray is an advanced Python desktop application that simulates dual-energy X-ray acquisition and performs mathematical material decomposition. In standard single-energy radiography, bone and soft tissue overlapping reduces diagnostic contrast. This underdetermined system is solved by acquiring two images at varying energy levels and leveraging the Beer-Lambert law. The application provides a robust matrix-inversion method to isolate tissue and bone thickness maps and visualizes them instantly. With a strict MVC architecture guaranteeing sub-50ms latency, it includes a comprehensive digital phantom library, real-time noise and scatter degradation modeling, interactive attenuation charts, and live quantitative evaluation metrics (MAE, CNR, SNR).

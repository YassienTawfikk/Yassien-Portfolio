---
title: FaceVector
short_description: Modular computer vision system for face detection and recognition
  using PCA-based embeddings.
overview_image_id: tX0whS5w/Face-Vector-overview.png
year: '2025'
domain_id: ai_data_science
category_id: computer_vision_image_processing
github_link: https://github.com/YassienTawfikk/FaceVector
tech_stack:
- Python
- OpenCV
- PyQt5
- NumPy
- scikit-learn
- Matplotlib
tags:
- Face Detection
- Face Recognition
- Computer Vision
- PCA
- Eigenfaces
- Machine Learning
highlights:
- Real-time face detection using Haar cascades.
- PCA-based face recognition with dynamic training and embedding projection.
- Supports both RGB and grayscale datasets with train/test splitting.
- Performance evaluation with ROC curves and classification metrics.
- Intuitive GUI for selecting images, viewing results, and adjusting detection parameters.
---

FaceVector combines classical face detection using Haar cascades with PCA-based recognition to classify identities efficiently. It flattens face images, computes eigenfaces, projects new images into eigenspace, and predicts identities using Euclidean distance. The system is optimized for small training datasets, supports RGB and grayscale images, and includes automatic caching and evaluation. Designed for fast, reproducible facial analysis with clear visualization of detection and recognition results.

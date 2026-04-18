---
title: MusicSpectroNet
short_description: Music genre classification on the GTZAN dataset using tabular ML
  and CNN-based spectrogram analysis.
overview_image_id: RMc8G7pd/Music-Spectro-Net-overview.png
year: '2024'
domain_id: signal_processing
category_id: ai_data_science
github_link: https://github.com/YassienTawfikk/MusicSpectroNet.git
tech_stack:
- Python
- Pandas
- NumPy
- scikit-learn
- XGBoost
- Librosa
- PyTorch
- Matplotlib
- Seaborn
tags:
- Audio Classification
- Music Genre
- Tabular ML
- CNN
- GTZAN
highlights:
- Tabular ML (XGBoost) achieved 92.64% test accuracy using extracted audio features.
- CNN on spectrogram images was explored but achieved 23.33% accuracy.
- Feature importance analysis highlights perceptual, spectral, and tonal characteristics
  as key indicators.
- Pipeline supports 3-second segment feature extraction and preprocessing.
- Comparison study between tabular and image-based approaches demonstrates performance
  trade-offs.
---

MusicSpectroNet investigates audio genre classification using two approaches: tabular ML on extracted audio features and CNNs on spectrogram images from the GTZAN dataset. The tabular ML approach (XGBoost) achieves 92.64% accuracy, significantly outperforming the CNN model. The project includes extensive preprocessing, feature extraction, and visualization of confusion matrices and feature importance, demonstrating real-world effectiveness of tabular audio features for music genre recognition.

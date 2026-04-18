---
title: MovieMatch100K
short_description: A modular movie recommendation system using the MovieLens 100K
  dataset with collaborative filtering and SVD.
overview_image_id: tXhfD3vJ/Movie-Match100K-overview.png
year: '2024'
domain_id: ai_data_science
category_id: ai_data_science
github_link: https://github.com/YassienTawfikk/MovieMatch100K.git
tech_stack:
- Python
- Pandas
- NumPy
- scikit-learn
- Surprise
- PyTorch
tags:
- Machine Learning
- Recommendation Systems
- Collaborative Filtering
- Matrix Factorization
- SVD
highlights:
- Supports User-Based, Item-Based, and SVD Matrix Factorization models.
- Top-k movie recommendations generated with evaluation metrics.
- Precision@k and Recall@k used for practical performance evaluation.
- SVD model achieves 41.78% Precision@5 and 14.75% Recall@5.
- Modular design for easily switching between recommendation methods.
---

MovieMatch100K is a modular recommendation system built on the MovieLens 100K dataset. It implements User-Based and Item-Based collaborative filtering as well as SVD matrix factorization. Each method predicts top-k movie recommendations, evaluated with Precision@k and Recall@k metrics. The system provides a clean modular design for testing multiple collaborative filtering strategies and comparing their performance. The SVD-based model achieves the best results, effectively learning latent features for improved recommendation quality.

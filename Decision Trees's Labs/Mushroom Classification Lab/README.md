# First Lab in Decision Trees Section: Mushroom Classification - Edible or Non-Edible 🌱🍄

## Overview
This is the first lab in the **Decision Trees** section, where we classify a set of mushrooms into two categories: **edible** and **non-edible**. The classification is performed using a **Decision Tree algorithm**, trained on a dataset with various mushroom features. These features include attributes such as cap shape, cap color, gill size, and more, which help predict whether a mushroom is safe to eat or not.

The project emphasizes:
- Data preprocessing and feature encoding using `LabelEncoder`.
- Hyperparameter tuning using `RandomizedSearchCV` to improve model performance.
- Training and evaluation of the Decision Tree Classifier.
- Performance analysis based on test data accuracy.

## Features ✨
- **Data Preprocessing**: 
  - Encodes categorical features into numeric values using `LabelEncoder`.
  - Splits the dataset into training and testing sets, ensuring proper stratification.

- **Model Tuning**: 
  - Applies `RandomizedSearchCV` for hyperparameter tuning of the Decision Tree Classifier.
  - Tests various parameters like `max_depth`, `min_samples_leaf`, and `min_samples_split` to identify the optimal configuration.

- **Model Training and Prediction**:
  - The classifier is trained on the encoded training data.
  - Predictions are made for both training and test datasets.

- **Model Evaluation**: 
  - Baseline accuracy is calculated based on the majority class.
  - The model's performance is evaluated on the test data, with accuracy metrics used for assessment.

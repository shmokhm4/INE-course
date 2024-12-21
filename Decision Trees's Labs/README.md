# First lab in the Decision Trees section: Mushroom Classification: Edible or Non-Edible 🌱🍄
This project is the first lab in the **Decision Trees** section, where we classify a set of mushrooms into two categories: **edible** and **non-edible**. The classification is performed using a **Decision Tree algorithm**, which is trained on a dataset containing various features of mushrooms, such as cap shape, cap color, gill size, and more. The goal is to predict whether a mushroom is safe to eat or not.

The project focuses on:
- Data preprocessing and feature encoding using `LabelEncoder`.
- Hyperparameter tuning using `RandomizedSearchCV`.
- Model training and evaluation using a Decision Tree Classifier.
- Performance assessment on test data to ensure the model's accuracy.

## Features ✨
- **Data Preprocessing**: 
  - Encodes categorical features into numeric values using `LabelEncoder`.
  - Splits the data into training and testing sets while maintaining class distribution.
  
- **Model Tuning**: 
  - Uses `RandomizedSearchCV` for hyperparameter tuning of the Decision Tree Classifier.
  - Tests various parameters like `max_depth`, `min_samples_leaf`, and `min_samples_split` to find the best combination.

- **Model Training and Prediction**:
  - Trains the model on the encoded training data.
  - Makes predictions on both training and test datasets.

- **Model Evaluation**: 
  - Calculates baseline accuracy based on the majority class.
  - Evaluates the model's performance using test data.

# 5th Lab in the Course: Adding Calculated Values to Query Results 💫
In this project, we enhance MySQL to perform operations not available by default in queries. We focus on calculating average sentiment confidence and negative confidence scores for various airlines, as well as creating a view for more complex aggregations.
## Features ✨
- Connect to a MySQL database using Python.
- Execute SQL queries to calculate average sentiment and confidence scores for different airlines.
- Create a view named `airline_sentiment` to store:
  - Average sentiment confidence
  - Geometric mean of sentiment confidence
  - Midrange of sentiment confidence
- Dynamically retrieve and calculate mid sentiment confidence for each airline.

## Sample Output 🪄
```bash
{
    'Delta': 0.6889,
    'United': 1.0,
    'Southwest': 0.6772,
    'US Airways': 1.0,
    'Virgin America': 1.0,
    'American': 0.6356
}
```

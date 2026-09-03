import os
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def train_regression_model(file_path: str):
    """
    Train a Linear Regression model using the first numerical column
    as the feature and the second numerical column as the target.
    """

    df = pd.read_csv(file_path)

    numerical_columns = df.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    if len(numerical_columns) < 2:
        raise ValueError(
            "Dataset must contain at least two numerical columns."
        )

    feature_column = numerical_columns[0]
    target_column = numerical_columns[1]

    df = df.dropna(subset=[feature_column, target_column])

    X = df[[feature_column]]
    y = df[target_column]

    if len(df) < 5:
        raise ValueError(
            "Dataset must contain at least 5 rows for modeling."
        )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = LinearRegression()

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    mse = mean_squared_error(y_test, predictions)
    rmse = mse ** 0.5

    r2 = r2_score(y_test, predictions)

    result = {
        "status": "success",
        "rows": int(len(df)),
        "feature": feature_column,
        "target": target_column,
        "training_rows": int(len(X_train)),
        "testing_rows": int(len(X_test)),
        "mae": float(mae),
        "rmse": float(rmse),
        "r2_score": float(r2),
        "coefficient": float(model.coef_[0]),
        "intercept": float(model.intercept_)
    }

    return result
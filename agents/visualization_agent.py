import os
import pandas as pd
import plotly.express as px


# =========================================================
# VISUALIZATION AGENT
# =========================================================

def run_visualization_agent(file_path: str, modeling_result=None):

    print("\n" + "=" * 60)
    print("[VISUALIZATION AGENT] Creating visualizations...")
    print("=" * 60)

    try:

        # -------------------------------------------------
        # 1. Check file
        # -------------------------------------------------

        if not file_path:
            return {
                "status": "error",
                "message": "File path is missing"
            }

        if not os.path.exists(file_path):
            return {
                "status": "error",
                "message": f"File not found: {file_path}"
            }

        # -------------------------------------------------
        # 2. Read dataset
        # -------------------------------------------------

        df = pd.read_csv(file_path)

        if df.empty:
            return {
                "status": "error",
                "message": "Dataset is empty"
            }

        print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

        # -------------------------------------------------
        # 3. Create visualization folder
        # -------------------------------------------------

        base_dir = os.path.dirname(file_path)

        visualization_dir = os.path.join(
            base_dir,
            "visualizations"
        )

        os.makedirs(
            visualization_dir,
            exist_ok=True
        )

        # -------------------------------------------------
        # 4. Identify columns
        # -------------------------------------------------

        numerical_columns = df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        categorical_columns = df.select_dtypes(
            exclude=["number"]
        ).columns.tolist()

        print("Numerical columns:", numerical_columns)
        print("Categorical columns:", categorical_columns)

        charts = []

        # =================================================
        # CHART 1 - HISTOGRAMS
        # =================================================

        for column in numerical_columns:

            print(f"Creating histogram for {column}")

            fig = px.histogram(
                df,
                x=column,
                title=f"Distribution of {column}"
            )

            output_file = os.path.join(
                visualization_dir,
                f"{column}_histogram.html"
            )

            fig.write_html(output_file)

            charts.append({
                "type": "histogram",
                "column": column,
                "file": output_file
            })

        # =================================================
        # CHART 2 - BOX PLOTS
        # =================================================

        for column in numerical_columns:

            print(f"Creating box plot for {column}")

            fig = px.box(
                df,
                y=column,
                title=f"Box Plot of {column}"
            )

            output_file = os.path.join(
                visualization_dir,
                f"{column}_boxplot.html"
            )

            fig.write_html(output_file)

            charts.append({
                "type": "boxplot",
                "column": column,
                "file": output_file
            })

        # =================================================
        # CHART 3 - SCATTER PLOT
        # =================================================

        # If there are at least two numerical columns,
        # use the first two.

        if len(numerical_columns) >= 2:

            x_column = numerical_columns[0]
            y_column = numerical_columns[1]

            print(
                f"Creating scatter plot: "
                f"{x_column} vs {y_column}"
            )

            # IMPORTANT:
            # No trendline is used.
            # This prevents the statsmodels error.

            fig = px.scatter(
                df,
                x=x_column,
                y=y_column,
                title=f"{x_column} vs {y_column}"
            )

            output_file = os.path.join(
                visualization_dir,
                "scatter_plot.html"
            )

            fig.write_html(output_file)

            charts.append({
                "type": "scatter",
                "x": x_column,
                "y": y_column,
                "file": output_file
            })

        # =================================================
        # CHART 4 - CORRELATION HEATMAP
        # =================================================

        if len(numerical_columns) >= 2:

            print("Creating correlation heatmap")

            correlation = df[
                numerical_columns
            ].corr()

            fig = px.imshow(
                correlation,
                text_auto=True,
                title="Correlation Heatmap"
            )

            output_file = os.path.join(
                visualization_dir,
                "correlation_heatmap.html"
            )

            fig.write_html(output_file)

            charts.append({
                "type": "heatmap",
                "file": output_file
            })

        # =================================================
        # CHART 5 - CATEGORICAL BAR CHARTS
        # =================================================

        for column in categorical_columns:

            # Avoid creating extremely large charts
            # for columns with many unique values.

            unique_count = df[column].nunique()

            if unique_count <= 20:

                print(
                    f"Creating bar chart for {column}"
                )

                value_counts = (
                    df[column]
                    .value_counts()
                    .reset_index()
                )

                value_counts.columns = [
                    column,
                    "Count"
                ]

                fig = px.bar(
                    value_counts,
                    x=column,
                    y="Count",
                    title=f"Distribution of {column}"
                )

                output_file = os.path.join(
                    visualization_dir,
                    f"{column}_bar_chart.html"
                )

                fig.write_html(output_file)

                charts.append({
                    "type": "bar",
                    "column": column,
                    "file": output_file
                })

        # =================================================
        # MODELING INFORMATION
        # =================================================

        model_info = {}

        if modeling_result:

            model_info = {
                "algorithm": modeling_result.get(
                    "algorithm"
                ),
                "feature": modeling_result.get(
                    "feature"
                ),
                "target": modeling_result.get(
                    "target"
                ),
                "r2_score": modeling_result.get(
                    "r2_score"
                ),
                "mae": modeling_result.get(
                    "mae"
                ),
                "rmse": modeling_result.get(
                    "rmse"
                )
            }

        # =================================================
        # FINAL RESULT
        # =================================================

        result = {

            "status": "success",

            "agent": "Visualization Agent",

            "rows": len(df),

            "columns": len(df.columns),

            "numerical_columns": numerical_columns,

            "categorical_columns": categorical_columns,

            "charts_created": len(charts),

            "visualization_directory": visualization_dir,

            "charts": charts,

            "modeling": model_info
        }

        print("\nVisualization completed successfully.")

        print(
            f"Charts created: {len(charts)}"
        )

        print(
            f"Saved in: {visualization_dir}"
        )

        return result

    except Exception as e:

        print(
            f"\nVisualization Agent Error: {str(e)}"
        )

        return {
            "status": "error",
            "agent": "Visualization Agent",
            "message": str(e)
        }
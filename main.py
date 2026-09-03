import shutil
from pathlib import Path
from groq import Groq
import os
from reportlab.lib.pagesizes import A4

from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
import pandas as pd
import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import plotly.express as px

# ============================================================
# AUTODS - AUTONOMOUS DATA SCIENTIST
# ============================================================
app = FastAPI(
    title="AutoDS",
    version="1.0.0",
    description="Autonomous Data Scientist Multi-Agent System"
)
# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DIRECTORIES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"
VISUALIZATION_DIR = BASE_DIR / "visualizations"

REPORT_DIR.mkdir(exist_ok=True)
VISUALIZATION_DIR.mkdir(exist_ok=True)


# ============================================================
# SERVE FILES
# ============================================================

app.mount(
    "/visualizations",
    StaticFiles(directory=str(VISUALIZATION_DIR)),
    name="visualizations"
)

app.mount(
    "/reports",
    StaticFiles(directory=str(REPORT_DIR)),
    name="reports"
)


# ============================================================
# GLOBAL WORKFLOW STATE
# ============================================================

workflow_state = {
    "input_file": None,
    "profiling_result": None,
    "cleaning_result": None,
    "eda_result": None,
    "modeling_result": None,
    "visualization_result": None,
    "insights_result": None,
    "final_report": None
}


def build_agent_payload(stage, result=None, summary=None, metrics=None, warnings=None, recommendations=None):
    payload = {
        "stage": stage,
        "status": "completed",
        "summary": summary or "The agent completed successfully.",
        "result": result or {},
        "metrics": metrics or {},
        "warnings": warnings or [],
        "recommendations": recommendations or []
    }

    if isinstance(result, dict):
        payload.update(result)

    return payload


def build_profiling_summary(result):
    if not isinstance(result, dict):
        return "The Profiling Agent analyzed the dataset structure and quality."

    rows = int(result.get("rows") or 0)
    columns = int(result.get("columns") or 0)
    duplicate_rows = int(result.get("duplicate_rows") or 0)
    missing_values = 0
    missing_map = result.get("missing_values") or {}
    if isinstance(missing_map, dict):
        missing_values = sum(int(v) for v in missing_map.values())
    numerical_columns = result.get("numerical_columns") or []

    if rows == 0 and columns == 0:
        return "The Profiling Agent analyzed the dataset structure and quality."

    summary = (
        f"The Profiling Agent analyzed the dataset structure and quality. "
        f"The dataset contains {rows} rows and {columns} columns, "
        f"including {len(numerical_columns)} numerical column(s). "
    )

    if missing_values == 0:
        summary += "No missing values were detected. "
    else:
        summary += f"{missing_values} missing value(s) were detected. "

    if duplicate_rows == 0:
        summary += "No duplicate rows were found."
    elif duplicate_rows == 1:
        summary += "1 duplicate record was identified."
    else:
        summary += f"{duplicate_rows} duplicate records were identified."

    return summary


def format_statistics(statistics):
    if not isinstance(statistics, dict) or not statistics:
        return "No descriptive statistics were generated."

    lines = []
    for column, values in statistics.items():
        lines.append(
            f"{column}: mean={values.get('mean', 'N/A')}, "
            f"median={values.get('median', 'N/A')}, "
            f"minimum={values.get('minimum', 'N/A')}, "
            f"maximum={values.get('maximum', 'N/A')}, "
            f"standard deviation={values.get('standard_deviation', 'N/A')}"
        )
    return "\n".join(lines)


def format_correlation(correlation):
    if not isinstance(correlation, dict) or not correlation:
        return "No correlation matrix was generated."

    return "\n".join(
        f"{row}: " + ", ".join(
            f"{column}={value}"
            for column, value in values.items()
        )
        for row, values in correlation.items()
    )


def get_current_file():
    cleaned_file = workflow_state.get("cleaned_file")

    if cleaned_file and Path(cleaned_file).exists():
        return Path(cleaned_file)

    input_file = workflow_state.get("input_file")

    if input_file and Path(input_file).exists():
        return Path(input_file)

    raise HTTPException(
        status_code=400,
        detail="No dataset found. Please upload a CSV file first."
    )


def load_csv():
    file_path = get_current_file()

    try:
        return pd.read_csv(file_path)

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=f"Unable to read CSV file: {str(e)}"
        )


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "status": "success",
        "project": "AutoDS",
        "version": "1.0.0",
        "message": "Autonomous Data Scientist Multi-Agent System"
    }


# ============================================================
# PHASE 1 - PROFILING
# ============================================================

@app.post("/api/phase1/analyze")
async def analyze_dataset(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".csv"):

        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported."
        )

    original_file = DATA_DIR / file.filename

    with open(original_file, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    workflow_state["input_file"] = str(original_file)

    df = pd.read_csv(original_file)

    numerical_columns = (
        df.select_dtypes(include=np.number)
        .columns
        .tolist()
    )

    categorical_columns = (
        df.select_dtypes(exclude=np.number)
        .columns
        .tolist()
    )

    result = {

        "rows": len(df),

        "columns": len(df.columns),

        "column_names": df.columns.tolist(),

        "data_types": {
            column: str(dtype)
            for column, dtype in df.dtypes.items()
        },

        "missing_values": {
            column: int(value)
            for column, value in df.isnull().sum().items()
        },

        "duplicate_rows": int(
            df.duplicated().sum()
        ),

        "numerical_columns":
            numerical_columns,

        "categorical_columns":
            categorical_columns
    }

    workflow_state["profiling_result"] = result

    summary = build_profiling_summary(result)
    payload = build_agent_payload(
        "profiling",
        result=result,
        summary=summary,
        metrics={
            "rows": len(df),
            "columns": len(df.columns),
            "duplicate_rows": int(df.duplicated().sum()),
            "missing_values": int(df.isnull().sum().sum())
        },
        warnings=[] if int(df.duplicated().sum()) == 0 else ["Duplicate rows were detected and may affect downstream analysis."],
        recommendations=["Review duplicate records before modeling."] if int(df.duplicated().sum()) > 0 else ["Proceed to cleaning and EDA to validate data quality."]
    )

    return {
        "status": "success",
        "phase": "Phase 1 - Profiling Agent",
        "workflow_status": "completed",
        **payload
    }


# ============================================================
# PHASE 2 - CLEANING
# ============================================================

@app.post("/api/phase2/clean")
async def clean_dataset(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".csv"):

        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported."
        )

    original_file = DATA_DIR / file.filename

    with open(original_file, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    df = pd.read_csv(original_file)

    original_rows = len(df)

    duplicates_removed = int(
        df.duplicated().sum()
    )

    missing_before = int(
        df.isnull().sum().sum()
    )

    # Remove duplicates
    df = df.drop_duplicates()

    # Fill missing values
    for column in df.columns:

        if pd.api.types.is_numeric_dtype(
            df[column]
        ):

            median = df[column].median()

            df[column] = df[column].fillna(
                median
            )

        else:

            mode = df[column].mode()

            if len(mode) > 0:

                df[column] = df[column].fillna(
                    mode[0]
                )

    missing_after = int(
        df.isnull().sum().sum()
    )

    cleaned_file = (
        DATA_DIR /
        f"{original_file.stem}_cleaned.csv"
    )

    df.to_csv(
        cleaned_file,
        index=False
    )

    workflow_state["input_file"] = str(
        original_file
    )

    workflow_state["cleaned_file"] = str(
        cleaned_file
    )

    result = {

        "original_rows":
            original_rows,

        "cleaned_rows":
            len(df),

        "duplicates_removed":
            duplicates_removed,

        "missing_values_before":
            missing_before,

        "missing_values_after":
            missing_after
    }

    workflow_state["cleaning_result"] = result

    return {

        "status": "success",

        "phase":
            "Phase 2 - Cleaning Agent",

        "workflow_status":
            "completed",

        "result":
            result
    }


# ============================================================
# PHASE 3 - EDA
# ============================================================

@app.post("/api/phase3/eda")
def eda_dataset():

    df = load_csv()

    numerical_columns = (
        df.select_dtypes(include=np.number)
        .columns
        .tolist()
    )

    categorical_columns = (
        df.select_dtypes(exclude=np.number)
        .columns
        .tolist()
    )

    statistics = {}

    for column in numerical_columns:

        statistics[column] = {

            "mean":
                float(df[column].mean()),

            "median":
                float(df[column].median()),

            "minimum":
                float(df[column].min()),

            "maximum":
                float(df[column].max()),

            "standard_deviation":
                float(df[column].std())
        }

    correlation = {}

    if len(numerical_columns) >= 2:

        correlation = (
            df[numerical_columns]
            .corr()
            .round(4)
            .to_dict()
        )

    result = {

        "rows":
            len(df),

        "columns":
            len(df.columns),

        "column_names":
            df.columns.tolist(),

        "numerical_columns":
            numerical_columns,

        "categorical_columns":
            categorical_columns,

        "missing_values": {
            column: int(value)
            for column, value
            in df.isnull().sum().items()
        },

        "unique_values": {
            column: int(df[column].nunique())
            for column in df.columns
        },

        "statistics":
            statistics,

        "correlation":
            correlation
    }

    workflow_state["eda_result"] = result

    return {

        "status": "success",

        "phase":
            "Phase 3 - EDA Agent",

        "workflow_status":
            "completed",

        "result":
            result
    }


# ============================================================
# PHASE 4 - MODELING
# ============================================================

@app.post("/api/phase4/model")
def modeling_dataset():

    df = load_csv()

    numerical_columns = (
        df.select_dtypes(include=np.number)
        .columns
        .tolist()
    )

    if len(numerical_columns) < 2:

        raise HTTPException(
            status_code=400,
            detail=(
                "Modeling requires at least "
                "two numerical columns."
            )
        )

    feature = numerical_columns[0]

    target = numerical_columns[1]

    X = df[[feature]]

    y = df[target]

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42
        )
    )

    model = LinearRegression()

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions
        )
    )

    r2 = r2_score(
        y_test,
        predictions
    )

    result = {

        "algorithm":
            "Linear Regression",

        "feature":
            feature,

        "target":
            target,

        "training_rows":
            len(X_train),

        "testing_rows":
            len(X_test),

        "mae":
            float(mae),

        "rmse":
            float(rmse),

        "r2_score":
            float(r2),

        "coefficient":
            float(model.coef_[0]),

        "intercept":
            float(model.intercept_)
    }

    workflow_state["modeling_result"] = result

    return {

        "status": "success",

        "phase":
            "Phase 4 - Modeling Agent",

        "workflow_status":
            "completed",

        "result":
            result
    }


# ============================================================
# PHASE 5 - VISUALIZATION
# ============================================================

@app.post("/api/phase5/visualize")
def visualization_dataset():

    df = load_csv()

    numerical_columns = (
        df.select_dtypes(include=np.number)
        .columns
        .tolist()
    )

    categorical_columns = (
        df.select_dtypes(exclude=np.number)
        .columns
        .tolist()
    )

    generated_plots = []

    # --------------------------------------------------------
    # HISTOGRAMS
    # --------------------------------------------------------

    for column in numerical_columns:

        fig = px.histogram(
            df,
            x=column,
            title=f"Distribution of {column}",
            marginal="box",
            nbins=30
        )

        fig.update_layout(
            template="plotly_white"
        )

        filename = (
            f"{column.lower()}_histogram.html"
        )

        filepath = (
            VISUALIZATION_DIR /
            filename
        )

        fig.write_html(
            str(filepath)
        )

        generated_plots.append({
            "type": "histogram",
            "name": filename,
            "url": f"/visualizations/{filename}"
        })

    # --------------------------------------------------------
    # SCATTER
    # --------------------------------------------------------

    if len(numerical_columns) >= 2:

        x_column = numerical_columns[0]

        y_column = numerical_columns[1]

        fig = px.scatter(
            df,
            x=x_column,
            y=y_column,
            title=f"{y_column} vs {x_column}"
        )

        fig.update_layout(
            template="plotly_white"
        )

        filename = (
            f"{x_column.lower()}_vs_"
            f"{y_column.lower()}.html"
        )

        filepath = (
            VISUALIZATION_DIR /
            filename
        )

        fig.write_html(
            str(filepath)
        )

        generated_plots.append({
            "type": "scatter",
            "name": filename,
            "url": f"/visualizations/{filename}"
        })

    # --------------------------------------------------------
    # HEATMAP
    # --------------------------------------------------------

    if len(numerical_columns) >= 2:

        correlation = (
            df[numerical_columns]
            .corr()
        )

        fig = px.imshow(
            correlation,
            text_auto=True,
            title="Correlation Heatmap",
            aspect="auto"
        )

        fig.update_layout(
            template="plotly_white"
        )

        filename = "correlation_heatmap.html"

        filepath = (
            VISUALIZATION_DIR /
            filename
        )

        fig.write_html(
            str(filepath)
        )

        generated_plots.append({
            "type": "heatmap",
            "name": filename,
            "url": f"/visualizations/{filename}"
        })

    # --------------------------------------------------------
    # BOXPLOTS
    # --------------------------------------------------------

    for column in numerical_columns:

        fig = px.box(
            df,
            y=column,
            title=f"Box Plot - {column}"
        )

        fig.update_layout(
            template="plotly_white"
        )

        filename = (
            f"{column.lower()}_boxplot.html"
        )

        filepath = (
            VISUALIZATION_DIR /
            filename
        )

        fig.write_html(
            str(filepath)
        )

        generated_plots.append({
            "type": "boxplot",
            "name": filename,
            "url": f"/visualizations/{filename}"
        })

    # --------------------------------------------------------
    # CATEGORICAL BAR CHARTS
    # --------------------------------------------------------

    for column in categorical_columns:

        if df[column].nunique() <= 30:

            counts = (
                df[column]
                .value_counts()
                .reset_index()
            )

            counts.columns = [
                column,
                "Count"
            ]

            fig = px.bar(
                counts,
                x=column,
                y="Count",
                title=f"Distribution of {column}"
            )

            fig.update_layout(
                template="plotly_white"
            )

            filename = (
                f"{column.lower()}_bar_chart.html"
            )

            filepath = (
                VISUALIZATION_DIR /
                filename
            )

            fig.write_html(
                str(filepath)
            )

            generated_plots.append({
                "type": "bar_chart",
                "name": filename,
                "url": f"/visualizations/{filename}"
            })

    result = {

        "library":
            "Plotly",

        "plots_generated":
            len(generated_plots),

        "generated_plots":
            generated_plots
    }

    workflow_state[
        "visualization_result"
    ] = result

    return {

        "status": "success",

        "phase":
            "Phase 5 - Visualization Agent",

        "workflow_status":
            "completed",

        "result":
            result
    }


# ============================================================
# PHASE 6 - AI INSIGHTS
# ============================================================

@app.post("/api/phase6/insights")
def insights_dataset():

    df = load_csv()

    numerical_columns = (
        df.select_dtypes(include=np.number)
        .columns
        .tolist()
    )

    observations = []

    missing_values = int(
        df.isnull().sum().sum()
    )

    duplicate_rows = int(
        df.duplicated().sum()
    )

    # Missing values
    if missing_values == 0:

        observations.append(
            "The dataset contains no missing values."
        )

    else:

        observations.append(
            f"The dataset contains "
            f"{missing_values} missing values."
        )

    # Duplicates
    if duplicate_rows == 0:

        observations.append(
            "No duplicate rows were found."
        )

    else:

        observations.append(
            f"The dataset contains "
            f"{duplicate_rows} duplicate rows."
        )

    correlation_value = None

    # Correlation
    if len(numerical_columns) >= 2:

        correlation_value = float(
            df[numerical_columns]
            .corr()
            .iloc[0, 1]
        )

        first = numerical_columns[0]

        second = numerical_columns[1]

        observations.append(
            f"Correlation between "
            f"{first} and {second} "
            f"is {correlation_value:.4f}."
        )

        if correlation_value > 0.7:

            observations.append(
                "The first two numerical variables "
                "have a strong positive relationship."
            )

        elif correlation_value < -0.7:

            observations.append(
                "The first two numerical variables "
                "have a strong negative relationship."
            )

        else:

            observations.append(
                "The first two numerical variables "
                "have a relatively weak relationship."
            )

    # Model insight
    if (
        workflow_state["modeling_result"]
        is not None
    ):

        observations.append(
            "A Linear Regression model was trained "
            "using the first numerical column "
            "to predict the second."
        )

    observations.append(
        "Plotly visualizations were generated "
        "for distributions, relationships, "
        "correlations and outliers."
    )

    result = {

        "observations":
            observations,

        "missing_values":
            missing_values,

        "duplicate_rows":
            duplicate_rows,

        "correlation":
            correlation_value
    }

    workflow_state[
        "insights_result"
    ] = result

    return {

        "status": "success",

        "phase":
            "Phase 6 - AI Insights Agent",

        "workflow_status":
            "completed",

        "result":
            result
    }


# ============================================================
# PHASE 7 - FINAL REPORT
# ============================================================

@app.post("/api/phase7/report")
def final_report():

    df = load_csv()

    cleaning = workflow_state.get(
        "cleaning_result"
    )

    eda = workflow_state.get(
        "eda_result"
    )

    modeling = workflow_state.get(
        "modeling_result"
    )

    visualization = workflow_state.get(
        "visualization_result"
    )

    insights = workflow_state.get(
        "insights_result"
    )

    report = f"""
============================================================
AUTODS - FINAL DATA SCIENCE REPORT
============================================================

1. DATASET OVERVIEW
-------------------

Rows        : {len(df)}
Columns     : {len(df.columns)}

Column Names:
{df.columns.tolist()}


2. DATA QUALITY
---------------

Missing Values : {int(df.isnull().sum().sum())}
Duplicate Rows : {int(df.duplicated().sum())}


3. CLEANING
-----------

Original Rows      : {
    cleaning.get("original_rows")
    if cleaning else "N/A"
}

Cleaned Rows       : {
    cleaning.get("cleaned_rows")
    if cleaning else "N/A"
}

Duplicates Removed : {
    cleaning.get("duplicates_removed")
    if cleaning else "N/A"
}


4. EXPLORATORY DATA ANALYSIS
----------------------------

Numerical Columns:
{
    eda.get("numerical_columns")
    if eda else "N/A"
}

Categorical Columns:
{
    eda.get("categorical_columns")
    if eda else "N/A"
}

Statistics:
{
    eda.get("statistics")
    if eda else "N/A"
}

Correlation:
{
    eda.get("correlation")
    if eda else "N/A"
}


5. MODELING
-----------

Algorithm:
{
    modeling.get("algorithm")
    if modeling else "N/A"
}

Feature:
{
    modeling.get("feature")
    if modeling else "N/A"
}

Target:
{
    modeling.get("target")
    if modeling else "N/A"
}

Training Rows:
{
    modeling.get("training_rows")
    if modeling else "N/A"
}

Testing Rows:
{
    modeling.get("testing_rows")
    if modeling else "N/A"
}

MAE:
{
    modeling.get("mae")
    if modeling else "N/A"
}

RMSE:
{
    modeling.get("rmse")
    if modeling else "N/A"
}

R2 Score:
{
    modeling.get("r2_score")
    if modeling else "N/A"
}


6. VISUALIZATION
----------------

Library:
Plotly

Plots Generated:
{
    visualization.get("plots_generated")
    if visualization else 0
}


7. AI INSIGHTS
--------------

{
    insights.get("observations")
    if insights else "N/A"
}


8. RECOMMENDATIONS
------------------

- Validate the model using unseen data.
- Perform cross-validation.
- Compare multiple machine learning algorithms.
- Add useful features.
- Monitor model performance.
- Use generated visualizations for analysis.


9. FINAL CONCLUSION
-------------------

The AutoDS system successfully processed the dataset
through profiling, cleaning, EDA, modeling,
visualization and AI insight generation.

The generated visualizations provide graphical support
for understanding distributions, relationships,
correlations and possible outliers.

============================================================
END OF AUTODS FINAL DATA SCIENCE REPORT
============================================================
"""

    report_file = (
        REPORT_DIR /
        "autods_final_report.txt"
    )

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(report)

    workflow_state[
        "final_report"
    ] = report

    return {

        "status": "success",

        "phase":
            "Phase 7 - Final Report Agent",

        "workflow_status":
            "completed",

        "report_file":
            "/reports/autods_final_report.txt",

        "report":
            report
    }

def create_report_pdf():
    txt_file = REPORT_DIR / "autods_final_report.txt"
    pdf_file = REPORT_DIR / "AUTODS_Final_Report.pdf"

    if not txt_file.exists():
        raise HTTPException(
            status_code=404,
            detail="Report has not been generated yet."
        )

    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase.pdfmetrics import stringWidth
    from reportlab.lib.units import mm

    # ---------------------------------------------------------
    # COLORS
    # ---------------------------------------------------------
    NAVY = colors.HexColor("#172554")
    BLUE = colors.HexColor("#2563EB")
    PURPLE = colors.HexColor("#7C3AED")
    CYAN = colors.HexColor("#0891B2")
    GREEN = colors.HexColor("#059669")
    DARK = colors.HexColor("#172033")
    GREY = colors.HexColor("#64748B")
    WHITE = colors.white
    LIGHT = colors.HexColor("#F8FAFC")

    PAGE_WIDTH, PAGE_HEIGHT = A4

    # ---------------------------------------------------------
    # READ REPORT
    # ---------------------------------------------------------
    with open(txt_file, "r", encoding="utf-8") as file:
        lines = file.read().splitlines()

    # ---------------------------------------------------------
    # CREATE PDF
    # ---------------------------------------------------------
    pdf = canvas.Canvas(
        str(pdf_file),
        pagesize=A4
    )

    pdf.setTitle("AUTODS Final Report")
    pdf.setAuthor("AUTODS")

    left = 18 * mm
    right = PAGE_WIDTH - (18 * mm)
    top = PAGE_HEIGHT - 22 * mm
    bottom = 20 * mm

    usable_width = right - left

    y = top

    # ---------------------------------------------------------
    # HELPERS
    # ---------------------------------------------------------
    def draw_header():
        pdf.setFillColor(NAVY)
        pdf.rect(
            0,
            PAGE_HEIGHT - 6,
            PAGE_WIDTH,
            6,
            fill=1,
            stroke=0
        )

    def draw_footer():
        pdf.setFillColor(PURPLE)
        pdf.rect(
            0,
            0,
            PAGE_WIDTH,
            4,
            fill=1,
            stroke=0
        )

        pdf.setFont("Helvetica", 8)
        pdf.setFillColor(GREY)

        pdf.drawString(
            left,
            10 * mm,
            "AUTODS | Autonomous Data Scientist"
        )

        pdf.drawRightString(
            right,
            10 * mm,
            f"Page {pdf.getPageNumber()}"
        )

    def new_page():
        nonlocal y
        draw_footer()
        pdf.showPage()
        draw_header()
        y = top

    def ensure_space(required_height):
        nonlocal y

        if y - required_height < bottom:
            new_page()

    def wrap_text(text, font_name, font_size, max_width):
        words = text.split()
        if not words:
            return [""]

        result = []
        current = words[0]

        for word in words[1:]:
            test = current + " " + word

            if stringWidth(
                test,
                font_name,
                font_size
            ) <= max_width:
                current = test
            else:
                result.append(current)
                current = word

        result.append(current)

        return result

    # ---------------------------------------------------------
    # FIRST PAGE HEADER
    # ---------------------------------------------------------
    draw_header()

    # Title background
    ensure_space(35 * mm)

    pdf.setFillColor(NAVY)
    pdf.roundRect(
        left,
        y - 30 * mm,
        usable_width,
        30 * mm,
        5 * mm,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(WHITE)
    pdf.setFont(
        "Helvetica-Bold",
        20
    )

    pdf.drawCentredString(
        PAGE_WIDTH / 2,
        y - 13 * mm,
        "AUTONOMOUS DATA SCIENTIST"
    )

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawCentredString(
        PAGE_WIDTH / 2,
        y - 21 * mm,
        "AUTODS FINAL DATA SCIENCE REPORT"
    )

    y -= 38 * mm

    # ---------------------------------------------------------
    # CONTENT
    # ---------------------------------------------------------
    section_colors = [
        BLUE,
        PURPLE,
        CYAN,
        GREEN
    ]

    section_index = 0

    for raw_line in lines:

        line = raw_line.strip()

        # Empty line
        if not line:
            y -= 4
            continue

        # Skip original report title
        if line.upper().startswith(
            "AUTODS - FINAL DATA SCIENCE REPORT"
        ):
            continue

        # Skip separator lines
        if len(line) > 3 and all(
            character in "=-"
            for character in line
        ):
            continue

        # -----------------------------------------------------
        # SECTION HEADING
        # -----------------------------------------------------
        is_heading = (
            len(line) >= 4
            and line[0].isdigit()
            and ". " in line[:5]
            and line.upper() == line
        )

        if is_heading:

            section_color = section_colors[
                section_index % len(section_colors)
            ]

            section_index += 1

            ensure_space(13 * mm)

            pdf.setFillColor(section_color)

            pdf.roundRect(
                left,
                y - 10 * mm,
                usable_width,
                10 * mm,
                2 * mm,
                fill=1,
                stroke=0
            )

            pdf.setFillColor(WHITE)

            pdf.setFont(
                "Helvetica-Bold",
                11
            )

            pdf.drawString(
                left + 4 * mm,
                y - 6.8 * mm,
                line
            )

            y -= 16 * mm

            continue

        # -----------------------------------------------------
        # BULLET
        # -----------------------------------------------------
        if line.startswith("- ") or line.startswith("• "):

            bullet_text = line[2:].strip()

            wrapped = wrap_text(
                bullet_text,
                "Helvetica",
                9.5,
                usable_width - 10 * mm
            )

            required = len(wrapped) * 5 * mm + 2 * mm

            ensure_space(required)

            pdf.setFillColor(BLUE)

            pdf.circle(
                left + 2 * mm,
                y - 1.2 * mm,
                1 * mm,
                fill=1,
                stroke=0
            )

            pdf.setFillColor(DARK)

            pdf.setFont(
                "Helvetica",
                9.5
            )

            text_y = y

            for wrapped_line in wrapped:

                pdf.drawString(
                    left + 6 * mm,
                    text_y,
                    wrapped_line
                )

                text_y -= 5 * mm

            y = text_y - 2 * mm

            continue

        # -----------------------------------------------------
        # NORMAL TEXT
        # -----------------------------------------------------
        wrapped = wrap_text(
            line,
            "Helvetica",
            9.5,
            usable_width
        )

        required = len(wrapped) * 5 * mm + 2 * mm

        ensure_space(required)

        pdf.setFillColor(DARK)

        pdf.setFont(
            "Helvetica",
            9.5
        )

        for wrapped_line in wrapped:

            pdf.drawString(
                left,
                y,
                wrapped_line
            )

            y -= 5 * mm

        y -= 1 * mm

    # ---------------------------------------------------------
    # FINALIZE
    # ---------------------------------------------------------
    draw_footer()

    pdf.save()

    return pdf_file
@app.get("/api/report/download")
def download_report():
    pdf_file = create_report_pdf()

    return FileResponse(
        path=str(pdf_file),
        media_type="application/pdf",
        filename="AUTODS_Final_Report.pdf",
    )
# ============================================================
# PHASE 8 - AUTONOMOUS ORCHESTRATOR
# ============================================================

@app.post("/api/autods/run")
async def run_autods(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".csv"):

        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported."
        )

    # ========================================================
    # SAVE FILE
    # ========================================================

    original_file = DATA_DIR / file.filename

    with open(
        original_file,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    workflow_state["input_file"] = str(
        original_file
    )

    # ========================================================
    # PHASE 1 - PROFILING
    # ========================================================

    df = pd.read_csv(original_file)

    numerical_columns = (
        df.select_dtypes(include=np.number)
        .columns
        .tolist()
    )

    categorical_columns = (
        df.select_dtypes(exclude=np.number)
        .columns
        .tolist()
    )

    profiling_result = {

        "rows":
            len(df),

        "columns":
            len(df.columns),

        "column_names":
            df.columns.tolist(),

        "data_types": {
            column: str(dtype)
            for column, dtype in df.dtypes.items()
        },

        "missing_values": {
            column: int(value)
            for column, value
            in df.isnull().sum().items()
        },

        "duplicate_rows":
            int(df.duplicated().sum()),

        "numerical_columns":
            numerical_columns,

        "categorical_columns":
            categorical_columns
    }

    workflow_state[
        "profiling_result"
    ] = profiling_result

    # ========================================================
    # PHASE 2 - CLEANING
    # ========================================================

    original_rows = len(df)

    duplicates_removed = int(
        df.duplicated().sum()
    )

    missing_before = int(
        df.isnull().sum().sum()
    )

    df = df.drop_duplicates()

    for column in df.columns:

        if pd.api.types.is_numeric_dtype(
            df[column]
        ):

            df[column] = df[column].fillna(
                df[column].median()
            )

        else:

            mode = df[column].mode()

            if len(mode) > 0:

                df[column] = df[column].fillna(
                    mode[0]
                )

    missing_after = int(
        df.isnull().sum().sum()
    )

    cleaned_file = (
        DATA_DIR /
        f"{original_file.stem}_cleaned.csv"
    )

    df.to_csv(
        cleaned_file,
        index=False
    )

    workflow_state[
        "cleaned_file"
    ] = str(cleaned_file)

    cleaning_result = {

        "original_rows":
            original_rows,

        "cleaned_rows":
            len(df),

        "duplicates_removed":
            duplicates_removed,

        "missing_values_before":
            missing_before,

        "missing_values_after":
            missing_after
    }

    workflow_state[
        "cleaning_result"
    ] = cleaning_result

    # ========================================================
    # PHASE 3 - EDA
    # ========================================================

    numerical_columns = (
        df.select_dtypes(include=np.number)
        .columns
        .tolist()
    )

    categorical_columns = (
        df.select_dtypes(exclude=np.number)
        .columns
        .tolist()
    )

    statistics = {}

    for column in numerical_columns:

        statistics[column] = {

            "mean":
                float(df[column].mean()),

            "median":
                float(df[column].median()),

            "minimum":
                float(df[column].min()),

            "maximum":
                float(df[column].max()),

            "standard_deviation":
                float(df[column].std())
        }

    correlation = {}

    if len(numerical_columns) >= 2:

        correlation = (
            df[numerical_columns]
            .corr()
            .round(4)
            .to_dict()
        )

    eda_result = {

        "rows":
            len(df),

        "columns":
            len(df.columns),

        "column_names":
            df.columns.tolist(),

        "numerical_columns":
            numerical_columns,

        "categorical_columns":
            categorical_columns,

        "statistics":
            statistics,

        "correlation":
            correlation
    }

    workflow_state[
        "eda_result"
    ] = eda_result

    # ========================================================
    # PHASE 4 - MODELING
    # ========================================================

    modeling_result = None

    if len(numerical_columns) >= 2:

        feature = numerical_columns[0]

        target = numerical_columns[1]

        X = df[[feature]]

        y = df[target]

        X_train, X_test, y_train, y_test = (
            train_test_split(
                X,
                y,
                test_size=0.20,
                random_state=42
            )
        )

        model = LinearRegression()

        model.fit(
            X_train,
            y_train
        )

        predictions = model.predict(
            X_test
        )

        mae = mean_absolute_error(
            y_test,
            predictions
        )

        rmse = np.sqrt(
            mean_squared_error(
                y_test,
                predictions
            )
        )

        r2 = r2_score(
            y_test,
            predictions
        )

        modeling_result = {

            "algorithm":
                "Linear Regression",

            "feature":
                feature,

            "target":
                target,

            "training_rows":
                len(X_train),

            "testing_rows":
                len(X_test),

            "mae":
                float(mae),

            "rmse":
                float(rmse),

            "r2_score":
                float(r2),

            "coefficient":
                float(model.coef_[0]),

            "intercept":
                float(model.intercept_)
        }

    workflow_state[
        "modeling_result"
    ] = modeling_result

    # ========================================================
    # PHASE 5 - VISUALIZATION
    # ========================================================

    generated_plots = []

    # Histograms
    for column in numerical_columns:

        fig = px.histogram(
            df,
            x=column,
            title=f"Distribution of {column}",
            marginal="box",
            nbins=30
        )

        fig.update_layout(
            template="plotly_white"
        )

        filename = (
            f"{column.lower()}_histogram.html"
        )

        filepath = (
            VISUALIZATION_DIR /
            filename
        )

        fig.write_html(
            str(filepath)
        )

        generated_plots.append({

            "type":
                "histogram",

            "name":
                filename,

            "url":
                f"/visualizations/{filename}"
        })

    # Scatter + Heatmap
    if len(numerical_columns) >= 2:

        x = numerical_columns[0]

        y = numerical_columns[1]

        # Scatter
        fig = px.scatter(
            df,
            x=x,
            y=y,
            title=f"{y} vs {x}"
        )

        fig.update_layout(
            template="plotly_white"
        )

        filename = (
            f"{x.lower()}_vs_{y.lower()}.html"
        )

        filepath = (
            VISUALIZATION_DIR /
            filename
        )

        fig.write_html(
            str(filepath)
        )

        generated_plots.append({

            "type":
                "scatter",

            "name":
                filename,

            "url":
                f"/visualizations/{filename}"
        })

        # Heatmap
        corr = df[
            numerical_columns
        ].corr()

        fig = px.imshow(
            corr,
            text_auto=True,
            title="Correlation Heatmap",
            aspect="auto"
        )

        fig.update_layout(
            template="plotly_white"
        )

        filename = (
            "correlation_heatmap.html"
        )

        filepath = (
            VISUALIZATION_DIR /
            filename
        )

        fig.write_html(
            str(filepath)
        )

        generated_plots.append({

            "type":
                "heatmap",

            "name":
                filename,

            "url":
                f"/visualizations/{filename}"
        })

    # Boxplots
    for column in numerical_columns:

        fig = px.box(
            df,
            y=column,
            title=f"Box Plot - {column}"
        )

        fig.update_layout(
            template="plotly_white"
        )

        filename = (
            f"{column.lower()}_boxplot.html"
        )

        filepath = (
            VISUALIZATION_DIR /
            filename
        )

        fig.write_html(
            str(filepath)
        )

        generated_plots.append({

            "type":
                "boxplot",

            "name":
                filename,

            "url":
                f"/visualizations/{filename}"
        })

    # Categorical charts
    for column in categorical_columns:

        if df[column].nunique() <= 30:

            counts = (
                df[column]
                .value_counts()
                .reset_index()
            )

            counts.columns = [
                column,
                "Count"
            ]

            fig = px.bar(
                counts,
                x=column,
                y="Count",
                title=f"Distribution of {column}"
            )

            fig.update_layout(
                template="plotly_white"
            )

            filename = (
                f"{column.lower()}_bar_chart.html"
            )

            filepath = (
                VISUALIZATION_DIR /
                filename
            )

            fig.write_html(
                str(filepath)
            )

            generated_plots.append({

                "type":
                    "bar_chart",

                "name":
                    filename,

                "url":
                    f"/visualizations/{filename}"
            })

    visualization_result = {

        "library":
            "Plotly",

        "plots_generated":
            len(generated_plots),

        "generated_plots":
            generated_plots
    }

    workflow_state[
        "visualization_result"
    ] = visualization_result

    # ========================================================
    # PHASE 6 - AI INSIGHTS
    # ========================================================

    observations = []

    missing_values = int(
        df.isnull().sum().sum()
    )

    duplicate_rows = int(
        df.duplicated().sum()
    )

    if missing_values == 0:

        observations.append(
            "The dataset contains no missing values."
        )

    else:

        observations.append(
            f"The dataset contains "
            f"{missing_values} missing values."
        )

    if duplicate_rows == 0:

        observations.append(
            "No duplicate rows were found."
        )

    else:

        observations.append(
            f"The dataset contains "
            f"{duplicate_rows} duplicate rows."
        )

    correlation_value = None

    if len(numerical_columns) >= 2:

        correlation_value = float(
            df[numerical_columns]
            .corr()
            .iloc[0, 1]
        )

        observations.append(
            f"Correlation between "
            f"{numerical_columns[0]} and "
            f"{numerical_columns[1]} "
            f"is {correlation_value:.4f}."
        )

        if correlation_value > 0.7:

            observations.append(
                "There is a strong positive "
                "relationship between the first "
                "two numerical variables."
            )

        elif correlation_value < -0.7:

            observations.append(
                "There is a strong negative "
                "relationship between the first "
                "two numerical variables."
            )

        else:

            observations.append(
                "The relationship between the first "
                "two numerical variables is relatively weak."
            )

    if modeling_result:

        observations.append(
            "A Linear Regression model was trained "
            "using the first numerical column "
            "to predict the second."
        )

    observations.append(
        "Plotly visualizations were generated "
        "for distributions, relationships, "
        "correlations and outliers."
    )

    insights_result = {

        "observations":
            observations,

        "correlation":
            correlation_value
    }

    workflow_state[
        "insights_result"
    ] = insights_result

    # ========================================================
    # PHASE 7 - REPORT
    # ========================================================

    report = f"""
============================================================
AUTODS - FINAL DATA SCIENCE REPORT
============================================================

DATASET UPLOAD
--------------
The uploaded dataset was accepted and passed to the AutoDS pipeline.


1. EXECUTIVE SUMMARY
--------------------
The AutoDS pipeline profiled, cleaned, explored, modeled and visualized the uploaded dataset, then consolidated the findings into this report.


2. PROBLEM STATEMENT
--------------------
The analysis evaluates dataset quality, relationships between variables, predictive performance and actionable findings using the uploaded data.


3. DATASET OVERVIEW
-------------------
Rows: {len(df)}
Columns: {len(df.columns)}
Columns: {df.columns.tolist()}


4. DATA QUALITY ASSESSMENT
------------
Missing Values: {missing_values}
Duplicate Rows: {duplicate_rows}


5. DATA CLEANING
--------
Original Rows: {original_rows}
Cleaned Rows: {len(df)}
Duplicates Removed: {duplicates_removed}


6. EXPLORATORY DATA ANALYSIS
-------------------------
Numerical Columns:
{numerical_columns}

Categorical Columns:
{categorical_columns}

Statistics:
{format_statistics(statistics)}

Correlation:
{format_correlation(correlation)}


8. BEST MODEL
--------
Algorithm:
{modeling_result.get("algorithm") if modeling_result else "N/A"}

Feature:
{modeling_result.get("feature") if modeling_result else "N/A"}

Target:
{modeling_result.get("target") if modeling_result else "N/A"}

Training Rows:
{modeling_result.get("training_rows") if modeling_result else "N/A"}

Testing Rows:
{modeling_result.get("testing_rows") if modeling_result else "N/A"}

MAE:
{modeling_result.get("mae") if modeling_result else "N/A"}

RMSE:
{modeling_result.get("rmse") if modeling_result else "N/A"}

R2 Score:
{modeling_result.get("r2_score") if modeling_result else "N/A"}


9. MODEL EVALUATION
-------------------
MAE: {modeling_result.get("mae") if modeling_result else "N/A"}
RMSE: {modeling_result.get("rmse") if modeling_result else "N/A"}
R2 Score: {modeling_result.get("r2_score") if modeling_result else "N/A"}


7. VISUALIZATION INSIGHTS
-------------
Library: Plotly
Plots Generated: {len(generated_plots)}


10. KEY DATA INSIGHTS
-----------
{chr(10).join("- " + x for x in observations)}


11. BUSINESS RECOMMENDATIONS
---------------
- Validate the model using unseen data.
- Perform cross-validation.
- Compare multiple ML algorithms.
- Add useful features.
- Monitor model performance.
- Analyze generated visualizations.


12. LIMITATIONS
---------------
The modeling result uses the available numerical columns and a single train/test split. Results should be interpreted within the scope and quality of the uploaded dataset.


13. FUTURE IMPROVEMENTS
-----------------------
- Compare additional model families.
- Use cross-validation and broader feature engineering.
- Validate recommendations with domain knowledge and new data.


14. CONCLUSION
----------------
The AutoDS system successfully processed the dataset
through profiling, cleaning, EDA, modeling,
visualization, AI insights and report generation.

============================================================
END OF REPORT
============================================================
"""

    report_file = (
        REPORT_DIR /
        "autods_final_report.txt"
    )

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(report)

    workflow_state[
        "final_report"
    ] = report

    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    phase1_summary = build_profiling_summary(profiling_result)
    phase2_summary = (
        "The Cleaning Agent removed duplicate rows and filled missing values to prepare a cleaner dataset for analysis. "
        f"{cleaning_result.get('duplicates_removed', 0)} duplicate record(s) were removed and the cleaned dataset contains {cleaning_result.get('cleaned_rows', 0)} rows."
    )
    phase3_summary = (
        "The EDA Agent analyzed the dataset distributions and calculated descriptive statistics across the numerical features. "
        f"{len(eda_result.get('numerical_columns', []))} numerical columns and {len(eda_result.get('categorical_columns', []))} categorical columns were evaluated."
    )
    phase4_summary = (
        "The Modeling Agent trained a predictive model and evaluated its performance on held-out data. "
        f"The selected model is {modeling_result.get('algorithm', 'Linear Regression')} with an R^2 score of {modeling_result.get('r2_score', 0):.4f}."
    ) if modeling_result else "The Modeling Agent did not produce a model because insufficient numerical data was available."
    phase5_summary = (
        f"The Visualization Agent generated {visualization_result.get('plots_generated', 0)} analytical charts and visualizations to support interpretation."
    ) if visualization_result else "The Visualization Agent did not generate any charts for this dataset."
    phase6_summary = (
        "The AI Insights Agent synthesized the dataset findings into a concise interpretation. "
        f"{len(observations)} observations were produced, including duplicate and correlation findings."
    )
    phase7_summary = (
        "The Report Agent consolidated the full pipeline into a final autonomous data science report. "
        "The narrative report, recommendations, and dataset findings are now available for review."
    )

    return {
        "status": "success",
        "workflow_status": "completed",
        "message": "AutoDS pipeline completed successfully.",
        "filename": original_file.name,
        "phase1": {
            **build_agent_payload(
                "profiling",
                result=profiling_result,
                summary=phase1_summary,
                metrics={
                    "rows": profiling_result.get("rows"),
                    "columns": profiling_result.get("columns"),
                    "duplicate_rows": profiling_result.get("duplicate_rows"),
                    "missing_values": sum(int(v) for v in (profiling_result.get("missing_values") or {}).values())
                },
                warnings=[] if int(profiling_result.get("duplicate_rows") or 0) == 0 else ["Duplicate rows were detected and should be reviewed before modeling."],
                recommendations=["Review duplicate records before modeling."] if int(profiling_result.get("duplicate_rows") or 0) > 0 else ["Proceed to cleaning and EDA to validate data quality."]
            ),
            "status": "completed"
        },
        "phase2": {
            **build_agent_payload(
                "cleaning",
                result=cleaning_result,
                summary=phase2_summary,
                metrics={
                    "original_rows": cleaning_result.get("original_rows"),
                    "cleaned_rows": cleaning_result.get("cleaned_rows"),
                    "duplicates_removed": cleaning_result.get("duplicates_removed"),
                    "missing_values_before": cleaning_result.get("missing_values_before"),
                    "missing_values_after": cleaning_result.get("missing_values_after")
                },
                warnings=[] if int(cleaning_result.get("duplicates_removed") or 0) == 0 else ["Duplicate rows were removed during cleaning."],
                recommendations=["Confirm the cleaned dataset remains representative before modeling."]
            ),
            "status": "completed"
        },
        "phase3": {
            **build_agent_payload(
                "eda",
                result=eda_result,
                summary=phase3_summary,
                metrics={
                    "rows": eda_result.get("rows"),
                    "columns": eda_result.get("columns"),
                    "numerical_columns": len(eda_result.get("numerical_columns") or []),
                    "categorical_columns": len(eda_result.get("categorical_columns") or [])
                },
                warnings=[],
                recommendations=["Use the strongest correlations and distributions to guide modeling choices."]
            ),
            "status": "completed"
        },
        "phase4": {
            **build_agent_payload(
                "modeling",
                result=(modeling_result if modeling_result else {}),
                summary=phase4_summary,
                metrics={
                    "algorithm": modeling_result.get("algorithm") if modeling_result else "N/A",
                    "r2_score": modeling_result.get("r2_score") if modeling_result else None,
                    "mae": modeling_result.get("mae") if modeling_result else None,
                    "rmse": modeling_result.get("rmse") if modeling_result else None
                },
                warnings=[],
                recommendations=["Review feature importance and prediction quality before deployment."] if modeling_result else ["Add more numerical features before modeling."]
            ),
            "status": "completed"
        },
        "phase5": {
            **build_agent_payload(
                "visualization",
                result=(visualization_result if visualization_result else {}),
                summary=phase5_summary,
                metrics={
                    "plots_generated": visualization_result.get("plots_generated") if visualization_result else 0,
                    "library": visualization_result.get("library") if visualization_result else "N/A"
                },
                warnings=[],
                recommendations=["Use the visual results to confirm the most important patterns before final reporting."]
            ),
            "status": "completed"
        },
        "phase6": {
            **build_agent_payload(
                "insights",
                result={
                    "insights": observations,
                    "correlation": correlation_value,
                    "missing_values": missing_values,
                    "duplicate_rows": duplicate_rows
                },
                summary=phase6_summary,
                metrics={
                    "observations": len(observations),
                    "correlation": correlation_value,
                    "missing_values": missing_values,
                    "duplicate_rows": duplicate_rows
                },
                warnings=[] if duplicate_rows == 0 else ["Duplicate rows were detected and may influence conclusions."],
                recommendations=["Use the generated insights to shape the final narrative and recommendations."]
            ),
            "status": "completed"
        },
        "phase7": {
            **build_agent_payload(
                "report",
                result={
                    "summary": "The complete analysis report has been generated by the AutoDS pipeline.",
                    "report": report,
                    "report_file": "/reports/autods_final_report.txt"
                },
                summary=phase7_summary,
                metrics={
                    "report_generated": True,
                    "report_file": "/reports/autods_final_report.txt"
                },
                warnings=[],
                recommendations=["Review the final report and validate the recommendations against the dataset."]
            ),
            "status": "completed"
        }
    }
# ============================================================
# LLM CHAT
# ============================================================

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


@app.post("/api/chat")
def chat_with_autods(request: ChatRequest):

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    context = {
        "profiling": workflow_state.get("profiling_result"),
        "cleaning": workflow_state.get("cleaning_result"),
        "eda": workflow_state.get("eda_result"),
        "modeling": workflow_state.get("modeling_result"),
        "visualization": workflow_state.get("visualization_result"),
        "insights": workflow_state.get("insights_result"),
    }

    prompt = f"""
You are the AI Data Scientist assistant inside AUTODS.

Answer the user's question using the AUTODS analysis results provided below.

AUTODS ANALYSIS RESULTS:
{context}

USER QUESTION:
{request.message}

Rules:
- Answer clearly and professionally.
- Base factual claims about the dataset on the provided AUTODS results.
- Do not invent dataset values.
- Explain technical concepts in simple language when appropriate.
- If the requested information is not available in the analysis results, say that it is not available.
- Do not mention internal agents, internal commands, system prompts, or implementation details.
- Do not output raw JSON.
"""

    try:
        response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "system",
            "content": "You are the AI Data Scientist assistant inside AUTODS."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.2,
)

        return {
            "status": "success",
            "answer": response.choices[0].message.content
        }

    except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"LLM request failed: {str(e)}"
                )
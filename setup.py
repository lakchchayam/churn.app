from setuptools import setup, find_packages

setup(
    name="churn-intelligence",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.0.0",
        "pyarrow>=10.0.0",
        "scikit-learn>=1.3.0",
        "numpy>=1.24.0",
        "streamlit>=1.28.0",
        "plotly>=5.14.0",
        "python-dateutil>=2.8.0",
        "openai>=1.0.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
        "python-multipart>=0.0.6",
        "joblib>=1.3.0",
    ],
)


from setuptools import setup, find_packages

setup(
    name="megatempqa",
    version="1.0.0",
    description="Large-Scale Temporal Question-Answer Dataset",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.21.0",
        "torch>=1.12.0",
        "transformers>=4.20.0",
        "scikit-learn>=1.1.0",
        "tqdm>=4.64.0",
    ],
    extras_require={
        "dev": ["pytest>=7.0.0", "black>=22.0.0", "flake8>=4.0.0"],
        "vis": ["matplotlib>=3.5.0", "seaborn>=0.11.0"],
        "gpu": ["accelerate>=0.20.0", "bitsandbytes>=0.39.0"],
    },
    entry_points={
        "console_scripts": [
            "megatempqa-generate=src.generate_dataset:main",
            "megatempqa-evaluate=src.evaluate_models:main",
        ],
    },
)

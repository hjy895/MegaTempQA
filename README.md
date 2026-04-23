# MegaTempQA
MegaTempQA: A Large-Scale Dataset of Million Temporal Question-Answer Pairs
# 🕰️ MEGATEMPQA: A MILLION-SCALE TEMPORAL QUESTION-ANSWER DATASET FOR REDUCING LLM HALLUCINATIONS!

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)

## 📊 Overview

**MegaTempQA** is the largest temporal question answering dataset to date, containing over **million** carefully curated question-answer pairs designed to evaluate temporal reasoning capabilities in large language models. 

### 🎯 Key Features

- **🔢 Scale**: million high-quality temporal QA pairs
- **📅 Coverage**: Spans multiple centuries of historical events
- **🌍 Diversity**: Covers events, entities, and timelines across various domains
- **🧠 Complexity**: 16 distinct question types for comprehensive evaluation
- **📈 Multi-granular**: Supports temporal reasoning at different time scales
- **🔗 Multi-hop**: Enables complex inferential reasoning tasks

### 📋 Question Types

| **Attribute Questions** | **Comparison Questions** | **Complex Reasoning** |
|------------------------|-------------------------|----------------------|
| 🎯 Event Attribute     | ⚖️ Event Comparison     | 🧠 Causal Reasoning  |
| 👤 Entity Attribute    | 👥 Entity Comparison    | ⏱️ Duration Estimation |
| 🕐 Time Attribute      | 📊 Time Comparison      | 📝 Sequence Ordering |
| **Counting Questions** | **Temporal Analysis**    | **Advanced Reasoning** |
| 📊 Event Counting      | 🔗 Temporal Clustering  | 🌐 Cross-Domain      |
| 👥 Entity Counting     | 📏 Multi-Granular       | 🤔 Counterfactual    |
|                        | 🔄 Temporal Overlap     |                      |


## 📁 Repository Structure

```
MegaTempQA/
├── 📜 README.md                    # Main documentation
├── 📋 requirements.txt             # Dependencies
├── 📄 LICENSE                      # MIT License
├── ⚙️  setup.py                     # Package setup
├── 
├── 📊 paper/                        # Paper materials
│   └── abstract.md                 # Paper abstract
├── 
├── 🔧 src/                          # Source code
│   ├── generate_dataset.py         # Main dataset generator
│   ├── evaluate_models.py          # Main evaluation script
│   │
│   ├── data_generation/             # Dataset generation modules
│   │   ├── generator.py             # Core generator
│   │   ├── knowledge_base.py        # Historical data
│   │   ├── question_types.py        # Question type definitions
│   │   ├── validators.py            # Quality validation
│   │   └── templates.py             # Question templates
│   │
│   ├── evaluation/                  # Model evaluation modules
│   │   ├── evaluator.py             # Main evaluator
│   │   ├── model_manager.py         # Model loading/management
│   │   ├── metrics.py               # Evaluation metrics
│   │   ├── prompt_builder.py        # Few-shot prompts
│   │   └── result_analyzer.py       # Results analysis
│   │
│   └── utils/                       # Utility modules
│       ├── config.py                # Configuration
│       ├── file_utils.py            # File operations
│       └── logging_utils.py         # Logging setup
├── 
├── 📊 data/                         # Dataset files
│   ├── README.md                    # Data documentation
│   ├── sample_dataset.csv           # Sample for testing
│   └── schema.json                  # Dataset schema
├── 
└── 🧪 tests/                        # Test suite
    └── test_generation.py           # Generation tests
```
## 📊 Complete Dataset Access
Due to the substantial size of our dataset, the complete MegaTempQA dataset is available through institutional data sharing agreements. The dataset is provided in its raw, unstructured format to preserve data integrity and enable diverse research applications.

Data Availability Statement: The complete dataset supporting the findings of this study is available from the corresponding authors upon reasonable request. Due to the large-scale nature of the data, researchers are encouraged to specify their computational requirements and intended use cases when requesting access. Given the unstructured nature of the complete dataset, researchers should implement appropriate preprocessing pipelines tailored to their specific research objectives. 

## 📊 Sample Datasets for Research
To facilitate immediate research and experimentation, we provide curated sample datasets through multiple channels:

🤗 Hugging Face Hub: Samples (1M QA pairs) available at ([huggingface.co/datasets/hjav/MegaTempQA](https://huggingface.co/datasets/hjav/MegaTempQA))

📊 GitHub Repository: Samples with multiple domain examples in the /samples directory

🔬 Research Portal: Domain-specific subsets for targeted evaluation

## 📊 Dataset Statistics

| Metric | Value |
|--------|-------|
| **Total Questions** | Million |
| **Question Types** | 16 Categories |
| **Time Range** | 1900-2025 |
| **Domains** | History, Science, Technology, Politics, Culture |
| **Languages** | English |
| **Format** | CSV, JSON |

## 🎯 Evaluation Results

Our comprehensive evaluation demonstrates:
- **Baseline Performance**: Most models struggle with temporal reasoning
- **Few-shot Learning**: 1-3 shot examples significantly improve performance  
- **Model Variations**: Significant performance differences across model families
- **Question Complexity**: Performance varies by temporal question type

## 📖 Citation

```bibtex
@dataset{megatempqa2025,
  title={MegaTempQA: A Large-Scale Dataset of Million Temporal Question-Answer Pairs for Language Models},
  year={20256},
  Accepted in ICASSP 2026
}
```

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues and enhancement requests.

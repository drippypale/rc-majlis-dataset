# Iranian Laws Dataset
## Dataset Description
This dataset contains the laws passed by the _Iranian parliament (Majlis)_ up to **April 29, 2024**. The data has been crawled from the website [rc.majlis.ir](https://rc.majlis.ir/fa/law/) and contains essential information about each law including its title, date of approval, the approving body, the content of the law, and a reference URL.

## Dataset Columns
- title (عنوان مصوبه): The title of the law.
- date (تاریخ تصویب): The date when the law was approved, converted to datetime format.
- reference (مرجع تصویب): The approving body.
- content (جزئیات متن قانون): The detailed content of the law, with stemming applied.
- url (لینک مصوبه): The URL linking to the original law on the rc.majlis.ir website.

## Data Cleaning Steps
- The `date` column has been converted to `datetime` format.
- The `title` and `content` columns have been striped to facilitate text analysis tasks.

## How to Use This Dataset
This dataset is suitable for a variety of tasks including, but not limited to:
- Text analysis and natural language processing (NLP) tasks.
- Legal research and comparative legal studies.
- Trend analysis in legislative activities.
- Machine learning projects focusing on text classification or clustering.

## Example Analysis
To help you get started, here are a few example tasks you could perform with this dataset:
- Text Classification: Classify laws based on their titles or content.
- Trend Analysis: Analyze trends in legislative activity over time.
- NLP Tasks: Apply various NLP techniques such as topic modeling, sentiment analysis, or named entity recognition.

## Getting Started
To get started with this dataset, simply download the `law_cleaned.csv` file and load it into your preferred data analysis tool. For example, in Python, you can use *pandas*:
```python
import pandas as pd

# Load the dataset
df = pd.read_csv('law_cleaned.csv')

# Display the first few rows
print(df.head())
```

## About the Data Collection Process
The data was collected by crawling the [rc.majlis.ir](https://rc.majlis.ir/fa/law/) website, which contains a comprehensive archive of Iranian laws. The dataset includes all available laws up to **April 29, 2024**.

## Kaggle
You can also find this dataset on the kaggle from [here](https://www.kaggle.com/datasets/mrsmde/rc-majlis-ir-laws).

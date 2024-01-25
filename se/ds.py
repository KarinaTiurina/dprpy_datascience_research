import pandas as pd
import xml.etree.ElementTree as ET
import re
from collections import Counter

from se.QuestionsAnalyzer import QuestionsAnalyzer


class DataScienceSEQuestionAnalyzer(QuestionsAnalyzer):
    def __init__(self, file_path):
        tags = {
            "data-science",
            "machine-learning",
            "statistics",
            "data-analysis",
            "python",
            "r",
            "big-data",
            "data-mining",
            "pandas",
            "numpy",
        }
        super().__init__(file_path, tags)


if __name__ == "__main__":
    file_path = "../datascience.stackexchange.com/Posts.xml"
    ds_analyzer = DataScienceSEQuestionAnalyzer(file_path)

    ds_analyzer.load_and_filter_questions()

    most_common_ds_questions = ds_analyzer.get_most_common_questions()

    output_file = "most_common_ds_questions.txt"
    ds_analyzer.save_most_common_questions_to_file(output_file)

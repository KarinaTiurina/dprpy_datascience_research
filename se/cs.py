import pandas as pd
import xml.etree.ElementTree as ET
import re
from collections import Counter

from se.QuestionsAnalyzer import QuestionsAnalyzer


class ComputerScienceSEQuestionAnalyzer(QuestionsAnalyzer):
    def __init__(self, file_path):
        tags = {
            "computer-science",
            "algorithms",
            "data-structures",
            "programming",
            "computer-architecture",
            "networking",
            "databases",
            "operating-systems",
            "software-engineering",
            "theoretical-computer-science",
        }
        super().__init__(file_path, tags)


if __name__ == "__main__":
    file_path_cs = "../cs.stackexchange.com/Posts.xml"
    cs_analyzer = ComputerScienceSEQuestionAnalyzer(file_path_cs)

    cs_analyzer.load_and_filter_questions()

    most_common_cs_questions = cs_analyzer.get_most_common_questions()

    output_file = "most_common_cs_questions.txt"
    cs_analyzer.save_most_common_questions_to_file(output_file)

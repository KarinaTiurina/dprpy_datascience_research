import pandas as pd
import xml.etree.ElementTree as ET
import re
from collections import Counter

from se.QuestionsAnalyzer import QuestionsAnalyzer


class AISEQuestionAnalyzer(QuestionsAnalyzer):
    def __init__(self, file_path):
        tags = {
            "artificial-intelligence",
            "neural-networks",
            "machine-learning",
            "deep-learning",
            "reinforcement-learning",
            "natural-language-processing",
            "computer-vision",
            "convolutional-neural-networks",
            "deep-rl",
            "classification",
            "training",
        }
        super().__init__(file_path, tags)


if __name__ == "__main__":
    file_path_ai = "../ai.stackexchange.com/Posts.xml"
    ai_analyzer = AISEQuestionAnalyzer(file_path_ai)

    ai_analyzer.load_and_filter_questions()

    most_common_ai_questions = ai_analyzer.get_most_common_questions()
    output_file = "most_common_ai_questions.txt"
    ai_analyzer.save_most_common_questions_to_file(output_file)

    comments_file_path = "../ai.stackexchange.com/Comments.xml"
    most_discussed_questions = ai_analyzer.get_most_discussed_questions(
        comments_file_path, 10
    )

    print(most_discussed_questions["Title"].head(10))

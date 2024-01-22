import pandas as pd
import xml.etree.ElementTree as ET
import re
from collections import Counter

class DataScienceSEQuestionAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.ds_related_tags = {'data-science', 'machine-learning', 'statistics', 'data-analysis', 'python',
                                'r', 'big-data', 'data-mining', 'pandas', 'numpy'}
        self.posts_df = None

    @staticmethod
    def clean_html(raw_html):
        cleanr = re.compile('<.*?>')
        return re.sub(cleanr, '', raw_html)

    def load_and_filter_questions(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        posts_data = []
        for post in root.findall(".//row[@PostTypeId='1']"):
            post_data = post.attrib
            if any(tag in post_data.get('Tags', '') for tag in self.ds_related_tags):
                posts_data.append({
                    'Id': post_data.get('Id'),
                    'Title': post_data.get('Title'),
                    'Tags': post_data.get('Tags'),
                    'CreationYear': post_data.get('CreationDate')[:4]
                })

        self.posts_df = pd.DataFrame(posts_data)
        self.posts_df["CreationYear"] = self.posts_df["CreationYear"].astype(int)
        self.posts_df['CleanTitle'] = self.posts_df['Title'].apply(self.clean_html)

    def load_and_filter_questions_all_tags(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        posts_data = []
        for post in root.findall(".//row[@PostTypeId='1']"):
            post_data = post.attrib
            posts_data.append({
                'Id': post_data.get('Id'),
                'Title': post_data.get('Title'),
                'Tags': post_data.get('Tags'),
                'CreationYear': post_data.get('CreationDate')[:4]
            })

        self.posts_df = pd.DataFrame(posts_data)
        self.posts_df["CreationYear"] = self.posts_df["CreationYear"].astype(int)
        self.posts_df['CleanTitle'] = self.posts_df['Title'].apply(self.clean_html)

    def get_most_common_questions(self, num_questions=10):
        if self.posts_df is None:
            return "Data not loaded. Please load data using load_and_filter_questions() method."

        question_titles = self.posts_df[self.posts_df['CleanTitle'].str.endswith('?')]['CleanTitle']
        question_counter = Counter(question_titles)
        return question_counter.most_common(num_questions)

    def save_most_common_questions_to_file(self, output_file):
        most_common_questions = self.get_most_common_questions()
        with open(output_file, 'w') as file:
            for question, count in most_common_questions:
                file.write(f"{question} (Occurrences: {count})\n")

    def getDf(self):
        return self.posts_df
    
    def getPostsCountByYear(self):
        return self.posts_df.groupby('CreationYear')['Id'].count().reset_index(name="Count")
    
if __name__ == "__main__":
    file_path = '../datascience.stackexchange.com/Posts.xml'
    ds_analyzer = DataScienceSEQuestionAnalyzer(file_path)

    ds_analyzer.load_and_filter_questions()

    most_common_ds_questions = ds_analyzer.get_most_common_questions()

    output_file = 'most_common_ds_questions.txt'
    ds_analyzer.save_most_common_questions_to_file(output_file)

from collections import Counter
import pandas as pd
import xml.etree.ElementTree as ET
import re


class QuestionsAnalyzer:
    def __init__(self, file_path=None, tags=None):
        self.file_path = file_path
        self.tags = tags
        self.posts_df = None

    @staticmethod
    def clean_html(raw_html):
        cleanr = re.compile("<.*?>")
        return re.sub(cleanr, "", raw_html)

    def load_and_filter_questions(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        posts_data = []
        for post in root.findall(".//row[@PostTypeId='1']"):
            post_data = post.attrib
            if any(tag in post_data.get("Tags", "") for tag in self.tags):
                posts_data.append(
                    {
                        "Id": post_data.get("Id"),
                        "Title": post_data.get("Title"),
                        "Tags": post_data.get("Tags"),
                        "CreationYear": post_data.get("CreationDate")[:4],
                    }
                )

        self.posts_df = pd.DataFrame(posts_data)
        self.posts_df["CreationYear"] = self.posts_df["CreationYear"].astype(int)
        self.posts_df["CleanTitle"] = self.posts_df["Title"].apply(self.clean_html)

    def load_and_filter_questions_all_tags(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        posts_data = []
        for post in root.findall(".//row[@PostTypeId='1']"):
            post_data = post.attrib
            posts_data.append(
                {
                    "Id": post_data.get("Id"),
                    "Title": post_data.get("Title"),
                    "Tags": post_data.get("Tags"),
                    "CreationYear": post_data.get("CreationDate")[:4],
                }
            )

        self.posts_df = pd.DataFrame(posts_data)
        self.posts_df["CreationYear"] = self.posts_df["CreationYear"].astype(int)
        self.posts_df["CleanTitle"] = self.posts_df["Title"].apply(self.clean_html)

    def get_most_common_questions(self, num_questions=10):
        if self.posts_df is None:
            return "Data not loaded. Please load data using load_and_filter_posts() method."

        question_titles = self.posts_df[self.posts_df["CleanTitle"].str.endswith("?")][
            "CleanTitle"
        ]
        question_counter = Counter(question_titles)
        return question_counter.most_common(num_questions)

    def save_most_common_questions_to_file(self, output_file):
        most_common_questions = self.get_most_common_questions()
        with open(output_file, "w") as file:
            for question, count in most_common_questions:
                file.write(f"{question} (Occurrences: {count})\n")

    def get_most_discussed_questions(self, comments_file_path, num_questions=10):
        if self.posts_df is None:
            return "Data not loaded. Please load data using load_and_filter_posts() method."

        # Parse the comments XML file
        tree = ET.parse(comments_file_path)
        root = tree.getroot()

        # Initialize a Counter for PostId
        comments_counter = Counter()

        # Count the occurrences of each PostId in the comments
        for comment in root.findall(".//row"):
            post_id = comment.attrib.get("PostId")
            if post_id:
                comments_counter[post_id] += 1

        # Convert the Counter to a DataFrame
        comments_df = pd.DataFrame.from_records(
            list(comments_counter.items()), columns=["Id", "CommentsCount"]
        )
        comments_df["Id"] = comments_df["Id"].astype(int)

        # Ensure the 'Id' column in posts_df is of type int
        self.posts_df["Id"] = self.posts_df["Id"].astype(int)

        # Join the comments count with the posts DataFrame
        posts_with_comments = pd.merge(self.posts_df, comments_df, on="Id", how="inner")

        # Sort by CommentsCount in descending order and return the top num_questions
        most_discussed_questions = (
            posts_with_comments.sort_values(by="CommentsCount", ascending=False)
            .head(num_questions)
            .reset_index()
        )[["CleanTitle", "CommentsCount"]]

        return most_discussed_questions

    def getPostsCountByYear(self):
        return (
            self.posts_df.groupby("CreationYear")["Id"]
            .count()
            .reset_index(name="Count")
        )

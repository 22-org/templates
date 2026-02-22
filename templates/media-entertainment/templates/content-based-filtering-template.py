"""
Content-Based Filtering Template for Media & Entertainment
This template implements content-based recommendations for movies, shows, and music
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer
import warnings

warnings.filterwarnings('ignore')


class ContentBasedRecommender:
    """
    Content-Based Recommendation System for Media & Entertainment
    Supports movies, TV shows, music, and other content types
    """

    def __init__(self, content_type='movies'):
        """
        Initialize the recommender

        Args:
            content_type (str): 'movies', 'music', 'shows', or 'general'
        """
        self.content_type = content_type
        self.content_features = None
        self.similarity_matrix = None
        self.content_mapping = {}
        self.reverse_content_mapping = {}
        self.tfidf_vectorizer = None
        self.mlb = None

    def prepare_content_data(self, content_df):
        """
        Prepare content data for content-based filtering

        Args:
            content_df (pd.DataFrame): Content metadata with columns:
                - content_id: Unique identifier
                - title: Content title
                - description: Content description/plot
                - genres: List of genres (optional)
                - tags: List of tags (optional)
                - other metadata columns based on content type

        Returns:
            pd.DataFrame: Processed content features
        """
        # Create content mapping
        self.content_mapping = {content_id: idx for idx, content_id in
                               enumerate(content_df['content_id'].unique())}
        self.reverse_content_mapping = {idx: content_id for content_id, idx in
                                       self.content_mapping.items()}

        # Map content IDs to indices
        content_df['content_idx'] = content_df['content_id'].map(
            self.content_mapping)

        # Sort by content_idx to maintain consistency
        content_df = content_df.sort_values('content_idx').reset_index(drop=True)

        # Process text features
        text_features = self._process_text_features(content_df)

        # Process categorical features
        categorical_features = self._process_categorical_features(content_df)

        # Process numerical features
        numerical_features = self._process_numerical_features(content_df)

        # Combine all features
        self.content_features = self._combine_features(
            text_features, categorical_features, numerical_features)

        return self.content_features

    def _process_text_features(self, content_df):
        """Process text-based features using TF-IDF"""
        # Combine text fields
        text_columns = ['title', 'description']
        available_text_columns = [col for col in text_columns if col in content_df.columns]

        if not available_text_columns:
            return None

        # Create combined text field
        content_df['combined_text'] = content_df[available_text_columns].fillna('').apply(
            lambda x: ' '.join(x), axis=1)

        # Initialize TF-IDF vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.8
        )

        # Fit and transform text features
        text_features = self.tfidf_vectorizer.fit_transform(
            content_df['combined_text'])

        return text_features.toarray()

    def _process_categorical_features(self, content_df):
        """Process categorical features like genres, tags"""
        categorical_columns = ['genres', 'tags']
        available_categorical = [col for col in categorical_columns if col in content_df.columns]

        if not available_categorical:
            return None

        # Process first available categorical column
        cat_col = available_categorical[0]

        # Handle different formats of categorical data
        if content_df[cat_col].dtype == 'object':
            # Handle string representation of lists
            try:
                content_df[cat_col] = content_df[cat_col].apply(
                    lambda x: eval(x) if isinstance(x, str) else x)
            except:
                content_df[cat_col] = content_df[cat_col].fillna('').apply(
                    lambda x: [x] if x else [])

        # Ensure all entries are lists
        content_df[cat_col] = content_df[cat_col].apply(
            lambda x: x if isinstance(x, list) else [x])

        # Multi-label binarization
        self.mlb = MultiLabelBinarizer()
        categorical_features = self.mlb.fit_transform(content_df[cat_col])

        return categorical_features

    def _process_numerical_features(self, content_df):
        """Process numerical features like ratings, year, duration"""
        numerical_columns = {
            'movies': ['year', 'duration', 'rating', 'vote_count'],
            'music': ['year', 'duration', 'tempo', 'energy', 'danceability'],
            'shows': ['year', 'seasons', 'episodes', 'rating'],
            'general': ['year', 'rating', 'popularity']
        }

        available_numerical = [col for col in numerical_columns.get(
            self.content_type, []) if col in content_df.columns]

        if not available_numerical:
            return None

        numerical_features = content_df[available_numerical].fillna(0).values

        # Normalize numerical features
        numerical_features = (numerical_features - numerical_features.mean()) / (
            numerical_features.std() + 1e-8)

        return numerical_features

    def _combine_features(self, text_features, categorical_features, numerical_features):
        """Combine different feature types into a single feature matrix"""
        features_list = []

        if text_features is not None:
            features_list.append(text_features)

        if categorical_features is not None:
            features_list.append(categorical_features)

        if numerical_features is not None:
            features_list.append(numerical_features)

        if not features_list:
            raise ValueError("No features available for content-based filtering")

        # Concatenate all features
        combined_features = np.hstack(features_list)

        return combined_features

    def compute_similarity(self):
        """
        Compute content similarity matrix
        """
        self.similarity_matrix = cosine_similarity(self.content_features)
        return self.similarity_matrix

    def get_similar_content(self, content_id, n_similar=10):
        """
        Get similar content based on content features

        Args:
            content_id: Original content ID
            n_similar (int): Number of similar items to return

        Returns:
            list: List of (content_id, similarity_score) tuples
        """
        if content_id not in self.content_mapping:
            return []

        content_idx = self.content_mapping[content_id]
        similarities = self.similarity_matrix[content_idx]

        # Get top similar content (excluding itself)
        similar_indices = np.argsort(similarities)[::-1][1:n_similar+1]

        similar_content = []
        for idx in similar_indices:
            original_id = self.reverse_content_mapping[idx]
            similarity_score = similarities[idx]
            similar_content.append((original_id, similarity_score))

        return similar_content

    def recommend_content(self, user_profile, n_recommendations=10):
        """
        Recommend content based on user profile

        Args:
            user_profile (dict): User profile with:
                - liked_content: List of content IDs user liked
                - disliked_content: List of content IDs user disliked
                - preferred_genres: List of preferred genres (optional)
            n_recommendations (int): Number of recommendations to generate

        Returns:
            list: List of (content_id, recommendation_score) tuples
        """
        if not user_profile.get('liked_content'):
            return []

        # Calculate user preference vector
        user_vector = self._calculate_user_vector(user_profile)

        # Calculate similarity between user vector and all content
        content_scores = cosine_similarity([user_vector], self.content_features)[0]

        # Exclude content user has already seen
        seen_content = set(user_profile.get('liked_content', []) +
                          user_profile.get('disliked_content', []))
        seen_indices = [self.content_mapping[content_id] for content_id in
                        seen_content if content_id in self.content_mapping]

        # Set scores of seen content to -1
        content_scores[seen_indices] = -1

        # Get top recommendations
        top_indices = np.argsort(content_scores)[::-1][:n_recommendations]

        recommendations = []
        for idx in top_indices:
            if content_scores[idx] > 0:  # Only include positive scores
                original_id = self.reverse_content_mapping[idx]
                recommendations.append((original_id, content_scores[idx]))

        return recommendations

    def _calculate_user_vector(self, user_profile):
        """Calculate user preference vector based on liked content"""
        liked_content = user_profile.get('liked_content', [])
        disliked_content = user_profile.get('disliked_content', [])

        if not liked_content:
            return np.zeros(self.content_features.shape[1])

        # Get features for liked content
        liked_indices = [self.content_mapping[content_id] for content_id in
                        liked_content if content_id in self.content_mapping]

        if not liked_indices:
            return np.zeros(self.content_features.shape[1])

        liked_features = self.content_features[liked_indices]

        # Calculate average preference vector
        user_vector = np.mean(liked_features, axis=0)

        # Subtract disliked content if available
        if disliked_content:
            disliked_indices = [self.content_mapping[content_id] for content_id in
                               disliked_content if content_id in self.content_mapping]

            if disliked_indices:
                disliked_features = self.content_features[disliked_indices]
                user_vector -= 0.5 * np.mean(disliked_features, axis=0)

        return user_vector

    def explain_recommendation(self, content_id, user_profile):
        """
        Explain why content was recommended to a user

        Args:
            content_id: Recommended content ID
            user_profile (dict): User profile

        Returns:
            dict: Explanation with key features and similar liked content
        """
        if content_id not in self.content_mapping:
            return {}

        content_idx = self.content_mapping[content_id]
        content_vector = self.content_features[content_idx]

        # Find most similar liked content
        liked_content = user_profile.get('liked_content', [])
        if not liked_content:
            return {}

        liked_indices = [self.content_mapping[content_id] for content_id in
                        liked_content if content_id in self.content_mapping]

        if not liked_indices:
            return {}

        liked_features = self.content_features[liked_indices]
        similarities = cosine_similarity([content_vector], liked_features)[0]

        # Get most similar liked content
        most_similar_idx = np.argmax(similarities)
        most_similar_content_id = liked_content[most_similar_idx]
        similarity_score = similarities[most_similar_idx]

        return {
            'most_similar_liked': most_similar_content_id,
            'similarity_score': similarity_score,
            'explanation': f"Recommended because you liked {most_similar_content_id}"
        }


def example_usage():
    """
    Example of how to use the content-based recommender
    """
    # Sample content data
    content_data = {
        'content_id': [1, 2, 3, 4, 5],
        'title': ['The Matrix', 'Inception', 'Interstellar', 'The Dark Knight', 'Pulp Fiction'],
        'description': [
            'A computer hacker learns about the true nature of reality',
            'A thief who steals corporate secrets through dream-sharing technology',
            'A team of explorers travel through a wormhole in space',
            'Batman faces the Joker in Gotham City',
            'The lives of two mob hitmen become intertwined'
        ],
        'genres': [['Sci-Fi', 'Action'], ['Sci-Fi', 'Thriller'], ['Sci-Fi', 'Drama'],
                  ['Action', 'Crime'], ['Crime', 'Drama']],
        'year': [1999, 2010, 2014, 2008, 1994],
        'rating': [8.7, 8.8, 8.6, 9.0, 8.9]
    }

    df = pd.DataFrame(content_data)

    # Initialize and train the recommender
    recommender = ContentBasedRecommender(content_type='movies')
    recommender.prepare_content_data(df)
    recommender.compute_similarity()

    # Get similar content
    similar_movies = recommender.get_similar_content(content_id=1, n_similar=3)
    print("Movies similar to The Matrix:", similar_movies)

    # Recommend content for a user
    user_profile = {
        'liked_content': [1, 3],  # The Matrix, Interstellar
        'disliked_content': [],
        'preferred_genres': ['Sci-Fi']
    }

    recommendations = recommender.recommend_content(user_profile, n_recommendations=3)
    print("Recommendations for user:", recommendations)

    # Explain recommendation
    if recommendations:
        explanation = recommender.explain_recommendation(
            recommendations[0][0], user_profile)
        print("Explanation:", explanation)


if __name__ == "__main__":
    example_usage()

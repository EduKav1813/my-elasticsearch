class SearchEngine:

    def get_score(self, query: str, content: str) -> float:
        """Calculates a match score for the content and the given query.
        The score is calculated by adding the full-match score with a
        partial-match score, where the full-match has higher value.

        The full match is where a word from query is fully present in the
        content.
        The partial match is where a word from query is a part from the word
        from the content, but is not equal to it.

        Both arguments are normalized before the score calculation.

        The default score is 0

        Returns:
            float: Calculated score
        """

        query_words = query.lower().split()
        content_words = content.lower().split()
        score = 0

        # Full match
        query_words_set = set(query_words)
        content_words_set = set(content_words)
        full_match_score = len(query_words_set.intersection(content_words_set))

        # Partial match
        partial_match_score = 0
        for content_word in content_words_set:
            for query_word in query_words_set:
                if query_word in content_word and query_word != content_word:
                    partial_match_score += 0.5

        score = full_match_score + partial_match_score
        return score

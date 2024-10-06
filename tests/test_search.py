from my_elasticsearch.searchengine import SearchEngine


def test_match():
    """If a word from query is present in content, score should be positive."""
    engine = SearchEngine()
    query = "man"
    content = "i am a strong man"
    score = engine.get_score(query, content)
    assert score == 1


def test_mismatch():
    """If no word from query is present in content, score should be zero."""
    engine = SearchEngine()
    query = "rock"
    content = "i am a strong man"
    score = engine.get_score(query, content)
    assert score == 0


def test_convertion_lower():
    """Both query and content should be converted to common case before comparison."""
    engine = SearchEngine()
    query = "APPLE"
    content = "apple"
    score = engine.get_score(query, content)
    assert score == 1


def test_partial_match():
    """If even a part of word from query is present in content, score should be positive."""
    engine = SearchEngine()
    query = "apple"
    content = "pineapple"
    score = engine.get_score(query, content)
    assert score == 0.5


def test_match_multiple():
    """If many words match, score should be larger."""
    engine = SearchEngine()
    query = "travel the world"
    content = "i wish i could travel the world"
    score = engine.get_score(query, content)
    assert score == 3

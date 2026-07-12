from app.scorer import DODIAnalyzer

analyzer = DODIAnalyzer()

LICENCE_HEAVY = (
    "The Company grants you a limited, revocable, non-transferable license to "
    "access the service. Your subscription may be terminated at our sole "
    "discretion without notice. You waive any right to a class action or jury "
    "trial and agree to arbitration. We share your data with third parties, "
    "affiliates and partners for advertising and marketing."
)

OWNERSHIP_FRIENDLY = (
    "When you buy a game here, you own it. Your purchase is yours to keep. "
    "You can download what you buy at any point and you own your copy forever."
)


def test_deterministic():
    assert analyzer.analyze(LICENCE_HEAVY) == analyzer.analyze(LICENCE_HEAVY)


def test_licence_heavy_scores_higher():
    heavy = analyzer.analyze(LICENCE_HEAVY)["dodi_score"]
    friendly = analyzer.analyze(OWNERSHIP_FRIENDLY)["dodi_score"]
    assert heavy > friendly


def test_no_ownership_words_maxes_ratio_component():
    result = analyzer.analyze("You are granted a license to access the service.")
    assert result["details"]["ownership_count"] == 0
    assert result["components"]["licence_ratio"] == 100


def test_score_is_weighted_sum_of_components():
    r = analyzer.analyze(LICENCE_HEAVY)
    c = r["components"]
    expected = c["readability"] * 0.25 + c["licence_ratio"] * 0.50 + c["red_flags"] * 0.25
    # components are rounded to 1 decimal, so allow a small tolerance
    assert abs(r["dodi_score"] - expected) < 0.2


def test_score_bounds():
    for text in (LICENCE_HEAVY, OWNERSHIP_FRIENDLY, "word"):
        score = analyzer.analyze(text)["dodi_score"]
        assert 0 <= score <= 100

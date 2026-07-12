"""DODI scorer, vendored from the published analysis repo
(github.com/Axwolf13/dodi-analysis, scripts/dodi_analyzer_clean.py).

The scoring math is identical to the analysis behind the write-up at
axwolf13.github.io/writing/dodi/. This copy additionally returns the three
weighted component scores so the web UI can show the breakdown.

Weights: 25% readability | 50% licence ratio | 25% red flags.
Based on Perzanowski & Hoofnagle (2017).
"""
import textstat


class DODIAnalyzer:
    def __init__(self):
        # Ownership terminology (positive)
        self.ownership_words = ["buy", "purchase", "own", "acquire", "possess"]

        # Licence terminology (negative)
        self.license_words = ["license", "subscription", "access", "service", "grant", "rent"]

        # Red flags (aggressive clauses)
        self.red_flags = [
            # Ownership/termination
            "without notice", "sole discretion", "terminate", "revoke",
            "suspend", "non-transferable", "forfeit", "at any time",

            # Legal rights
            "class action", "waiver", "arbitration", "jury trial",
            "indemnify", "hold harmless", "limitation of liability",
            "as is", "no warranty", "jurisdiction",

            # Privacy/data
            "third party", "third parties", "affiliates", "advertising",
            "marketing", "track", "monitor", "location", "profile",
            "partners", "share your", "sell your", "opt-out", "opt out"
        ]

    def analyze(self, text):
        text_lower = text.lower()

        # --- Metric 1: licence/ownership ratio (50% weight) ---
        ownership_count = sum(text_lower.count(w) for w in self.ownership_words)
        license_count = sum(text_lower.count(w) for w in self.license_words)

        if ownership_count == 0:
            ratio = license_count  # infinite-ratio penalty
            ratio_score = 100
        else:
            ratio = license_count / ownership_count
            # Cap at 100 (ratio > 10 is max deception)
            ratio_score = min((ratio / 10) * 100, 100)

        # --- Metric 2: readability (25% weight) ---
        try:
            grade_level = textstat.flesch_kincaid_grade(text)
        except Exception:
            grade_level = 12  # fallback

        # Linear penalty: grade 8 = 0 pts, grade 16 = 100 pts
        if grade_level <= 8:
            readability_penalty = 0
        elif grade_level >= 16:
            readability_penalty = 100
        else:
            readability_penalty = ((grade_level - 8) / 8) * 100

        # --- Metric 3: red flags (25% weight) ---
        red_flag_count = sum(text_lower.count(phrase) for phrase in self.red_flags)
        # Cap at 50 flags for max score
        red_flag_score = min((red_flag_count / 50) * 100, 100)

        # --- Final weighted score (25/50/25) ---
        dodi_score = (readability_penalty * 0.25) + (ratio_score * 0.50) + (red_flag_score * 0.25)

        return {
            "dodi_score": round(dodi_score, 1),
            "components": {
                "readability": round(readability_penalty, 1),
                "licence_ratio": round(ratio_score, 1),
                "red_flags": round(red_flag_score, 1),
            },
            "details": {
                "ownership_count": ownership_count,
                "license_count": license_count,
                "ratio": round(ratio, 2),
                "grade_level": round(grade_level, 1),
                "red_flag_count": red_flag_count,
            },
        }

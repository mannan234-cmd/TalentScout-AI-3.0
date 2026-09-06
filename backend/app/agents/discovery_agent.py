"""
Discovery Agent — filters and categorizes new student submissions the
moment they arrive from the frontend portal. Categories deliberately span
both tech and non-tech fields, since TalentScout AI is built for every
student — Business, Design, Healthcare, Education, Law, etc. — not just
Computer Science.
"""
import re
from app.agents.base_agent import BaseAgent

CATEGORY_KEYWORDS = {
    "Software & AI": ["python", "developer", "software", "ai", "machine learning", "data science",
                       "programming", "computer science", "web development", "app development"],
    "Design & Creative Media": ["design", "ui", "ux", "figma", "graphic", "creative", "art",
                                "video editing", "photography", "animation", "fashion design",
                                "content writing", "journalism", "media production"],
    "Business & Management": ["business", "management", "marketing", "finance", "economics",
                               "commerce", "sales", "accounting", "human resources",
                               "entrepreneurship", "supply chain", "social media management"],
    "Engineering & Physical Sciences": ["physics", "engineering", "mechanical", "electrical",
                                        "mathematics", "civil engineering", "chemistry"],
    "Healthcare & Life Sciences": ["nursing", "medicine", "medical", "public health", "biology",
                                   "pharmacy", "nutrition", "clinical", "healthcare"],
    "Education & Social Sciences": ["teaching", "education", "psychology", "sociology",
                                    "social work", "counseling", "linguistics"],
    "Law & Public Policy": ["law", "legal", "paralegal", "public policy", "political science"],
    "Agriculture & Environment": ["agriculture", "environmental science", "farming", "sustainability"],
    "Hospitality & Culinary Arts": ["hospitality", "tourism", "culinary", "event management", "hotel management"],
    "General / Other": [],
}


def _keyword_present(keyword: str, haystack: str) -> bool:
    """Word-boundary match so short/generic keywords (e.g. 'art', 'ai')
    don't false-positive inside unrelated words (e.g. 'smart', 'said')."""
    pattern = r"(?<![a-z])" + re.escape(keyword) + r"(?![a-z])"
    return re.search(pattern, haystack) is not None


class DiscoveryAgent(BaseAgent):
    name = "discovery_agent"

    def run(self, student: dict) -> dict:
        """Categorize a new student submission. Returns patch dict."""
        haystack = " ".join([
            student.get("degree_program", ""),
            student.get("bio", ""),
            " ".join(student.get("skills", [])),
        ]).lower()

        category = "General / Other"
        best_hits = 0
        for cat, keywords in CATEGORY_KEYWORDS.items():
            hits = sum(1 for kw in keywords if _keyword_present(kw, haystack))
            if hits > best_hits:
                best_hits = hits
                category = cat

        self.log(f"Categorized student {student.get('id')} as '{category}'")
        return {"category": category, "status": "processing"}

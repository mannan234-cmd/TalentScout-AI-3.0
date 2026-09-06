"""
Demo AI provider: rule-based "signals extraction" and "cover letter
generation". No external API calls — this is what makes the whole platform
runnable with zero API keys, and it's also used as the automatic fallback
for GroqAIProvider if a live call fails.
"""
import re
from app.providers.base_provider import BaseAIProvider

# A cross-field skill vocabulary the keyword matcher looks for inside
# free-text evidence/bio. Deliberately spans BOTH tech and non-tech domains
# — this platform is built for every field, not just Computer Science, so
# a Business, Design, Media, Education, or Healthcare student's evidence
# gets recognized just as well as a developer's. Not exhaustive — just
# broad enough for a convincing cross-field demo.
SKILL_VOCAB = [
    # --- Software & Data ---
    "python", "javascript", "typescript", "react", "vue", "angular", "node.js",
    "node", "django", "flask", "fastapi", "sql", "postgresql", "mysql",
    "mongodb", "machine learning", "deep learning", "tensorflow", "pytorch",
    "data analysis", "pandas", "numpy", "excel", "power bi", "tableau",
    "aws", "azure", "gcp", "docker", "kubernetes", "git", "html", "css",
    "java", "c++", "c#", "go", "rust", "php", "swift", "kotlin",
    "figma", "ui/ux", "product management",

    # --- Business, Finance & Management ---
    "marketing", "digital marketing", "seo", "sales", "business development",
    "accounting", "finance", "financial modeling", "bookkeeping", "auditing",
    "human resources", "recruitment", "supply chain", "operations",
    "entrepreneurship", "business analysis", "market research",
    "customer service", "retail management", "negotiation",

    # --- Design, Media & Creative ---
    "graphic design", "video editing", "photography", "videography",
    "content writing", "copywriting", "social media management",
    "photoshop", "illustrator", "premiere pro", "animation",
    "fashion design", "interior design", "journalism", "blogging",

    # --- Education, Social Sciences & Humanities ---
    "teaching", "tutoring", "curriculum design", "psychology", "counseling",
    "sociology", "social work", "public policy", "translation",
    "public speaking", "debate", "academic research",

    # --- Healthcare & Life Sciences ---
    "nursing", "first aid", "patient care", "clinical research",
    "nutrition", "public health", "biology", "chemistry", "pharmacy",

    # --- Law, Agriculture & Other Fields ---
    "law", "paralegal", "legal research", "agriculture", "environmental science",
    "hospitality", "event management", "culinary arts", "tourism",

    # --- Cross-field soft skills (apply everywhere) ---
    "communication", "leadership", "research", "writing", "project management",
    "teamwork", "problem solving", "time management", "critical thinking",
]


def _find_keywords(text: str, vocab: list[str]) -> list[str]:
    text_l = text.lower()
    found = []
    for kw in vocab:
        if re.search(r"(?<![a-z])" + re.escape(kw) + r"(?![a-z])", text_l):
            found.append(kw)
    return found


class DemoAIProvider(BaseAIProvider):
    def extract_signals(self, student: dict, evidence_texts: list[str]) -> dict:
        claimed = [s.lower() for s in student.get("skills", [])]
        combined_text = " ".join([student.get("bio", "")] + evidence_texts)
        evidence_hits = _find_keywords(combined_text, SKILL_VOCAB)

        detected = {}
        # claimed skills start with solid confidence
        for s in claimed:
            detected[s] = max(detected.get(s, 0.0), 0.55)
        # skills backed by evidence text get a confidence boost (or are added new)
        for s in evidence_hits:
            base = 0.85 if s in detected else 0.65
            detected[s] = max(detected.get(s, 0.0), base)

        detected_skills = [
            {
                "skill": skill,
                "confidence": round(conf, 2),
                "evidence_snippet": _snippet_for(skill, combined_text),
            }
            for skill, conf in sorted(detected.items(), key=lambda kv: -kv[1])
        ]

        strengths = [d["skill"] for d in detected_skills if d["confidence"] >= 0.7][:5]
        gaps = []
        if len(detected_skills) < 3:
            gaps.append("Limited verifiable technical evidence — consider adding project links.")
        if not student.get("portfolio_url"):
            gaps.append("No portfolio/GitHub link provided.")
        if len(evidence_texts) == 0 or all(not t.strip() for t in evidence_texts):
            gaps.append("No supporting evidence submitted alongside the profile.")

        # Potential score: weighted blend of skill breadth, confidence, and evidence presence.
        breadth = min(len(detected_skills), 8) / 8 * 40          # up to 40 pts
        avg_conf = (sum(d["confidence"] for d in detected_skills) / len(detected_skills)) if detected_skills else 0
        conf_score = avg_conf * 35                                # up to 35 pts
        evidence_bonus = 15 if any(t.strip() for t in evidence_texts) else 0
        portfolio_bonus = 10 if student.get("portfolio_url") else 0
        potential_score = round(min(100.0, breadth + conf_score + evidence_bonus + portfolio_bonus), 1)

        summary = (
            f"{student.get('full_name', 'Candidate')} shows {len(detected_skills)} identifiable "
            f"skill signal(s) with an average confidence of {round(avg_conf * 100)}%. "
            + ("Strong supporting evidence was found in submitted materials. "
               if evidence_bonus else "Little to no supporting evidence text was provided. ")
            + ("A portfolio link strengthens verifiability." if portfolio_bonus
               else "No portfolio link was provided, which limits verifiability.")
        )

        return {
            "detected_skills": detected_skills,
            "strengths": strengths or claimed[:3],
            "gaps": gaps,
            "potential_score": potential_score,
            "summary": summary,
            "generated_by": "demo",
        }

    def generate_cover_letter(self, student: dict, opportunity: dict, match: dict) -> dict:
        name = student.get("full_name", "The candidate")
        org = opportunity.get("organization", "your organization")
        title = opportunity.get("title", "the role")
        matched = match.get("matched_skills", [])
        skills_line = ", ".join(matched[:5]) if matched else ", ".join(student.get("skills", [])[:5])

        cover_letter = (
            f"Dear Hiring Team at {org},\n\n"
            f"I am writing to express my interest in the {title} opportunity. "
            f"As a {student.get('degree_program', 'student')} at {student.get('university', 'my university')}, "
            f"I have developed hands-on strengths in {skills_line}, which align directly with what "
            f"you are looking for in this role.\n\n"
            f"{student.get('bio', '').strip() or 'I bring a strong work ethic and a demonstrated ability to learn quickly and apply new skills to real projects.'}\n\n"
            f"I would welcome the opportunity to discuss how my background can contribute to your team. "
            f"Thank you for your time and consideration.\n\n"
            f"Sincerely,\n{name}"
        )
        highlights = matched[:5] or student.get("skills", [])[:5]
        return {"cover_letter": cover_letter, "highlights": highlights, "generated_by": "demo"}


def _snippet_for(skill: str, text: str, window: int = 40) -> str:
    idx = text.lower().find(skill)
    if idx == -1:
        return ""
    start = max(0, idx - window)
    end = min(len(text), idx + len(skill) + window)
    return ("…" if start > 0 else "") + text[start:end].strip() + ("…" if end < len(text) else "")

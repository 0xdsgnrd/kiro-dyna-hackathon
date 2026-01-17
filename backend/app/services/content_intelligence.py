import re
from typing import List, Dict, Optional, Tuple
from collections import Counter
from sqlalchemy.orm import Session
from app.models.content import Content
from app.models.tag import Tag

class ContentIntelligenceService:
    """Service for content analysis, auto-tagging, and recommendations"""

    # Common stop words to filter out
    STOP_WORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need',
        'it', 'its', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
        'she', 'we', 'they', 'what', 'which', 'who', 'when', 'where', 'why',
        'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other',
        'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
        'than', 'too', 'very', 'just', 'about', 'into', 'through', 'during',
        'before', 'after', 'above', 'below', 'between', 'under', 'again',
        'further', 'then', 'once', 'here', 'there', 'any', 'new', 'also'
    }

    # Average reading speed (words per minute)
    WORDS_PER_MINUTE = 200

    def __init__(self, db: Session):
        self.db = db

    def analyze_content(self, content: Content) -> Dict:
        """Perform comprehensive analysis on a content item"""
        text = f"{content.title} {content.content_text or ''}"

        return {
            "suggested_tags": self.suggest_tags(text),
            "reading_time": self.calculate_reading_time(content.content_text),
            "quality_score": self.calculate_quality_score(content),
            "word_count": self._count_words(content.content_text)
        }

    def suggest_tags(self, text: str, max_tags: int = 5) -> List[Dict]:
        """Extract keyword suggestions for tags with confidence scores"""
        if not text:
            return []

        # Extract words and filter
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        words = [w for w in words if w not in self.STOP_WORDS]

        # Count word frequency
        word_counts = Counter(words)

        # Get existing tags for better suggestions
        existing_tags = {t.name.lower(): t.name for t in self.db.query(Tag).all()}

        suggestions = []
        for word, count in word_counts.most_common(max_tags * 2):
            # Prefer existing tags
            if word in existing_tags:
                confidence = min(0.9, 0.5 + (count * 0.1))
                suggestions.append({
                    "tag": existing_tags[word],
                    "confidence": round(confidence, 2),
                    "is_existing": True
                })
            elif count >= 2:  # Only suggest new tags if word appears multiple times
                confidence = min(0.7, 0.3 + (count * 0.1))
                suggestions.append({
                    "tag": word,
                    "confidence": round(confidence, 2),
                    "is_existing": False
                })

            if len(suggestions) >= max_tags:
                break

        return sorted(suggestions, key=lambda x: x["confidence"], reverse=True)

    def calculate_reading_time(self, text: Optional[str]) -> int:
        """Calculate estimated reading time in minutes"""
        if not text:
            return 0

        word_count = self._count_words(text)
        minutes = max(1, round(word_count / self.WORDS_PER_MINUTE))
        return minutes

    def calculate_quality_score(self, content: Content) -> int:
        """Calculate content quality score (0-100)"""
        score = 0

        # Title quality (0-25 points)
        if content.title:
            title_len = len(content.title)
            if 10 <= title_len <= 100:
                score += 25
            elif title_len > 5:
                score += 15
            else:
                score += 5

        # Content presence (0-25 points)
        if content.content_text:
            text_len = len(content.content_text)
            if text_len > 500:
                score += 25
            elif text_len > 200:
                score += 20
            elif text_len > 50:
                score += 10
            else:
                score += 5

        # URL presence (0-15 points)
        if content.url:
            score += 15

        # Tags (0-20 points)
        tag_count = len(content.tags)
        score += min(20, tag_count * 5)

        # Category (0-15 points)
        if content.category_id:
            score += 15

        return min(100, score)

    def find_related_content(self, content: Content, limit: int = 5) -> List[Tuple[Content, float]]:
        """Find related content based on tags and title similarity"""
        if not content.tags:
            return []

        tag_ids = [t.id for t in content.tags]

        # Find content with overlapping tags
        from sqlalchemy import func
        from app.models.tag import content_tags

        related = self.db.query(
            Content,
            func.count(content_tags.c.tag_id).label('match_count')
        ).join(
            content_tags, Content.id == content_tags.c.content_id
        ).filter(
            content_tags.c.tag_id.in_(tag_ids),
            Content.id != content.id,
            Content.user_id == content.user_id
        ).group_by(Content.id).order_by(
            func.count(content_tags.c.tag_id).desc()
        ).limit(limit).all()

        # Calculate similarity score
        results = []
        for item, match_count in related:
            similarity = match_count / max(len(tag_ids), 1)
            results.append((item, round(similarity, 2)))

        return results

    def batch_analyze(self, user_id: int, limit: int = 100) -> Dict:
        """Analyze multiple content items for a user"""
        contents = self.db.query(Content).filter(
            Content.user_id == user_id
        ).limit(limit).all()

        results = {
            "analyzed": 0,
            "suggestions": []
        }

        for content in contents:
            analysis = self.analyze_content(content)

            # Update content with analysis results
            content.reading_time = analysis["reading_time"]
            content.quality_score = analysis["quality_score"]

            results["analyzed"] += 1
            if analysis["suggested_tags"]:
                results["suggestions"].append({
                    "content_id": content.id,
                    "title": content.title,
                    "suggested_tags": analysis["suggested_tags"]
                })

        self.db.commit()
        return results

    def _count_words(self, text: Optional[str]) -> int:
        """Count words in text"""
        if not text:
            return 0
        return len(re.findall(r'\b\w+\b', text))

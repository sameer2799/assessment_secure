from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
import json

db = SQLAlchemy()

class CVE(db.Model):
    __tablename__ = 'cves'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cve_id = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    published_date = Column(DateTime)
    last_modified_date = Column(DateTime)
    cvss_v2_score = Column(Float)
    cvss_v3_score = Column(Float)
    raw_data = Column(Text)  # Store full JSON for future reference

    def __init__(self, cve_data):
        self.cve_id = cve_data.get('id', '')
        self.description = self._extract_description(cve_data)
        self.published_date = self._parse_date(cve_data.get('published'))
        self.last_modified_date = self._parse_date(cve_data.get('lastModified'))
        self.cvss_v2_score = self._extract_cvss_score(cve_data, 'V2')
        self.cvss_v3_score = self._extract_cvss_score(cve_data, 'V3')
        self.raw_data = json.dumps(cve_data)

    def _extract_description(self, cve_data):
        descriptions = cve_data.get('descriptions', [])
        for desc in descriptions:
            if desc.get('lang') == 'en':
                return desc.get('value', '')
        return ''

    def _parse_date(self, date_str):
        if date_str:
            try:
                return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            except:
                return None
        return None

    def _extract_cvss_score(self, cve_data, version):
        metrics = cve_data.get('metrics', {})
        cvss_key = f'cvssMetric{version}'
        if cvss_key in metrics and metrics[cvss_key]:
            return metrics[cvss_key][0].get('cvssData', {}).get('baseScore')
        return None

    def to_dict(self):
        return {
            'cve_id': self.cve_id,
            'description': self.description,
            'published_date': self.published_date.isoformat() if self.published_date else None,
            'last_modified_date': self.last_modified_date.isoformat() if self.last_modified_date else None,
            'cvss_v2_score': self.cvss_v2_score,
            'cvss_v3_score': self.cvss_v3_score
        }

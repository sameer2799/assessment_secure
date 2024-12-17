import requests
import logging
from datetime import datetime, timedelta
from database import db, CVE
from flask import Flask
from sqlalchemy.exc import IntegrityError

class CVESync:
    BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    
    def __init__(self, app=None):
        self.app = app or Flask(__name__)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def sync_cves(self, start_index=0, results_per_page=2000, max_pages=5):
        with self.app.app_context():
            for page in range(max_pages):
                try:
                    params = {
                        'startIndex': start_index + (page * results_per_page),
                        'resultsPerPage': results_per_page
                    }
                    response = requests.get(self.BASE_URL, params=params)
                    
                    if response.status_code != 200:
                        self.logger.error(f"Failed to fetch CVEs: {response.status_code}")
                        break

                    data = response.json()
                    vulnerabilities = data.get('vulnerabilities', [])

                    if not vulnerabilities:
                        break

                    self._process_vulnerabilities(vulnerabilities)

                except Exception as e:
                    self.logger.error(f"Error during CVE sync: {e}")
                    break

    def _process_vulnerabilities(self, vulnerabilities):
        for vuln in vulnerabilities:
            try:
                cve_data = vuln.get('cve', {})
                new_cve = CVE(cve_data)
                
                # Check if CVE already exists
                existing_cve = CVE.query.filter_by(cve_id=new_cve.cve_id).first()
                
                if not existing_cve:
                    db.session.add(new_cve)
                else:
                    # Update existing record if modified
                    if existing_cve.last_modified_date != new_cve.last_modified_date:
                        existing_cve.description = new_cve.description
                        existing_cve.last_modified_date = new_cve.last_modified_date
                        existing_cve.cvss_v2_score = new_cve.cvss_v2_score
                        existing_cve.cvss_v3_score = new_cve.cvss_v3_score
                        existing_cve.raw_data = new_cve.raw_data

                db.session.commit()
            except IntegrityError:
                db.session.rollback()
            except Exception as e:
                self.logger.error(f"Error processing CVE {new_cve.cve_id}: {e}")
                db.session.rollback()

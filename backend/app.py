from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import desc
from database import db, CVE
from cve_sync import CVESync
from datetime import datetime, timedelta
import os

app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cves.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/details/<cve_id>')
def details(cve_id):
    return render_template('details.html')

@app.route('/cves/list')
def list_cves():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Optional filtering parameters
    year = request.args.get('year')
    min_score = request.args.get('min_score', type=float)
    last_modified_days = request.args.get('last_modified_days', type=int)

    query = CVE.query

    if year:
        query = query.filter(CVE.cve_id.like(f'CVE-{year}%'))
    
    if min_score is not None:
        query = query.filter((CVE.cvss_v2_score >= min_score) | (CVE.cvss_v3_score >= min_score))
    
    if last_modified_days is not None:
        threshold_date = datetime.now() - timedelta(days=last_modified_days)
        query = query.filter(CVE.last_modified_date >= threshold_date)
    
    # Sorting
    query = query.order_by(desc(CVE.last_modified_date))
    
    # Pagination
    paginated_cves = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'cves': [cve.to_dict() for cve in paginated_cves.items],
        'total_records': paginated_cves.total,
        'pages': paginated_cves.pages,
        'current_page': page
    })

@app.route('/cves/<cve_id>')
def get_cve_details(cve_id):
    cve = CVE.query.filter_by(cve_id=cve_id).first()
    if cve:
        return jsonify(cve.to_dict())
    return jsonify({'error': 'CVE not found'}), 404

@app.route('/sync-cves', methods=['POST'])
def trigger_cve_sync():
    sync = CVESync(app)
    sync.sync_cves(results_per_page=100)
    return jsonify({'message': 'CVE sync completed'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        CORS(app)
    app.run(debug=True)

# CVE Tracker: NVD Vulnerability Database Browser

## Project Overview
This application retrieves, stores, and visualizes Common Vulnerabilities and Exposures (CVEs) from the National Vulnerability Database (NVD) using their public API.

## Features
- Retrieve CVE data from NVD API
- Store CVEs in a local SQLite database
- Pagination of CVE listings
- Filtering by:
  - Year
  - CVSS Score
- Detailed CVE information page
- Periodic data synchronization

## Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/nvd-cve-tracker.git
cd nvd-cve-tracker
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate.bat
```

### 3. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 4. Initialize Database
```bash
python backend/app.py
```
This will create the SQLite database file.

## Running the Application
```bash
python backend/app.py
```
Open a web browser and navigate to `http://localhost:5000`

## Synchronizing CVE Data
You can manually trigger CVE synchronization by:
1. Programmatically via `/sync-cves` endpoint
2. Setting up a scheduled task/cron job

## API Endpoints
- `GET /cves/list`: Retrieve paginated CVE list
  - Query Parameters:
    - `page`: Page number
    - `per_page`: Results per page
    - `year`: Filter by CVE year
    - `min_score`: Minimum CVSS score
- `GET /cves/<cve_id>`: Get specific CVE details
- `POST /sync-cves`: Trigger CVE data synchronization

## Environment Variables
Create a `.env` file in the backend directory for configuration:
```
FLASK_ENV=development
DATABASE_URL=sqlite:///cves.db
NVD_API_BASE_URL=https://services.nvd.nist.gov/rest/json/cves/2.0
```

## Testing
```bash
python -m unittest discover tests
```

## Security Considerations
- Regularly update dependencies
- Use environment-specific configurations
- Implement proper error handling

## Performance Optimization
- Indexing database columns
- Caching mechanism for frequently accessed data
- Asynchronous data synchronization


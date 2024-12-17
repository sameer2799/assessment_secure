document.addEventListener('DOMContentLoaded', () => {
    const tableBody = document.getElementById('cveTableBody');
    const prevButton = document.getElementById('prevPage');
    const nextButton = document.getElementById('nextPage');
    const pageInfo = document.getElementById('pageInfo');
    const resultsPerPageSelect = document.getElementById('resultsPerPage');
    const yearFilter = document.getElementById('yearFilter');
    const scoreFilter = document.getElementById('scoreFilter');

    let currentPage = 1;
    let totalPages = 1;

    function fetchCVEs(page = 1, perPage = 10) {
        const params = new URLSearchParams({
            page: page,
            per_page: perPage,
            year: yearFilter.value || '',
            min_score: scoreFilter.value || ''
        });

        fetch(`http://localhost:5000/cves/list?${params}`)
            .then(response => response.json())
            .then(data => {
                tableBody.innerHTML = '';
                data.cves.forEach(cve => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td><a href="/cves/${cve.cve_id}">${cve.cve_id}</a></td>
                        <td>${cve.description}</td>
                        <td>${new Date(cve.published_date).toLocaleDateString()}</td>
                        <td>${new Date(cve.last_modified_date).toLocaleDateString()}</td>
                        <td>${cve.cvss_v3_score || cve.cvss_v2_score || 'N/A'}</td>
                    `;
                    row.addEventListener('click', () => {
                        window.location.href = `/cves/${cve.cve_id}`;
                    });
                    tableBody.appendChild(row);
                });

                currentPage = data.current_page;
                totalPages = data.pages;
                updatePaginationControls();
            });
    }

    function updatePaginationControls() {
        prevButton.disabled = currentPage === 1;
        nextButton.disabled = currentPage === totalPages;
        pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
    }

    prevButton.addEventListener('click', () => {
        if (currentPage > 1) {
            fetchCVEs(currentPage - 1, resultsPerPageSelect.value);
        }
    });

    nextButton.addEventListener('click', () => {
        if (currentPage < totalPages) {
            fetchCVEs(currentPage + 1, resultsPerPageSelect.value);
        }
    });

    resultsPerPageSelect.addEventListener('change', () => {
        fetchCVEs(1, resultsPerPageSelect.value);
    });

    yearFilter.addEventListener('change', () => {
        fetchCVEs(1, resultsPerPageSelect.value);
    });

    scoreFilter.addEventListener('change', () => {
        fetchCVEs(1, resultsPerPageSelect.value);
    });

    // Initial load
    fetchCVEs();
});

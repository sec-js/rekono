import logging
from urllib.parse import urlparse

import requests
from findings.enums import Severity
from requests.adapters import HTTPAdapter, Retry

# Mapping between severity values and CVSS values
CVSS_RANGES = {
    Severity.CRITICAL: (9, 10),
    Severity.HIGH: (7, 9),
    Severity.MEDIUM: (4, 7),
    Severity.LOW: (2, 4),
    Severity.INFO: (0, 2)
}

logger = logging.getLogger()                                                    # Rekono logger


class NvdNist:
    '''NVD NIST API handler to get information for a CVE code.'''

    api_url_pattern = 'https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve}'   # API Rest URL
    cve_reference_pattern = 'https://nvd.nist.gov/vuln/detail/{cve}'            # CVE reference format

    def __init__(self, cve: str) -> None:
        '''NVE NIST API constructor.

        Args:
            cve (str): CVE code
        '''
        self.cve = cve
        self.reference = self.cve_reference_pattern.format(cve=cve)             # CVE reference
        self.raw_cve_info = self.request()                                      # CVE raw information
        self.description = self.parse_description() if self.raw_cve_info else ''    # CVE description
        self.cwe = self.parse_cwe() if self.raw_cve_info else None              # CVE weakness as CWE code
        # CVE severity based on CVSS score
        self.severity = self.parse_severity() if self.raw_cve_info else Severity.MEDIUM

    def request(self) -> dict:
        '''Get information from a CVE using the NVD NIST API Rest.

        Returns:
            dict: Raw NVD NIST CVE information
        '''
        schema = urlparse(self.api_url_pattern).scheme                          # Get API schema
        session = requests.Session()                                            # Create HTTP session
        # Configure retry protocol to prevent unexpected errors
        # Free NVD NIST API has a rate limit of 10 requests by second
        retries = Retry(total=10, backoff_factor=1, status_forcelist=[403, 500, 502, 503, 504, 599])
        session.mount(f'{schema}://', HTTPAdapter(max_retries=retries))
        try:
            response = session.get(self.api_url_pattern.format(cve=self.cve))
        except requests.exceptions.ConnectionError:
            response = session.get(self.api_url_pattern.format(cve=self.cve))
        logger.info(f'[NVD NIST] GET {self.cve} > HTTP {response.status_code}')
        return response.json().get("vulnerabilities")[0].get("cve", {}) if response.status_code == 200 else {}

    def parse_description(self) -> str:
        '''Get description from raw CVE information.

        Returns:
            str: CVE description
        '''
        for d in self.raw_cve_info.get("descriptions", []) or []:
            if d.get('lang') == 'en':
                return d.get('value')
        return ''

    def parse_cwe(self) -> str:
        '''Get CWE from raw CVE information.

        Returns:
            str: CWE code
        '''
        for item in self.raw_cve_info.get("weaknesses", []) or []:
            if item.get("type") != "Primary":
                continue
            for desc in item.get("description") or []:
                if desc.get('value', '').lower().startswith('cwe-'):
                    return desc.get('value')
        return ''

    def parse_severity(self) -> str:
        '''Get severity value from raw CVE information, based on CVSS score.

        Returns:
            Optional[str]: Severity value
        '''
        score = 5                                                               # Score by default: MEDIUM
        score_assigned = False
        cvss_metrics = self.raw_cve_info.get("metrics", {}) or {}
        for field in [
            "cvssMetricV31",
            "cvssMetricV30",
            "cvssMetricV3",
            "cvssMetricV2",
        ]:
            for cvss in cvss_metrics.get(field) or sum(
                [
                    list(items)
                    for key, items in cvss_metrics.items()
                    if key.lower().startswith(field)
                ],
                []
            ):
                if cvss.get("type") == "Primary":
                    base_score = cvss.get("cvssData", {}).get("baseScore")
                    if base_score:
                        score = base_score
                        score_assigned = True
                        break
            if score_assigned:
                break
        for severity in CVSS_RANGES.keys():
            down, up = CVSS_RANGES[severity]
            # Search severity value based on CVSS ranges
            if (score >= down and score < up) or (severity == Severity.CRITICAL and score >= down and score <= up):
                return severity
        return Severity.MEDIUM

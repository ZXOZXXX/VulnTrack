
def linear_search_vulnerability(vulnerabilities, target_id):
    """
    Find a vulnerability by ID using Linear Search.

    Returns the matching record if found, otherwise None.
    """

    target_id = target_id.strip().casefold()

    for vulnerability in vulnerabilities:
        current_id = vulnerability["vuln_id"].strip().casefold()

        if current_id == target_id:
            return vulnerability

    return None

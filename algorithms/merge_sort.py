
def merge_sort_vulnerabilities(vulnerabilities, descending=True):
    """
    Sort vulnerability records by risk_score.

    descending=True: highest risk first.
    descending=False: lowest risk first.

    Returns a new list without modifying the original list.
    """

    if len(vulnerabilities) <= 1:
        return vulnerabilities.copy()

    middle = len(vulnerabilities) // 2

    left = merge_sort_vulnerabilities(
        vulnerabilities[:middle], descending
    )
    right = merge_sort_vulnerabilities(
        vulnerabilities[middle:], descending
    )

    return merge(left, right, descending)


def merge(left, right, descending=True):
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if descending:
            take_left = (
                left[i]["risk_score"] >= right[j]["risk_score"]
            )
        else:
            take_left = (
                left[i]["risk_score"] <= right[j]["risk_score"]
            )

        if take_left:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result

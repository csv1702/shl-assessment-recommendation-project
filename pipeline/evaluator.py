def recall_at_k(retrieved_urls, relevant_urls, k=10):
    retrieved_k = retrieved_urls[:k]

    retrieved_set = set(retrieved_k)
    relevant_set = set(relevant_urls)

    if len(relevant_set) == 0:
        return 0.0

    hits = retrieved_set.intersection(relevant_set)
    return len(hits) / len(relevant_set)


def mean_recall_at_k(results, k=10):
    """
    results: list of tuples (retrieved_urls, relevant_urls)
    """
    scores = [
        recall_at_k(retrieved, relevant, k)
        for retrieved, relevant in results
    ]

    return sum(scores) / len(scores)

from config.settings import SIMILARITY_THRESHOLD


def passes_grounding_threshold(
    similarity_score: float,
) -> bool:

    print(
        f"Threshold Loaded = {SIMILARITY_THRESHOLD}"
    )

    return similarity_score <= SIMILARITY_THRESHOLD
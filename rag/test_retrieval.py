from rag.pipeline import (
    PolicyRAGPipeline,
)


def main():

    pipeline = (
        PolicyRAGPipeline()
    )

    results = pipeline.retrieve(
        query=(
            "What are the eligibility requirements "
            "for a customer applying for a loan?"
        ),
        top_k=5
    )

    for index, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\n{'=' * 70}"
        )

        print(
            f"Rank: {index}"
        )

        print(
            f"Score: {result.score:.4f}"
        )

        print(
            f"Source: "
            f"{result.metadata.get('source')}"
        )

        print(
            f"Page: "
            f"{result.metadata.get('page')}"
        )

        print(
            result.text
        )


if __name__ == "__main__":

    main()
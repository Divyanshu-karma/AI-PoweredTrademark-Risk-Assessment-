from src.rag.generate_answer import generate_rag_answer


def main():
    print("=== AI Trademark Risk Assessment ===\n")

    query = (
     "Trademark: TEAR, POUR, LIVE MORE\n"
    "Applicant: Kraft Foods Group Brands LLC\n"
    "Entity Type: Limited Liability Company\n"
    "Citizenship/State: Delaware\n"
    "Dates: Filed: 2016-06-21\n"
    "Question: Are the applicant's entity and citizenship details sufficient?"
    )

    answer = generate_rag_answer(
        query=query,
        top_k=3
    )

    print("RAG Answer:\n")
    print(answer)


if __name__ == "__main__":
    main()

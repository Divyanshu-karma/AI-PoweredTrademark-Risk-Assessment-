# import json
# from pathlib import Path
# from .weaviate_client import get_client, create_schema, CLASS_NAME


# def load_embeddings(embeddings_path: Path) -> None:
#     client = get_client()

#     try:
#         create_schema(client)
#         collection = client.collections.get(CLASS_NAME)

#         data = json.loads(embeddings_path.read_text(encoding="utf-8"))

#         print(f"⏳ Ingesting {len(data)} chunks into Weaviate Cloud...")

#         # v4 batch API
#         with collection.batch.dynamic() as batch:
#             for item in data:
#                 batch.add_object(
#                     properties={
#                         "text": item["text"],
#                         "section_id": item["metadata"]["section_id"],
#                         "section_title": item["metadata"]["section_title"],
#                         "section_path": item["metadata"]["section_path"],
#                         "doc_version": item["metadata"]["doc_version"],
#                         "chunk_index": item["metadata"]["chunk_index"],
#                     },
#                     vector=item["embedding"],
#                 )

#         print("✅ All chunks ingested successfully")

#     finally:
#         client.close()


import json
from pathlib import Path

from .weaviate_client import get_client, create_schema, CLASS_NAME


EMBEDDINGS_PATH = Path("data/embeddings/tmep_e5_embeddings.json")


def load_embeddings(embeddings_path: Path) -> None:
    if not embeddings_path.exists():
        raise FileNotFoundError(
            f"Embeddings file not found: {embeddings_path}"
        )

    client = get_client()

    try:
        create_schema(client)
        collection = client.collections.get(CLASS_NAME)

        data = json.loads(
            embeddings_path.read_text(encoding="utf-8")
        )

        print(f"⏳ Ingesting {len(data)} chunks into Weaviate...")

        with collection.batch.dynamic() as batch:
            for item in data:
                batch.add_object(
                    properties={
                        "chunk_id": item["chunk_id"],   # ✅ store as property
                        "text": item["text"],
                        "section_id": item["section_id"],
                        "section_path": item["section_path"],
                        "source_file": item.get("source_file"),
                        "doc_version": item["doc_version"],
                        "source": item["source"],
                    },
                    vector=item["embedding"],
                )


        print("✅ All chunks ingested successfully")

    finally:
        client.close()


# ✅ THIS WAS MISSING
def main():
    load_embeddings(EMBEDDINGS_PATH)


if __name__ == "__main__":
    main()

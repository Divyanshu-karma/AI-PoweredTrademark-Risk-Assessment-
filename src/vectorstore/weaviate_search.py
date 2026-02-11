# from typing import List, Dict
# from .weaviate_client import get_client, CLASS_NAME
# from src.embeddings.query_embedding import embed_query


# def similarity_search(query: str, top_k: int = 5) -> List[Dict]:
#     client = get_client()

#     try:
#         collection = client.collections.get(CLASS_NAME)
#         query_vector = embed_query(query)

#         response = collection.query.near_vector(
#             near_vector=query_vector,
#             limit=top_k,
#             return_metadata=["distance"]
#         )

#         results = []
#         for obj in response.objects:
#             results.append({
#                 "text": obj.properties["text"],
#                 "section_id": obj.properties["section_id"],
#                 "section_title": obj.properties["section_title"],
#                 "section_path": obj.properties["section_path"],
#                 "doc_version": obj.properties["doc_version"],
#                 "chunk_index": obj.properties["chunk_index"],
#                 "distance": obj.metadata.distance,
#             })

#         return results

#     finally:
#         client.close()


from typing import List, Dict
from .weaviate_client import get_client, CLASS_NAME
from src.embeddings.query_embedding import embed_query


def similarity_search(query: str, top_k: int = 5) -> List[Dict]:
    client = get_client()

    try:
        collection = client.collections.get(CLASS_NAME)
        query_vector = embed_query(query)

        response = collection.query.near_vector(
            near_vector=query_vector,
            limit=top_k,
            return_metadata=["distance"]
        )

        results = []
        for obj in response.objects:
            results.append({
                "text": obj.properties["text"],
                "section_id": obj.properties["section_id"],
                "section_path": obj.properties["section_path"],
                "source_file": obj.properties.get("source_file"),
                "doc_version": obj.properties["doc_version"],
                "source": obj.properties["source"],
                "distance": obj.metadata.distance,
            })

        return results

    finally:
        client.close()

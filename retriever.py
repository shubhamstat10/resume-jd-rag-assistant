from query_router import route_query


def retrieve(query, vector_store, k=5):

    route = route_query(query)

    if route == "out_of_scope":
        return [], route

    elif route == "resume":

        search_query = query

        # Improve retrieval for project-related questions
        if "project" in query.lower():

            search_query = (
                "projects project names project titles "
                "project experience key projects "
                + query
            )

            results = vector_store.similarity_search(
                search_query,
                k=15,
                filter={"document_type": "resume"}
            )

        else:

            results = vector_store.similarity_search(
                search_query,
                k=5,
                filter={"document_type": "resume"}
            )

    elif route == "jd":

        results = vector_store.similarity_search(
            query,
            k=k,
            filter={"document_type": "job_description"}
        )

    else:

        # Both resume + JD

        # First retrieve relevant chunks from both documents
        resume_results = vector_store.similarity_search(
            query,
            k=10,
            filter={"document_type": "resume"}
        )

        jd_results = vector_store.similarity_search(
            query,
            k=10,
            filter={"document_type": "job_description"}
        )

        # Find the sections that were retrieved
        resume_sections = set(
            result.metadata.get("section")
            for result in resume_results
        )

        jd_sections = set(
            result.metadata.get("section")
            for result in jd_results
        )

        # Retrieve more information from those sections
        for section in resume_sections:

            if section:
                section_results = vector_store.similarity_search(
                    query,
                    k=5,
                    filter={
                        "document_type": "resume",
                        "section": section
                    }
                )

                resume_results.extend(section_results)

        for section in jd_sections:

            if section:
                section_results = vector_store.similarity_search(
                    query,
                    k=5,
                    filter={
                        "document_type": "job_description",
                        "section": section
                    }
                )

                jd_results.extend(section_results)

        # Remove duplicate chunks
        results = []
        seen = set()

        for result in resume_results + jd_results:

            key = (
                result.metadata.get("document_type"),
                result.metadata.get("section"),
                result.page_content
            )

            if key not in seen:
                seen.add(key)
                results.append(result)

    print("\nROUTE:", route)

    for result in results:
        print(
            "\nSECTION:",
            result.metadata.get("section"),
            "\nTEXT:",
            result.page_content[:500]
        )

    return results, route
import streamlit as st
import ollama


# =================================================
# CREATE LOCAL LLM GENERATOR
# =================================================

@st.cache_resource
def create_generator():

    return "llama3.2:1b"


# =================================================
# REWRITE FOLLOW-UP QUESTION
# =================================================

def rewrite_question(
    generator,
    question,
    chat_history
):

    if not chat_history:

        return question


    history_text = "\n".join(
        f"{message['role']}: {message['content']}"
        for message in chat_history[-6:]
    )


    prompt = f"""
You are a question rewriting assistant.

Rewrite the user's latest question into a standalone question
that can be understood without the previous conversation.

Use the conversation history to resolve references such as:
- it
- they
- this
- that
- the model
- the dataset
- the research
- the paper

Do not answer the question.
Only return the rewritten question.

Conversation history:

{history_text}

Latest question:

{question}

Standalone question:
"""


    response = ollama.generate(
        model=generator,
        prompt=prompt,
        options={
            "temperature": 0.1,
            "num_predict": 100
        }
    )


    return response["response"].strip()


# =================================================
# GENERATE ANSWER
# =================================================

def generate_answer(
    generator,
    question,
    documents
):

    if not documents:

        return (
            "I could not find relevant information "
            "in the uploaded research paper."
        )


    context_parts = []


    for document in documents:

        page_number = document.metadata.get(
            "page",
            "Unknown"
        )


        context_parts.append(
            f"[Page {page_number}]\n"
            f"{document.page_content}"
        )


    context = "\n\n".join(
        context_parts
    )


    prompt = f"""
You are ResearchMate, an AI assistant that answers
questions about research papers.

Use ONLY the provided context from the uploaded
research paper.

IMPORTANT:
- Answer the user's question directly.
- Use information from the provided context.
- Combine information from multiple pages when necessary.
- Do not invent facts.
- If the context does not contain enough information,
  clearly say so.
- Give a clear and concise answer in 2-5 sentences.
- Do not mention that you are an AI.
- Do not include page numbers in your answer because
  the application displays sources separately.

Context from the research paper:

{context}

Question:

{question}

Answer:
"""


    response = ollama.generate(
        model=generator,
        prompt=prompt,
        options={
            "temperature": 0.2,
            "num_predict": 200
        }
    )


    return response["response"].strip()


# =================================================
# GENERATE FULL RESEARCH PAPER SUMMARY
# =================================================

def generate_full_summary(
    generator,
    chunks
):

    if not chunks:

        return (
            "I could not find enough information "
            "to summarize the uploaded research paper."
        )


    # -------------------------------------------------
    # Prepare document text
    # -------------------------------------------------

    text_parts = []

    for chunk in chunks:

        page_number = chunk.get(
            "page_number",
            "Unknown"
        )

        text = chunk.get(
            "text",
            ""
        )

        if text:

            text_parts.append(
                f"[Page {page_number}]\n{text}"
            )


    # -------------------------------------------------
    # Create batches
    # -------------------------------------------------

    batch_size = 5

    batches = []

    for i in range(
        0,
        len(text_parts),
        batch_size
    ):

        batch = text_parts[
            i:i + batch_size
        ]

        batches.append(
            "\n\n".join(batch)
        )


    # -------------------------------------------------
    # Summarize each batch
    # -------------------------------------------------

    batch_summaries = []


    for i, batch in enumerate(
        batches
    ):

        prompt = f"""
You are ResearchMate, an AI research paper assistant.

Summarize the following section of a research paper.

Use ONLY the information provided.

IMPORTANT:
- Do not invent facts.
- Preserve exact numerical results when available.
- Preserve dataset sizes and experimental details accurately.
- If the text contains conflicting information, do not resolve
  the conflict by guessing.
- Mention important limitations.
- Keep the summary concise.
- Focus on important research information.

Research paper section:

{batch}

Section summary:
"""


        response = ollama.generate(
            model=generator,
            prompt=prompt,
            options={
                "temperature": 0.1,
                "num_predict": 300
            }
        )


        batch_summaries.append(
            response["response"].strip()
        )


    # -------------------------------------------------
    # Combine batch summaries
    # -------------------------------------------------

    combined_summary = "\n\n".join(
        batch_summaries
    )


    # -------------------------------------------------
    # Generate Final Summary
    # -------------------------------------------------

    final_prompt = f"""
You are ResearchMate, an AI research paper assistant.

Create a final structured summary of the research paper
using ONLY the section summaries provided below.

The final summary must contain:

1. Research Objective
2. Proposed Methodology
3. Dataset and Experimental Setup
4. Main Results
5. Key Findings
6. Limitations
7. Conclusion

IMPORTANT:
- Use ONLY the provided section summaries.
- Do not invent facts.
- Preserve numerical values exactly as provided.
- Do not combine conflicting numbers into a new number.
- If different sections report different values, clearly state
  that the reported values are inconsistent.
- Do not assume missing information.
- Keep the summary concise but informative.
- Use clear headings.
- Use bullet points where appropriate.
- Do not include page numbers.

Section summaries:

{combined_summary}

Final Research Paper Summary:
"""


    response = ollama.generate(
        model=generator,
        prompt=final_prompt,
        options={
            "temperature": 0.1,
            "num_predict": 700
        }
    )


    return response["response"].strip()


"""
Echo — Text Utilities
Chunking, cleaning, and text processing for document ingestion.
"""

from __future__ import annotations

import re
from typing import List

import tiktoken


def count_tokens(text: str, model: str = "cl100k_base") -> int:
    """Count the number of tokens in a text string."""
    try:
        encoding = tiktoken.get_encoding(model)
    except Exception:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def clean_text(text: str) -> str:
    """Clean extracted text by removing artifacts and normalizing whitespace."""
    # Remove null bytes
    text = text.replace("\x00", "")
    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Remove excessive blank lines (more than 2 consecutive)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Remove excessive spaces
    text = re.sub(r"[ \t]{3,}", "  ", text)
    # Remove control characters except newline and tab
    text = re.sub(r"[\x01-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    return text.strip()


def chunk_text(
    text: str,
    chunk_size: int = 512,
    chunk_overlap: int = 64,
    separator: str = "\n\n",
) -> List[str]:
    """Split text into overlapping chunks based on token count.

    Uses paragraph boundaries as preferred split points, falling back
    to sentence boundaries, then word boundaries.

    Args:
        text: The input text to chunk.
        chunk_size: Target size in tokens for each chunk.
        chunk_overlap: Number of overlapping tokens between chunks.
        separator: Primary separator for splitting.

    Returns:
        List of text chunks.
    """
    if not text.strip():
        return []

    # Split by paragraphs first
    paragraphs = text.split(separator)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    chunks: List[str] = []
    current_chunk: List[str] = []
    current_tokens = 0

    for paragraph in paragraphs:
        paragraph_tokens = count_tokens(paragraph)

        # If a single paragraph exceeds chunk_size, split it further
        if paragraph_tokens > chunk_size:
            # Flush current chunk
            if current_chunk:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = []
                current_tokens = 0

            # Split the long paragraph by sentences
            sub_chunks = _split_long_text(paragraph, chunk_size, chunk_overlap)
            chunks.extend(sub_chunks)
            continue

        # Check if adding this paragraph would exceed chunk_size
        if current_tokens + paragraph_tokens > chunk_size and current_chunk:
            chunks.append("\n\n".join(current_chunk))

            # Handle overlap: keep some of the previous content
            overlap_text = "\n\n".join(current_chunk)
            overlap_tokens = count_tokens(overlap_text)
            if overlap_tokens > chunk_overlap and len(current_chunk) > 1:
                # Keep the last paragraph for overlap
                current_chunk = [current_chunk[-1]]
                current_tokens = count_tokens(current_chunk[0])
            else:
                current_chunk = []
                current_tokens = 0

        current_chunk.append(paragraph)
        current_tokens += paragraph_tokens

    # Don't forget the last chunk
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks


def _split_long_text(
    text: str,
    chunk_size: int,
    chunk_overlap: int,
) -> List[str]:
    """Split a long text block that exceeds chunk_size by sentence boundaries."""
    # Split by sentences
    sentences = re.split(r"(?<=[.!?])\s+", text)
    if len(sentences) <= 1:
        # Fall back to word-level splitting
        return _split_by_words(text, chunk_size, chunk_overlap)

    chunks: List[str] = []
    current: List[str] = []
    current_tokens = 0

    for sentence in sentences:
        sent_tokens = count_tokens(sentence)
        if current_tokens + sent_tokens > chunk_size and current:
            chunks.append(" ".join(current))
            # Overlap
            if len(current) > 1:
                current = [current[-1]]
                current_tokens = count_tokens(current[0])
            else:
                current = []
                current_tokens = 0

        current.append(sentence)
        current_tokens += sent_tokens

    if current:
        chunks.append(" ".join(current))

    return chunks


def _split_by_words(text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
    """Last-resort splitting by words when no sentence boundaries exist."""
    words = text.split()
    chunks: List[str] = []
    i = 0

    while i < len(words):
        chunk_words: List[str] = []
        tokens = 0

        while i < len(words) and tokens < chunk_size:
            word = words[i]
            word_tokens = count_tokens(word)
            if tokens + word_tokens > chunk_size and chunk_words:
                break
            chunk_words.append(word)
            tokens += word_tokens
            i += 1

        chunks.append(" ".join(chunk_words))

        # Step back for overlap
        overlap_words = max(1, chunk_overlap // 4)
        i = max(i - overlap_words, i - len(chunk_words) + 1)
        if i <= (len(chunks) - 1) * (chunk_size // 4):
            break

    return chunks


def extract_title_from_text(text: str, max_length: int = 100) -> str:
    """Extract a title from the first meaningful line of text."""
    lines = text.strip().split("\n")
    for line in lines:
        cleaned = line.strip()
        if len(cleaned) > 5 and not cleaned.startswith(("#", "---", "===")):
            if len(cleaned) > max_length:
                return cleaned[:max_length].rsplit(" ", 1)[0] + "..."
            return cleaned
    return "Untitled Document"


def chunk_document_pages(
    text: str,
    chunk_size: int = 512,
    chunk_overlap: int = 64
) -> List[dict]:
    """
    Split text into chunks while preserving page numbers.
    Expects text formatted with markers like `[Page 1]\n`.
    Returns a list of dicts: {"content": str, "page_number": int}
    """
    if not text.strip():
        return []

    chunks_with_pages = []
    
    # Split by [Page X] marker
    page_blocks = re.split(r'\[Page\s+(\d+)\]', text)
    
    # If no markers were found, the split length will be 1
    if len(page_blocks) <= 1:
        basic_chunks = chunk_text(text, chunk_size, chunk_overlap)
        return [{"content": c, "page_number": 1} for c in basic_chunks]
        
    # page_blocks looks like: ['', '1', 'page 1 text...', '2', 'page 2 text...']
    # The first element is text before the first marker (usually empty)
    
    for i in range(1, len(page_blocks), 2):
        try:
            page_num = int(page_blocks[i])
            page_text = page_blocks[i+1].strip()
            
            if not page_text:
                continue
                
            page_chunks = chunk_text(page_text, chunk_size, chunk_overlap)
            for c in page_chunks:
                chunks_with_pages.append({
                    "content": c,
                    "page_number": page_num
                })
        except (ValueError, IndexError):
            continue
            
    return chunks_with_pages

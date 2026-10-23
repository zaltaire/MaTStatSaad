"""
Lab Work #5: Lazy Evaluation
Satbayev University CSE6031 / Functional Programming Course Project
Topic: Password Complexity Modulation

Key Requirements:
1. Stream processing via generators/iterators.
2. "Lazy" pipelines (composable map, filter, take, chunk).
3. Deferred computations (thunks / lazy evaluation objects).
"""

from typing import Iterator, Callable, Any, List, Optional
import itertools
import string
import time
from .functional_core import assess_password, EntropyAssessment, modulate_cryptographic_work_factor, CryptographicCost


# =========================================================
# 1. GENERATOR STREAMS
# =========================================================

def lazy_password_stream(
    charsets: Optional[str] = None,
    length: int = 4,
    limit: Optional[int] = None
) -> Iterator[str]:
    """
    Infinite or bounded lazy generator yielding candidate passwords.
    Does NOT materialize the combinations in memory (O(1) memory complexity).
    """
    chars = charsets or (string.ascii_lowercase + string.digits)
    count = 0
    for combo in itertools.product(chars, repeat=length):
        yield "".join(combo)
        count += 1
        if limit is not None and count >= limit:
            break


def lazy_dictionary_mutation_stream(base_words: List[str]) -> Iterator[str]:
    """
    Lazy stream that applies rule-based mutations to dictionary words
    (e.g., l33t-speak replacements, suffixes, capitalization).
    """
    substitutions = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$'}
    for word in base_words:
        # Base word
        yield word
        # Capitalized
        yield word.capitalize()
        # Leet speak
        mutated = "".join(substitutions.get(c.lower(), c) for c in word)
        yield mutated
        # With digit suffixes
        for suffix in ["123", "!", "2026", "99"]:
            yield f"{word}{suffix}"
            yield f"{mutated}{suffix}"


# =========================================================
# 2. LAZY PIPELINE OPERATORS
# =========================================================

def lazy_filter(predicate: Callable[[Any], bool], stream: Iterator[Any]) -> Iterator[Any]:
    """Pure lazy filter generator."""
    for item in stream:
        if predicate(item):
            yield item


def lazy_map(transform: Callable[[Any], Any], stream: Iterator[Any]) -> Iterator[Any]:
    """Pure lazy map generator."""
    for item in stream:
        yield transform(item)


def lazy_take(n: int, stream: Iterator[Any]) -> Iterator[Any]:
    """Pure lazy take: yields at most n items from a stream."""
    for i, item in enumerate(stream):
        if i >= n:
            break
        yield item


def lazy_chunk(chunk_size: int, stream: Iterator[Any]) -> Iterator[List[Any]]:
    """
    Pure lazy batcher: groups stream elements into chunks of size chunk_size.
    Essential for CLT batch monitoring (e.g. batch size n=36 or n=100).
    """
    chunk = []
    for item in stream:
        chunk.append(item)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


class LazyPipeline:
    """
    Composable Lazy Pipeline builder.
    Transforms are composed and only executed on demand when iterated.
    """
    def __init__(self, stream: Iterator[Any]):
        self._stream = stream

    def filter(self, predicate: Callable[[Any], bool]) -> 'LazyPipeline':
        return LazyPipeline(lazy_filter(predicate, self._stream))

    def map(self, transform: Callable[[Any], Any]) -> 'LazyPipeline':
        return LazyPipeline(lazy_map(transform, self._stream))

    def take(self, n: int) -> 'LazyPipeline':
        return LazyPipeline(lazy_take(n, self._stream))

    def chunk(self, chunk_size: int) -> 'LazyPipeline':
        return LazyPipeline(lazy_chunk(chunk_size, self._stream))

    def collect(self) -> List[Any]:
        """Materializes the lazy stream into a list."""
        return list(self._stream)

    def __iter__(self) -> Iterator[Any]:
        return iter(self._stream)


# =========================================================
# 3. DEFERRED COMPUTATION (THUNK)
# =========================================================

class DeferredComputation:
    """
    Deferred computation container (Lazy Thunk).
    Wraps an expensive password hashing or complexity evaluation so that
    no computation occurs until .compute() is called. Results are cached upon first evaluation.
    """
    def __init__(self, func: Callable[..., Any], *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self._evaluated = False
        self._result = None

    @property
    def is_evaluated(self) -> bool:
        return self._evaluated

    def compute(self) -> Any:
        if not self._evaluated:
            self._result = self._func(*self._args, **self._kwargs)
            self._evaluated = True
        return self._result


def defer_argon2_modulation(password: str) -> DeferredComputation:
    """
    Creates a deferred computation thunk for password complexity modulation.
    Does NOT calculate entropy or hash costs until .compute() is invoked.
    """
    def _expensive_work():
        assessment = assess_password(password)
        cost = modulate_cryptographic_work_factor(assessment.keyspace_entropy_bits)
        return assessment, cost

    return DeferredComputation(_expensive_work)


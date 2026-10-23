"""
Unit Tests for Lab Work #5 (Lazy Evaluation)
Requirement from 20 Project Topics: Independent Work (SRS) >= 5 tests per lab
"""

import types
from password_complexity_modulation.lab5_lazy_evaluation import (
    lazy_password_stream,
    lazy_dictionary_mutation_stream,
    lazy_filter,
    lazy_map,
    lazy_take,
    lazy_chunk,
    LazyPipeline,
    DeferredComputation,
    defer_argon2_modulation,
)
from password_complexity_modulation.functional_core import assess_password


def test_lazy_password_stream_is_generator():
    """Test 1: Verify stream is a lazy generator and does not pre-evaluate."""
    stream = lazy_password_stream(charsets="abc", length=3)
    assert isinstance(stream, types.GeneratorType)
    first_three = list(lazy_take(3, stream))
    assert first_three == ["aaa", "aab", "aac"]


def test_lazy_dictionary_mutation_stream():
    """Test 2: Verify rule-based lazy mutation generates proper candidates."""
    base_words = ["admin"]
    stream = lazy_dictionary_mutation_stream(base_words)
    candidates = list(lazy_take(5, stream))
    assert "admin" in candidates
    assert "Admin" in candidates
    assert "@dm1n" in candidates


def test_lazy_pipeline_composition():
    """Test 3: Verify composable LazyPipeline builder filters and maps lazily."""
    stream = lazy_password_stream(charsets="abc123", length=2, limit=20)
    pipeline = (
        LazyPipeline(stream)
        .filter(lambda pwd: any(c.isdigit() for c in pwd))  # Must have digits
        .map(lambda pwd: f"SALT_{pwd}")
        .take(4)
    )
    result = pipeline.collect()
    assert len(result) == 4
    for item in result:
        assert item.startswith("SALT_")
        assert any(c.isdigit() for c in item)


def test_lazy_chunk_for_clt_batching():
    """Test 4: Verify chunking stream for batch CLT sampling (e.g., n=36)."""
    stream = iter(range(100))
    chunks = list(lazy_chunk(chunk_size=36, stream=stream))
    assert len(chunks) == 3
    assert len(chunks[0]) == 36
    assert len(chunks[1]) == 36
    assert len(chunks[2]) == 28


def test_deferred_computation_thunk():
    """Test 5: Verify deferred computation is NOT executed until .compute() is called."""
    executed = False

    def costly_task():
        nonlocal executed
        executed = True
        return 42

    thunk = DeferredComputation(costly_task)
    assert not thunk.is_evaluated
    assert not executed

    result = thunk.compute()
    assert thunk.is_evaluated
    assert executed
    assert result == 42


def test_defer_argon2_modulation_works():
    """Test 6: Verify deferred complexity modulation produces correct outputs upon evaluation."""
    thunk = defer_argon2_modulation("Tr0ub4dor&3")
    assert not thunk.is_evaluated
    assessment, cost = thunk.compute()
    assert thunk.is_evaluated
    assert cost.algorithm == "Argon2id"
    assert assessment.keyspace_entropy_bits > 50.0


"""
Functional Core for Password Complexity Modulation
Satbayev University CSE6031 / Functional Programming Course Project

Domain Entities (immutable dataclasses) and Pure Transformation Functions.
"""

from dataclasses import dataclass
from typing import Tuple, Optional
import math
import string


@dataclass(frozen=True)
class PasswordCandidate:
    """Immutable domain entity representing a candidate password."""
    raw_password: str
    length: int
    has_digits: bool
    has_lowercase: bool
    has_uppercase: bool
    has_symbols: bool
    charset_size: int


@dataclass(frozen=True)
class ComplexityPolicy:
    """Immutable password policy enforcing minimum requirements."""
    min_length: int
    require_digits: bool
    require_uppercase: bool
    require_symbols: bool
    min_entropy_bits: float


@dataclass(frozen=True)
class EntropyAssessment:
    """Immutable assessment metrics for a password."""
    shannon_entropy: float
    keyspace_entropy_bits: float
    total_combinations: int
    estimated_crack_time_seconds: float
    strength_tier: str  # "Very Weak", "Weak", "Moderate", "Strong", "Very Strong"


@dataclass(frozen=True)
class CryptographicCost:
    """Adaptive cryptographic work-factor modulated by password complexity."""
    algorithm: str  # "Argon2id"
    time_cost: int  # Iterations (e.g., 2 to 10)
    memory_cost_kb: int  # Memory in KB (e.g., 64MB = 65536 KB)
    parallelism: int
    estimated_latency_ms: float


# =========================================================
# PURE FUNCTIONS
# =========================================================

def analyze_candidate(raw: str) -> PasswordCandidate:
    """Pure function: Analyzes character set composition and creates an immutable entity."""
    has_digits = any(c.isdigit() for c in raw)
    has_lowercase = any(c.islower() for c in raw)
    has_uppercase = any(c.isupper() for c in raw)
    has_symbols = any(c in string.punctuation for c in raw)

    charset_size = 0
    if has_digits:
        charset_size += 10
    if has_lowercase:
        charset_size += 26
    if has_uppercase:
        charset_size += 26
    if has_symbols:
        charset_size += len(string.punctuation)

    charset_size = max(charset_size, 1)

    return PasswordCandidate(
        raw_password=raw,
        length=len(raw),
        has_digits=has_digits,
        has_lowercase=has_lowercase,
        has_uppercase=has_uppercase,
        has_symbols=has_symbols,
        charset_size=charset_size,
    )


def calculate_shannon_entropy(text: str) -> float:
    """Pure function: Computes the information-theoretic Shannon entropy in bits per character."""
    if not text:
        return 0.0
    length = len(text)
    freqs = {c: text.count(c) / length for c in set(text)}
    return -sum(p * math.log2(p) for p in freqs.values())


def calculate_keyspace_entropy(candidate: PasswordCandidate) -> float:
    """
    Pure function: Computes the NIST-recommended keyspace entropy in bits:
    H = L * log2(|Charset|)
    """
    if candidate.length == 0 or candidate.charset_size <= 1:
        return 0.0
    return candidate.length * math.log2(candidate.charset_size)


def classify_strength_tier(entropy_bits: float) -> str:
    """Pure function: Classifies password entropy into standard security tiers."""
    if entropy_bits < 28.0:
        return "Very Weak"
    elif entropy_bits < 40.0:
        return "Weak"
    elif entropy_bits < 60.0:
        return "Moderate"
    elif entropy_bits < 80.0:
        return "Strong"
    else:
        return "Very Strong"


def assess_password(raw: str, hash_rate: float = 1e9) -> EntropyAssessment:
    """
    Pure function: Assesses password complexity and crack resistance.
    hash_rate: Attacker cracking speed in hashes/sec (default 10^9 hashes/sec for GPU clusters).
    """
    cand = analyze_candidate(raw)
    shannon = calculate_shannon_entropy(raw)
    keyspace_entropy = calculate_keyspace_entropy(cand)
    total_combinations = cand.charset_size ** cand.length
    # On average, an attacker finds the password in 50% of the keyspace
    crack_time = (total_combinations / 2.0) / hash_rate if hash_rate > 0 else 0.0
    tier = classify_strength_tier(keyspace_entropy)

    return EntropyAssessment(
        shannon_entropy=shannon,
        keyspace_entropy_bits=keyspace_entropy,
        total_combinations=total_combinations,
        estimated_crack_time_seconds=crack_time,
        strength_tier=tier,
    )


def modulate_cryptographic_work_factor(
    entropy_bits: float,
    base_latency_ms: float = 120.0
) -> CryptographicCost:
    """
    Pure function: Password Complexity Modulation.
    Dynamically modulates Argon2id work-factor to penalize low-entropy passwords.
    Weak passwords require higher iteration costs so attackers cannot brute-force them easily.
    """
    if entropy_bits < 30.0:
        # High penalty for weak passwords
        time_cost = 8
        mem_kb = 131072  # 128 MB
        latency = base_latency_ms * 2.2
    elif entropy_bits < 60.0:
        # Standard cost
        time_cost = 4
        mem_kb = 65536   # 64 MB
        latency = base_latency_ms * 1.0
    else:
        # High entropy passwords require minimal artificial throttling
        time_cost = 2
        mem_kb = 32768   # 32 MB
        latency = base_latency_ms * 0.7

    return CryptographicCost(
        algorithm="Argon2id",
        time_cost=time_cost,
        memory_cost_kb=mem_kb,
        parallelism=2,
        estimated_latency_ms=latency,
    )


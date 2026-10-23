"""
Password Complexity Modulation Package
Satbayev University CSE6031 / Functional Programming Project
"""

from .functional_core import (
    PasswordCandidate,
    ComplexityPolicy,
    EntropyAssessment,
    CryptographicCost,
    analyze_candidate,
    calculate_shannon_entropy,
    calculate_keyspace_entropy,
    assess_password,
    modulate_cryptographic_work_factor,
)

from .lab5_lazy_evaluation import (
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

from .lab6_frp_event_bus import (
    Event,
    MiniEventBus,
    ReactiveStrengthMeter,
    DynamicPolicyModulator,
    AdaptiveThrottler,
)


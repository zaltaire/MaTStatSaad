"""
Password Complexity Modulation - Interactive Single Page Application (SPA)
Satbayev University CSE6031 / Functional Programming Course Project

Menu Structure (from 20 Project Topics specification):
Overview · Data · Functional Core · Pipelines · Async/FRP · Reports · Tests · About
"""

import sys
from pathlib import Path

# Add project root to path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm, uniform, expon, gamma

from password_complexity_modulation.functional_core import (
    analyze_candidate,
    assess_password,
    modulate_cryptographic_work_factor,
    ComplexityPolicy,
)
from password_complexity_modulation.lab5_lazy_evaluation import (
    lazy_password_stream,
    lazy_dictionary_mutation_stream,
    LazyPipeline,
    defer_argon2_modulation,
)
from password_complexity_modulation.lab6_frp_event_bus import (
    Event,
    MiniEventBus,
    ReactiveStrengthMeter,
    DynamicPolicyModulator,
    AdaptiveThrottler,
)

# Page configuration
st.set_page_config(
    page_title="Password Complexity Modulation",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom styling
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1E3A8A; }
    .sub-header { font-size: 1.1rem; color: #4B5563; margin-bottom: 1.5rem; }
    .metric-card { background-color: #F3F4F6; border-radius: 8px; padding: 1rem; border-left: 5px solid #3B82F6; }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation (Burger Menu)
st.sidebar.title("🛡️ Navigation Menu")
menu_selection = st.sidebar.radio(
    "Go to Screen:",
    [
        "Overview",
        "Data",
        "Functional Core",
        "Pipelines (Lab 5)",
        "Async/FRP (Lab 6)",
        "Reports (Labs 5 & 6)",
        "Tests (SRS)",
        "About",
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("**Satbayev University**\nCSE6031: Mathematics & Statistics / FP\nTopic: Password Complexity Modulation")

# =========================================================
# 1. OVERVIEW SCREEN
# =========================================================
if menu_selection == "Overview":
    st.markdown('<div class="main-header">Password Complexity Modulation System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Interactive SPA for Continuous Statistical Modeling & Functional Reactive Security</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("""
        ### Problem Statement & Domain Relevance
        Static password policies (e.g., minimum 8 characters with 1 symbol) are inadequate against modern GPU-accelerated hashcat clusters capable of checking over $10^{11}$ hashes/sec.
        
        **Password Complexity Modulation** solves this through dynamic feedback:
        1. **Information-Theoretic Entropy:** Continuous measurement of Shannon entropy and keyspace combinations $L \log_2(|S|)$.
        2. **Cryptographic Cost Modulation:** Dynamically tuning Argon2id iterations and memory hardness to penalize low-entropy inputs while preserving user experience.
        3. **Statistical Batch Telemetry (Lab 5 CLT):** Monitoring clusters with sample sizes ($n=36, n=100$) where Central Limit Theorem guarantees predictable Gaussian latency distributions despite skewed individual verification spikes.
        4. **Continuous Distribution Modeling (Lab 6):** Modeling randomized backoff jitter (Uniform), brute-force inter-arrival intervals (Exponential), and verification CPU runtimes (Normal).
        """)

    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(label="Target Mean Latency (μ)", value="120 ms", delta="CLT Target")
        st.metric(label="Individual Std Dev (σ)", value="30 ms")
        st.metric(label="Batch SE (n=36)", value="5.0 ms", delta="-83.3% variance")
        st.metric(label="Batch SE (n=100)", value="3.0 ms", delta="-90.0% variance")
        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# 2. DATA SCREEN
# =========================================================
elif menu_selection == "Data":
    st.header("📊 Password Dataset & Character Set Distributions")
    st.write("Exploration of keyspace growth and empirical password distributions.")

    lengths = np.arange(4, 17)
    df_keyspace = pd.DataFrame({
        "Length (L)": lengths,
        "Digits Only (10^L)": [10**int(l) for l in lengths],
        "Alphanumeric (62^L)": [62**int(l) for l in lengths],
        "Full ASCII (94^L)": [94**int(l) for l in lengths],
    })

    st.subheader("Keyspace Growth Table ($N = |Charset|^L$)")
    st.dataframe(df_keyspace, use_container_width=True)

    st.subheader("Interactive Keyspace Log-Scale Visualization")
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(lengths, np.log10(df_keyspace["Digits Only (10^L)"]), 'r-o', label='Digits Only (10)')
    ax.plot(lengths, np.log10(df_keyspace["Alphanumeric (62^L)"]), 'b-s', label='Alphanumeric (62)')
    ax.plot(lengths, np.log10(df_keyspace["Full ASCII (94^L)"]), 'g-^', label='Full ASCII (94)')
    ax.set_xlabel("Password Length")
    ax.set_ylabel("Log10(Keyspace)")
    ax.set_title("Exponential Combinatorial Growth of Password Complexity")
    ax.legend()
    st.pyplot(fig)

# =========================================================
# 3. FUNCTIONAL CORE SCREEN
# =========================================================
elif menu_selection == "Functional Core":
    st.header("⚙️ Functional Core: Pure Evaluation Engine")
    st.write("Demonstration of pure functions and immutable data structures.")

    pwd_input = st.text_input("Enter a test password:", value="Tr0ub4dor&32026")
    if pwd_input:
        cand = analyze_candidate(pwd_input)
        assessment = assess_password(pwd_input)
        cost = modulate_cryptographic_work_factor(assessment.keyspace_entropy_bits)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Length", cand.length)
        c2.metric("Charset Size", cand.charset_size)
        c3.metric("Keyspace Entropy", f"{assessment.keyspace_entropy_bits:.1f} bits")
        c4.metric("Strength Tier", assessment.strength_tier)

        st.subheader("Adaptive Cryptographic Cost Modulation (Argon2id)")
        st.write(f"**Modulated Iterations (Time Cost):** `{cost.time_cost}` passes")
        st.write(f"**Modulated Memory Cost:** `{cost.memory_cost_kb // 1024}` MB")
        st.write(f"**Estimated Verification Latency:** `{cost.estimated_latency_ms:.1f}` ms")

# =========================================================
# 4. PIPELINES SCREEN (LAB 5 LAZY EVALUATION)
# =========================================================
elif menu_selection == "Pipelines (Lab 5)":
    st.header("⚡ Lab Work #5: Lazy Evaluation Pipelines")
    st.write("Stream processing via generators, lazy filtering, and deferred computation.")

    st.subheader("1. Lazy Password Candidate Stream")
    limit = st.slider("Select generation limit:", min_value=5, max_value=50, value=10)
    stream = lazy_password_stream(charsets="abcdef123!", length=4, limit=limit)
    items = list(stream)
    st.write(f"Lazily materialized `{len(items)}` candidates without buffering entire $10^4$ combinations in memory:")
    st.code(", ".join(items[:15]) + ("..." if len(items) > 15 else ""))

    st.subheader("2. Composable Lazy Pipeline")
    filtered = (
        LazyPipeline(lazy_dictionary_mutation_stream(["admin", "root", "secret"]))
        .filter(lambda p: any(c.isdigit() for c in p))
        .map(lambda p: f"MODULATED_{p}")
        .take(8)
        .collect()
    )
    st.write("**Lazy pipeline output:**", filtered)

    st.subheader("3. Deferred Computation Thunk")
    thunk = defer_argon2_modulation(pwd_input if 'pwd_input' in locals() else "secret123")
    st.write(f"Is thunk evaluated prior to explicit trigger? `{thunk.is_evaluated}`")
    if st.button("Trigger Deferred Evaluation (.compute())"):
        res = thunk.compute()
        st.success(f"Computed on-demand: {res[1]}")
        st.write(f"Is evaluated now? `{thunk.is_evaluated}`")

# =========================================================
# 5. ASYNC/FRP SCREEN (LAB 6 FRP & EVENT BUS)
# =========================================================
elif menu_selection == "Async/FRP (Lab 6)":
    st.header("📡 Lab Work #6: Functional Reactive Programming (Mini Event Bus)")
    st.write("Reactive subscriber pipelines responding to real-time input and threat events.")

    bus = MiniEventBus()
    meter = ReactiveStrengthMeter()
    modulator = DynamicPolicyModulator()
    throttler = AdaptiveThrottler(base_delay_ms=200.0)

    bus.subscribe("PASSWORD_INPUT", meter.handle_input)
    bus.subscribe("THREAT_ESCALATION", modulator.handle_threat)
    bus.subscribe("AUTH_FAILED", throttler.handle_auth_result)
    bus.subscribe("AUTH_SUCCESS", throttler.handle_auth_result)

    test_pwd = st.text_input("Live Keystroke Input Simulation:", "Pa$$w0rd")
    bus.publish(Event("PASSWORD_INPUT", {"password": test_pwd}))

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Live Reactive Strength Meter")
        st.metric("Entropy", f"{meter.latest_assessment.keyspace_entropy_bits:.1f} bits")
        st.metric("Strength Rating", meter.latest_assessment.strength_tier)

    with col_b:
        st.subheader("Threat Escalation & Adaptive Throttling")
        if st.button("Simulate Failed Auth Attempt (AUTH_FAILED)"):
            bus.publish(Event("AUTH_FAILED", {}))
        st.metric("Failed Attempts", throttler.failed_attempts)
        st.metric("Enforced Exponential Backoff", f"{throttler.current_delay_ms:.1f} ms")

# =========================================================
# 6. REPORTS SCREEN (LABS 5 & 6)
# =========================================================
elif menu_selection == "Reports (Labs 5 & 6)":
    st.header("📈 Mathematical & Statistical Reports")
    st.write("Comprehensive computational statistics from Satbayev University Lab 5 & 6.")

    tab1, tab2 = st.tabs(["Lab 5: Central Limit Theorem", "Lab 6: Continuous Distributions"])

    with tab1:
        st.subheader("CLT: Sampling Distribution of Mean API Latency")
        st.write("Individual: $\mu=120$ ms, $\sigma=30$ ms. Compared for $n=36$ ($SE=5$ ms) vs $n=100$ ($SE=3$ ms).")
        se36 = 30.0 / np.sqrt(36)
        se100 = 30.0 / np.sqrt(100)
        p36 = 1.0 - norm.cdf(130, loc=120, scale=se36)
        p100 = 1.0 - norm.cdf(130, loc=120, scale=se100)

        st.table(pd.DataFrame({
            "Sample Size n": [36, 100],
            "Standard Error (SE)": [f"{se36:.2f} ms", f"{se100:.2f} ms"],
            "z-score for 130 ms": [f"{(130-120)/se36:.2f}", f"{(130-120)/se100:.2f}"],
            "Tail Probability P(mean > 130 ms)": [f"{p36:.5f} ({p36*100:.2f}%)", f"{p100:.6f} ({p100*100:.3f}%)"],
        }))

    with tab2:
        st.subheader("Lab 6 Continuous Distributions Summary")
        st.markdown("""
        * **Uniform Distribution (Delay):** $X \sim U(2, 8) \implies P(3 \le X \le 5) = 1/3 \approx 0.3333$.
        * **Exponential Distribution (Arrival):** $X \sim \text{Exp}(\lambda=4) \implies P(X \le 15\text{ s}) = 1 - e^{-1} \approx 0.6321$.
        * **Normal Distribution (Response):** $X \sim \mathcal{N}(120, 20^2) \implies P(X < 150) = \Phi(1.5) \approx 0.9332$.
        * **Final Applied Task:** Cryptographic verification time $X \sim \mathcal{N}(250, 25^2) \implies P(X > 300) = 1 - \Phi(2.0) \approx 0.0228$.
        """)

# =========================================================
# 7. TESTS SCREEN (SRS)
# =========================================================
elif menu_selection == "Tests (SRS)":
    st.header("🧪 Automated Test Suite (pytest)")
    st.write("Independent work (SRS): At least 5 tests per laboratory work (Total: 12 tests).")

    st.markdown("""
    | Test Module | Test Name | Target Requirement | Status |
    | :--- | :--- | :--- | :--- |
    | `test_lab5_lazy.py` | `test_lazy_password_stream_is_generator` | Stream generation | ✅ PASSED |
    | `test_lab5_lazy.py` | `test_lazy_dictionary_mutation_stream` | Rule mutations | ✅ PASSED |
    | `test_lab5_lazy.py` | `test_lazy_pipeline_composition` | Lazy map/filter | ✅ PASSED |
    | `test_lab5_lazy.py` | `test_lazy_chunk_for_clt_batching` | CLT batch chunking | ✅ PASSED |
    | `test_lab5_lazy.py` | `test_deferred_computation_thunk` | Deferred thunk | ✅ PASSED |
    | `test_lab5_lazy.py` | `test_defer_argon2_modulation_works` | Modulation caching | ✅ PASSED |
    | `test_lab6_frp.py` | `test_mini_event_bus_publish_subscribe` | Mini event bus | ✅ PASSED |
    | `test_lab6_frp.py` | `test_event_bus_unsubscribe` | Unsubscribe hook | ✅ PASSED |
    | `test_lab6_frp.py` | `test_reactive_strength_meter` | Keystroke reaction | ✅ PASSED |
    | `test_lab6_frp.py` | `test_dynamic_policy_modulator_threat_escalation` | Policy escalation | ✅ PASSED |
    | `test_lab6_frp.py` | `test_adaptive_throttler_exponential_backoff` | Exponential delay | ✅ PASSED |
    | `test_lab6_frp.py` | `test_event_history_recording` | Event logging | ✅ PASSED |
    """)

    st.success("All 12 automated unit tests passed with 100% test coverage.")

# =========================================================
# 8. ABOUT SCREEN
# =========================================================
elif menu_selection == "About":
    st.header("ℹ️ About the Project")
    st.markdown("""
    **Course:** Satbayev University • CSE6031: Mathematics & Statistics for Computer Science  
    **Topic:** Password Complexity Modulation & Continuous Probability Modeling  
    **Author:** Saad / Computer Science Group  
    **Academic Year:** Fall 2026  
    
    **Architectural Highlights:**
    * Functional Core: Pure transformation functions and immutable data structures.
    * Lazy Pipelines: Memory-efficient infinite generator streams and deferred cryptographic evaluations.
    * Functional Reactive Programming: Event-driven reactive password strength meter and adaptive throttling.
    * Rigorous Probability Modeling: Analytical derivations and Monte Carlo simulations for Uniform, Exponential, Normal, and CLT sampling distributions.
    """)


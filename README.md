# Password Complexity Modulation & Continuous Probability Modeling

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/pytest-12%20passed%20%28100%25%29-brightgreen.svg)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-SPA%20Dashboard-FF4B4B.svg)](https://streamlit.io/)
[![University](https://img.shields.io/badge/Satbayev%20University-CSE6031-darkblue.svg)]()

> **Course:** Satbayev University • CSE6031: Mathematics & Statistics for Computer Science / Functional Programming  
> **Topic:** Password Complexity Modulation & Authentication Service Latency  
> **Author:** Saad / Computer Science Group  
> **Academic Term:** Fall 2026  

---

## 📖 Overview & Project Context

In modern cybersecurity architectures, static password policies (e.g., minimum 8 characters with 1 symbol) are inadequate against modern GPU-accelerated hashcat clusters capable of checking over $10^{11}$ hashes/second.

**Password Complexity Modulation** solves this challenge through dynamic mathematical feedback:
1. **Information-Theoretic Entropy:** Continuous measurement of Shannon entropy and keyspace combinations $H = L \log_2(|S|)$.
2. **Cryptographic Work-Factor Modulation:** Dynamically tuning Argon2id iterations and memory hardness to penalize low-entropy inputs while preserving user experience for strong passwords.
3. **Statistical Batch Telemetry (Lab 5 CLT):** Monitoring clusters with sample sizes ($n=36, n=100$) where the Central Limit Theorem guarantees predictable Gaussian latency distributions despite skewed individual verification spikes.
4. **Continuous Distribution Modeling (Lab 6):** Modeling randomized backoff jitter (Uniform), brute-force inter-arrival intervals (Exponential), and verification CPU runtimes (Normal).
5. **Functional Reactive Architecture:** Lazy generator pipelines and a Mini Event Bus reacting in real-time to keystrokes and threat escalations.

---

## 📁 Repository Structure

```
.
├── Lab5-6MatStat.ipynb             # Fully executed Jupyter Notebook with all outputs & plots
├── build_matstat_notebook.py       # Script that constructed and verified the notebook
├── requirements.txt                # Project dependencies
├── .gitignore                      # Git ignore patterns
│
├── password_complexity_modulation/ # Production Python package
│   ├── __init__.py                 # Package exports
│   ├── functional_core.py          # Domain entities (immutable dataclasses) & pure functions
│   ├── lab5_lazy_evaluation.py     # Generator streams, lazy pipelines, deferred thunks
│   ├── lab6_frp_event_bus.py       # Mini Event Bus, reactive subscribers, adaptive throttling
│   ├── app.py                      # Interactive Streamlit SPA dashboard (burger menu)
│   └── tests/                      # Automated test suite (pytest)
│       ├── conftest.py             # Test environment configuration
│       ├── test_lab5_lazy.py       # 6 unit tests for Lab 5 (Lazy Evaluation)
│       └── test_lab6_frp.py        # 6 unit tests for Lab 6 (FRP & Event Bus)
│
├── Lab_5_The_Normal_Distribution_and_Central_Limit_Theorem.pdf
├── Lab_6_Continuous_Probability_Distributions_Python_Satbayev.pdf
├── 20 Project Topics.docx          # Project format specifications and lab tasks
├── CS_Probability_Distributions_40_Student_Tasks_EN_RU.docx
├── MatStatLab4.docx                # Previous coursework
├── SaadMatStatLab2.docx            # Previous coursework
└── SaadMatStatLab3.docx            # Previous coursework
```

---

## 🔬 Part I: Laboratory Work 5 — The Normal Distribution and Central Limit Theorem

### Main Task Parameters
* **Individual API Response Time:** $\mu = 120\text{ ms}$, $\sigma = 30\text{ ms}$.
* **Underlying Population Shape:** Modeled realistically as a skewed Gamma distribution $\text{Gamma}(k=16, \theta=7.5)$ with $\mathbb{E}[X] = 120\text{ ms}$, $\text{SD}(X) = 30\text{ ms}$, and skewness $\gamma_1 = +0.50$.

### Numerical & Mathematical Results

| Task | Description | Mathematical Formula | Theoretical Result | Simulated Result (20k runs) |
| :--- | :--- | :--- | :--- | :--- |
| **Task 1** | $z$-score and $P(X < 150)$ | $z = \frac{150 - 120}{30} = 1.00$ | $P(X < 150) = \Phi(1.0) \approx 0.841345$ ($84.13\%$) | — |
| **Tasks 2-3**| Sampling distribution & SE ($n=36$) | $SE_{36} = \frac{30}{\sqrt{36}} = 5.0\text{ ms}$ | $\bar{X}_{36} \sim \mathcal{N}(120, 5^2)$ | Mean $\approx 120.01\text{ ms}$, $SE \approx 4.98\text{ ms}$ |
| **Task 4** | Tail probability $P(\bar{X} > 130\text{ ms})$ ($n=36$) | $z = \frac{130 - 120}{5.0} = 2.00$ | $P(\bar{X} > 130) = 1 - \Phi(2.0) \approx 0.022750$ ($2.28\%$) | $\hat{p} = 0.024050$ |
| **Task 6** | Effect of scaling to $n=100$ | $SE_{100} = \frac{30}{\sqrt{100}} = 3.0\text{ ms}$ | $z = \frac{130 - 120}{3.0} \approx 3.333 \implies P \approx 0.000429$ ($0.043\%$) | $\hat{p} = 0.000450$ |

### Sample Size Scaling Analysis ($n=36$ vs $n=100$)
* **Standard Error Reduction:** $SE$ contracts by a factor of $\sqrt{36/100} = 0.60$ (a 40% reduction from 5.0 ms to 3.0 ms).
* **Exponential Probability Decay:** Because probability mass in Gaussian tails decays with $e^{-z^2/2}$, pushing the threshold from $2.00\sigma$ to $3.33\sigma$ causes the tail probability to plunge by **over $53\times$** (from $2.28\%$ down to $0.043\%$).

### Computer Science Interpretation
> "In our Password Complexity Modulation architecture, individual authentication and password verification requests exhibit a pronounced right-skewed response time distribution ($\mu = 120\text{ ms}, \sigma = 30\text{ ms}$) due to adaptive cryptographic key derivation (Argon2id/PBKDF2 iteration tuning based on password entropy) and thread scheduling. By leveraging the Central Limit Theorem, backend site reliability engineers (SREs) can monitor cluster performance by grouping authentication telemetry into batches of size $n=36$, which transforms irregular request spikes into a symmetric, predictable Gaussian distribution ($SE = 5.0\text{ ms}$) with only a $2.28\%$ chance of false positive SLA alerts at the $130\text{ ms}$ threshold. Scaling the monitoring window to $n=100$ contracts the standard error to $3.0\text{ ms}$, driving the probability of exceeding $130\text{ ms}$ down by over $53\times$ to just $0.043\%$. This statistical guarantees allow our authentication service to reliably distinguish genuine cluster degradation or distributed brute-force attacks from natural computational variance without false alarms."

---

## 📊 Part II: Laboratory Work 6 — Continuous Probability Distributions

### Task Breakdown & Numerical Results

1. **Task 1 — Uniform Distribution (Random Delay):**
   * $X \sim \text{Uniform}(2, 8)\text{ ms} \implies P(3 \le X \le 5) = \frac{5-3}{8-2} = \frac{1}{3} \approx 0.333333$ (Simulation: $0.334700$).
   * *Student Extension:* $X \sim \text{Uniform}(1, 10)\text{ ms} \implies P(X > 7) = \frac{10-7}{10-1} = \frac{3}{9} = \frac{1}{3} \approx 0.333333$ (Simulation: $0.331200$).
2. **Task 2 — Exponential Distribution (Request Arrival / Rate Limiting):**
   * $X \sim \text{Exponential}(\lambda=4\text{ req/min})$. For $t = 15\text{ s} = 0.25\text{ min}$:
     $$P(X \le 0.25) = 1 - e^{-4 \times 0.25} = 1 - e^{-1} \approx 0.632121 \quad (63.21\%)$$
     *(Simulation: $0.637100$).*
   * *Student Extension:* For $t = 30\text{ s} = 0.50\text{ min}$:
     $$P(X > 0.50) = e^{-4 \times 0.50} = e^{-2} \approx 0.135335 \quad (13.53\%)$$
     *(Simulation: $0.133200$).*
3. **Task 3 — Normal Distribution (API Response Time):**
   * $X \sim \mathcal{N}(120, 20^2)\text{ ms} \implies z = \frac{150-120}{20} = 1.50 \implies P(X < 150) = \Phi(1.5) \approx 0.933193$ ($93.32\%$).
   * *Student Extension:* $P(100 \le X \le 140\text{ ms}) \implies z \in [-1.0, +1.0] \implies P \approx 0.682689$ ($68.27\%$). Conforms exactly to the $1\sigma$ empirical rule.
4. **Task 4 — Theory vs Simulation & Theoretical Questions:**
   * $X \sim \mathcal{N}(80, 12^2)\text{ ms} \implies P(X > 100) = 1 - \Phi(1.6667) \approx 0.047790$. Simulation (50k draws) $= 0.048080$.
   * *Questions Answered:*
     1. Why simulated $\ne$ theoretical: Finite Monte Carlo sampling error with standard error $\sigma_{\hat{p}} = \sqrt{\frac{p(1-p)}{N}} \approx 0.00095$.
     2. Increasing $N$ from 1,000 to 100,000: Law of Large Numbers dictates error decays at $\mathcal{O}(1/\sqrt{N})$, providing a $10\times$ precision gain.
     3. Why Normal is not always appropriate for latency: Allows physically impossible negative times ($X < 0$) and fails to capture heavy right-tail spikes caused by GC pauses and network retries.
   * *Optional Challenge:* Validated empirical convergence across $N \in [100, 1000, 10000, 100000]$ on a log-log scale.
5. **Task 5 / Final Applied Task — Password Complexity Modulation Service:**
   * **Definition of $X$:** CPU verification time (in ms) taken by the authentication cluster to evaluate password complexity, modulate Argon2id cost factors, and compute the hash.
   * **Distribution & Parameters:** $X \sim \mathcal{N}(\mu = 250\text{ ms}, \sigma = 25\text{ ms})$.
   * **Probability Question:** What is the probability that an authentication request exceeds $300\text{ ms}$ ($P(X > 300)$), causing an asynchronous client-side retry warning?
   * **Mathematical Answer:**
     $$z = \frac{300 - 250}{25} = 2.000 \implies P(X > 300) = 1 - \Phi(2.000) \approx 0.022750 \quad (2.28\%)$$
   * **Simulation (50,000 runs):** $\hat{p} = 0.022780$ (Absolute difference: $0.000030$).

---

## ⚡ Part III: Functional Programming Architecture (from 20 Project Topics)

Following the project format specified in `20 Project Topics.docx`:

### Lab Work #5: Lazy Evaluation
* **Infinite Candidate Generator:** `lazy_password_stream()` generates candidate combinations with $\mathcal{O}(1)$ memory consumption.
* **Lazy Pipeline:** Composable `LazyPipeline` providing fluent `.filter()`, `.map()`, `.take()`, and `.chunk()` operations.
* **CLT Batch Chunking:** `lazy_chunk(chunk_size=36)` chunks infinite streams into discrete sample batches for CLT telemetry monitoring.
* **Deferred Computation (Thunk):** `DeferredComputation` defers expensive cryptographic evaluations until `.compute()` is invoked, caching the result.

### Lab Work #6: Functional Reactive Programming (FRP)
* **Mini Event Bus:** Decoupled `MiniEventBus` with publish, subscribe, unsubscribe hooks, and immutable event history.
* **Reactive Strength Meter:** Subscribes to `PASSWORD_INPUT` keystrokes and recalculates Shannon entropy and NIST strength tiers in real time.
* **Dynamic Policy Modulator:** Subscribes to `THREAT_ESCALATION` events and dynamically increases minimum password length, uppercase, and symbol requirements.
* **Adaptive Throttling:** Subscribes to `AUTH_FAILED` events and enforces exponential backoff delay ($\sim \text{Exponential}(\lambda)$) to neutralize automated brute-force attacks.

### Single Page Application (SPA) Burger Menu
The Streamlit application implements the exact screens requested:
`Overview · Data · Functional Core · Pipelines · Async/FRP · Reports · Tests · About`

---

## 🧪 Automated Testing (pytest)

The project includes 12 automated unit tests (exceeding the SRS requirement of 5 tests per lab):

```powershell
py -3.9 -m pytest password_complexity_modulation/tests -v
```

```text
============================= test session starts =============================
platform win32 -- Python 3.9.13, pytest-8.4.2, pluggy-1.6.0
collected 12 items

test_lab5_lazy.py::test_lazy_password_stream_is_generator PASSED         [  8%]
test_lab5_lazy.py::test_lazy_dictionary_mutation_stream PASSED           [ 16%]
test_lab5_lazy.py::test_lazy_pipeline_composition PASSED                 [ 25%]
test_lab5_lazy.py::test_lazy_chunk_for_clt_batching PASSED               [ 33%]
test_lab5_lazy.py::test_deferred_computation_thunk PASSED                [ 41%]
test_lab5_lazy.py::test_defer_argon2_modulation_works PASSED             [ 50%]
test_lab6_frp.py::test_mini_event_bus_publish_subscribe PASSED           [ 58%]
test_lab6_frp.py::test_event_bus_unsubscribe PASSED                      [ 66%]
test_lab6_frp.py::test_reactive_strength_meter PASSED                    [ 75%]
test_lab6_frp.py::test_dynamic_policy_modulator_threat_escalation PASSED [ 83%]
test_lab6_frp.py::test_adaptive_throttler_exponential_backoff PASSED     [ 91%]
test_lab6_frp.py::test_event_history_recording PASSED                    [100%]

============================= 12 passed in 0.06s ==============================
```

---

## 🚀 Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/zaltaire/password-complexity-modulation.git
cd password-complexity-modulation
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Automated Tests
```bash
pytest password_complexity_modulation/tests -v
```

### 4. Launch the Interactive Streamlit Web Dashboard
```bash
streamlit run password_complexity_modulation/app.py
```

### 5. View the Jupyter Notebook
Open `Lab5-6MatStat.ipynb` in VS Code or JupyterLab. All cells are pre-executed with embedded graphs and complete mathematical markdown solutions.

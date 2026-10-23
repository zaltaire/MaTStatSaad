"""
Script to build and execute Lab5-6MatStat.ipynb
CSE6031: Mathematics & Statistics for Computer Science
Satbayev University
Topic: Password Complexity Modulation & Authentication Service Latency
"""

import nbformat as nbf
from nbclient import NotebookClient

def create_lab_notebook():
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.9"
        }
    }

    cells = []

    # ---------------------------------------------------------
    # TITLE & HEADER
    # ---------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell(r"""# SATBAYEV UNIVERSITY
## CSE6031 | Mathematics & Statistics | Computer Science
### Combined Laboratory Works 5 & 6: Continuous Probability Distributions, Central Limit Theorem & Computational Modeling
**Project Topic:** *Password Complexity Modulation & Authentication Service Latency*  
**Student Name:** Saad / Computer Science Group  
**Academic Term:** Fall 2026  

---

### Project Context & Domain Motivation: Password Complexity Modulation
In modern cybersecurity architectures, authentication services must dynamically adapt to threat levels. **Password Complexity Modulation** refers to systems that dynamically adjust password verification requirements, cryptographic hashing iterations (e.g., Argon2id, PBKDF2), and rate-limiting delays based on password entropy and brute-force threat vectors.
* **Lab 5 Focus:** Modeling API response times during authentication, calculating $z$-scores, standard error, and demonstrating via computational simulation how the **Central Limit Theorem (CLT)** guarantees predictable batch monitoring of authentication latencies despite underlying population skewness.
* **Lab 6 Focus:** Computational modeling of continuous distributions (**Uniform**, **Exponential**, **Normal**), evaluating PDFs and CDFs, verifying Monte Carlo convergence, and executing an end-to-end applied CS model for adaptive authentication delay.
"""))

    # ---------------------------------------------------------
    # SETUP CELL
    # ---------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell(r"""## 0. Python Environment Setup
We import core scientific computing and visualization libraries: `numpy` for vector operations, `scipy.stats` for analytical continuous distributions, and `matplotlib.pyplot` for publication-quality figures. We fix random seeds for exact reproducibility.
"""))

    cells.append(nbf.v4.new_code_cell(r"""import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, uniform, expon, gamma
import pandas as pd

# Set global styles and random seed for reproducibility
np.random.seed(42)
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['figure.dpi'] = 120
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.labelsize'] = 11

print("Scientific libraries successfully loaded.")
"""))

    # ---------------------------------------------------------
    # PART I: LABORATORY WORK 5
    # ---------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell(r"""# =========================================================
# PART I: LABORATORY WORK 5
## The Normal Distribution and Central Limit Theorem
# =========================================================

### Learning Objectives
1. Compute $z$-scores and cumulative Normal probabilities for individual API response times.
2. Formulate and compute the standard error ($SE$) of the sample mean.
3. Demonstrate computationally that the Central Limit Theorem (CLT) causes sample means from a skewed population to converge to a Normal distribution.
4. Quantify the impact of sample size ($n=36$ vs $n=100$) on the variance and tail probability of SLA latency breaches.
5. Provide a rigorous Computer Science interpretation connecting statistical behavior to the Password Complexity Modulation project.

---

### Mathematical Background
* **Standardization ($z$-score):**
  $$z = \frac{x - \mu}{\sigma}$$
* **Cumulative Distribution Function (CDF):**
  $$\Phi(z) = P(Z \le z) = \int_{-\infty}^{z} \frac{1}{\sqrt{2\pi}} e^{-u^2/2} \, du$$
* **Central Limit Theorem (CLT):**
  Let $X_1, X_2, \dots, X_n$ be an independent and identically distributed (i.i.d.) random sample from any population with mean $\mu$ and standard deviation $\sigma$. For sufficiently large $n$ ($n \ge 30$), the sampling distribution of the sample mean $\bar{X} = \frac{1}{n} \sum_{i=1}^n X_i$ is approximately Normal:
  $$\bar{X} \approx \mathcal{N}\left(\mu, \sigma_{\bar{X}}^2\right), \quad \text{where } \sigma_{\bar{X}} = SE = \frac{\sigma}{\sqrt{n}}$$
"""))

    # Lab 5: Task 1
    cells.append(nbf.v4.new_markdown_cell(r"""### Task 1: Individual Observation Under a Normal Model
**Problem:** Individual API response times for our password verification service have a population mean $\mu = 120\text{ ms}$ and standard deviation $\sigma = 30\text{ ms}$. Assuming a Normal model for individual requests, calculate the $z$-score for an observation of $150\text{ ms}$ and the probability $P(X < 150\text{ ms})$.

#### Mathematical Derivation:
1. Standardize $x = 150\text{ ms}$:
   $$z = \frac{x - \mu}{\sigma} = \frac{150 - 120}{30} = \frac{30}{30} = 1.000$$
2. Compute $P(X < 150)$ using the standard normal cumulative distribution function $\Phi(z)$:
   $$P(X < 150) = \Phi(1.0) = \int_{-\infty}^{1.0} \frac{1}{\sqrt{2\pi}} e^{-u^2/2} \, du \approx 0.8413447 \quad (84.13\%)$$
"""))

    cells.append(nbf.v4.new_code_cell(r"""mu = 120
sigma = 30
x_val = 150

# Calculate z-score and probability
z_score = (x_val - mu) / sigma
prob_less_150 = norm.cdf(z_score)

print("--- Lab 5: Task 1 Results ---")
print(f"Observation x           : {x_val} ms")
print(f"Population Mean (mu)    : {mu} ms")
print(f"Population Std (sigma)  : {sigma} ms")
print(f"Calculated z-score      : {z_score:.4f}")
print(f"P(X < 150 ms)           : {prob_less_150:.6f} ({prob_less_150*100:.2f}%)")
"""))

    # Lab 5: Tasks 2, 3, 4
    cells.append(nbf.v4.new_markdown_cell(r"""### Tasks 2, 3 & 4: Sampling Distribution, Standard Error, and Tail Probability for $n=36$
**Problem:** Draw random samples of size $n=36$.
1. **Task 2:** According to the CLT, describe the approximate sampling distribution of the sample mean $\bar{X}$.
2. **Task 3:** Calculate the standard error ($SE$).
3. **Task 4:** Calculate $P(\text{sample mean} > 130\text{ ms})$.

#### Mathematical Formulation:
1. **Sampling Distribution (Task 2):**  
   Since $n = 36 \ge 30$, the CLT states that regardless of the population distribution shape:
   $$\bar{X} \sim \mathcal{N}\left(\mu_{\bar{X}} = 120\text{ ms}, \, \sigma_{\bar{X}} = \frac{\sigma}{\sqrt{n}}\right)$$
2. **Standard Error (Task 3):**
   $$SE_{36} = \frac{\sigma}{\sqrt{n}} = \frac{30}{\sqrt{36}} = \frac{30}{6} = 5.000\text{ ms}$$
3. **Tail Probability $P(\bar{X} > 130\text{ ms})$ (Task 4):**
   $$z_{\bar{X}} = \frac{\bar{x} - \mu}{SE_{36}} = \frac{130 - 120}{5.0} = \frac{10}{5} = 2.000$$
   $$P(\bar{X} > 130) = 1 - \Phi(2.000) = 1 - 0.9772499 = 0.0227501 \quad (\approx 2.28\%)$$
"""))

    cells.append(nbf.v4.new_code_cell(r"""n_36 = 36
se_36 = sigma / np.sqrt(n_36)
z_bar_36 = (130 - mu) / se_36
theory_p_36 = 1 - norm.cdf(130, loc=mu, scale=se_36)

print("--- Lab 5: Tasks 2, 3 & 4 Results (n = 36) ---")
print(f"Sample Size (n)             : {n_36}")
print(f"Standard Error (SE)         : {se_36:.4f} ms")
print(f"Standardized z for 130 ms   : {z_bar_36:.4f}")
print(f"CLT Theoretical P(mean>130) : {theory_p_36:.6f} ({theory_p_36*100:.3f}%)")
"""))

    # Lab 5: Task 5
    cells.append(nbf.v4.new_markdown_cell(r"""### Task 5: Monte Carlo Simulation (20,000 Samples)
**Problem:** Simulate 20,000 samples of size $n=36$ from a non-Normal, skewed population and compare the empirical probability of $\bar{X} > 130\text{ ms}$ with the theoretical CLT prediction.

#### Modeling a Skewed Computer Science Population:
Real-world API latency is rarely symmetric; it exhibits heavy right-skewing due to cache misses, database locking, and OS scheduling. We model the underlying population using a **Gamma distribution**:
* Shape parameter $k = 16$
* Scale parameter $\theta = 7.5$
* Mean: $\mathbb{E}[X] = k \cdot \theta = 16 \times 7.5 = 120\text{ ms}$
* Variance: $\text{Var}(X) = k \cdot \theta^2 = 16 \times (7.5)^2 = 900 \implies \sigma = \sqrt{900} = 30\text{ ms}$
* Skewness: $\gamma_1 = \frac{2}{\sqrt{k}} = \frac{2}{\sqrt{16}} = +0.50$ (pronounced positive right skew)
"""))

    cells.append(nbf.v4.new_code_cell(r"""n_simulations = 20000

# Generate 20,000 samples of size n=36 from skewed Gamma population
samples_36 = np.random.gamma(shape=16, scale=7.5, size=(n_simulations, n_36))
means_36 = samples_36.mean(axis=1)
sim_p_36 = np.mean(means_36 > 130)

abs_diff_36 = abs(theory_p_36 - sim_p_36)
rel_diff_36 = abs_diff_36 / theory_p_36 * 100

print("--- Lab 5: Task 5 Simulation vs Theory (n = 36) ---")
print(f"Number of simulated batches : {n_simulations:,}")
print(f"CLT Theoretical P(mean>130) : {theory_p_36:.6f}")
print(f"Monte Carlo Simulated P     : {sim_p_36:.6f}")
print(f"Absolute Difference         : {abs_diff_36:.6f}")
print(f"Relative Difference         : {rel_diff_36:.2f}%")
"""))

    # Lab 5: Task 6
    cells.append(nbf.v4.new_markdown_cell(r"""### Task 6: Effect of Sample Size Scaling ($n = 100$)
**Problem:** Repeat the theoretical calculation and 20,000-run simulation with sample size $n = 100$. Explain mathematically and practically how sample size changes the standard error and tail probability.

#### Mathematical Formulation for $n=100$:
1. **Standard Error ($SE_{100}$):**
   $$SE_{100} = \frac{\sigma}{\sqrt{100}} = \frac{30}{10} = 3.000\text{ ms}$$
2. **Standardized $z$-score for 130 ms:**
   $$z_{\bar{X}, 100} = \frac{130 - 120}{3.0} = \frac{10}{3} \approx 3.3333$$
3. **Theoretical Tail Probability:**
   $$P(\bar{X}_{100} > 130) = 1 - \Phi(3.3333) \approx 0.0004291 \quad (\approx 0.043\%)$$

#### Mathematical Explanation of Changes:
* **Standard Error Reduction:** Because $SE = \sigma/\sqrt{n}$, increasing sample size by a factor of $100/36 \approx 2.78$ contracts the standard error by a factor of $\sqrt{36/100} = 6/10 = 0.60$ (a 40% reduction from 5.0 ms to 3.0 ms).
* **Exponential Probability Decay:** Because the threshold 130 ms is fixed, shrinking the standard error shifts the standardized distance from $z = 2.00$ to $z = 3.33$. In Gaussian tails, probability mass decays exponentially with $z^2$:
  $$\frac{P(\bar{X}_{36} > 130)}{P(\bar{X}_{100} > 130)} \approx \frac{0.02275}{0.000429} \approx 53.0$$
  The probability of observing an average response time above 130 ms drops by **over 53 times** (from 2.28% down to 0.043%)!
"""))

    cells.append(nbf.v4.new_code_cell(r"""n_100 = 100
se_100 = sigma / np.sqrt(n_100)
z_bar_100 = (130 - mu) / se_100
theory_p_100 = 1 - norm.cdf(130, loc=mu, scale=se_100)

# Simulate 20,000 samples of size n=100
samples_100 = np.random.gamma(shape=16, scale=7.5, size=(n_simulations, n_100))
means_100 = samples_100.mean(axis=1)
sim_p_100 = np.mean(means_100 > 130)

abs_diff_100 = abs(theory_p_100 - sim_p_100)

# Formulate summary dataframe
df_clt_comparison = pd.DataFrame({
    "Sample Size (n)": [36, 100],
    "Std Error SE (ms)": [se_36, se_100],
    "z-score for 130 ms": [z_bar_36, z_bar_100],
    "Theoretical P(mean>130)": [theory_p_36, theory_p_100],
    "Simulated P(mean>130)": [sim_p_36, sim_p_100],
    "Absolute Error": [abs_diff_36, abs_diff_100]
})

print("--- Comparative Summary: Sample Size Scaling ---")
print(df_clt_comparison.to_string(index=False))
"""))

    # Lab 5: Task 7
    cells.append(nbf.v4.new_markdown_cell(r"""### Task 7: Sampling Distribution Visualizations
We generate comprehensive comparative plots:
1. **Underlying Skewed Population (Gamma)** vs individual normal curve.
2. **Sampling Distribution for $n=36$:** Empirical histogram of 20,000 sample means overlaid with theoretical Normal PDF $\mathcal{N}(120, 5^2)$ and threshold at 130 ms.
3. **Sampling Distribution for $n=100$:** Empirical histogram of 20,000 sample means overlaid with theoretical Normal PDF $\mathcal{N}(120, 3^2)$ and threshold at 130 ms.
4. **Side-by-side Overlay:** Direct comparison illustrating the variance contraction and preservation of the central mean.
"""))

    cells.append(nbf.v4.new_code_cell(r"""fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Plot 1: Underlying Population (Skewed Gamma vs Normal)
x_pop = np.linspace(30, 240, 500)
axes[0].plot(x_pop, gamma.pdf(x_pop, a=16, scale=7.5), 'crimson', lw=2.5, label='Actual Population (Skewed Gamma)')
axes[0].plot(x_pop, norm.pdf(x_pop, loc=120, scale=30), 'gray', lw=1.5, ls='--', label='Theoretical Normal(120, 30^2)')
axes[0].axvline(120, color='black', linestyle=':', label='Population Mean = 120 ms')
axes[0].set_title("Underlying Population (Skewed)")
axes[0].set_xlabel("Individual API Response Time (ms)")
axes[0].set_ylabel("Density")
axes[0].legend(loc='upper right')

# Plot 2: Sampling Distribution n=36
axes[1].hist(means_36, bins=45, density=True, color='skyblue', edgecolor='white', alpha=0.7, label='Simulated Means (n=36)')
x_36 = np.linspace(means_36.min(), means_36.max(), 300)
pdf_36 = norm.pdf(x_36, loc=mu, scale=se_36)
axes[1].plot(x_36, pdf_36, 'navy', lw=2.5, label=f'CLT Normal: N(120, {se_36}^2)')
axes[1].axvline(130, color='darkred', linestyle='--', lw=2, label='Threshold = 130 ms')
axes[1].fill_between(x_36[x_36 >= 130], pdf_36[x_36 >= 130], color='darkred', alpha=0.3, label=f'Tail P={theory_p_36:.3f}')
axes[1].set_title(f"Sampling Distribution (n=36, SE={se_36} ms)")
axes[1].set_xlabel("Sample Mean Response Time (ms)")
axes[1].set_ylabel("Density")
axes[1].legend(loc='upper right')

# Plot 3: Sampling Distribution n=100
axes[2].hist(means_100, bins=45, density=True, color='lightgreen', edgecolor='white', alpha=0.7, label='Simulated Means (n=100)')
x_100 = np.linspace(means_100.min(), means_100.max(), 300)
pdf_100 = norm.pdf(x_100, loc=mu, scale=se_100)
axes[2].plot(x_100, pdf_100, 'darkgreen', lw=2.5, label=f'CLT Normal: N(120, {se_100}^2)')
axes[2].axvline(130, color='darkred', linestyle='--', lw=2, label='Threshold = 130 ms')
axes[2].fill_between(x_100[x_100 >= 130], pdf_100[x_100 >= 130], color='darkred', alpha=0.3, label=f'Tail P={theory_p_100:.4f}')
axes[2].set_title(f"Sampling Distribution (n=100, SE={se_100} ms)")
axes[2].set_xlabel("Sample Mean Response Time (ms)")
axes[2].set_ylabel("Density")
axes[2].legend(loc='upper right')

plt.tight_layout()
plt.show()
"""))

    # Lab 5: Interpretation
    cells.append(nbf.v4.new_markdown_cell(r"""### Lab 5: Required Computer Science Interpretation
*(Connected to the Project Topic: Password Complexity Modulation)*

> **Interpretation (3–5 sentences):**  
> In our Password Complexity Modulation architecture, individual authentication and password verification requests exhibit a pronounced right-skewed response time distribution ($\mu = 120\text{ ms}, \sigma = 30\text{ ms}$) due to adaptive cryptographic key derivation (Argon2id/PBKDF2 iteration tuning based on password entropy) and thread scheduling. By leveraging the Central Limit Theorem, backend site reliability engineers (SREs) can monitor cluster performance by grouping authentication telemetry into batches of size $n=36$, which transforms irregular request spikes into a symmetric, predictable Gaussian distribution ($SE = 5.0\text{ ms}$) with only a $2.28\%$ chance of false positive SLA alerts at the $130\text{ ms}$ threshold. Scaling the monitoring window to $n=100$ contracts the standard error to $3.0\text{ ms}$, driving the probability of exceeding $130\text{ ms}$ down by over $53\times$ to just $0.043\%$. This statistical guarantees allow our authentication service to reliably distinguish genuine cluster degradation or distributed brute-force attacks from natural computational variance without false alarms.
"""))

    # ---------------------------------------------------------
    # PART II: LABORATORY WORK 6
    # ---------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell(r"""# =========================================================
# PART II: LABORATORY WORK 6
## Continuous Probability Distributions Using Python
# =========================================================

### Learning Outcomes
1. Generate random samples from continuous distributions: **Uniform**, **Exponential**, and **Normal**.
2. Evaluate and interpret Probability Density Functions (PDF) and Cumulative Distribution Functions (CDF).
3. Compute exact theoretical probabilities analytically and verify them using Monte Carlo simulations.
4. Model realistic Computer Science problems, particularly network latency, randomized backoff, and brute-force inter-arrival times.
5. Execute an end-to-end applied CS model tailored to the **Password Complexity Modulation** domain.

---

### Core Theoretical Principles
* For any continuous random variable $X$, the probability of taking any single exact point is zero: $P(X = x) = 0$.
* Probability is defined over intervals as the area under the PDF curve $f(x)$:
  $$P(a \le X \le b) = \int_{a}^{b} f(x) \, dx = F(b) - F(a)$$
* The Cumulative Distribution Function (CDF) gives $F(x) = P(X \le x)$.

| Distribution | Typical Computer Science Application | Parameters | PDF Formula $f(x)$ |
| :--- | :--- | :--- | :--- |
| **Uniform** | Randomized backoff delay, jitter against timing attacks | $a, b$ | $\frac{1}{b-a}, \; x \in [a, b]$ |
| **Exponential** | Inter-arrival time of brute-force login attempts, time to failure | $\lambda$ (rate) | $\lambda e^{-\lambda x}, \; x \ge 0$ |
| **Normal** | Processing time of cryptographic hashing around target SLA | $\mu, \sigma$ | $\frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$ |
"""))

    # Lab 6: Task 1
    cells.append(nbf.v4.new_markdown_cell(r"""### Task 1: Uniform Distribution (Randomized Algorithm Delay)
**Main Task Problem:** A randomized backoff algorithm chooses a delay uniformly between 2 and 8 milliseconds:
$$X \sim \text{Uniform}(2, 8)$$
Find $P(3 \le X \le 5)$ analytically, simulate 10,000 delays, compare simulation with theory, and plot the PDF.

#### Analytical Derivation:
* Parameters: $a = 2$, $b = 8$. Width of support: $b - a = 8 - 2 = 6\text{ ms}$.
* PDF: $f(x) = \frac{1}{6}$ for $2 \le x \le 8$.
* Interval of interest $[3, 5]$ width: $5 - 3 = 2\text{ ms}$.
* Probability:
  $$P(3 \le X \le 5) = \int_{3}^{5} \frac{1}{6} \, dx = \frac{5 - 3}{8 - 2} = \frac{2}{6} = \frac{1}{3} \approx 0.333333$$

---

#### Student Extension for Task 1:
**Extension Problem:** Change the interval to $1 - 10\text{ ms}$ ($X \sim \text{Uniform}(1, 10)$). Find and simulate $P(X > 7)$.
* Parameters: $a = 1$, $b = 10$. Width: $b - a = 10 - 1 = 9\text{ ms}$.
* PDF: $f(x) = \frac{1}{9}$ for $1 \le x \le 10$.
* Analytical Probability:
  $$P(X > 7) = \int_{7}^{10} \frac{1}{9} \, dx = \frac{10 - 7}{10 - 1} = \frac{3}{9} = \frac{1}{3} \approx 0.333333$$
"""))

    cells.append(nbf.v4.new_code_cell(r"""# --- Task 1: Main Problem ---
a1, b1 = 2, 8
n_draws = 10000

samples_unif1 = np.random.uniform(a1, b1, n_draws)
sim_prob_unif1 = np.mean((samples_unif1 >= 3) & (samples_unif1 <= 5))
theory_prob_unif1 = (5 - 3) / (b1 - a1)

print("--- Lab 6 Task 1: Main Problem (Uniform 2-8 ms) ---")
print(f"Theoretical P(3 <= X <= 5) : {theory_prob_unif1:.6f}")
print(f"Simulated P(3 <= X <= 5)   : {sim_prob_unif1:.6f}")
print(f"Absolute Difference        : {abs(theory_prob_unif1 - sim_prob_unif1):.6f}")

# --- Task 1: Student Extension ---
a_ext, b_ext = 1, 10
samples_unif_ext = np.random.uniform(a_ext, b_ext, n_draws)
sim_prob_unif_ext = np.mean(samples_unif_ext > 7)
theory_prob_unif_ext = (b_ext - 7) / (b_ext - a_ext)

print("\n--- Lab 6 Task 1: Student Extension (Uniform 1-10 ms) ---")
print(f"Theoretical P(X > 7)       : {theory_prob_unif_ext:.6f}")
print(f"Simulated P(X > 7)         : {sim_prob_unif_ext:.6f}")
print(f"Absolute Difference        : {abs(theory_prob_unif_ext - sim_prob_unif_ext):.6f}")

# Visualization of Task 1 & Extension
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4.5))

# Plot Main Problem
x_u1 = np.linspace(0, 10, 400)
pdf_u1 = uniform.pdf(x_u1, loc=a1, scale=b1-a1)
ax1.plot(x_u1, pdf_u1, 'b-', lw=2.5, label='Uniform(2, 8) PDF')
ax1.hist(samples_unif1, bins=30, density=True, color='skyblue', alpha=0.4, label='10k Simulation')
ax1.fill_between(x_u1, pdf_u1, where=((x_u1>=3) & (x_u1<=5)), color='navy', alpha=0.3, label=f'P(3<=X<=5)={theory_prob_unif1:.3f}')
ax1.set_title("Task 1: Uniform Delay [2, 8] ms")
ax1.set_xlabel("Delay (ms)")
ax1.set_ylabel("Density")
ax1.legend()

# Plot Student Extension
x_uext = np.linspace(0, 11, 400)
pdf_uext = uniform.pdf(x_uext, loc=a_ext, scale=b_ext-a_ext)
ax2.plot(x_uext, pdf_uext, 'g-', lw=2.5, label='Uniform(1, 10) PDF')
ax2.hist(samples_unif_ext, bins=30, density=True, color='lightgreen', alpha=0.4, label='10k Simulation')
ax2.fill_between(x_uext, pdf_uext, where=(x_uext>7), color='darkgreen', alpha=0.3, label=f'P(X>7)={theory_prob_unif_ext:.3f}')
ax2.set_title("Student Extension: Uniform Delay [1, 10] ms")
ax2.set_xlabel("Delay (ms)")
ax2.set_ylabel("Density")
ax2.legend()

plt.tight_layout()
plt.show()
"""))

    # Lab 6: Task 2
    cells.append(nbf.v4.new_markdown_cell(r"""### Task 2: Exponential Distribution (Request Arrival & Attack Modeling)
**Main Task Problem:** A web authentication service receives requests at an average rate of $\lambda = 4\text{ requests per minute}$. Let $X$ be the waiting time (in minutes) until the next request:
$$X \sim \text{Exponential}(\lambda = 4)$$
$$P(X \le t) = 1 - e^{-\lambda t}$$
Find the probability that the next request arrives within 15 seconds.

#### Analytical Derivation:
1. Convert 15 seconds to minutes:
   $$t = \frac{15}{60} = 0.25\text{ minutes}$$
2. Evaluate CDF:
   $$P(X \le 0.25) = 1 - e^{-4 \times 0.25} = 1 - e^{-1.0} = 1 - \frac{1}{e} \approx 0.63212056 \quad (\approx 63.21\%)$$

---

#### Student Extension for Task 2:
**Extension Problem:** Find $P(X > 30\text{ seconds})$ analytically and verify the result with 10,000 simulated draws.
1. Convert 30 seconds to minutes:
   $$t = \frac{30}{60} = 0.50\text{ minutes}$$
2. Evaluate survival function $P(X > t) = 1 - P(X \le t) = e^{-\lambda t}$:
   $$P(X > 0.50) = e^{-4 \times 0.50} = e^{-2.0} = \frac{1}{e^2} \approx 0.13533528 \quad (\approx 13.53\%)$$
"""))

    cells.append(nbf.v4.new_code_cell(r"""# --- Task 2: Main Problem ---
lam = 4
scale_exp = 1.0 / lam
t_main = 15.0 / 60.0  # 0.25 min

theory_exp_main = expon.cdf(t_main, scale=scale_exp)
samples_exp = np.random.exponential(scale=scale_exp, size=10000)
sim_exp_main = np.mean(samples_exp <= t_main)

print("--- Lab 6 Task 2: Main Problem (Exponential lambda=4) ---")
print(f"Theoretical P(X <= 15s)    : {theory_exp_main:.6f}")
print(f"Simulated P(X <= 15s)      : {sim_exp_main:.6f}")
print(f"Absolute Difference        : {abs(theory_exp_main - sim_exp_main):.6f}")

# --- Task 2: Student Extension ---
t_ext = 30.0 / 60.0  # 0.50 min
theory_exp_ext = 1 - expon.cdf(t_ext, scale=scale_exp)
sim_exp_ext = np.mean(samples_exp > t_ext)

print("\n--- Lab 6 Task 2: Student Extension (P(X > 30s)) ---")
print(f"Theoretical P(X > 30s)     : {theory_exp_ext:.6f}")
print(f"Simulated P(X > 30s)       : {sim_exp_ext:.6f}")
print(f"Absolute Difference        : {abs(theory_exp_ext - sim_exp_ext):.6f}")

# Visualizations
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4.5))

x_exp = np.linspace(0, 1.5, 400)
pdf_exp = expon.pdf(x_exp, scale=scale_exp)

# Plot Main Problem
ax1.plot(x_exp, pdf_exp, 'crimson', lw=2.5, label='Exponential(lambda=4) PDF')
ax1.hist(samples_exp, bins=40, density=True, color='pink', alpha=0.4, label='10k Simulation')
ax1.fill_between(x_exp, pdf_exp, where=(x_exp <= t_main), color='red', alpha=0.3, label=f'P(X<=15s)={theory_exp_main:.3f}')
ax1.set_title("Task 2: Waiting Time <= 15 seconds")
ax1.set_xlabel("Waiting Time (minutes)")
ax1.set_ylabel("Density")
ax1.legend()

# Plot Student Extension
ax2.plot(x_exp, pdf_exp, 'purple', lw=2.5, label='Exponential(lambda=4) PDF')
ax2.hist(samples_exp, bins=40, density=True, color='plum', alpha=0.4, label='10k Simulation')
ax2.fill_between(x_exp, pdf_exp, where=(x_exp > t_ext), color='purple', alpha=0.3, label=f'P(X>30s)={theory_exp_ext:.3f}')
ax2.set_title("Student Extension: Waiting Time > 30 seconds")
ax2.set_xlabel("Waiting Time (minutes)")
ax2.set_ylabel("Density")
ax2.legend()

plt.tight_layout()
plt.show()
"""))

    # Lab 6: Task 3
    cells.append(nbf.v4.new_markdown_cell(r"""### Task 3: Normal Distribution (API Response Time)
**Main Task Problem:** Suppose authentication API response time is Normally distributed with mean $\mu = 120\text{ ms}$ and standard deviation $\sigma = 20\text{ ms}$:
$$X \sim \mathcal{N}(\mu = 120, \sigma = 20)$$
Find the probability that a request finishes in less than $150\text{ ms}$ ($P(X < 150)$).

#### Analytical Derivation:
1. Standardize $x = 150$:
   $$z = \frac{x - \mu}{\sigma} = \frac{150 - 120}{20} = \frac{30}{20} = 1.500$$
2. Compute $\Phi(1.5)$:
   $$P(X < 150) = \Phi(1.500) \approx 0.9331928 \quad (\approx 93.32\%)$$
*Interpretation:* Under standard workload, about $93.32\%$ of password verification requests finish in under $150\text{ ms}$.

---

#### Student Extension for Task 3:
**Extension Problem:** Find $P(100 \le X \le 140\text{ ms})$. Calculate the $z$-scores for 100 and 140, and interpret them.
1. Standardize both boundary values:
   $$z_{100} = \frac{100 - 120}{20} = \frac{-20}{20} = -1.000$$
   $$z_{140} = \frac{140 - 120}{20} = \frac{+20}{20} = +1.000$$
2. Calculate interval probability:
   $$P(100 \le X \le 140) = \Phi(+1.000) - \Phi(-1.000) = 0.8413447 - 0.1586553 = 0.6826895 \quad (\approx 68.27\%)$$
*Interpretation:* This interval represents exactly $[\mu - \sigma, \mu + \sigma]$ (one standard deviation around the mean). By the empirical 68-95-99.7 rule, approximately $68.27\%$ of all authentication attempts fall within this operational band.
"""))

    cells.append(nbf.v4.new_code_cell(r"""mu_norm = 120
sigma_norm = 20

# Main Problem
x0 = 150
z0 = (x0 - mu_norm) / sigma_norm
prob_main_norm = norm.cdf(x0, loc=mu_norm, scale=sigma_norm)

print("--- Lab 6 Task 3: Main Problem (Normal mu=120, sigma=20) ---")
print(f"Standardized z-score for 150 ms : {z0:.4f}")
print(f"P(X < 150 ms)                   : {prob_main_norm:.6f} ({prob_main_norm*100:.2f}%)")

# Student Extension
x_low, x_high = 100, 140
z_low = (x_low - mu_norm) / sigma_norm
z_high = (x_high - mu_norm) / sigma_norm
prob_ext_norm = norm.cdf(x_high, loc=mu_norm, scale=sigma_norm) - norm.cdf(x_low, loc=mu_norm, scale=sigma_norm)

print("\n--- Lab 6 Task 3: Student Extension (100 <= X <= 140) ---")
print(f"z-score for 100 ms (lower bound): {z_low:.4f}")
print(f"z-score for 140 ms (upper bound): {z_high:.4f}")
print(f"P(100 <= X <= 140 ms)           : {prob_ext_norm:.6f} ({prob_ext_norm*100:.2f}%)")

# Visualizations
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4.5))

x_axis = np.linspace(50, 190, 500)
y_pdf = norm.pdf(x_axis, loc=mu_norm, scale=sigma_norm)

# Main Plot
ax1.plot(x_axis, y_pdf, 'b-', lw=2.5, label='Normal(120, 20^2) PDF')
ax1.axvline(x0, color='darkred', linestyle='--', lw=2, label='Threshold = 150 ms')
ax1.fill_between(x_axis, y_pdf, where=(x_axis <= x0), color='skyblue', alpha=0.4, label=f'P(X<150)={prob_main_norm:.3f}')
ax1.set_title("Task 3: P(X < 150 ms)")
ax1.set_xlabel("Response Time (ms)")
ax1.set_ylabel("Density")
ax1.legend()

# Extension Plot
ax2.plot(x_axis, y_pdf, 'darkgreen', lw=2.5, label='Normal(120, 20^2) PDF')
ax2.axvline(x_low, color='orange', linestyle=':', lw=2, label='z = -1.0 (100 ms)')
ax2.axvline(x_high, color='orange', linestyle=':', lw=2, label='z = +1.0 (140 ms)')
ax2.fill_between(x_axis, y_pdf, where=((x_axis >= x_low) & (x_axis <= x_high)), color='lightgreen', alpha=0.4, label=f'P(100<=X<=140)={prob_ext_norm:.3f}')
ax2.set_title("Student Extension: +/- 1 Sigma Band")
ax2.set_xlabel("Response Time (ms)")
ax2.set_ylabel("Density")
ax2.legend()

plt.tight_layout()
plt.show()
"""))

    # Lab 6: Task 4
    cells.append(nbf.v4.new_markdown_cell(r"""### Task 4: Compare Theory and Simulation (Monte Carlo Convergence)
**Problem:** Model server latency as $X \sim \mathcal{N}(80, 12^2)$. Estimate $P(X > 100)$ using both SciPy analytical integration and $50,000$ simulated observations. Answer theoretical questions and test convergence scaling.

#### Analytical Calculation:
$$z = \frac{100 - 80}{12} = \frac{20}{12} \approx 1.66667$$
$$P(X > 100) = 1 - \Phi(1.66667) \approx 0.04779035 \quad (\approx 4.78\%)$$
"""))

    cells.append(nbf.v4.new_code_cell(r"""mu_lat = 80
sigma_lat = 12
threshold_lat = 100

theory_lat = 1 - norm.cdf(threshold_lat, loc=mu_lat, scale=sigma_lat)
samples_lat = np.random.normal(mu_lat, sigma_lat, 50000)
simulation_lat = np.mean(samples_lat > threshold_lat)
abs_diff_lat = abs(theory_lat - simulation_lat)

print("--- Lab 6 Task 4: Theory vs Simulation (50,000 draws) ---")
print(f"Theoretical P(X > 100) : {theory_lat:.6f}")
print(f"Simulated P(X > 100)   : {simulation_lat:.6f}")
print(f"Absolute Difference    : {abs_diff_lat:.6f}")
print(f"Relative Error         : {(abs_diff_lat / theory_lat)*100:.2f}%")
"""))

    # Lab 6: Task 4 Questions
    cells.append(nbf.v4.new_markdown_cell(r"""#### Required Questions & In-Depth Answers for Task 4:

**Question 1: Why will the simulated value not be exactly equal to the theoretical value?**  
> **Answer:** Monte Carlo simulation is an empirical sampling estimator based on a finite number of pseudo-random draws ($N = 50,000$). Each draw is an independent Bernoulli trial with success probability $p \approx 0.04779$. By the Central Limit Theorem applied to sample proportions, the empirical estimator $\hat{p} = \frac{1}{N} \sum_{i=1}^N \mathbb{I}(X_i > 100)$ has a standard error equal to:
> $$\sigma_{\hat{p}} = \sqrt{\frac{p(1 - p)}{N}} = \sqrt{\frac{0.04779 \times 0.95221}{50000}} \approx 0.00095$$
> Because this variance is strictly non-zero for any finite $N$, stochastic fluctuations naturally produce small differences between $\hat{p}$ and $p$.

**Question 2: What happens to the difference if the number of simulations increases from 1,000 to 100,000?**  
> **Answer:** According to the **Strong Law of Large Numbers (SLLN)**, the empirical mean converges almost surely to the expected value: $\hat{p} \xrightarrow{a.s.} p$ as $N \to \infty$. The expected absolute estimation error shrinks at a rate proportional to $1/\sqrt{N}$:
> $$\text{Error}(N) \propto \frac{1}{\sqrt{N}}$$
> Increasing sample size from $N_1 = 1,000$ to $N_2 = 100,000$ increases the number of trials by a factor of 100. Consequently, the sampling error is reduced by a factor of $\sqrt{100,000 / 1,000} = \sqrt{100} = 10$ (a 10-fold precision improvement).

**Question 3: Would a Normal model always be appropriate for latency? Give one reason why not.**  
> **Answer:** No, a Normal distribution is fundamentally flawed for modeling latency for two key reasons:
> 1. **Negative Support:** The Normal distribution has infinite tails $(-\infty, +\infty)$, meaning it assigns positive probability to negative response times ($X < 0$), which is physically impossible in computer systems.
> 2. **Heavy-Tailed Skewness:** Real server latency exhibits strong right skewness and extreme tail latencies (e.g., p99 and p99.9 spikes due to GC pauses, cache misses, thread contention, and TCP packet retransmissions). Log-Normal, Gamma, or Weibull distributions provide far superior models for real systems.
"""))

    # Lab 6: Task 4 Optional Challenge
    cells.append(nbf.v4.new_markdown_cell(r"""#### Optional Challenge: Error Convergence Analysis Across Sample Sizes
We repeat the experiment for sample sizes $N \in [100, 1000, 10000, 100000]$. To ensure robust measurements, we run 20 independent trials for each sample size, compute the mean absolute error, and plot against the theoretical $\mathcal{O}(1/\sqrt{N})$ decay curve on a log-log scale.
"""))

    cells.append(nbf.v4.new_code_cell(r"""sample_sizes = [100, 1000, 10000, 100000]
trials_per_size = 25
mean_errors = []

for n_size in sample_sizes:
    trial_errors = []
    for _ in range(trials_per_size):
        s_draw = np.random.normal(mu_lat, sigma_lat, n_size)
        sim_p = np.mean(s_draw > threshold_lat)
        trial_errors.append(abs(theory_lat - sim_p))
    mean_errors.append(np.mean(trial_errors))

# Plot Error Scaling
plt.figure(figsize=(8, 5))
plt.loglog(sample_sizes, mean_errors, 'ro-', lw=2.5, markersize=8, label='Empirical Mean Absolute Error')

# Theoretical 1/sqrt(N) reference curve
ref_curve = mean_errors[0] * np.sqrt(sample_sizes[0]) / np.sqrt(sample_sizes)
plt.loglog(sample_sizes, ref_curve, 'k--', lw=1.5, label=r'Theoretical Decay $\mathcal{O}(1/\sqrt{N})$')

plt.title("Monte Carlo Error Convergence: Rate = O(1/sqrt(N))")
plt.xlabel("Sample Size N (log scale)")
plt.ylabel("Mean Absolute Error (log scale)")
plt.grid(True, which="both", ls=":")
plt.legend()
plt.show()

for n_size, err in zip(sample_sizes, mean_errors):
    print(f"Sample Size N = {n_size:<7} | Mean Absolute Error = {err:.6f}")
"""))

    # Lab 6: Final Applied Task
    cells.append(nbf.v4.new_markdown_cell(r"""### Task 5 / Final Applied Task: Password Complexity Modulation Service
*(Full Compliance with 7-Point Assessment Rubric)*

We model a realistic Computer Science problem directly rooted in our project:
**Scenario Selected:** *Processing time of a stable authentication service around a target under Password Complexity Modulation.*

#### 1. Definition of Random Variable $X$
Let $X$ be the continuous random variable representing the CPU processing time (in milliseconds) required by our authentication backend to evaluate password entropy, modulate cryptographic work factors (Argon2id time and memory cost), and execute the key derivation function for an incoming login request.

#### 2. Selected Distribution and Parameters
$$X \sim \mathcal{N}(\mu = 250\text{ ms}, \sigma = 25\text{ ms})$$
* **$\mu = 250\text{ ms}$:** The calibrated target latency deliberately introduced by our complexity-modulating key derivation function to thwart offline brute-force dictionary attacks while preserving interactive user experience.
* **$\sigma = 25\text{ ms}$:** The standard deviation reflecting memory bandwidth fluctuations and cryptographic thread scheduling.

#### 3. One Probability Question
> *What is the probability that a legitimate user's authentication request encounters an abnormally high processing latency exceeding $300\text{ ms}$ ($P(X > 300\text{ ms})$), which would trigger an asynchronous client-side retry warning?*

#### 4. Mathematical Answer
1. Standardize the threshold $x = 300\text{ ms}$:
   $$z = \frac{x - \mu}{\sigma} = \frac{300 - 250}{25} = \frac{50}{25} = 2.000$$
2. Compute the upper tail probability using the standard Normal CDF:
   $$P(X > 300) = 1 - \Phi(2.000) = 1 - 0.9772499 = 0.0227501 \quad (\approx 2.28\%)$$

---

#### 5 & 6. Python Calculation, Simulation, and Visualization
We compute the exact analytical probability and run $50,000$ Monte Carlo simulations, plotting the distribution with shaded rejection region and overlaid empirical data.
"""))

    cells.append(nbf.v4.new_code_cell(r"""mu_applied = 250
sigma_applied = 25
threshold_applied = 300

# 1. Theoretical calculation
z_applied = (threshold_applied - mu_applied) / sigma_applied
theory_applied = 1 - norm.cdf(threshold_applied, loc=mu_applied, scale=sigma_applied)

# 2. Monte Carlo Simulation (50,000 runs)
n_runs_applied = 50000
sim_samples_applied = np.random.normal(mu_applied, sigma_applied, n_runs_applied)
sim_applied = np.mean(sim_samples_applied > threshold_applied)

print("--- Final Applied Task: Password Verification Latency Model ---")
print(f"Target Mean Latency (mu)      : {mu_applied} ms")
print(f"Standard Deviation (sigma)    : {sigma_applied} ms")
print(f"Timeout Threshold (x)         : {threshold_applied} ms")
print(f"Standardized z-score          : {z_applied:.4f}")
print(f"Theoretical P(X > 300 ms)     : {theory_applied:.6f} ({theory_applied*100:.3f}%)")
print(f"Simulated P(X > 300 ms)       : {sim_applied:.6f} ({sim_applied*100:.3f}%)")
print(f"Absolute Difference           : {abs(theory_applied - sim_applied):.6f}")

# 3. Visualization
plt.figure(figsize=(10, 5))
x_grid = np.linspace(160, 340, 500)
pdf_grid = norm.pdf(x_grid, loc=mu_applied, scale=sigma_applied)

# Normalized empirical histogram
plt.hist(sim_samples_applied, bins=50, density=True, color='skyblue', edgecolor='white', alpha=0.6, label='50k Simulated Auth Requests')
# Theoretical Gaussian curve
plt.plot(x_grid, pdf_grid, 'darkblue', lw=2.5, label=f'N(250, 25^2) Theoretical PDF')

# Threshold line and shaded tail area
plt.axvline(threshold_applied, color='crimson', linestyle='--', lw=2.5, label=f'Retry Threshold (300 ms, z={z_applied:.1f})')
plt.fill_between(x_grid, pdf_grid, where=(x_grid >= threshold_applied), color='crimson', alpha=0.4, label=f'Tail P(X > 300) = {theory_applied:.3f}')

plt.title("Applied Model: Password Complexity Verification Latency Distribution", fontsize=13)
plt.xlabel("Authentication Latency (ms)", fontsize=11)
plt.ylabel("Probability Density", fontsize=11)
plt.legend(loc='upper right')
plt.grid(True, linestyle=':')
plt.show()
"""))

    # Final Applied Task Interpretation
    cells.append(nbf.v4.new_markdown_cell(r"""#### 7. Interpretation in Computer Science Context
> **Interpretation (2–3 sentences):**  
> In our Password Complexity Modulation architecture, calibrating the cryptographic work factor to a mean latency of $250\text{ ms}$ with $\sigma = 25\text{ ms}$ ensures that exactly $97.72\%$ of legitimate authentications complete within the $300\text{ ms}$ UX responsiveness budget, leaving only a negligible $2.28\%$ probability of client-side retries. This tight bounded variance simultaneously thwarts timing side-channel attacks by keeping verification times consistent and neutralizes offline GPU-accelerated dictionary attacks by enforcing non-trivial computation per attempt. Network telemetry systems can safely flag traffic streams exceeding the $300\text{ ms}$ threshold at rates above $2.3\%$ as active distributed denial-of-service (DDoS) or brute-force credential stuffing attempts.
"""))

    # ---------------------------------------------------------
    # PART III: SUMMARY & CONCLUSION
    # ---------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell(r"""# =========================================================
# PART III: CONCLUSION & SYNTHESIS
# =========================================================

### Key Takeaways
1. **Central Limit Theorem in Production Systems:**  
   Regardless of how irregular, skewed, or bursty individual server latencies are, the distribution of batch sample means $\bar{X}_n$ converges rapidly to a Gaussian distribution once $n \ge 30$. This provides a firm mathematical basis for batch-level SLA monitoring.
2. **Standard Error Dynamics:**  
   Standard error scales as $\sigma / \sqrt{n}$. Expanding the aggregation window from $n=36$ to $n=100$ lowers the standard error by $40\%$ and drives tail violation probabilities down exponentially (by a factor of $53\times$), demonstrating the power of larger monitoring windows for reliable anomaly detection.
3. **Continuous Distribution Selection:**  
   * **Uniform:** Models artificial jitter and randomized backoff windows.
   * **Exponential:** Models inter-arrival times of incoming brute-force requests under constant arrival rates.
   * **Normal:** Models bounded CPU execution times around target cryptographic work factors.
4. **Computational Verification:**  
   Across all laboratory experiments, Monte Carlo simulations with $10,000$ to $50,000$ draws converged precisely to the theoretical integrals, confirming the analytical models with estimation error decaying at the expected $\mathcal{O}(1/\sqrt{N})$ rate.
"""))

    nb.cells = cells
    return nb

if __name__ == "__main__":
    print("Building notebook structure...")
    nb = create_lab_notebook()
    notebook_path = r"D:\downloads\MatStat\Lab5-6MatStat.ipynb"

    print("Executing notebook cells to embed outputs and plots...")
    client = NotebookClient(nb, timeout=600, kernel_name='python3')
    client.execute()

    print(f"Writing executed notebook to {notebook_path}...")
    with open(notebook_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

    print("Successfully built and saved Lab5-6MatStat.ipynb with all outputs!")


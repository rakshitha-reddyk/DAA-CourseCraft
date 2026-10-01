# 🎓 CourseCraft: Student Course Selection Optimizer

An algorithmic solution to eliminate course registration stress by generating 100% conflict-free, prerequisite-valid semester schedules using graph theory and constraint programming.

---

## 🧠 DAA Problem & Approach

### Problem Formulation
Course selection is a multi-objective constraint optimization problem. Students face:
1. **Hard Constraints:** Topological prerequisites, credit limits ($C_{\text{min}} \le \text{Credits} \le C_{\text{max}}$), and zero time slot collisions.
2. **Combinatorial Complexity:** Exponential schedule permutations when selecting across multiple elective sections.

### Hybrid DAA Technique
1. **Phase 1 — Prerequisites Graph Filtering (DAG):**
   * Uses Directed Acyclic Graph (DAG) logic to filter eligible courses in $\mathcal{O}(V + E)$ time.
   * Ensures courses with unfulfilled prerequisites are pruned prior to schedule generation.
2. **Phase 2 — Constraint Satisfaction Backtracking (CSP):**
   * Implements recursive backtracking with early branch pruning.
   * Immediately drops search paths that introduce time slot collisions on the same day/time window.

---

## ⏱️ Complexity Analysis

| Algorithm Phase | Approach | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- |
| **Prerequisite Verification** | DAG Topological Graph Check | $\mathcal{O}(V + E)$ | $\mathcal{O}(V + E)$ |
| **Schedule Generation** | Backtracking CSP Solver | $\mathcal{O}(S^K)$ Worst-Case / $\mathcal{O}(K \log K)$ Pruned | $\mathcal{O}(K)$ Rec Stack |

*Where $V$ = total courses, $E$ = prerequisite links, $K$ = eligible courses, $S$ = sections per course.*

---

## 🚀 How to Run locally

### 1. Installation
```bash
# Clone the repository
git clone [https://github.com/](https://github.com/)<your-username>/DAA-CourseCraft.git
cd DAA-CourseCraft

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
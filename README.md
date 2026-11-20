# Numerical Methods – Linear Systems

A small [Streamlit](https://streamlit.io) app that solves systems of linear equations (3, 4 or 5 unknowns) with four iterative methods and shows every iteration in a lecture-style table.

**Live app:** _paste your Streamlit link here after deploying_

---

## Methods

| Method | How it works | Stops when |
|---|---|---|
| **Jacobi** | every new value is computed from the previous iteration | max \|change\| < accuracy |
| **Gauss–Seidel** | uses the new values as soon as they are computed | max \|change\| < accuracy |
| **Relaxation** | each step updates only the variable with the largest residual | max \|residual\| ≤ accuracy |
| **SOR** | computes the new values, then over-relaxes: `x = x_old + ω (x_new − x_old)` | max \|change\| ≤ accuracy |

## How to use

1. Pick the **method** and the **number of variables** (3, 4 or 5).
2. Type each equation **solved for its own variable**, using `a b c d e`.

   | System | What you type |
   |---|---|
   | `10a + b + 2c = 13` | `A =` `1.3-.1*b-.2*c` |
   | `2a + 10b + 3c = 15` | `B =` `1.5-.2*a-.3*c` |
   | `5a − 3b + 10c = 12` | `C =` `1.2-.5*a+.3*b` |

   Allowed: `+ - * / **` (and `^` for powers), brackets, `sqrt sin cos tan exp log pi`.
   You can also paste `A=1.3-.1*b-.2*c`, the `A=` part is ignored.
3. Set the **starting guess**, **max iterations**, **accuracy** and **digits** (and **ω** for SOR).
4. Press **Solve**.

If an equation has a typo (for example an unknown name), the app shows an error instead of crashing.

## Reading the table

- **x₁ … xₙ** – the values at iteration `k`.
- **Relaxation:** the right block is the residual `r`. The red number is the variable relaxed next, together with its (largest) residual.
- **Jacobi / Seidel / SOR:** the right block is `Δx`, the change since the previous iteration.
- The boxed last row is the **solution**, and the oval shows the stopping condition that was met.
- If the method does not reach the accuracy within the max iterations, a warning is shown instead.

## Default example

```
A = 1.3 − .1B − .2C
B = 1.5 − .2A − .3C
C = 1.2 − .5A + .3B
```

Exact solution: A = B = C = 1.

## Run locally

```bash
git clone https://github.com/M0hamed-A-hmed/program2.git
cd program2
pip install -r requirements.txt
streamlit run app.py
```

`python app.py` also works – it starts Streamlit for you.

## Deploy on Streamlit Community Cloud

1. Push this repo to GitHub (`app.py` and `requirements.txt` in the root).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **Create app** → **Yup, I have an app**.
4. Repository: `M0hamed-A-hmed/program2` · Branch: `main` · Main file path: `app.py`.
5. Click **Deploy**.

Every `git push` to `main` updates the live app automatically.

## Project structure

```
program2/
├── app.py             # the whole app (methods + page)
├── requirements.txt   # dependencies
├── README.md
└── .gitignore
```

## Notes

- Jacobi, Seidel and SOR only converge for systems that converge under the iteration (for example strictly diagonally dominant ones). Otherwise you will get "Maximum iterations reached".
- The equations are entered in the *solved* form (`x = c − …`), the same form used in the lecture (`TX + C = R`).

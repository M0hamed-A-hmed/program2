import sys
import math
import subprocess
from html import escape

# colours / look of the table (same idea as the lecture slide)
CSS = """
<style>
table.nt{--hd:#6fa8c8;--bd:#a5d3c3;--tx:#1b3a5c;--red:#e00000;--box:#1565c0;
 width:100%;border-collapse:separate;border-spacing:0;text-align:center;
 font-family:'Cambria Math',Cambria,'Times New Roman',serif;font-size:1.05rem}
table.nt th{background:var(--hd);color:#10253f;padding:10px 6px;font-weight:600;border:none}
table.nt td{background:var(--bd);color:var(--tx);padding:7px 6px;border:none;border-top:1px solid rgba(255,255,255,.6)}
table.nt td.red{color:var(--red);font-weight:700}
table.nt td.bx{border-top:2px solid var(--box);border-bottom:2px solid var(--box)}
table.nt td.bl{border-left:2px solid var(--box)}
table.nt td.br{border-right:2px solid var(--box)}
table.nt td.bb{border:2px solid var(--box)}
table.nt .gap{background:transparent;border:none;width:14px;padding:0}
table.nt tr.foot td{background:transparent;border:none;padding-top:16px}
table.nt .oval{display:inline-block;border:2px solid var(--box);border-radius:999px;
 padding:3px 28px;color:var(--red);font-weight:700}
</style>
""".replace("\n", "")


def _fmt(v, digits):
    v = round(v, digits)
    return f"{(v if v else 0.0):.{digits}f}"      # no "-0.0000"


def _table(rows, n, digits, second, acc, cmp, converged):
    sub = lambda i: f"<sub>{i+1}</sub>"
    head = "<th>k</th>"
    head += "".join(f"<th>x{sub(i)}<sup>(k)</sup></th>" for i in range(n))
    head += '<th class="gap"></th>'
    head += "".join(f"<th>{second}{sub(i)}<sup>(k)</sup></th>" for i in range(n))

    last = rows[-1][0]
    body = ""
    for k, x, s, pick in rows:
        final = converged and k == last
        tds = f"<td>{k}</td>"

        # x block  (red = the variable that will be relaxed next)
        for j, v in enumerate(x):
            cls = []
            if pick == j:
                cls.append("red")
            if final:
                cls.append("bx")
                if j == 0:
                    cls.append("bl")
                if j == n - 1:
                    cls.append("br")
            tds += f'<td class="{" ".join(cls)}">{_fmt(v, digits)}</td>'

        tds += '<td class="gap"></td>'

        # r / change block
        if s is None:
            tds += "<td>&mdash;</td>" * n
        else:
            big = max(range(n), key=lambda j: abs(s[j]))
            for j, v in enumerate(s):
                cls = []
                if pick == j:
                    cls.append("red")
                if final and j == big:
                    cls.append("bb")
                tds += f'<td class="{" ".join(cls)}">{_fmt(v, digits)}</td>'

        body += f"<tr>{tds}</tr>"

    if converged:
        label = escape(f"{cmp} {acc:g}")
        body += ('<tr class="foot"><td></td>'
                 f'<td colspan="{n}"><span class="oval">Solution</span></td>'
                 '<td class="gap"></td>'
                 f'<td colspan="{n}"><span class="oval">{label}</span></td></tr>')

    return (f'<div style="overflow-x:auto"><table class="nt"><thead><tr>{head}</tr></thead>'
            f'<tbody>{body}</tbody></table></div>')


def start(file, title):
    """
    First thing in a method file.
      python file.py          -> re-launches itself with streamlit (opens the browser)
      streamlit run file.py   -> sets the page title and carries on
    """
    try:
        import streamlit as st
        from streamlit.runtime import exists
    except ImportError:
        print("Streamlit is not installed (pip install streamlit)  ->  terminal output only")
        return

    if not exists():                                   # started with plain python
        try:
            subprocess.run([sys.executable, "-m", "streamlit", "run", file])
        except KeyboardInterrupt:
            pass
        sys.exit()

    st.set_page_config(page_title=title, layout="wide")
    st.title(title)


NAMES = "abcde"

# default systems that fill the input fields
SYSTEMS = {
    3: ["1.3-.1*b-.2*c",
        "1.5-.2*a-.3*c",
        "1.2-.5*a+.3*b"],
    4: ["1.3-.1*b-.2*c+.1*d",
        "1.5-.2*a-.3*c-.1*d",
        "1.2-.5*a+.3*b+.1*d",
        "1.0-.2*a+.1*b-.3*c"],
    5: ["1.3-.1*b-.2*c+.1*d-.1*e",
        "1.5-.2*a-.3*c-.1*d+.1*e",
        "1.2-.5*a+.2*b+.1*d-.1*e",
        "1.0-.2*a+.1*b-.3*c+.2*e",
        "0.8+.1*a-.2*b+.3*c-.1*d"],
}

# what you are allowed to type inside an equation
ENV = {"__builtins__": {}, "abs": abs, "pi": math.pi,
       "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
       "tan": math.tan, "exp": math.exp, "log": math.log}


def _st():
    """streamlit module if we are running inside streamlit, else None"""
    try:
        import streamlit as st
        from streamlit.runtime import exists
    except ImportError:
        return None
    return st if exists() else None


def _make(text, n):
    """'1.3-.1*b-.2*c'  ->  lambda a,b,c: 1.3-.1*b-.2*c"""
    text = text.replace("^", "**")
    if "=" in text:                                   # allow pasting  A=1.3-.1*b-.2*c
        text = text.split("=", 1)[1]
    return eval("lambda " + ",".join(NAMES[:n]) + ": " + text, ENV)


def inputs(size=15, accuracy=0.01, digits=4, w=None):
    """
    Draws the input fields on the page and returns
        n, guess, size, accuracy, digits, w, eq
    n      : number of variables (3, 4 or 5)
    guess  : starting values  [a,b,c...]
    eq     : [lambda a,b,c: ..., ...]  built from the equations you typed
    (w is only shown when a value is given, e.g. for SOR)
    """
    st = _st()
    if st is None:                                    # terminal only -> defaults, 3 variables
        return 3, [0, 0, 0], size, accuracy, digits, w, [_make(t, 3) for t in SYSTEMS[3]]

    n = st.radio("Number of variables", [3, 4, 5], horizontal=True)
    names = NAMES[:n]

    with st.form("form%d" % n):
        st.markdown("**Equations**  - write the right side using " + ", ".join(names) +
                    "  (example:  `1.3-.1*b-.2*c`)")
        texts = [st.text_input(names[j].upper() + " =", SYSTEMS[n][j], key="eq%d_%d" % (n, j))
                 for j in range(n)]

        st.markdown("**Starting guess**")
        cols = st.columns(n)
        guess = [cols[j].number_input(names[j].upper() + "\u2080", value=0.0, format="%g",
                                      key="g%d_%d" % (n, j)) for j in range(n)]

        c1, c2, c3 = st.columns(3)
        size = c1.number_input("Max iterations", min_value=1, max_value=1000, value=size, step=1, key="size")
        accuracy = c2.number_input("Accuracy", min_value=0.000001, value=accuracy,
                                   step=0.001, format="%.6f", key="accuracy")
        digits = c3.number_input("Digits", min_value=1, max_value=10, value=digits, step=1, key="digits")
        if w is not None:
            w = st.slider("\u03c9  (relaxation factor)", 0.1, 1.9, w, 0.05, key="w")

        st.form_submit_button("Solve", type="primary")

    eq = []
    for j in range(n):
        try:
            f = _make(texts[j], n)
            f(*guess)                                 # test it once
        except Exception as err:
            st.error("Equation %s:  %s      (use only %s and + - * / **)" %
                     (names[j].upper(), err, ", ".join(names)))
            st.stop()
        eq.append(f)

    return n, guess, int(size), accuracy, int(digits), w, eq


def show(title, table, accuracy, digits, converged, cmp="<", second="\u0394x"):
    """
    Last line of every method function: draws the table of that call.
    table : [k, [x...], [r or change...] or None, index_to_highlight or None]
    (does nothing when the file is not running inside streamlit)
    """
    st = _st()
    if st is None:
        return

    n = len(table[0][1])
    st.subheader(title)
    st.markdown(CSS + _table(table, n, digits, second, accuracy, cmp, converged),
                unsafe_allow_html=True)
    if converged:
        st.success(f"Converged at k = {table[-1][0]}")
    else:
        st.warning("Maximum iterations reached - no solution within the accuracy")

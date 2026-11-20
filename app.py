import sys
import math
import subprocess
from html import escape

try:
    import streamlit as st
    from streamlit.runtime import exists
except ImportError:
    print("Streamlit is not installed  ->  pip install streamlit")
    sys.exit()

if __name__=="__main__" and not exists():          # started with:  python app.py
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", __file__])
    except KeyboardInterrupt:
        pass
    sys.exit()

st.set_page_config(page_title="Numerical Methods", layout="wide")


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


def show(title, table, accuracy, digits, converged, cmp="<", second="\u0394x"):
    # draws the table of one run:  table = [k, [x...], [r or change...] or None, index_to_highlight or None]
    n = len(table[0][1])
    st.subheader(title)
    st.markdown(CSS + _table(table, n, digits, second, accuracy, cmp, converged),
                unsafe_allow_html=True)
    if converged:
        st.success(f"Converged at k = {table[-1][0]}")
    else:
        st.warning("Maximum iterations reached - no solution within the accuracy")


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


def _make(text, n):
    """'1.3-.1*b-.2*c'  ->  lambda a,b,c: 1.3-.1*b-.2*c"""
    text = text.replace("^", "**")
    if "=" in text:                                   # allow pasting  A=1.3-.1*b-.2*c
        text = text.split("=", 1)[1]
    return eval("lambda " + ",".join(NAMES[:n]) + ": " + text, ENV)


# =====================================================================
#                     JACOBI  (3, 4, 5 variables)                      
# =====================================================================


def jacobi(a,b,c,size,accuracy,digits,eq1,eq2,eq3):
 print("A=",a,"B=",b,"C=",c)
 table=[[0,[a,b,c],None,None]]
 i=0
 while(i<size):
    A=eq1(a,b,c)
    B=eq2(a,b,c)
    C=eq3(a,b,c)
    x=max(abs(A-a),abs(B-b),abs(C-c))
    table.append([i+1,[A,B,C],[A-a,B-b,C-c],None])
    if(x<accuracy):
        print( "solution is  =>" ,"A=",f"{A:.{digits}f}","B=",f"{B:.{digits}f}","C=",f"{C:.{digits}f}")
        break
    else:
        a=A
        b=B
        c=C
        print( "x1-x0=",f"{x:.{digits}f}","A=",f"{A:.{digits}f}","B=",f"{B:.{digits}f}","C=",f"{C:.{digits}f}")
    i+=1
 else:
    print("Maximum iterations reached")
 show("Jacobi Method - 3 variables",table,accuracy,digits,i<size)


def jacobi4(a,b,c,d,size,accuracy,digits,eq1,eq2,eq3,eq4):
 print("A=",a,"B=",b,"C=",c,"D=",d)
 table=[[0,[a,b,c,d],None,None]]
 i=0
 while(i<size):
    A=eq1(a,b,c,d)
    B=eq2(a,b,c,d)
    C=eq3(a,b,c,d)
    D=eq4(a,b,c,d)
    x=max(abs(A-a),abs(B-b),abs(C-c),abs(D-d))
    table.append([i+1,[A,B,C,D],[A-a,B-b,C-c,D-d],None])
    if(x<accuracy):
        print( "solution is  =>" ,"A=",f"{A:.{digits}f}","B=",f"{B:.{digits}f}","C=",f"{C:.{digits}f}","D=",f"{D:.{digits}f}")
        break
    else:
        a=A
        b=B
        c=C
        d=D
        print( "x1-x0=",f"{x:.{digits}f}","A=",f"{A:.{digits}f}","B=",f"{B:.{digits}f}","C=",f"{C:.{digits}f}","D=",f"{D:.{digits}f}")
    i+=1
 else:
    print("Maximum iterations reached")
 show("Jacobi Method - 4 variables",table,accuracy,digits,i<size)


def jacobi5(a,b,c,d,e,size,accuracy,digits,eq1,eq2,eq3,eq4,eq5):
 print("A=",a,"B=",b,"C=",c,"D=",d,"E=",e)
 table=[[0,[a,b,c,d,e],None,None]]
 i=0
 while(i<size):
    A=eq1(a,b,c,d,e)
    B=eq2(a,b,c,d,e)
    C=eq3(a,b,c,d,e)
    D=eq4(a,b,c,d,e)
    E=eq5(a,b,c,d,e)
    x=max(abs(A-a),abs(B-b),abs(C-c),abs(D-d),abs(E-e))
    table.append([i+1,[A,B,C,D,E],[A-a,B-b,C-c,D-d,E-e],None])
    if(x<accuracy):
        print( "solution is  =>" ,"A=",f"{A:.{digits}f}","B=",f"{B:.{digits}f}","C=",f"{C:.{digits}f}","D=",f"{D:.{digits}f}","E=",f"{E:.{digits}f}")
        break
    else:
        a=A
        b=B
        c=C
        d=D
        e=E
        print( "x1-x0=",f"{x:.{digits}f}","A=",f"{A:.{digits}f}","B=",f"{B:.{digits}f}","C=",f"{C:.{digits}f}","D=",f"{D:.{digits}f}","E=",f"{E:.{digits}f}")
    i+=1
 else:
    print("Maximum iterations reached")
 show("Jacobi Method - 5 variables",table,accuracy,digits,i<size)


# =====================================================================
#                     SEIDEL  (3, 4, 5 variables)                      
# =====================================================================


def seidel(a,b,c,size,accuracy,digits,eq1,eq2,eq3):
 print("A=",a,"B=",b,"C=",c)
 table=[[0,[a,b,c],None,None]]
 i=0
 while(i<size):
    A=eq1(a,b,c)
    B=eq2(A,b,c)
    C=eq3(A,B,c)
    x=max(abs(A-a),abs(B-b),abs(C-c))
    table.append([i+1,[A,B,C],[A-a,B-b,C-c],None])
    if(x<accuracy):
        print( "x1-x0=",f"{x:.{digits}f}","solution is  =>" ,"A=",f"{A:.{digits}f}","B=",f"{B:.{digits}f}","C=",f"{C:.{digits}f}")
        break
    else:
        a=A
        b=B
        c=C
        print( "x1-x0=",f"{x:.{digits}f}","A=",f"{A:.{digits}f}","B=",f"{B:.{digits}f}","C=",f"{C:.{digits}f}")
    i+=1
 else:
    print("Maximum iterations reached")
 show("Seidel Method - 3 variables",table,accuracy,digits,i<size)


def seidel4(a,b,c,d,size,accuracy,digits,eq1,eq2,eq3,eq4):
 print("A=",a,"B=",b,"C=",c,"D=",d)
 table=[[0,[a,b,c,d],None,None]]
 i=0
 while(i<size):
    A=eq1(a,b,c,d)
    B=eq2(A,b,c,d)
    C=eq3(A,B,c,d)
    D=eq4(A,B,C,d)
    x=max(abs(A-a),abs(B-b),abs(C-c),abs(D-d))
    table.append([i+1,[A,B,C,D],[A-a,B-b,C-c,D-d],None])
    if(x<accuracy):
        print( "x1-x0=",f"{x:.{digits}f}","solution is  =>" ,"A=",f"{A:.{digits}f}","B=",f"{B:.{digits}f}","C=",f"{C:.{digits}f}","D=",f"{D:.{digits}f}")
        break
    else:
        a=A
        b=B
        c=C
        d=D
        print( "x1-x0=",f"{x:.{digits}f}","A=",f"{A:.{digits}f}","B=",f"{B:.{digits}f}","C=",f"{C:.{digits}f}","D=",f"{D:.{digits}f}")
    i+=1
 else:
    print("Maximum iterations reached")
 show("Seidel Method - 4 variables",table,accuracy,digits,i<size)


def seidel5(a,b,c,d,e,size,accuracy,digits,eq1,eq2,eq3,eq4,eq5):
 print("A=",a,"B=",b,"C=",c,"D=",d,"E=",e)
 table=[[0,[a,b,c,d,e],None,None]]
 i=0
 while(i<size):
    A=eq1(a,b,c,d,e)
    B=eq2(A,b,c,d,e)
    C=eq3(A,B,c,d,e)
    D=eq4(A,B,C,d,e)
    E=eq5(A,B,C,D,e)
    x=max(abs(A-a),abs(B-b),abs(C-c),abs(D-d),abs(E-e))
    table.append([i+1,[A,B,C,D,E],[A-a,B-b,C-c,D-d,E-e],None])
    if(x<accuracy):
        print( "x1-x0=",f"{x:.{digits}f}","solution is  =>" ,"A=",f"{A:.{digits}f}","B=",f"{B:.{digits}f}","C=",f"{C:.{digits}f}","D=",f"{D:.{digits}f}","E=",f"{E:.{digits}f}")
        break
    else:
        a=A
        b=B
        c=C
        d=D
        e=E
        print( "x1-x0=",f"{x:.{digits}f}","A=",f"{A:.{digits}f}","B=",f"{B:.{digits}f}","C=",f"{C:.{digits}f}","D=",f"{D:.{digits}f}","E=",f"{E:.{digits}f}")
    i+=1
 else:
    print("Maximum iterations reached")
 show("Seidel Method - 5 variables",table,accuracy,digits,i<size)


# =====================================================================
#                   RELAXATION  (3, 4, 5 variables)                    
# =====================================================================


def relaxation(a,b,c,size,accuracy,digits,eqa1,eqa2,eqa3):
 print("A=",a,"B=",b,"C=",c)
 table=[]
 i=0
 while(i<size):
    A=eqa1(a,b,c)
    B=eqa2(a,b,c)
    C=eqa3(a,b,c)
    d=A-a
    f=B-b
    g=C-c

    x=max(abs(d),abs(f),abs(g))

    if(x<=accuracy):
        table.append([i,[a,b,c],[d,f,g],None])
        print("i=",i,"solution is  =>",
              "A=",f"{a:.{digits}f}",
              "B=",f"{b:.{digits}f}",
              "C=",f"{c:.{digits}f}",
              "A1-A0=",f"{d:.{digits}f}",
              "B1-B0=",f"{f:.{digits}f}",
              "C1-C0=",f"{g:.{digits}f}")
        break

    else:
       table.append([i,[a,b,c],[d,f,g],[abs(d),abs(f),abs(g)].index(x)])
       print("i=",i,
             "A=",f"{a:.{digits}f}",
             "B=",f"{b:.{digits}f}",
             "C=",f"{c:.{digits}f}",
             "A1-A0=",f"{d:.{digits}f}",
             "B1-B0=",f"{f:.{digits}f}",
             "C1-C0=",f"{g:.{digits}f}")

       if(x==abs(d)): a=A
       elif(x==abs(f)): b=B
       else: c=C

    i+=1
 else:
    print("Maximum iterations reached")
 show("Relaxation Method - 3 variables",table,accuracy,digits,i<size,"≤","r")


def relaxation4(a,b,c,d,size,accuracy,digits,eqa1,eqa2,eqa3,eqa4):
 print("A=",a,"B=",b,"C=",c,"D=",d)
 table=[]
 i=0
 while(i<size):
    A=eqa1(a,b,c,d)
    B=eqa2(a,b,c,d)
    C=eqa3(a,b,c,d)
    D=eqa4(a,b,c,d)
    e=A-a
    f=B-b
    g=C-c
    h=D-d

    x=max(abs(e),abs(f),abs(g),abs(h))

    if(x<=accuracy):
        table.append([i,[a,b,c,d],[e,f,g,h],None])
        print("i=",i,"solution is  =>",
              "A=",f"{a:.{digits}f}",
              "B=",f"{b:.{digits}f}",
              "C=",f"{c:.{digits}f}",
              "D=",f"{d:.{digits}f}",
              "A1-A0=",f"{e:.{digits}f}",
              "B1-B0=",f"{f:.{digits}f}",
              "C1-C0=",f"{g:.{digits}f}",
              "D1-D0=",f"{h:.{digits}f}")
        break

    else:
       table.append([i,[a,b,c,d],[e,f,g,h],[abs(e),abs(f),abs(g),abs(h)].index(x)])
       print("i=",i,
             "A=",f"{a:.{digits}f}",
             "B=",f"{b:.{digits}f}",
             "C=",f"{c:.{digits}f}",
             "D=",f"{d:.{digits}f}",
             "A1-A0=",f"{e:.{digits}f}",
             "B1-B0=",f"{f:.{digits}f}",
             "C1-C0=",f"{g:.{digits}f}",
             "D1-D0=",f"{h:.{digits}f}")

       if(x==abs(e)): a=A
       elif(x==abs(f)): b=B
       elif(x==abs(g)): c=C
       else: d=D

    i+=1
 else:
    print("Maximum iterations reached")
 show("Relaxation Method - 4 variables",table,accuracy,digits,i<size,"≤","r")


def relaxation5(a,b,c,d,e,size,accuracy,digits,eqa1,eqa2,eqa3,eqa4,eqa5):
 print("A=",a,"B=",b,"C=",c,"D=",d,"E=",e)
 table=[]
 i=0
 while(i<size):
    A=eqa1(a,b,c,d,e)
    B=eqa2(a,b,c,d,e)
    C=eqa3(a,b,c,d,e)
    D=eqa4(a,b,c,d,e)
    E=eqa5(a,b,c,d,e)
    f=A-a
    g=B-b
    h=C-c
    j=D-d
    k=E-e

    x=max(abs(f),abs(g),abs(h),abs(j),abs(k))

    if(x<=accuracy):
        table.append([i,[a,b,c,d,e],[f,g,h,j,k],None])
        print("i=",i,"solution is  =>",
              "A=",f"{a:.{digits}f}",
              "B=",f"{b:.{digits}f}",
              "C=",f"{c:.{digits}f}",
              "D=",f"{d:.{digits}f}",
              "E=",f"{e:.{digits}f}",
              "A1-A0=",f"{f:.{digits}f}",
              "B1-B0=",f"{g:.{digits}f}",
              "C1-C0=",f"{h:.{digits}f}",
              "D1-D0=",f"{j:.{digits}f}",
              "E1-E0=",f"{k:.{digits}f}")
        break

    else:
       table.append([i,[a,b,c,d,e],[f,g,h,j,k],[abs(f),abs(g),abs(h),abs(j),abs(k)].index(x)])
       print("i=",i,
             "A=",f"{a:.{digits}f}",
             "B=",f"{b:.{digits}f}",
             "C=",f"{c:.{digits}f}",
             "D=",f"{d:.{digits}f}",
             "E=",f"{e:.{digits}f}",
             "A1-A0=",f"{f:.{digits}f}",
             "B1-B0=",f"{g:.{digits}f}",
             "C1-C0=",f"{h:.{digits}f}",
             "D1-D0=",f"{j:.{digits}f}",
             "E1-E0=",f"{k:.{digits}f}")

       if(x==abs(f)): a=A
       elif(x==abs(g)): b=B
       elif(x==abs(h)): c=C
       elif(x==abs(j)): d=D
       else: e=E

    i+=1
 else:
    print("Maximum iterations reached")
 show("Relaxation Method - 5 variables",table,accuracy,digits,i<size,"≤","r")


# =====================================================================
#                       SOR  (3, 4, 5 variables)                       
# =====================================================================


def SOR(a,b,c,size,accuracy,digits,w,eq1,eq2,eq3):

 print("A=",a,"B=",b,"C=",c)

 table=[[0,[a,b,c],None,None]]

 i=0

 while(i<size):

    # Calculate new values
    A=eq1(a,b,c)
    B=eq2(a,b,c)
    C=eq3(a,b,c)

    # Calculate differences
    d=A-a
    f=B-b
    g=C-c

    # Apply Successive Over-Relaxation
    A=a+w*d
    B=b+w*f
    C=c+w*g

    # Calculate actual changes after relaxation
    x=max(abs(A-a),abs(B-b),abs(C-c))
    table.append([i+1,[A,B,C],[A-a,B-b,C-c],None])

    # Check convergence
    if(x<=accuracy):

        print("i=",i,"solution is =>",
              "A=",f"{A:.{digits}f}",
              "B=",f"{B:.{digits}f}",
              "C=",f"{C:.{digits}f}")

        break

    else:

       # Update all variables
       a=A
       b=B
       c=C

       print("i=",i,
             "A=",f"{A:.{digits}f}",
             "B=",f"{B:.{digits}f}",
             "C=",f"{C:.{digits}f}",
             "A1-A0=",f"{w*d:.{digits}f}",
             "B1-B0=",f"{w*f:.{digits}f}",
             "C1-C0=",f"{w*g:.{digits}f}")

    i+=1

 else:
    print("Maximum iterations reached")

 show("SOR Method - 3 variables",table,accuracy,digits,i<size,"≤")


def SOR4(a,b,c,d,size,accuracy,digits,w,eq1,eq2,eq3,eq4):

 print("A=",a,"B=",b,"C=",c,"D=",d)

 table=[[0,[a,b,c,d],None,None]]

 i=0

 while(i<size):

    # Calculate new values
    A=eq1(a,b,c,d)
    B=eq2(a,b,c,d)
    C=eq3(a,b,c,d)
    D=eq4(a,b,c,d)

    # Calculate differences
    e=A-a
    f=B-b
    g=C-c
    h=D-d

    # Apply Successive Over-Relaxation
    A=a+w*e
    B=b+w*f
    C=c+w*g
    D=d+w*h

    # Calculate actual changes after relaxation
    x=max(abs(A-a),abs(B-b),abs(C-c),abs(D-d))
    table.append([i+1,[A,B,C,D],[A-a,B-b,C-c,D-d],None])

    # Check convergence
    if(x<=accuracy):

        print("i=",i,"solution is =>",
              "A=",f"{A:.{digits}f}",
              "B=",f"{B:.{digits}f}",
              "C=",f"{C:.{digits}f}",
              "D=",f"{D:.{digits}f}")

        break

    else:

       # Update all variables
       a=A
       b=B
       c=C
       d=D

       print("i=",i,
             "A=",f"{A:.{digits}f}",
             "B=",f"{B:.{digits}f}",
             "C=",f"{C:.{digits}f}",
             "D=",f"{D:.{digits}f}",
             "A1-A0=",f"{w*e:.{digits}f}",
             "B1-B0=",f"{w*f:.{digits}f}",
             "C1-C0=",f"{w*g:.{digits}f}",
             "D1-D0=",f"{w*h:.{digits}f}")

    i+=1

 else:
    print("Maximum iterations reached")

 show("SOR Method - 4 variables",table,accuracy,digits,i<size,"≤")


def SOR5(a,b,c,d,e,size,accuracy,digits,w,eq1,eq2,eq3,eq4,eq5):

 print("A=",a,"B=",b,"C=",c,"D=",d,"E=",e)

 table=[[0,[a,b,c,d,e],None,None]]

 i=0

 while(i<size):

    # Calculate new values
    A=eq1(a,b,c,d,e)
    B=eq2(a,b,c,d,e)
    C=eq3(a,b,c,d,e)
    D=eq4(a,b,c,d,e)
    E=eq5(a,b,c,d,e)

    # Calculate differences
    f=A-a
    g=B-b
    h=C-c
    j=D-d
    k=E-e

    # Apply Successive Over-Relaxation
    A=a+w*f
    B=b+w*g
    C=c+w*h
    D=d+w*j
    E=e+w*k

    # Calculate actual changes after relaxation
    x=max(abs(A-a),abs(B-b),abs(C-c),abs(D-d),abs(E-e))
    table.append([i+1,[A,B,C,D,E],[A-a,B-b,C-c,D-d,E-e],None])

    # Check convergence
    if(x<=accuracy):

        print("i=",i,"solution is =>",
              "A=",f"{A:.{digits}f}",
              "B=",f"{B:.{digits}f}",
              "C=",f"{C:.{digits}f}",
              "D=",f"{D:.{digits}f}",
              "E=",f"{E:.{digits}f}")

        break

    else:

       # Update all variables
       a=A
       b=B
       c=C
       d=D
       e=E

       print("i=",i,
             "A=",f"{A:.{digits}f}",
             "B=",f"{B:.{digits}f}",
             "C=",f"{C:.{digits}f}",
             "D=",f"{D:.{digits}f}",
             "E=",f"{E:.{digits}f}",
             "A1-A0=",f"{w*f:.{digits}f}",
             "B1-B0=",f"{w*g:.{digits}f}",
             "C1-C0=",f"{w*h:.{digits}f}",
             "D1-D0=",f"{w*j:.{digits}f}",
             "E1-E0=",f"{w*k:.{digits}f}")

    i+=1

 else:
    print("Maximum iterations reached")

 show("SOR Method - 5 variables",table,accuracy,digits,i<size,"≤")


# =====================================================================
#                               THE PAGE                               
# =====================================================================


DEFAULTS = {"Jacobi":(15,4), "Seidel":(15,5), "Relaxation":(60,4), "SOR":(100,5)}   # (max iterations, digits)

FUNCS = {"Jacobi":    {3:jacobi,     4:jacobi4,     5:jacobi5},
         "Seidel":    {3:seidel,     4:seidel4,     5:seidel5},
         "Relaxation":{3:relaxation, 4:relaxation4, 5:relaxation5},
         "SOR":       {3:SOR,        4:SOR4,        5:SOR5}}

st.title("Numerical Methods - Linear Systems")

c1,c2=st.columns([1,2])
method=c1.selectbox("Method",list(FUNCS))
n=c2.radio("Number of variables",[3,4,5],horizontal=True)
names=NAMES[:n]

size,digits=DEFAULTS[method]
accuracy=0.01
w=1.2

with st.form("form%d"%n):

    st.markdown("**Equations**  - write the right side using "+", ".join(names)+"  (example:  `1.3-.1*b-.2*c`)")
    texts=[st.text_input(names[j].upper()+" =",SYSTEMS[n][j],key="eq%d_%d"%(n,j)) for j in range(n)]

    st.markdown("**Starting guess**")
    cols=st.columns(n)
    guess=[cols[j].number_input(names[j].upper()+"\u2080",value=0.0,format="%g",key="g%d_%d"%(n,j)) for j in range(n)]

    c1,c2,c3=st.columns(3)
    size=c1.number_input("Max iterations",min_value=1,max_value=1000,value=size,step=1,key="size_"+method)
    accuracy=c2.number_input("Accuracy",min_value=0.000001,value=accuracy,step=0.001,format="%.6f",key="accuracy")
    digits=c3.number_input("Digits",min_value=1,max_value=10,value=digits,step=1,key="digits_"+method)
    if method=="SOR":
        w=st.slider("\u03c9  (relaxation factor)",0.1,1.9,w,0.05,key="w")

    st.form_submit_button("Solve",type="primary")

# turn the typed text into lambdas  (a,b,c...) -> value
eq=[]
for j in range(n):
    try:
        f=_make(texts[j],n)
        f(*guess)                                  # test it once
    except Exception as err:
        st.error("Equation %s:  %s      (use only %s and + - * / **)"%(names[j].upper(),err,", ".join(names)))
        st.stop()
    eq.append(f)

solve=FUNCS[method][n]
if method=="SOR": solve(*guess,int(size),accuracy,int(digits),w,*eq)
else: solve(*guess,int(size),accuracy,int(digits),*eq)
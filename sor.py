from table_view import start, show, inputs

if __name__=="__main__":
    start(__file__,"SOR Method")


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


n,guess,size,accuracy,digits,w,eq=inputs(size=100,accuracy=0.01,digits=5,w=1.2)

if n==3: SOR(*guess,size,accuracy,digits,w,*eq)
elif n==4: SOR4(*guess,size,accuracy,digits,w,*eq)
else: SOR5(*guess,size,accuracy,digits,w,*eq)

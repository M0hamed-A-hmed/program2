from table_view import start, show, inputs

if __name__=="__main__":
    start(__file__,"Seidel Method")


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


n,guess,size,accuracy,digits,w,eq=inputs(size=15,accuracy=0.01,digits=5)

if n==3: seidel(*guess,size,accuracy,digits,*eq)
elif n==4: seidel4(*guess,size,accuracy,digits,*eq)
else: seidel5(*guess,size,accuracy,digits,*eq)

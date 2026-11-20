from table_view import start, show, inputs

if __name__=="__main__":
    start(__file__,"Relaxation Method")


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


n,guess,size,accuracy,digits,w,eq=inputs(size=60,accuracy=0.01,digits=4)

if n==3: relaxation(*guess,size,accuracy,digits,*eq)
elif n==4: relaxation4(*guess,size,accuracy,digits,*eq)
else: relaxation5(*guess,size,accuracy,digits,*eq)

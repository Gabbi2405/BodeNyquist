from sympy import symbols, Matrix



def create_observability_matrix(a:Matrix, c:Matrix, dim:int):
    """"in this function we crate the Matrix O (osservable).
     It's construction is [C, CA, CA^2, ..., CA^n-1]^T"""   
    temp=c
    res=temp
    i=0
    for i in range(i,dim-1):
        temp=temp*a
        res=Matrix.vstack(res,temp)
    return res

def create_reachability_matrix(a:Matrix, b:Matrix, dim:int):
    """"in this function we crate the Matrix R (reachable).
     It's construction is [B, AB, A^2B, ..., A^n-1B]"""   
    temp=b
    res=temp
    i=0
    for i in range(i,dim-1):
        temp=a*temp
        res=Matrix.hstack(res,temp)
    return res



if __name__=="__main__":
    A=Matrix([[0,0,0],
               [1,-1,0],
               [1,0,0]])
    B=Matrix([[1],[1],[0]])
    C=Matrix([[1,0,0]])
    o=create_observability_matrix(A,C,3)
    r=create_reachability_matrix(A,B,3)
    print(f"matrice di osservabilità: {o}")
    print(f"matrice di ragiungibilità: {r}")
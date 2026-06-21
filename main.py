from sympy import symbols, Matrix
from Logger import Log
from dynamic_systems.system import DynamicSystem
from dynamic_systems.eigenvalues import (
    compute_eigenvalues,
    right_eigenvectors,
    left_eigenvectors,
    compute_eigenvalues_numeric,
    right_eigenvectors_numeric,
    left_eigenvectors_numeric
)
from dynamic_systems.utils import print_system, print_eigenresults, print_eigenvalues_only, print_numeric_results


def demo_simple_system():
    print("\n" + "=" * 60)
    print("DEMO 1: Sistema semplice con variabili")
    print("=" * 60)
    
    a, b, c, d = symbols('a b c d')
    
    A = [[a, b],
         [c, d]]
    
    B = [[1],
         [0]]
    
    C = [[1, 0]]
    
    D = [[0]]
    
    system = DynamicSystem.from_matrices(A, B, C, D)
    
    print_system(system)
    
    print("\n--- AUTOVALORI (simbolici) ---")
    eigenvals = compute_eigenvalues(A)
    print_eigenvalues_only(eigenvals)
    
    print("\n--- AUTOVETTORI DESTRI (simbolici) ---")
    right_eig = right_eigenvectors(A)
    print_eigenresults(right_eig, title="AUTOVETTORI DESTRI")
    
    print("\n--- AUTOVETTORI SINISTRI (simbolici) ---")
    left_eig = left_eigenvectors(A)
    print_eigenresults(left_eig, title="AUTOVETTORI SINISTRI", left=True)
    
    print("\n--- RISULTATI NUMERICI (a=1, b=2, c=3, d=4) ---")
    values = {a: 1, b: 2, c: 3, d: 4}
    
    eigenvals_num = compute_eigenvalues_numeric(A, values)
    print_numeric_results(eigenvals_num, values)
    
    right_eig_num = right_eigenvectors_numeric(A, values)
    print_eigenresults(right_eig_num, title="AUTOVETTORI DESTRI NUMERICI")
    
    left_eig_num = left_eigenvectors_numeric(A, values)
    print_eigenresults(left_eig_num, title="AUTOVETTORI SINISTRI NUMERICI", left=True)


def demo_complex_system():
    print("\n" + "=" * 60)
    print("DEMO 2: Sistema con autovalori complessi")
    print("=" * 60)
    
    w = symbols('w')
    
    A = [[0, -w],
         [w, 0]]
    
    B = [[1],
         [0]]
    
    C = [[1, 0]]
    
    D = [[0]]
    
    system = DynamicSystem.from_matrices(A, B, C, D)
    
    print_system(system)
    
    print("\n--- AUTOVALORI (simbolici) ---")
    eigenvals = compute_eigenvalues(A)
    print_eigenvalues_only(eigenvals)
    
    print("\n--- AUTOVETTORI DESTRI (simbolici) ---")
    right_eig = right_eigenvectors(A)
    print_eigenresults(right_eig, title="AUTOVETTORI DESTRI")
    
    print("\n--- RISULTATI NUMERICI (w=2) ---")
    values = {w: 2}
    
    eigenvals_num = compute_eigenvalues_numeric(A, values)
    print_numeric_results(eigenvals_num, values)
    
    right_eig_num = right_eigenvectors_numeric(A, values)
    print_eigenresults(right_eig_num, title="AUTOVETTORI DESTRI NUMERICI")


def demo_numeric_only():
    print("\n" + "=" * 60)
    print("DEMO 3: Sistema solo numerico")
    print("=" * 60)
    
    A = [[-2, 1],
         [1, -2]]
    
    B = [[0],
         [1]]
    
    C = [[1, 0]]
    
    D = [[0]]
    
    system = DynamicSystem.from_matrices(A, B, C, D)
    
    print_system(system)
    
    print("\n--- AUTOVALORI ---")
    eigenvals = compute_eigenvalues(A)
    print_eigenvalues_only(eigenvals)
    
    print("\n--- AUTOVETTORI DESTRI ---")
    right_eig = right_eigenvectors(A)
    print_eigenresults(right_eig, title="AUTOVETTORI DESTRI")
    
    print("\n--- AUTOVETTORI SINISTRI ---")
    left_eig = left_eigenvectors(A)
    print_eigenresults(left_eig, title="AUTOVETTORI SINISTRI", left=True)

def manual_system():
     """This fuction serv to create a sistem manualy"""
     #TODO
def main():
    while(True):
          comand=input("Per favore scegliere una delle seguenti opzioni\n" \
          "1) demo simple system\n" \
          "2) demo complex system\n" \
          "3) demo numeric only\n" \
          "quit) per chiudere il programma")

          match comand:
               case "1":
                    demo_simple_system()
               case "2":
                    demo_complex_system()
               case "3":
                    demo_numeric_only()
               case "quit":
                    print("Arrivederci..")
                    break
               case _:
                    Log.Log(level=Log.Level.WARNING,message="Input incoretto...\n Per favore inserire un opzione coretta\n")

if __name__ == "__main__":
    main()
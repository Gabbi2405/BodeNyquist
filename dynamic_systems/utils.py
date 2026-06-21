from sympy import latex, simplify, Matrix
import numpy as np


def print_system(system):
    """
    Stampa il sistema dinamico in formato leggibile.
    
    Args:
        system: Oggetto DynamicSystem da stampare
    """
    dims = system.get_dimensions()
    n, m, p = dims['n'], dims['m'], dims['p']
    
    print("=" * 60)
    print("SISTEMA DINAMICO")
    print("=" * 60)
    print()
    print("Forma standard:")
    print("  x'(t) = A·x(t) + B·u(t)")
    print("  y(t)  = C·x(t) + D·u(t)")
    print()
    print(f"Dimensioni: n={n} (stati), m={m} (ingressi), p={p} (uscite)")
    print()
    
    print("MATRICE A (sistema):")
    _print_matrix(system.A)
    print()
    
    if system.B is not None:
        print("MATRICE B (ingresso):")
        _print_matrix(system.B)
        print()
    
    if system.C is not None:
        print("MATRICE C (uscita):")
        _print_matrix(system.C)
        print()
    
    if system.D is not None:
        print("MATRICE D (feedthrough):")
        _print_matrix(system.D)
        print()


def _print_matrix(M):
    """
    Stampa una matrice in formato tabellare.
    
    Args:
        M: Matrice (Matrix sympy o lista di liste)
    """
    M = Matrix(M)
    rows, cols = M.shape
    cell_width = 15
    
    for i in range(rows):
        row_str = "  |"
        for j in range(cols):
            entry = M[i, j]
            entry_str = str(simplify(entry))
            if len(entry_str) > cell_width - 2:
                entry_str = entry_str[:cell_width-5] + "..."
            row_str += f" {entry_str:^{cell_width}}"
        row_str += " |"
        print(row_str)


def print_eigenresults(eigen_dict, title="AUTOVALORI E AUTOVETTORI", left=False):
    """
    Stampa gli autovalori e autovettori in formato leggibile.
    
    Args:
        eigen_dict: Dizionario con gli autovalori/autovettori
        title: Titolo della sezione
        left: Se True, indica autovettori sinistri
    """
    print("=" * 60)
    if left:
        print(f"{title} (SINISTRI)")
    else:
        print(f"{title} (DESTRI)")
    print("=" * 60)
    print()
    
    eigenvector_type = "sinistri" if left else "destri"
    
    for eigenvalue, data in eigen_dict.items():
        eig = data['eigenvalue']
        mult = data['multiplicity']
        eigenvectors = data['eigenvectors']
        is_complex = data['is_complex']
        
        print(f"Autovalore λ = {eig}")
        print(f"  Molteplicità: {mult}")
        print(f"  Complesso: {'Sì' if is_complex else 'No'}")
        print(f"  Parte reale: {eig.real if isinstance(eig, complex) else eig.as_real_imag()[0]}")
        if is_complex:
            print(f"  Parte immaginaria: {eig.imag if isinstance(eig, complex) else eig.as_real_imag()[1]}")
        print()
        
        print(f"  Autovettori {eigenvector_type}:")
        for i, vec in enumerate(eigenvectors):
            vec_str = _format_eigenvector(vec)
            print(f"    v{i+1} = {vec_str}")
        print()


def _format_eigenvector(vec):
    """
    Formatta un autovettore come stringa leggibile.
    
    Args:
        vec: Autovettore (lista o Matrix)
        
    Returns:
        Stringa rappresentante l'autovettore in formato [v1, v2, ...]ᵀ
    """
    vec = Matrix(vec)
    n = vec.shape[0]
    
    if n == 1:
        return f"[{vec[0,0]}]"
    
    entries = []
    for i in range(n):
        entry = simplify(vec[i, 0])
        entries.append(str(entry))
    
    return "[" + ", ".join(entries) + "]ᵀ"


def print_eigenvalues_only(eigenvalues_list):
    print("=" * 60)
    print("AUTOVALORI")
    print("=" * 60)
    print()
    
    for i, data in enumerate(eigenvalues_list, 1):
        eig = data['value']
        mult = data['multiplicity']
        is_complex = data['is_complex']
        
        print(f"λ{i} = {eig}")
        print(f"    Molteplicità: {mult}")
        if is_complex:
            if isinstance(eig, complex):
                print(f"    Complesso: {eig.real:.4f} + {eig.imag:.4f}j")
            else:
                print(f"    Complesso: Sì")
        print()


def print_numeric_results(eigenvalues_list, variable_values=None):
    print("=" * 60)
    print("RISULTATI NUMERICI")
    print("=" * 60)
    if variable_values:
        print(f"Valori delle variabili: {variable_values}")
    print()
    
    for i, data in enumerate(eigenvalues_list, 1):
        eig = data['value']
        mult = data['multiplicity']
        
        if isinstance(eig, complex):
            print(f"λ{i} = {eig:.6f}")
            print(f"    |λ{i}| = {abs(eig):.6f}")
            if eig.imag != 0:
                print(f"    Re(λ{i}) = {eig.real:.6f}")
                print(f"    Im(λ{i}) = {eig.imag:.6f}")
        else:
            print(f"λ{i} = {eig:.6f}")
        
        print(f"    Molteplicità: {mult}")
        print()
from typing import List
from sympy import Matrix, I, nsimplify, simplify, solveset, solve, Eq, Symbol
from sympy.matrices import MatrixBase
import numpy as np


def compute_eigenvalues(A:List[List])->List:
    """Calculate the eigenvalues of the passed matrix and return a list containing [{'values':eigenvalue},'multiplicity': multiplicity,'is_complex':Bool]"""
    A = Matrix(A)
    eigenvalues = A.eigenvals()
    result = []
    for eigenvalue, multiplicity in eigenvalues.items():
        result.append({
            'value': eigenvalue,
            'multiplicity': multiplicity,
            'is_complex': eigenvalue.as_real_imag()[1] != 0
        })
    return result


def right_eigenvectors(A):
    """
    Calcola gli autovettori destri della matrice A.
    
    Gli autovettori destri v soddisfano: A*v = λ*v
    
    Args:
        A: Matrice (lista di liste o Matrix sympy)
        
    Returns:
        Dizionario con chiave = autovalore, valore = dict con:
            - 'eigenvalue': autovalore
            - 'multiplicity': molteplicità algebrica
            - 'eigenvectors': lista di autovettori
            - 'is_complex': booleano che indica se l'autovalore è complesso
    """
    A = Matrix(A)
    eigenvecs = A.eigenvects()
    result = {}
    for eigenvalue, multiplicity, eigenvectors in eigenvecs:
        eigenvals = [eigenvalue] * multiplicity
        result[eigenvalue] = {
            'eigenvalue': eigenvalue,
            'multiplicity': multiplicity,
            'eigenvectors': eigenvectors,
            'is_complex': eigenvalue.as_real_imag()[1] != 0
        }
    return result


def left_eigenvectors(A):
    """
    Calcola gli autovettori sinistri della matrice A.
    
    Gli autovettori sinistri w soddisfano: w*A = λ*w
    Equivalentemente, sono gli autovettori destri di A^T (trasposta).
    
    Args:
        A: Matrice (lista di liste o Matrix sympy)
        
    Returns:
        Dizionario con chiave = autovalore, valore = dict con:
            - 'eigenvalue': autovalore
            - 'multiplicity': molteplicità algebrica
            - 'eigenvectors': lista di autovettori sinistri
            - 'is_complex': booleano che indica se l'autovalore è complesso
    """
    A = Matrix(A)
    A_T = A.T
    eigenvecs = A_T.eigenvects()
    result = {}
    for eigenvalue, multiplicity, eigenvectors in eigenvecs:
        result[eigenvalue] = {
            'eigenvalue': eigenvalue,
            'multiplicity': multiplicity,
            'eigenvectors': eigenvectors,
            'is_complex': eigenvalue.as_real_imag()[1] != 0
        }
    return result


def evaluate_numerically(A, variable_values):
    """
    Sostituisce i valori numerici nelle variabili simboliche della matrice.
    
    Args:
        A: Matrice (lista di liste o Matrix sympy)
        variable_values: Dizionario {simbolo: valore} per la sostituzione
        
    Returns:
        Matrice con valori numerici (float)
    """
    A = Matrix(A)
    A_num = A.subs(variable_values)
    try:
        A_float = A_num.astype(float)
    except:
        A_float = A_num.evalf()
    return A_float


def compute_eigenvalues_numeric(A, variable_values=None):
    """
    Calcola gli autovalori numerici della matrice A.
    
    Se vengono forniti valori per le variabili simboliche, sostituisce i valori
    e calcola gli autovalori numerici complessi.
    
    Args:
        A: Matrice (lista di liste o Matrix sympy)
        variable_values: Dizionario opzionale {simbolo: valore} per la sostituzione
        
    Returns:
        Lista di dizionari con:
            - 'value': autovalore come numero complesso
            - 'multiplicity': molteplicità algebrica
            - 'real': parte reale
            - 'imag': parte immaginaria
            - 'is_complex': booleano che indica se l'autovalore è complesso
    """
    if variable_values:
        A = evaluate_numerically(A, variable_values)
    else:
        A = Matrix(A)
    
    eigenvalues = A.eigenvals()
    result = []
    for eigenvalue, multiplicity in eigenvalues.items():
        val = complex(eigenvalue)
        result.append({
            'value': val,
            'multiplicity': multiplicity,
            'real': val.real,
            'imag': val.imag,
            'is_complex': val.imag != 0
        })
    return result


def right_eigenvectors_numeric(A, variable_values=None):
    """
    Calcola gli autovettori destri numerici della matrice A.
    
    Se vengono forniti valori per le variabili simboliche, sostituisce i valori
    e calcola gli autovettori numerici complessi.
    
    Args:
        A: Matrice (lista di liste o Matrix sympy)
        variable_values: Dizionario opzionale {simbolo: valore} per la sostituzione
        
    Returns:
        Dizionario con chiave = autovalore complesso, valore = dict con:
            - 'eigenvalue': autovalore come numero complesso
            - 'multiplicity': molteplicità algebrica
            - 'eigenvectors': lista di autovettori (liste di numeri complessi)
            - 'is_complex': booleano che indica se l'autovalore è complesso
    """
    if variable_values:
        A = evaluate_numerically(A, variable_values)
    else:
        A = Matrix(A)
    
    eigenvecs = A.eigenvects()
    result = {}
    for eigenvalue, multiplicity, eigenvectors in eigenvecs:
        val = complex(eigenvalue)
        result[val] = {
            'eigenvalue': val,
            'multiplicity': multiplicity,
            'eigenvectors': [[complex(x) for x in vec] for vec in eigenvectors],
                    'is_complex': val.imag != 0
        }
    return result


def left_eigenvectors_numeric(A, variable_values=None):
    """
    Calcola gli autovettori sinistri numerici della matrice A.
    
    Gli autovettori sinistri sono calcolati come autovettori di A^T.
    Se vengono forniti valori per le variabili simboliche, sostituisce i valori
    e calcola gli autovettori numerici complessi.
    
    Args:
        A: Matrice (lista di liste o Matrix sympy)
        variable_values: Dizionario opzionale {simbolo: valore} per la sostituzione
        
    Returns:
        Dizionario con chiave = autovalore complesso, valore = dict con:
            - 'eigenvalue': autovalore come numero complesso
            - 'multiplicity': molteplicità algebrica
            - 'eigenvectors': lista di autovettori sinistri (liste di numeri complessi)
            - 'is_complex': booleano che indica se l'autovalore è complesso
    """
    if variable_values:
        A = evaluate_numerically(A, variable_values)
    else:
        A = Matrix(A)
    
    A_T = A.T
    eigenvecs = A_T.eigenvects()
    result = {}
    for eigenvalue, multiplicity, eigenvectors in eigenvecs:
        val = complex(eigenvalue)
        result[val] = {
            'eigenvalue': val,
            'multiplicity': multiplicity,
            'eigenvectors': [[complex(x) for x in vec] for vec in eigenvectors],
            'is_complex': val.imag != 0
        }
    return result
import sympy as sp

def routh_simbolico(poly_str_list):
    """
    Calcola la Tabella di Routh per un polinomio espresso come lista di stringhe.
    Supporta parametri letterali come 'k'.
    """
    print("\n" + "="*60)
    print("CRITERIO DI ROUTH-HURWITZ SIMBOLICO")
    print("="*60)
    
    # Converte le stringhe in espressioni simboliche di SymPy
    coefs = [sp.sympify(c) for c in poly_str_list]
    n = len(coefs) - 1
    
    rows = n + 1
    cols = (n + 2) // 2
    # Inizializza la matrice simbolica riempita di zeri
    routh_table = sp.Matrix.zeros(rows, cols)
    
    # 1. Riempimento delle prime due righe
    r0, r1 = 0, 0
    for i in range(len(coefs)):
        if i % 2 == 0:
            routh_table[0, r0] = coefs[i]
            r0 += 1
        else:
            routh_table[1, r1] = coefs[i]
            r1 += 1

    # 2. Calcolo del resto della tabella di Routh
    for i in range(2, rows):
        first_elem = routh_table[i-1, 0]
        if first_elem == 0:
            # Sostituzione formale in caso di zero sulla prima colonna
            first_elem = sp.Symbol('epsilon')
            
        for j in range(cols - 1):
            num1 = routh_table[i-2, 0]
            num2 = routh_table[i-2, j+1]
            num3 = routh_table[i-1, 0]
            num4 = routh_table[i-1, j+1]
            
            # Formula del determinante di Routh
            det = (num1 * num4) - (num2 * num3)
            routh_table[i, j] = sp.simplify(-det / first_elem)

    # 3. Stampa a schermo della Tabella
    print("\nTabella di Routh Simbolica:")
    for i in range(rows):
        power = n - i
        row_str = f"s^{power}: "
        row_elements = []
        for j in range(cols):
            val = routh_table[i, j]
            if val != 0 or j == 0:
                row_elements.append(f"[{sp.pretty(val)}]")
        print(row_str + "   ".join(row_elements))

    # 4. Estrazione delle condizioni di stabilità dalla prima colonna
    print("\nCondizioni per la stabilità (Tutti gli elementi della 1° colonna devono essere > 0):")
    for i in range(rows):
        elem = routh_table[i, 0]
        print(f"   s^{n-i} :  {elem} > 0")


def jury_simbolico(poly_str_list):
    """
    Esegue il Criterio di Jury in modo simbolico supportando parametri letterali.
    I coefficienti vanno inseriti dal grado massimo z^n fino a z^0.
    """
    print("\n" + "="*60)
    print("CRITERIO DI JURY SIMBOLICO")
    print("="*60)
    
    coefs = [sp.sympify(c) for c in poly_str_list]
    n = len(coefs) - 1
    
    # Definizione della variabile z per ricostruire il polinomio e fare i calcoli al bordo
    z = sp.Symbol('z')
    P_z = sum(coefs[i] * (z**(n-i)) for i in range(len(coefs)))
    
    print(f"Polinomio caratteristico P(z): {sp.simplify(P_z)} = 0\n")
    
    # 1. Condizioni Necessarie (Limiti al bordo)
    a_n = coefs[0]
    a_0 = coefs[-1]
    
    print("1. Condizioni necessarie al bordo:")
    print(f"   |a_0| < a_n        =>   |{a_0}| < {a_n}")
    
    P_1 = sp.simplify(P_z.subs(z, 1))
    print(f"   P(1) > 0           =>   {P_1} > 0")
    
    P_minus_1 = sp.simplify(P_z.subs(z, -1))
    cond_minus_1 = sp.simplify(((-1)**n) * P_minus_1)
    print(f"   (-1)^n * P(-1) > 0 =>   {cond_minus_1} > 0")
    
    # 2. Costruzione delle righe ridotte di Jury (Condizioni Sufficienti)
    print("\n2. Costruzione della Tabella di Jury (Righe Ridotte):")
    current_row = list(coefs)
    
    for r in range(n - 1):
        if len(current_row) <= 2:
            break
            
        print(f"   Riga {n-r} (lunghezza {len(current_row)}): {[str(sp.simplify(x)) for x in current_row]}")
        
        # Elementi per il calcolo del moltiplicatore K
        a_first = current_row[0]
        a_last = current_row[-1]
        
        # Nel criterio di Jury simbolico standard si verifica che la prima colonna domini l'ultima
        print(f"   Verifica elemento iniziale/finale: |{a_first}| > |{a_last}|")
        
        # Calcolo della riga successiva usando l'algoritmo dei determinanti di Jury
        next_row = []
        for c in range(len(current_row) - 1):
            # Determinante 2x2 tipico di Jury
            det = (current_row[0] * current_row[c]) - (current_row[-1] * current_row[-1-c])
            next_row.append(sp.simplify(det))
            
        current_row = next_row

# ==========================================
# Esempio di utilizzo richiesto
# ==========================================
if __name__ == "__main__":
    # Definiamo la variabile simbolica k per poterla mostrare a video
    k = sp.Symbol('k')
    
    # Input modificati secondo la tua richiesta (Espressioni in formato stringa)
    poly_routh = ["1", "100", "1", "100+k", "-10*k"]
    poly_jury = ["1", "100", "1", "100+k", "-10*k"]
    
    # Avvio del calcolo di Routh
    routh_simbolico(poly_routh)
    
    # Avvio del calcolo di Jury
    #jury_simbolico(poly_jury)

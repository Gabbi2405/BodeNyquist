from sympy import Matrix, symbols, latex
from sympy.matrices import MatrixBase


class DynamicSystem:
    """
    Rappresenta un sistema dinamico lineare tempo-invariante (LTI) nella forma:
    
        x'(t) = A·x(t) + B·u(t)
        y(t)  = C·x(t) + D·u(t)
    
    Dove:
        - A: matrice di sistema (n x n)
        - B: matrice di ingresso (n x m)
        - C: matrice di uscita (p x n)
        - D: matrice di feedthrough (p x m)
    
    Attributes:
        A: Matrix sympy - matrice di sistema
        B: Matrix sympy opzionale - matrice di ingresso
        C: Matrix sympy opzionale - matrice di uscita
        D: Matrix sympy opzionale - matrice di feedthrough
    """
    
    def __init__(self, A, B=None, C=None, D=None):
        """
        Inizializza un sistema dinamico con le matrici specificate.
        
        Args:
            A: Matrice di sistema (lista di liste o Matrix sympy) - richiesta
            B: Matrice di ingresso (lista di liste o Matrix sympy) - opzionale
            C: Matrice di uscita (lista di liste o Matrix sympy) - opzionale
            D: Matrice di feedthrough (lista di liste o Matrix sympy) - opzionale
        """
        self.A = Matrix(A)
        self.B = Matrix(B) if B is not None else None
        self.C = Matrix(C) if C is not None else None
        self.D = Matrix(D) if D is not None else None

    @classmethod
    def from_matrices(cls, A, B=None, C=None, D=None):
        """
        Factory method per creare un sistema dinamico dalle matrici.
        
        Args:
            A: Matrice di sistema (lista di liste o Matrix sympy) - richiesta
            B: Matrice di ingresso (lista di liste o Matrix sympy) - opzionale
            C: Matrice di uscita (lista di liste o Matrix sympy) - opzionale
            D: Matrice di feedthrough (lista di liste o Matrix sympy) - opzionale
            
        Returns:
            Nuovo oggetto DynamicSystem
        """
        return cls(A, B, C, D)

    def __repr__(self):
        """
        Rappresentazione stringa del sistema dinamico.
        
        Returns:
            Stringa con la rappresentazione del sistema
        """
        lines = []
        lines.append("DynamicSystem(")
        lines.append(f"  A={self.A.tolist()}")
        if self.B is not None:
            lines.append(f"  B={self.B.tolist()}")
        if self.C is not None:
            lines.append(f"  C={self.C.tolist()}")
        if self.D is not None:
            lines.append(f"  D={self.D.tolist()}")
        lines.append(")")
        return "\n".join(lines)

    def get_dimensions(self):
        """
        Restituisce le dimensioni del sistema.
        
        Returns:
            Dizionario con:
                - 'n': numero di stati (dimensione di A)
                - 'm': numero di ingressi (dimensione di B)
                - 'p': numero di uscite (dimensione di C)
        """
        n = self.A.shape[0]
        m = self.B.shape[1] if self.B is not None else 0
        p = self.C.shape[0] if self.C is not None else 0
        return {'n': n, 'm': m, 'p': p}

    def latex(self):
        """
        Genera la rappresentazione LaTeX del sistema dinamico.
        
        Returns:
            Stringa con il codice LaTeX del sistema
        """
        lines = []
        lines.append(r"\begin{aligned}")
        lines.append(r"\dot{x}(t) &= A x(t) + B u(t) \\")
        lines.append(r"y(t) &= C x(t) + D u(t)")
        lines.append(r"\end{aligned}")
        lines.append("")
        lines.append(f"A = {latex(self.A)}")
        if self.B is not None:
            lines.append(f"B = {latex(self.B)}")
        if self.C is not None:
            lines.append(f"C = {latex(self.C)}")
        if self.D is not None:
            lines.append(f"D = {latex(self.D)}")
        return "\n".join(lines)
import sympy as sp
import control as ctrl
import matplotlib.pyplot as plt
DEBUG=True#if DEBUG:print(f"[DEBUG] ")


def parse_transfer_function(expr_str):
    s = sp.symbols('s')
    if DEBUG:print(f"[DEBUG] s: {s}")
    # Converte stringa in espressione simbolica
    expr = sp.sympify(expr_str)
    if DEBUG:print(f"[DEBUG] expr: {expr}")
    # Separa numeratore e denominatore
    num, den = sp.fraction(expr)
    if DEBUG:print(f"[DEBUG] num: {num}, den: {den}")


    # Espande i polinomi
    num_poly = sp.expand(num)
    den_poly = sp.expand(den)

    # Ottiene coefficienti
    num_coeffs = sp.Poly(num_poly, s).all_coeffs()
    den_coeffs = sp.Poly(den_poly, s).all_coeffs()

    # Converte in float
    num_coeffs = [float(c) for c in num_coeffs]
    den_coeffs = [float(c) for c in den_coeffs]

    return num_coeffs, den_coeffs
#5*(1+s)*(10+s)/((0.1+s)^2*(50+s))

def main():
    print("Inserisci la funzione di trasferimento in s (es: (s-10)*(s+100)/(s**2*(s-1)**2*(s+10)**2):")
    expr = input("> ")

    num, den = parse_transfer_function(expr)

    print("\nNumeratore:", num)
    print("Denominatore:", den)

    system = ctrl.TransferFunction(num, den)

    print("\nFunzione di trasferimento:")
    print(system)

    # Bode
    plt.figure()
    ctrl.bode(system, dB=True, deg=True)

    # Nyquist
    plt.figure()
    ctrl.nyquist(system)

    plt.show()


if __name__ == "__main__":
    main()
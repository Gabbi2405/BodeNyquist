import sympy as sp
import numpy as np
import control as ctrl
import matplotlib.pyplot as plt

s = sp.symbols('s')

# -------------------------------
# Parsing funzione
# -------------------------------
def parse_transfer_function(expr_str):
    expr = sp.sympify(expr_str)
    num, den = sp.fraction(expr)

    num_poly = sp.expand(num)
    den_poly = sp.expand(den)

    num_coeffs = sp.Poly(num_poly, s).all_coeffs()
    den_coeffs = sp.Poly(den_poly, s).all_coeffs()

    num_coeffs = [float(c) for c in num_coeffs]
    den_coeffs = [float(c) for c in den_coeffs]

    return num_coeffs, den_coeffs


# -------------------------------
# BODE ASINTOTICO COMPLETO
# -------------------------------
def bode_asintotico(system):
    poles = ctrl.pole(system)
    zeros = ctrl.zero(system)

    w = np.logspace(-2, 3, 1000)

    # Guadagno
    K = abs(system.dcgain()) if system.dcgain() not in [None, np.inf] else 1

    # ---------------- MODULO ----------------
    mag = np.ones_like(w) * 20 * np.log10(K)

    slope = 0

    # Integratori
    n_integrators = sum(1 for p in poles if np.isclose(p, 0))
    slope -= 20 * n_integrators

    # Funzione per contributo modulo
    def update_slope(freq, delta):
        nonlocal slope
        for i in range(len(w)):
            if w[i] > freq:
                mag[i] += delta * np.log10(w[i]/freq)

    # ZERI
    for z in zeros:
        if np.isclose(z, 0):
            continue

        if np.iscomplex(z):
            wn = abs(z)
            update_slope(wn, +40)  # secondo ordine
        else:
            update_slope(abs(z), +20)

    # POLI
    for p in poles:
        if np.isclose(p, 0):
            continue

        if np.iscomplex(p):
            wn = abs(p)
            update_slope(wn, -40)
        else:
            update_slope(abs(p), -20)

    # integratori (sempre attivi)
    for i in range(len(w)):
        mag[i] += slope * np.log10(w[i])

    # ---------------- FASE ----------------
    phase = np.zeros_like(w)

    for i, omega in enumerate(w):
        phi = 0

        # integratori
        phi -= 90 * n_integrators

        # ZERI
        for z in zeros:
            if np.isclose(z, 0):
                continue

            wn = abs(z)

            if np.iscomplex(z):
                # secondo ordine
                if omega < wn/10:
                    pass
                elif omega > 10*wn:
                    phi += 180
                else:
                    phi += 90 * np.log10(omega/(wn/10))
            else:
                # reale
                if omega < wn/10:
                    pass
                elif omega > 10*wn:
                    phi += 90
                else:
                    phi += 45 * np.log10(omega/(wn/10))

        # POLI
        for p in poles:
            if np.isclose(p, 0):
                continue

            wn = abs(p)

            if np.iscomplex(p):
                # secondo ordine
                if omega < wn/10:
                    pass
                elif omega > 10*wn:
                    phi -= 180
                else:
                    phi -= 90 * np.log10(omega/(wn/10))
            else:
                # reale
                if np.real(p) > 0:
                    # ⚠️ RHP (fase invertita)
                    if omega < wn/10:
                        pass
                    elif omega > 10*wn:
                        phi += 90
                    else:
                        phi += 45 * np.log10(omega/(wn/10))
                else:
                    if omega < wn/10:
                        pass
                    elif omega > 10*wn:
                        phi -= 90
                    else:
                        phi -= 45 * np.log10(omega/(wn/10))

        phase[i] = phi

    # ---------------- PLOT ----------------
    plt.figure()

    plt.subplot(2,1,1)
    plt.semilogx(w, mag)
    plt.title("Bode Asintotico (completo)")
    plt.ylabel("Modulo (dB)")
    plt.grid(True, which="both")

    plt.subplot(2,1,2)
    plt.semilogx(w, phase)
    plt.ylabel("Fase (°)")
    plt.xlabel("Frequenza (rad/s)")
    plt.yticks(np.arange(-360, 361, 45))
    plt.grid(True, which="both")


# -------------------------------
# MAIN
# -------------------------------
def main():
    expr = input("Inserisci G(s): ")

    num, den = parse_transfer_function(expr)

    system = ctrl.TransferFunction(num, den)

    print("\nSistema:")
    print(system)

    # Bode reale
    plt.figure()
    ctrl.bode(system, dB=True, deg=True)

    # Nyquist
    plt.figure()
    ctrl.nyquist(system)

    # Bode approssimato corretto
    bode_asintotico(system)

    plt.show()


if __name__ == "__main__":
    main()
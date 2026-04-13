import sympy as sp
import control as ctrl
import matplotlib.pyplot as plt
import numpy as np

DEBUG=False#if(DEBUG):print(f"[Debug] ")

s = sp.symbols('s')

# -------------------------------
# Parsing funzione classica
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

    return num_coeffs, den_coeffs, expr


# -------------------------------
# Generazione forma di Bode
# -------------------------------
def bode_form(expr):
    num, den = sp.fraction(expr)

    num_factors = sp.factor(num)
    den_factors = sp.factor(den)

    print("\nForma fattorizzata:")
    print("Numeratore:", num_factors)
    print("Denominatore:", den_factors)

    # Estrazione zeri e poli
    zeros = sp.solve(num, s)
    poles = sp.solve(den, s)

    print("\nZeri:", zeros)
    print("Poli:", poles)


# -------------------------------
# Input manuale forma di Bode
# -------------------------------
def input_bode_form():
    print("\nInserisci guadagno K:")
    K = float(input("> "))

    expr = K

    print("Quanti zeri? ")
    z = int(input("> "))
    for _ in range(z):
        print("Zero del tipo (1 + s/w) → inserisci w:")
        w = float(input("> "))
        expr *= (1 + s/w)

    print("Quanti poli? ")
    p = int(input("> "))
    for _ in range(p):
        print("Polo del tipo (1 + s/w) → inserisci w:")
        w = float(input("> "))
        expr /= (1 + s/w)

    print("Quanti integratori (1/s)? ")
    n = int(input("> "))
    expr /= s**n

    return expr

# -------------------------------
# Bode aprossimativo
# -------------------------------

def bode_asintotico(system):
    import numpy as np
    import matplotlib.pyplot as plt

    poles = ctrl.poles(system)
    zeros = ctrl.zeros(system)

    if(DEBUG):print(f"[Debug] poles: {poles}, zeros: {zeros}")

    # Separazione poli/zeri
    wp = sorted([abs(p) for p in poles if p != 0])
    wz = sorted([abs(z) for z in zeros if z != 0])

    # Integratori
    n_integrators = sum(1 for p in poles if p == 0)

    # Frequenze log
    w = np.logspace(-2, 3, 1000)

    # Guadagno iniziale
    num_coeffs = np.asarray(system.num[0][0], dtype=float)
    den_coeffs = np.asarray(system.den[0][0], dtype=float)
    num_leading = abs(num_coeffs[0]) if num_coeffs.size else 1
    den_leading = abs(den_coeffs[0]) if den_coeffs.size else 1
    zero_factor = np.prod(wz) if wz else 1
    pole_factor = np.prod(wp) if wp else 1
    K = (num_leading / den_leading) * (zero_factor / pole_factor)
    #K = 20* np.log()
    mag = np.zeros_like(w)

    if(DEBUG):print(f"[Debug] dcgain: {system.dcgain()}")
    if(DEBUG):print(f"[Debug] system: {system}")
    if(DEBUG):print(f"[Debug] guadagno: {K}") 

    # Lista eventi (frequenze di spezzata)
    events = []
    for z in wz:
        events.append((z, +20))
    for p in wp:
        events.append((p, -20))

    events.sort()

    # Pendenza iniziale
    slope = -20 * n_integrators

    current_mag = 20 * np.log10(K)

    last_w = w[0]

    mag_vals = []

    for omega in w:
        # aggiorna slope se superi breakpoint
        for freq, delta in events:
            if last_w < freq <= omega:
                # aggiorna valore fino al breakpoint
                current_mag += slope * np.log10(freq / last_w)
                slope += delta
                last_w = freq

        # continua con slope corrente
        mag_point = current_mag + slope * np.log10(omega / last_w)
        mag_vals.append(mag_point)

    # -------- FASE (approssimata stile umano) --------
    phase = np.zeros_like(w)
    

    for i, omega in enumerate(w):
        phi = -90 * n_integrators

        for z in wz:
            if omega < z/10:
                pass
            elif omega > 10*z:
                phi += 90
            else:
                phi += 45 * np.log10(omega / (z/10))

        for p in wp:
            if omega < p/10:
                pass
            elif omega > 10*p:
                phi -= 90
            else:
                phi -= 45 * np.log10(omega / (p/10))

        phase[i] = phi

    # -------- PLOT --------
    plt.figure()

    plt.subplot(2,1,1)
    plt.semilogx(w, mag_vals)
    plt.title("Bode Asintotico (CORRETTO)")
    plt.ylabel("Modulo (dB)")
    plt.grid(True, which="both")

    plt.subplot(2,1,2)
    plt.semilogx(w, phase)
    plt.ylabel("Fase (°)")
    plt.xlabel("Frequenza (rad/s)")
    plt.grid(True, which="both")
    plt.yticks(np.arange(min(phase)-45, max(phase)+45, 45))


# -------------------------------
# MAIN
# -------------------------------
def main():
    print("Scegli modalità:")
    print("1 → Funzione G(s)")
    print("2 → Forma di Bode")

    choice = input("> ")

    if choice == "1":
        expr_str = input("Inserisci G(s): ")
        num, den, expr = parse_transfer_function(expr_str)

        bode_form(expr)

    elif choice == "2":
        expr = input_bode_form()
        num, den, _ = parse_transfer_function(str(expr))

    else:
        print("Scelta non valida")
        return
    
    if(DEBUG):print(f"[Debug] num {num}, den {den}")
    system = ctrl.TransferFunction(num, den)

    print("\nSistema:")
    print(system)

    # Bode
    plt.figure()
    ctrl.bode(system, dB=True, deg=True)

    bode_asintotico(system)

    #Nyquist polar
    plt.figure()
    ctrl.nyquist(system)
    ax=plt.gca()
    def format_coord(x,y):
        r= np.sqrt(x**2+y**2)
        theta=np.arctan2(y,x)
        theta=np.degrees(theta)
        return f"x={x:.2f}, y={y:.2f} | r={r:.2f}, θ={theta:.2f} grad"
    ax.format_coord=format_coord
    plt.show()

if __name__ == "__main__":
    main()
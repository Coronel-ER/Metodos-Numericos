import math
import csv
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def modelo_exponencial(p0, r, t):
    return p0 * math.exp(r * t)


def taylor_exp(x, n):
    suma = 1.0
    termino = 1.0
    for i in range(1, n):
        termino *= x / i
        suma += termino
    return suma


def modelo_taylor(p0, r, t, n):
    return p0 * taylor_exp(r * t, n)

#errores

def error_absoluto(real, aproximado):
    return abs(real - aproximado)


def error_relativo(real, aproximado):
    if real == 0:
        return 0.0
    return abs((real - aproximado) / real) * 100

#casos de ejemplo
def casos_ejemplo():
    casos = {
        1: {
            "nombre": "Poblacion de Mexico",
            "p0": 130_000_000,
            "r": 0.011,
            "tiempo_max": 20,
            "unidad_tiempo": "años",
            "descripcion": "Crecimiento anual de Mexico (~1.1% anual). t en años."
        },
        2: {
            "nombre": "Cultivo de bacterias",
            "p0": 1_000,
            "r": 0.35,
            "tiempo_max": 10,
            "unidad_tiempo": "horas",
            "descripcion": "Colonia bacteriana en medio de cultivo. t en horas."
        },
        3: {
            "nombre": "Propagacion de virus",
            "p0": 50,
            "r": 0.25,
            "tiempo_max": 14,
            "unidad_tiempo": "dias",
            "descripcion": "Casos iniciales de un virus en poblacion cerrada. t en dias."
        },
        4: {
            "nombre": "Inversion financiera",
            "p0": 10_000,
            "r": 0.08,
            "tiempo_max": 20,
            "unidad_tiempo": "años",
            "descripcion": "Capital con interes compuesto continuo al 8% anual. t en años."
        },
        5: {
            "nombre": "Celulas cancerosas",
            "p0": 100,
            "r": 0.15,
            "tiempo_max": 30,
            "unidad_tiempo": "dias",
            "descripcion": "Crecimiento de tumor en etapa inicial. t en dias."
        },
        6: {
            "nombre": "Usuarios de red social",
            "p0": 500,
            "r": 0.05,
            "tiempo_max": 24,
            "unidad_tiempo": "meses",
            "descripcion": "Adopcion de plataforma digital. t en meses."
        }
    }
    return casos

# entrada de datos
def pedir_datos_manuales():
    p0 = float(input("  Poblacion inicial (P0): "))
    r = float(input("  Tasa de crecimiento r (ej. 0.02): "))
    tiempo_max = int(input("  Tiempo maximo: "))
    unidad = input("  Unidad de tiempo (años/dias/horas/meses): ").strip()
    if not unidad:
        unidad = "unidades"
    return p0, r, tiempo_max, unidad


def menu_principal():
    print("Estimacion del crecimiento poblacional mediante modelos exponenciales y aproximación con la serie de Taylor ")
    print("\n  1. Usar caso de ejemplo")
    print("  2. Ingresar datos manualmente")
    opcion = input("\n  Opcion: ").strip()
    return opcion


def mostrar_casos(casos):
    print("\n--- Casos disponibles ---")
    for clave, caso in casos.items():
        print(f"  {clave}. {caso['nombre']}")
        print(f"     {caso['descripcion']}")
    while True:
        try:
            eleccion = int(input("\n  Elige el numero de caso: "))
            if eleccion in casos:
                return casos[eleccion]
            print("  Opcion no valida, intenta de nuevo.")
        except ValueError:
            print("  Ingresa un numero valido.")


#Calculo de resultados

def calcular_resultados(p0, r, tiempo_max, n):
    tiempos, exactos, aproximados = [], [], []
    errores_abs, errores_rel = [], []

    for t in range(tiempo_max + 1):
        exacto = modelo_exponencial(p0, r, t)
        aproximado = modelo_taylor(p0, r, t, n)
        tiempos.append(t)
        exactos.append(exacto)
        aproximados.append(aproximado)
        errores_abs.append(error_absoluto(exacto, aproximado))
        errores_rel.append(error_relativo(exacto, aproximado))

    return tiempos, exactos, aproximados, errores_abs, errores_rel


#tablas

def imprimir_tabla(tiempos, exactos, aproximados, errores_abs, errores_rel, n, unidad):
    print(f"\n Resultados con n = {n} terminos de Taylor")
    print(f"{'t (' + unidad + ')':^12}{'Exacto':^20}{'Taylor':^20}{'Error Abs':^18}{'Error %':^12}")
    print("-" * 82)
    for i in range(len(tiempos)):
        print(f"{tiempos[i]:^12}"
              f"{exactos[i]:^20.4f}"
              f"{aproximados[i]:^20.4f}"
              f"{errores_abs[i]:^18.4f}"
              f"{errores_rel[i]:^12.6f}")


def imprimir_comparacion(tiempos, exactos, resultados_por_n, unidad):
    print(f"\nComparacion de aproximaciones")
    encabezado = f"{'t (' + unidad + ')':^12}{'Exacto':^18}"
    for n in resultados_por_n:
        encabezado += f"{'n='+str(n):^18}"
    print(encabezado)
    print("-" * len(encabezado))

    for i in range(len(tiempos)):
        fila = f"{tiempos[i]:^12}{exactos[i]:^18.4f}"
        for n in resultados_por_n:
            fila += f"{resultados_por_n[n]['aproximados'][i]:^18.4f}"
        print(fila)

    print("\n Error relativo promedio")
    for n in resultados_por_n:
        errores = resultados_por_n[n]['errores_rel']
        promedio = sum(errores) / len(errores)
        print(f"  n = {n} -> {promedio:.6f}%")


def exportar_csv(tiempos, exactos, resultados_por_n, nombre_archivo, unidad):
    with open(nombre_archivo, 'w', newline='') as archivo:
        escritor = csv.writer(archivo)
        encabezado = [f'tiempo ({unidad})', 'exacto']
        for n in resultados_por_n:
            encabezado += [f'taylor_n{n}', f'error_abs_n{n}', f'error_rel_%_n{n}']
        escritor.writerow(encabezado)

        for i in range(len(tiempos)):
            fila = [tiempos[i], exactos[i]]
            for n in resultados_por_n:
                fila += [
                    resultados_por_n[n]['aproximados'][i],
                    resultados_por_n[n]['errores_abs'][i],
                    resultados_por_n[n]['errores_rel'][i]
                ]
            escritor.writerow(fila)

    print(f"\n  Datos exportados: {nombre_archivo}")


#diseno graficas

COLORES_N = {3: '#e74c3c', 5: '#f39c12', 7: '#2ecc71'}
ESTILOS_N = {3: '--', 5: '-.', 7: ':'}
MARCADORES_N = {3: 's', 5: '^', 7: 'd'}


def graficar_todo(tiempos, exactos, resultados_por_n, titulo, unidad):
    fig = plt.figure(figsize=(14, 9))
    fig.suptitle(f"Análisis numérico — {titulo}", fontsize=14, fontweight='bold', y=0.98)

    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)
    ax_pob   = fig.add_subplot(gs[0, 0])
    ax_errel = fig.add_subplot(gs[0, 1])
    ax_erabs = fig.add_subplot(gs[1, :])

#poblacion
    ax_pob.plot(tiempos, exactos, color='black', linewidth=2.5,
                marker='o', markersize=4, label='Exacto e^(rt)', zorder=5)
    for n in resultados_por_n:
        ax_pob.plot(tiempos, resultados_por_n[n]['aproximados'],
                    color=COLORES_N[n], linestyle=ESTILOS_N[n],
                    linewidth=1.8, marker=MARCADORES_N[n], markersize=4,
                    label=f'Taylor n={n}')
    ax_pob.set_title("Población vs Tiempo")
    ax_pob.set_xlabel(f"Tiempo ({unidad})")
    ax_pob.set_ylabel("Población")
    ax_pob.legend(fontsize=8)
    ax_pob.grid(True, alpha=0.4)
    # Formato de eje Y con separadores de miles
    ax_pob.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f"{x:,.0f}")
    )
#error relativo
    for n in resultados_por_n:
        ax_errel.plot(tiempos, resultados_por_n[n]['errores_rel'],
                      color=COLORES_N[n], linestyle=ESTILOS_N[n],
                      linewidth=1.8, marker=MARCADORES_N[n], markersize=4,
                      label=f'n={n}')
    ax_errel.set_title("Error Relativo (%) vs Tiempo")
    ax_errel.set_xlabel(f"Tiempo ({unidad})")
    ax_errel.set_ylabel("Error relativo (%)")
    ax_errel.legend(fontsize=8)
    ax_errel.grid(True, alpha=0.4)
    ax_errel.axhline(y=1, color='gray', linestyle=':', linewidth=1,
                     label='1% umbral')

  #error absoluto
    usa_log = False
    for n in resultados_por_n:
        errs = resultados_por_n[n]['errores_abs']
        if max(errs) > 0 and max(errs) / (min(e for e in errs if e > 0) or 1) > 1000:
            usa_log = True
            break

    for n in resultados_por_n:
        ax_erabs.plot(tiempos, resultados_por_n[n]['errores_abs'],
                      color=COLORES_N[n], linestyle=ESTILOS_N[n],
                      linewidth=1.8, marker=MARCADORES_N[n], markersize=4,
                      label=f'n={n}')

    if usa_log:
        ax_erabs.set_yscale('log')
        ax_erabs.set_ylabel("Error absoluto (escala log)")
    else:
        ax_erabs.set_ylabel("Error absoluto")
        ax_erabs.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, _: f"{x:,.4f}")
        )

    ax_erabs.set_title("Error Absoluto vs Tiempo")
    ax_erabs.set_xlabel(f"Tiempo ({unidad})")
    ax_erabs.legend(fontsize=8)
    ax_erabs.grid(True, alpha=0.4)

    for n in sorted(resultados_por_n.keys()):
        errs_rel = resultados_por_n[n]['errores_rel']
        t_ok = next((tiempos[i] for i, e in enumerate(errs_rel) if e < 1.0), None)
        if t_ok is not None:
            ax_errel.annotate(
                f"n={n}: <1% error\nhasta t={t_ok}",
                xy=(t_ok, 1), xytext=(t_ok + 0.5, max(errs_rel) * 0.6),
                fontsize=7, color=COLORES_N[n],
                arrowprops=dict(arrowstyle='->', color=COLORES_N[n], lw=1)
            )
        break  # solo anotar para n=3

    plt.savefig(f"grafica_{titulo.replace(' ', '_')}.png", dpi=150, bbox_inches='tight')
    print(f"  Grafica guardada: grafica_{titulo.replace(' ', '_')}.png")
    plt.show()


# analisis final

def imprimir_analisis(resultados_por_n, p0, r, tiempo_max, unidad):
    print("  ANALISIS DE RESULTADOS")

    print(f"\n  Modelo: P(t) = {p0:,.0f} * e^({r}*t)")
    print(f"  Tiempo maximo: {tiempo_max} {unidad}")
    print("\n  Error relativo promedio por numero de terminos:")
    mejor_n = None
    mejor_error = float('inf')

    for n in resultados_por_n:
        errores = resultados_por_n[n]['errores_rel']
        promedio = sum(errores) / len(errores)
        max_err = max(errores)
        print(f"    n = {n}  ->  promedio: {promedio:.6f}%  |  maximo: {max_err:.4f}%")
        if promedio < mejor_error:
            mejor_error = promedio
            mejor_n = n

    print(f"\n  Mejor aproximacion: n = {mejor_n} terminos")
    print(f"  Error promedio: {mejor_error:.8f}%")

    if mejor_error < 0.001:
        nivel = "EXCELENTE — practicamente identico al valor exacto"
    elif mejor_error < 1:
        nivel = "MUY BUENO — error por debajo del 1%"
    elif mejor_error < 5:
        nivel = "ACEPTABLE — error por debajo del 5%"
    else:
        nivel = "CONSIDERABLE — se recomienda aumentar n"

    print(f"  Nivel de precision: {nivel}")


# ─────────────────────────────────────────────
#  PROGRAMA PRINCIPAL
# ─────────────────────────────────────────────

def main():
    try:
        opcion = menu_principal()

        if opcion == "1":
            casos = casos_ejemplo()
            caso = mostrar_casos(casos)
            p0 = caso['p0']
            r = caso['r']
            tiempo_max = caso['tiempo_max']
            unidad = caso['unidad_tiempo']
            titulo = caso['nombre']

            print(f"\n  Caso seleccionado: {titulo}")
            print(f"  Poblacion inicial (P0): {p0:,.0f}")
            print(f"  Tasa de crecimiento (r): {r}")
            print(f"  Tiempo maximo: {tiempo_max} {unidad}")
        else:
            p0, r, tiempo_max, unidad = pedir_datos_manuales()
            titulo = "Datos manuales"

        if p0 <= 0:
            print("\n  Error: la poblacion inicial debe ser positiva.")
            return

        valores_n = [3, 5, 7]

        resultados_por_n = {}
        tiempos = exactos = None

        for n in valores_n:
            t, e, a, ea, er = calcular_resultados(p0, r, tiempo_max, n)
            tiempos, exactos = t, e
            resultados_por_n[n] = {
                'aproximados': a,
                'errores_abs': ea,
                'errores_rel': er
            }

        # Tabla detallada del primer n
        imprimir_tabla(
            tiempos, exactos,
            resultados_por_n[3]['aproximados'],
            resultados_por_n[3]['errores_abs'],
            resultados_por_n[3]['errores_rel'],
            3, unidad
        )

        # Comparacion
        imprimir_comparacion(tiempos, exactos, resultados_por_n, unidad)

        # CSV
        nombre_csv = f"resultados_{titulo.replace(' ', '_')}.csv"
        exportar_csv(tiempos, exactos, resultados_por_n, nombre_csv, unidad)

        # Grafica unica con 3 paneles
        graficar_todo(tiempos, exactos, resultados_por_n, titulo, unidad)

        # Analisis
        imprimir_analisis(resultados_por_n, p0, r, tiempo_max, unidad)

    except ValueError:
        print("\n  Error: ingresa solo valores numericos validos.")
    except KeyError:
        print("\n  Error: caso no encontrado.")
    except Exception as e:
        print(f"\n  Error inesperado: {e}")


if __name__ == "__main__":
    main()

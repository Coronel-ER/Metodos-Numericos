import math
import csv
import matplotlib.pyplot as plt


# modelo exponencial exacto
def modelo_exponencial(p0, r, t):
    return p0 * math.exp(r * t)


# aproximacion e^x taylor
def taylor_exp(x, n):

    suma = 1.0
    termino = 1.0

    # serie de taylor
    for i in range(1, n):

        termino *= x / i
        suma += termino

    return suma


# modelo con taylor
def modelo_taylor(p0, r, t, n):
    return p0 * taylor_exp(r * t, n)


# error absoluto
def error_absoluto(real, aproximado):
    return abs(real - aproximado)


# error relativo
def error_relativo(real, aproximado):
    if real == 0:
        return 0
    return abs((real - aproximado) / real) * 100


# casos de ejemplo predefinidos
def casos_ejemplo():

    casos = {
        1: {
            "nombre": "poblacion de mexico",
            "p0": 130000000,
            "r": 0.011,
            "tiempo_max": 10,
            "descripcion": "crecimiento aproximado anual de mexico (1.1%)"
        },
        2: {
            "nombre": "cultivo de bacterias",
            "p0": 1000,
            "r": 0.35,
            "tiempo_max": 8,
            "descripcion": "crecimiento rapido de colonia bacteriana"
        },
        3: {
            "nombre": "propagacion de virus",
            "p0": 50,
            "r": 0.25,
            "tiempo_max": 10,
            "descripcion": "casos de un virus en una poblacion cerrada"
        },
        4: {
            "nombre": "inversion financiera",
            "p0": 10000,
            "r": 0.08,
            "tiempo_max": 15,
            "descripcion": "capital con interes compuesto continuo al 8%"
        }
    }

    return casos


# pedir datos al usuario
def pedir_datos_manuales():

    p0 = float(input("ingresa la poblacion inicial: "))
    r = float(input("ingresa la tasa de crecimiento: "))
    tiempo_max = int(input("ingresa el tiempo maximo: "))

    return p0, r, tiempo_max


# elegir modo de entrada
def menu_principal():

    print("\n==========================================")
    print(" crecimiento poblacional - serie taylor ")
    print("==========================================")
    print("\nelige una opcion:")
    print("  1. usar caso de ejemplo")
    print("  2. ingresar datos manualmente")

    opcion = input("\nopcion: ").strip()

    return opcion


# mostrar los casos de ejemplo
def mostrar_casos(casos):

    print("\n--- casos disponibles ---")

    for clave, caso in casos.items():
        print(f"  {clave}. {caso['nombre']}")
        print(f"     {caso['descripcion']}")

    eleccion = int(input("\nelige el caso: "))

    return casos[eleccion]


# calcular tabla de resultados para un n
def calcular_resultados(p0, r, tiempo_max, n):

    tiempos = []
    exactos = []
    aproximados = []
    errores_abs = []
    errores_rel = []

    for t in range(tiempo_max + 1):

        exacto = modelo_exponencial(p0, r, t)
        aproximado = modelo_taylor(p0, r, t, n)
        error_abs = error_absoluto(exacto, aproximado)
        error_rel = error_relativo(exacto, aproximado)

        tiempos.append(t)
        exactos.append(exacto)
        aproximados.append(aproximado)
        errores_abs.append(error_abs)
        errores_rel.append(error_rel)

    return tiempos, exactos, aproximados, errores_abs, errores_rel


# imprimir tabla de un solo n
def imprimir_tabla(tiempos, exactos, aproximados, errores_abs, errores_rel, n):

    print(f"\n--- resultados con n = {n} terminos ---")
    print(f"{'t':^5}{'exacto':^20}{'taylor':^20}{'error abs':^18}{'error %':^12}")
    print("-" * 75)

    for i in range(len(tiempos)):

        print(f"{tiempos[i]:^5}"
              f"{exactos[i]:^20.6f}"
              f"{aproximados[i]:^20.6f}"
              f"{errores_abs[i]:^18.6f}"
              f"{errores_rel[i]:^12.6f}")


# imprimir comparacion de varios n
def imprimir_comparacion(tiempos, exactos, resultados_por_n):

    print("\n--- comparacion con diferentes n ---")

    encabezado = f"{'t':^5}{'exacto':^18}"

    for n in resultados_por_n.keys():
        encabezado += f"{'n=' + str(n):^18}"

    print(encabezado)
    print("-" * len(encabezado))

    for i in range(len(tiempos)):

        fila = f"{tiempos[i]:^5}{exactos[i]:^18.4f}"

        for n in resultados_por_n.keys():

            aprox = resultados_por_n[n]['aproximados'][i]
            fila += f"{aprox:^18.4f}"

        print(fila)

    # promedios de error
    print("\n--- error relativo promedio ---")

    for n in resultados_por_n.keys():

        errores = resultados_por_n[n]['errores_rel']
        promedio = sum(errores) / len(errores)
        print(f"  n = {n} terminos -> error promedio: {promedio:.6f}%")


# guardar resultados en csv
def exportar_csv(tiempos, exactos, resultados_por_n, nombre_archivo):

    with open(nombre_archivo, 'w', newline='') as archivo:

        escritor = csv.writer(archivo)

        # encabezado
        encabezado = ['tiempo', 'exacto']

        for n in resultados_por_n.keys():
            encabezado.append(f'taylor_n{n}')
            encabezado.append(f'error_abs_n{n}')
            encabezado.append(f'error_rel_n{n}')

        escritor.writerow(encabezado)

        # filas de datos
        for i in range(len(tiempos)):

            fila = [tiempos[i], exactos[i]]

            for n in resultados_por_n.keys():

                fila.append(resultados_por_n[n]['aproximados'][i])
                fila.append(resultados_por_n[n]['errores_abs'][i])
                fila.append(resultados_por_n[n]['errores_rel'][i])

            escritor.writerow(fila)

    print(f"\narchivo guardado: {nombre_archivo}")


# graficar comparacion del modelo
def graficar_modelos(tiempos, exactos, resultados_por_n, titulo):

    plt.figure(figsize=(9, 5))

    plt.plot(
        tiempos,
        exactos,
        marker='o',
        linewidth=2.5,
        label='modelo exacto',
        color='black'
    )

    estilos = ['--', '-.', ':']
    marcadores = ['s', '^', 'd']

    i = 0

    for n in resultados_por_n.keys():

        plt.plot(
            tiempos,
            resultados_por_n[n]['aproximados'],
            marker=marcadores[i % len(marcadores)],
            linestyle=estilos[i % len(estilos)],
            linewidth=1.8,
            label=f'taylor n={n}'
        )

        i += 1

    plt.title(f"crecimiento poblacional - {titulo}")
    plt.xlabel("tiempo")
    plt.ylabel("poblacion")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


# graficar errores absolutos
def graficar_error_absoluto(tiempos, resultados_por_n):

    plt.figure(figsize=(9, 5))

    for n in resultados_por_n.keys():

        plt.plot(
            tiempos,
            resultados_por_n[n]['errores_abs'],
            marker='d',
            label=f'n = {n}'
        )

    plt.title("error absoluto vs tiempo")
    plt.xlabel("tiempo")
    plt.ylabel("error absoluto")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


# graficar errores relativos
def graficar_error_relativo(tiempos, resultados_por_n):

    plt.figure(figsize=(9, 5))

    for n in resultados_por_n.keys():

        plt.plot(
            tiempos,
            resultados_por_n[n]['errores_rel'],
            marker='o',
            label=f'n = {n}'
        )

    plt.title("error relativo (%) vs tiempo")
    plt.xlabel("tiempo")
    plt.ylabel("error relativo (%)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


# analisis final
def imprimir_analisis(resultados_por_n):

    print("\n==========================================")
    print("analisis de resultados")
    print("==========================================")

    print("\nformula utilizada:")
    print("  e^x ≈ 1 + x + x^2/2! + x^3/3! + ... + x^(n-1)/(n-1)!")

    print("\nerror relativo promedio por cada n:")

    mejor_n = None
    mejor_error = float('inf')

    for n in resultados_por_n.keys():

        errores = resultados_por_n[n]['errores_rel']
        promedio = sum(errores) / len(errores)

        print(f"  n = {n} -> {promedio:.6f}%")

        if promedio < mejor_error:
            mejor_error = promedio
            mejor_n = n

    print(f"\nla mejor aproximacion fue con n = {mejor_n} terminos")
    print(f"con un error promedio de {mejor_error:.6f}%")

    if mejor_error < 1:
        print("la aproximacion es altamente precisa")
    elif mejor_error < 5:
        print("la aproximacion es aceptable")
    else:
        print("la aproximacion presenta errores considerables")

    print("\nconclusion:")
    print("al aumentar el numero de terminos de la serie de taylor")
    print("el error disminuye y la aproximacion se acerca al")
    print("valor exacto del modelo exponencial.")


# programa principal
def main():

    try:

        opcion = menu_principal()

        # elegir fuente de datos
        if opcion == "1":

            casos = casos_ejemplo()
            caso = mostrar_casos(casos)

            p0 = caso['p0']
            r = caso['r']
            tiempo_max = caso['tiempo_max']
            titulo = caso['nombre']

            print(f"\ncaso seleccionado: {titulo}")
            print(f"  poblacion inicial: {p0}")
            print(f"  tasa de crecimiento: {r}")
            print(f"  tiempo maximo: {tiempo_max}")

        else:

            p0, r, tiempo_max = pedir_datos_manuales()
            titulo = "datos manuales"

        # validar datos
        if p0 <= 0:
            print("error: la poblacion debe ser positiva")
            return

        # valores de n para comparar
        print("\nse compararan las aproximaciones con n = 3, 5 y 7 terminos")

        valores_n = [3, 5, 7]

        # calcular para cada n
        resultados_por_n = {}
        tiempos = None
        exactos = None

        for n in valores_n:

            t, e, a, ea, er = calcular_resultados(p0, r, tiempo_max, n)

            tiempos = t
            exactos = e

            resultados_por_n[n] = {
                'aproximados': a,
                'errores_abs': ea,
                'errores_rel': er
            }

        # mostrar tabla detallada del primero
        imprimir_tabla(
            tiempos,
            exactos,
            resultados_por_n[valores_n[0]]['aproximados'],
            resultados_por_n[valores_n[0]]['errores_abs'],
            resultados_por_n[valores_n[0]]['errores_rel'],
            valores_n[0]
        )

        # mostrar comparacion
        imprimir_comparacion(tiempos, exactos, resultados_por_n)

        # exportar csv
        nombre_csv = f"resultados_{titulo.replace(' ', '_')}.csv"
        exportar_csv(tiempos, exactos, resultados_por_n, nombre_csv)

        # graficas
        graficar_modelos(tiempos, exactos, resultados_por_n, titulo)
        graficar_error_absoluto(tiempos, resultados_por_n)
        graficar_error_relativo(tiempos, resultados_por_n)

        # analisis final
        imprimir_analisis(resultados_por_n)

    except ValueError:
        print("error: ingresa solo valores numericos")

    except Exception as e:
        print("ocurrio un error:", e)


# ejecutar
if __name__ == "__main__":
    main()

import math
import matplotlib.pyplot as plt


#modelo exponencial excato
def modelo_exponencial(p0, r, t):
    return p0 * math.exp(r * t)


# aproximacion e^x taloyre

def taylor_exp(x, n):
    suma = 1.0
    termino = 1.0

    for i in range(1, n):
        termino *= x / i
        suma += termino

    return suma


#modelo con taylor
def modelo_taylor(p0, r, t, n):
    return p0 * taylor_exp(r * t, n)


#error absoluto
def error_absoluto(real, aproximado):
    return abs(real - aproximado)


#error relativo
def error_relativo(real, aproximado):
    return abs((real - aproximado) / real) * 100


#progrma
def main():

    print("==========================================")
    print(" CRECIMIENTO POBLACIONAL - SERIE TAYLOR ")
    print("==========================================")

    try:

        
        p0 = float(input("Ingresa la población inicial: "))
        r = float(input("Ingresa la tasa de crecimiento: "))
        tiempo_max = int(input("Ingresa el tiempo máximo: "))

        print("\n==========================================")
        print("RESULTADOS")
        print("==========================================")

        tiempos = []
        exactos = []
        aproximados = []

        #encabezado de a tabla
        print(f"{'t':<5}{'Exacto':<20}{'Taylor':<20}{'Error Abs':<15}{'Error %'}")

        # calculos
        for t in range(tiempo_max + 1):

            exacto = modelo_exponencial(p0, r, t)

            # usar 6 términos de Taylor
            aproximado = modelo_taylor(p0, r, t, 6)

            error_abs = error_absoluto(exacto, aproximado)
            error_rel = error_relativo(exacto, aproximado)

            tiempos.append(t)
            exactos.append(exacto)
            aproximados.append(aproximado)

            print(f"{t:<5}{exacto:<20.6f}{aproximado:<20.6f}{error_abs:<15.6f}{error_rel:.6f}%")

       #grafica

        plt.plot(tiempos, exactos, marker='o', label='Modelo Exacto')
        plt.plot(tiempos, aproximados, marker='s', label='Taylor')

        plt.title("Crecimiento Poblacional")
        plt.xlabel("Tiempo")
        plt.ylabel("Población")
        plt.grid(True)
        plt.legend()

        plt.show()

       #analisis de los resultados

        print("\n==========================================")
        print("ANÁLISIS")
        print("==========================================")

        print("La aproximación mediante la serie de Taylor")
        print("produce resultados muy cercanos al modelo")
        print("exponencial exacto.")
        print("Al aumentar el número de términos,")
        print("el error disminuye considerablemente.")

    except ValueError:
        print("Error: Ingresa únicamente valores numéricos.")

    except Exception as e:
        print("Ocurrió un error:", e)

#ejecutar
if __name__ == "__main__":
    main()

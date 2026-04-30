import tkinter as tk
import math

def clicar(tecla):
    atual = entrada.get()
    entrada.delete(0, tk.END)
    if tecla == ',':
        entrada.insert(0, atual + '.')
    else:
        entrada.insert(0, atual + str(tecla))

def calcular():
    try:
        expressao = entrada.get()
        expressao = expressao.replace('^', '**')
        while '√' in expressao:
            pos = expressao.find('√')
            if pos + 1 < len(expressao) and expressao[pos + 1] == '(':
                # √(algo)
                count = 1
                i = pos + 2
                while i < len(expressao) and count > 0:
                    if expressao[i] == '(':
                        count += 1
                    elif expressao[i] == ')':
                        count -= 1
                    i += 1
                sub_expr = expressao[pos + 2:i - 1]
                expressao = expressao[:pos] + f'({sub_expr})**0.5' + expressao[i:]
            else:
                i = pos + 1
                while i < len(expressao) and (expressao[i].isalnum() or expressao[i] == '.'):
                    i += 1
                sub_expr = expressao[pos + 1:i]
                expressao = expressao[:pos] + f'({sub_expr})**0.5' + expressao[i:]

        contexto = {
            'log': math.log10,
            '__builtins__': None
        }

        resultado = eval(expressao, contexto)
        entrada.delete(0, tk.END)
        entrada.insert(0, str(resultado))

    except ZeroDivisionError:
        entrada.delete(0, tk.END)
        entrada.insert(0, 'Erro (divisão por zero)')
    except Exception:
        entrada.delete(0, tk.END)
        entrada.insert(0, 'Erro')

def limpar():
    entrada.delete(0, tk.END)

def apagar_ultimo():
    atual = entrada.get()
    entrada.delete(0, tk.END)
    entrada.insert(0, atual[:-1])

janela = tk.Tk()
janela.title('Calculadora')
janela.geometry('415x600')

entrada = tk.Entry(janela, width=18, font=('Arial', 20), borderwidth=2, relief='solid', justify='right')
entrada.grid(row=0, column=0, columnspan=4, padx=10, pady=20)

botoes = [
    ('^', 1, 0), ('√', 1, 1), ('log(', 1, 2), ('/', 1, 3),
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3),
    ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
    ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
    ('0', 5, 0), (',', 5, 1), ('=', 6, 2), ('CE', 5, 3),
    ('(', 6, 0), (')', 6, 1), ('C', 5, 2)
]

for (texto, linha, coluna) in botoes:
    if texto == '=':
        botao = tk.Button(janela, text=texto, width=5, height=2, font=('Arial', 18), command=calcular)
    elif texto == 'C':
        botao = tk.Button(janela, text=texto, width=5, height=2, font=('Arial', 18), command=limpar)
    elif texto == 'CE':
        botao = tk.Button(janela, text=texto, width=5, height=2, font=('Arial', 18), command=apagar_ultimo)
    else:
        botao = tk.Button(janela, text=texto, width=5, height=2, font=('Arial', 18), command=lambda t=texto: clicar(t))
    botao.grid(row=linha, column=coluna, padx=5, pady=5)

janela.mainloop()
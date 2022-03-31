
# Definicion de los nombres de los tokens
tokens  = (
    'CALCULAR',
    'PARIZQ',
    'PARDER',
    'PTCOMA',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'ENTERO',
    'DECIMAL'
)

# Definicion de palabras reservadas y simbolos del lenguaje
t_CALCULAR  = r'calcular'
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_PTCOMA    = r';'
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'

# Definicion de ER para numero enteros y decimales
def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Floaat value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Definicion de caracteres ignorados
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
# Definicion de caractet ilegal
def t_error(t):
    print("Error lexico, caracter ilegal: '%s'" % t.value[0])
    t.lexer.skip(1)


 
# Construccion del analizador lexico
import ply.lex as lex
lexer = lex.lex()

# Precedencia de operadores
precedence = (
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO'),
    ('right','NEGATIVO'),
)

# Definición de la gramática

def p_instrucciones_lista(t):
    '''instrucciones    : instruccion instrucciones
                        | instruccion '''

def p_instruccion_calcular(t):
    'instruccion : CALCULAR PARIZQ expresion PARDER PTCOMA'
    print('El valor de la expresión es: ' + str(t[3]))

def p_expresion_binaria(t):
    '''expresion : expresion MAS expresion
                  | expresion MENOS expresion
                  | expresion POR expresion
                  | expresion DIVIDIDO expresion'''
    if t[2] == '+'  : t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]

def p_expresion_unaria(t):
    'expresion : MENOS expresion %prec NEGATIVO'
    t[0] = -t[2]

def p_expresion_agrupacion(t):
    'expresion : PARIZQ expresion PARDER'
    t[0] = t[2]

def p_expresion_numero(t):
    '''expresion    : ENTERO
                    | DECIMAL'''
    t[0] = t[1]

def p_error(t):
    print("Error sintactico en: '%s'" % t.value)


import ply.yacc as yacc
parser = yacc.yacc()

#Leer entrada y analizarla
f = open("./entrada.txt", "r")
input = f.read()
print(input)
parser.parse(input)
import re
import os

palavras_reservadas = {'int', 'char', 'long', 'short', 'float', 'double', 'void', 'if', 'else', 'for', 'while', 'do', 'break', 'continue', 'struct', 'switch', 'case', 'default', 'return'}
operadores = {'=', '+', '-', '*', '/', '++', '--', '!', '&', '%', '->', '==', '!=', '||', '&&', '+=', '-=', '*=', '/=', '<', '>', '<=', '>='}
delimitadores = {'(', ')', '[', ']', '{', '}', ';', ','}
const_inteira = r'\d+'
const_ponto_flutuante = r'\d+\.\d+'
const_textual = r'"[^\n]*"'
identificador = r'[a-zA-Z_][a-zA-Z0-9_™]*'
const_identificador = r'\d+[a-zA-Z_][a-zA-Z0-9_]*'
expressao_regular = '|'.join([
    re.escape(palavra) for palavra in palavras_reservadas | operadores | delimitadores
])
expressao_regular += f'|{const_identificador}|{const_inteira}|{const_ponto_flutuante}|{const_textual}|{identificador}'

def analisador_lexico(path):
    with open(path, 'r') as f:
        codigo = removeComments(f.read())

    tokens = re.findall(expressao_regular, codigo)
    tipos = []
    for token in tokens:
        if token in palavras_reservadas:
            tipos.append(('PALAVRA RESERVADA', token))
        elif token in operadores:
            tipos.append(('OPERADOR', token))
        elif token in delimitadores:
            tipos.append(('DELIMITADOR', token))
        elif re.match(const_inteira, token):
            if not all(c.isdigit() for c in token):
                tipos.append(('TOKEN INVALIDO', token))
            else:
                tipos.append(('CONSTANTE INTEIRA', token))
        elif re.match(const_ponto_flutuante, token):
            tipos.append(('CONSTANTE PONTO FLUTUANTE', token))
        elif re.match(const_textual, token):
            tipos.append(('CONSTANTE TEXTUAL', token))
        elif re.match(identificador, token):
            if token[0].isdigit():
                tipos.append(('TOKEN INVALIDO', token))
            elif token in palavras_reservadas:
                tipos.append(('PALAVRA RESERVADA', token))
            elif not all(c.isalnum() or c == '_' for c in token):
                tipos.append(('TOKEN INVALIDO', token))
            else:
                tipos.append(('IDENTIFICADOR', token))
        else:
            tipos.append(('TOKEN INVALIDO', token))
    return tipos

def removeComments(codigo):
    pattern = r'\/\*[\s\S]*?\*\/|\/\/.*'
    return re.sub(pattern, '', codigo)


for arquivo in os.listdir("./codigos"):
    if arquivo.endswith('.c'):
        path = os.path.join("./codigos", arquivo)
        tipos = analisador_lexico(path)
        print(f'Arquivo: {arquivo}')
        for tipo in tipos:
            print(tipo)
        print('\n')

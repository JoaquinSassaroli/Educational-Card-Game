"""
Archivo de preguntas para el modo Intruso
Contiene todas las opciones de preguntas organizadas por materia
"""

# Preguntas del modo Intruso organizadas por materia
PREGUNTAS_INTRUSO = {
    "Matemáticas": [
        # Números pares vs impar
        ([2, 4, 6, 8, 10], 7, "números pares"),  # 7 es impar entre pares
        ([1, 3, 5, 7, 9], 4, "números impares"),   # 4 es par entre impares
        
        # Números primos vs compuesto
        ([2, 3, 5, 7, 11], 9, "números primos"),  # 9 no es primo
        ([4, 6, 8, 9, 10], 7, "números compuestos"),  # 7 es primo entre compuestos
        
        # Múltiplos de un número
        ([5, 10, 15, 20, 25], 12, "múltiplos de 5"),  # 12 no es múltiplo de 5
        ([3, 6, 9, 12, 15], 8, "múltiplos de 3"),     # 8 no es múltiplo de 3
        
        # Números de una cifra vs dos cifras
        ([1, 2, 3, 4, 5], 12, "números de una cifra"),      # 12 tiene dos cifras
        ([10, 11, 12, 13, 14], 5, "números de dos cifras"), # 5 tiene una cifra
    ],
    
    "Historia": [
        # Fechas del siglo XX vs otra época
        (["1914", "1939", "1969", "1989", "1991"], "1492", "fechas del siglo XX"),  # 1492 es del siglo XV
        
        # Personajes argentinos vs extranjero
        (["San Martín", "Belgrano", "Sarmiento", "Rivadavia", "Moreno"], "Napoleón", "personajes argentinos"),
        
        # Guerras mundiales vs otro conflicto
        (["Primera Guerra", "Segunda Guerra", "Guerra Fría", "Guerra Vietnam", "Guerra Corea"], "Revolución Francesa", "conflictos del siglo XX"),
        
        # Países americanos vs europeo
        (["Argentina", "Brasil", "Chile", "Perú", "Colombia"], "Francia", "países americanos"),
        
        # Siglo XIX vs otra época
        (["1810", "1816", "1853", "1880", "1890"], "1969", "fechas del siglo XIX"),
    ],
    
    "Química": [
        # Elementos vs compuesto
        (["H", "O", "C", "N", "Ca"], "H₂O", "elementos"),  # H₂O es compuesto
        
        # Gases vs sólido
        (["O₂", "N₂", "CO₂", "CH₄", "NH₃"], "Fe", "gases"),  # Fe es sólido
        
        # Metales vs no metal
        (["Fe", "Ca", "Na", "Mg", "Al"], "O", "metales"),  # O es no metal
        
        # Compuestos orgánicos vs inorgánico
        (["CH₄", "C₂H₆", "C₃H₈", "C₄H₁₀", "C₆H₆"], "NaCl", "compuestos orgánicos"),  # NaCl es inorgánico
        
        # Elementos de una letra vs dos letras
        (["H", "O", "C", "N", "F"], "Ca", "elementos de una letra"),  # Ca tiene dos letras
    ],
    
    "Geografía": [
        # Capitales sudamericanas vs europea
        (["Buenos Aires", "Brasilia", "Santiago", "Lima", "Bogotá"], "París", "capitales sudamericanas"),
        
        # Países sudamericanos vs europeo
        (["Argentina", "Brasil", "Chile", "Perú", "Colombia"], "Francia", "países sudamericanos"),
        
        # Ríos vs montaña
        (["Amazonas", "Nilo", "Misisipi", "Paraná", "Orinoco"], "Everest", "ríos"),
        
        # Continente americano vs otro continente
        (["Argentina", "Brasil", "Estados Unidos", "Canadá", "México"], "Francia", "países americanos"),
        
        # Océanos vs mar
        (["Atlántico", "Pacífico", "Índico", "Ártico", "Antártico"], "Mediterráneo", "océanos"),
    ]
}
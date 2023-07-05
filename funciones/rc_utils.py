import re
 
def check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    return True if re.fullmatch(regex, email) else False


def get_estadocurp(edo):
    
    switcher = {
        25:"AGUASCALIENTES",
        26:"BAJA CALIFORNIA",
        27:"BAJA CALIFORNIA SUR",
        28:"CAMPECHE",
        29:"COAHUILA",
        30:"COLIMA",
        31:"CHIAPAS",
        32:"CHIHUAHUA",
        33:"CIUDAD DE MEXICO",
        34:"DURANGO",
        35:"GUANAJUATO",
        36:"GUERRERO",
        37:"HIDALGO",
        38:"JALISCO",
        39:"MEXICO",
        40:"MICHOACAN",
        41:"MORELOS",
        42:"NAYARIT",
        43:"NUEVO LEON",
        44:"OAXACA",
        45:"PUEBLA",
        46:"QUERETARO",
        47:"QUINTANA ROO",
        48:"SAN LUIS POTOSI",
        49:"SINALOA",
        50:"SONORA",
        51:"TABASCO",
        52:"TAMAULIPAS",
        53:"TLAXCALA",
        54:"VERACRUZ",
        55:"YUCATAN",
        56:"ZACATECAS"
    }
    return switcher.get(int(edo), "Invalid month")
 

def get_estadoid(edo):
    
    switcher = {
        "AGUASCALIENTES":25,
        "BAJA CALIFORNIA":26,
        "BAJA CALIFORNIA SUR":27,
        "CAMPECHE":28,
        "COAHUILA":29,
        "COLIMA":30,
        "CHIAPAS":31,
        "CHIHUAHUA":32,
        "CIUDAD DE MEXICO":33,
        "DISTRITO FEDERAL":33,
        "DURANGO":34,
        "GUANAJUATO":35,
        "GUERRERO":36,
        "HIDALGO":37,
        "JALISCO":38,
        "MEXICO":39,
        "ESTADO DE MEXICO":39,
        "MICHOACAN":40,
        "MORELOS":41,
        "NAYARIT":42,
        "NUEVO LEON":43,
        "OAXACA":44,
        "PUEBLA":45,
        "QUERETARO":46,
        "QUINTANA ROO":47,
        "SAN LUIS POTOSI":48,
        "SINALOA":49,
        "SONORA":50,
        "TABASCO":51,
        "TAMAULIPAS":52,
        "TLAXCALA":53,
        "VERACRUZ":54,
        "VERACRUZ IGNACIO DE LA LLAVE":54,
        "YUCATAN":55,
        "ZACATECAS":56
    }
    return switcher.get(str(edo), "134")
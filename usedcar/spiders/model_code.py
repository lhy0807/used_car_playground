def model_code(code):
    year = 0
    make = 'a'
    model = 'a'

    if code == 'c22000':
        year = 2010
        make = 'BMW'
        model = '3 Series'

    elif code == 'c24539':
        year = 2015
        make = 'BMW'
        model = '3 Series'
    
    elif code == 'c28991':
        year = 2020
        make = 'BMW'
        model = '3 Series'

    elif code == 'c24654':
        year = 2015
        make = 'Toyota'
        model = 'Camry'
    
    elif code == 'c24466':
        year = 2015
        make = 'VW'
        model = 'Jetta'
    
    elif code == 'c24582':
        year = 2015
        make = 'MB'
        model = 'E-Class'
    
    elif code == 'c24684':
        year = 2015
        make = 'Honda'
        model = 'CRV'
    
    elif code == 'c24348':
        year = 2015
        make = 'Subaru'
        model = 'Forester'
    
    
    return [year, make, model]
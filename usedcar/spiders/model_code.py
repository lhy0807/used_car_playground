def model_code(code):
    year = 0
    make = 'a'
    model = 'a'

    if code == 'c22000':
        year = 2010
        make = 'BMW'
        model = '3 Series'

    if code == 'c24539':
        year = 2015
        make = 'BMW'
        model = '3 Series'
    
    if code == 'c28991':
        year = 2020
        make = 'BMW'
        model = '3 Series'
    
    return [year, make, model]
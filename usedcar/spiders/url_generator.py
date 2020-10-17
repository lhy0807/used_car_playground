import geopandas as gpd

def generator(model_codes):
    usa = gpd.read_file('../zipcodes.shp')
    urls = []
    #only focus in NY right now
    #for z in usa['ZIP_CODE']:
    for model in model_codes:
        for z in usa[usa['STATE'] == 'NY']['ZIP_CODE']:
            urls.append('https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?zip={}&showNegotiable=true&sortDir=ASC&sourceContext=carGurusHomePageModel&distance=10&entitySelectingHelper.selectedEntity2={}&sortType=DEAL_SCORE&entitySelectingHelper.selectedEntity={}'.format(z, model, model))
    print("All URLs Generated!")
    return urls
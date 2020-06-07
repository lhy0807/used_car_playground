import geopandas as gpd

def generator():
    usa = gpd.read_file('../zipcodes.shp')
    urls = []
    #for z in usa['ZIP_CODE']:
    for z in usa[usa['STATE'] == 'NY']['ZIP_CODE']:
        urls.append('https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?zip={}&showNegotiable=true&sortDir=ASC&sourceContext=carGurusHomePageModel&distance=10&entitySelectingHelper.selectedEntity2=c24539&sortType=DEAL_SCORE&entitySelectingHelper.selectedEntity=c24539'.format(z))

    return urls
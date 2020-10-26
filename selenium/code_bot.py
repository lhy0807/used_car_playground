from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from atlas_db import atlas
import pymongo

class CodeBot():
    def __init__(self):
        self.driver = webdriver.Chrome("E:/chromedriver.exe")
        self.driver.get("https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?zip=10002&showNegotiable=true&sortDir=ASC&sourceContext=carGurusHomePageModel&distance=50&entitySelectingHelper.selectedEntity2=c25907&sortType=DEAL_SCORE&entitySelectingHelper.selectedEntity=c25907")
        #all makes
        self.make_options = []
        #all models, accessed by model_options[make]
        self.model_options = {}
        #all codes
        self.codes = {}

        self.client = pymongo.MongoClient(atlas)
        self.db = self.client["usedcar"]
    def get_makes(self):
        self.make_select = Select(self.driver.find_element_by_name("selectedMakeId"))
        for option in self.make_select.options:
            #skip All Makes
            if option.text == "All Makes":
                continue
            #end until Volvo (last popular make)
            elif option.text == "Volvo":
                self.make_options.append(option.text)
                break
            self.make_options.append(option.text)

    def get_models(self):
        for make in self.make_options:
            self.model_options[make] = []
            self.make_select.select_by_visible_text(make)
            self.model_select = Select(self.driver.find_element_by_name("selectedModelId"))
            for model in self.model_select.options:
                #skip All Models
                if model.text == "All Models":
                    continue
                #only read popular models
                if len(self.model_options[make]) > 0 and model.text[0] < self.model_options[make][-1][0]:
                    break
                self.model_options[make].append(model.text)

    def get_code(self):
        self.year_select = Select(self.driver.find_element_by_name("selectedStartYear"))
        for make in self.make_options:
            self.codes[make] = {}
            self.make_select.select_by_visible_text(make)
            for model in self.model_options[make]:
                self.model_select.select_by_visible_text(model)
                self.codes[make][model] = {}
                for code in self.year_select.options:
                    if code.text == "All Years":
                        continue
                    #we don't want cars older than 2000
                    if int(code.text) < 2000:
                        break
                    self.codes[make][model][code.text] = code.get_attribute("value")

    def upload_db(self):
        for make in self.codes.keys():
            for model in self.codes[make].keys():
                for year in self.codes[make][model].keys():
                    code = self.codes[make][model][year]
                    self.db.modelcode.insert({"year":year, "make":make, "model":model, "code":code})


if  __name__ == "__main__":
    bot = CodeBot()
    bot.get_makes()
    bot.get_models()
    bot.get_code()
    bot.upload_db()
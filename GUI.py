
## Reading the Dataset


import pandas as pd
import numpy as np

from stats_can import StatsCan #Import StatsCan library 
sc = StatsCan()
crop_yield = sc.table_to_df("32-10-0359-01") #Convert crop yield data table into pandas dataframe

crop_yield.columns = [c.replace(' ', '_') for c in crop_yield.columns] #Improve header readability

#Drop unnecessary columns from crop yield table
crop_yield = crop_yield.drop(columns=["DGUID"]) 
crop_yield = crop_yield.drop(crop_yield.loc[:,"UOM_ID":"COORDINATE"].columns, axis = 1)
crop_yield = crop_yield.drop(crop_yield.loc[:,"STATUS":"DECIMALS"].columns, axis = 1)
crop_yield = crop_yield.dropna() #Not sure on this one?

#Reset index based on new number of rows
crop_yield.reset_index(inplace=True)
crop_yield = crop_yield.drop("index", 1)

def redo_columns(df): #Find averages for provinces that have more than one weather station; amalgamate these averages into new columns named for provinces and discard remaining columns
  df['Alberta'] = df[['CALGARY', 'EDMONTON']].mean(axis=1)
  df['Quebec'] = df[['MONTREAL', 'QUEBEC']].mean(axis=1) #Means of multiple weather stations
  df['Ontario'] = df[['OTTAWA', 'TORONTO']].mean(axis=1)
  new_columns = {'MONCTON': 'New Brunswick',
        'SASKATOON': 'Saskatchewan',
        'STJOHNS': 'Newfoundland and Labrador',
        'VANCOUVER': 'British Columbia',
        'WINNIPEG': 'Manitoba',
        'HALIFAX': 'Nova Scotia',
        'CHARLOTTETOWN': 'Prince Edward Island'} #Dict to replace weather station names with provinces

  df.rename(columns=new_columns,
          inplace=True)

  df.drop(['CALGARY','EDMONTON','MONTREAL','OTTAWA','QUEBEC','TORONTO','WHITEHORSE'], axis = 1,inplace=True) #Remove columns that provided means 
  return df

#Provincial precipitation

#Read in broad temperature data (all and PEI)

temp = pd.read_csv('https://raw.githubusercontent.com/BenKelly-Data/Canadian-Agricutural-Yields-vs-Climate/main/temperature_data.csv')
pei_temp_2012 = pd.read_csv('https://raw.githubusercontent.com/BenKelly-Data/Canadian-Agricutural-Yields-vs-Climate/main/en_climate_monthly_PE_8300300_1943-2012_P1M.csv')
pei_Yearly_temp = pei_temp_2012.groupby(["Year"]).mean() #Mean data by year
pei_temp_data_2013 = pd.read_csv('https://raw.githubusercontent.com/BenKelly-Data/Canadian-Agricutural-Yields-vs-Climate/main/pei_2013.csv')
pei_temp_data_2013.set_index('YEAR', inplace = True)

#Select only temp data from PEI daata
pei_temp_data_2013 = pei_temp_data_2013[['Mean Temp (°C)']]
pei_Yearly_temp = pei_Yearly_temp[['Mean Temp (°C)']]
pei_temp = pei_Yearly_temp.append(pei_temp_data_2013) #Append 2013-2019 data to 90's-2012 data
#Match indexes between 
pei_temp['YEAR'] = pei_temp.index
temp.set_index('YEAR')

#Join PEI data to the rest of the provinces
temp = temp.join(pei_temp.set_index('YEAR'),on = 'YEAR',how = 'left')

#Match formating between columns and with precipitation data
temp.rename(columns = {'Mean Temp (°C)':'MEAN_TEMPERATURE_CHARLOTTETOWN'}, inplace = True)
temp.columns = [t.replace('MEAN_TEMPERATURE_', '') for t in temp.columns]

temp = redo_columns(temp)

#GitHub Precip Data
precip = pd.read_csv('https://raw.githubusercontent.com/BenKelly-Data/Canadian-Agricutural-Yields-vs-Climate/main/precipitation_data_updated.csv')
precip.rename(columns = {'Total Precip (mm)':'TOTAL_PRECIPITATION_CHARLOTTETOWN'}, inplace = True)
precip.columns = [p.replace('TOTAL_PRECIPITATION_', '') for p in precip.columns]

precip= redo_columns(precip)
precip['YEAR'] = temp['YEAR'] #Re-add year data

precip.drop(precip.tail(1).index,inplace = True) #Remove extra error row
precip['YEAR'] = precip['YEAR'].astype(int)

"""## Data Cleaning"""

#FOCUSSING ON PROVINCIAL DATA
provs = ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick', 
         'Newfoundland and Labrador', 'Nova Scotia', 'Ontario', 
         'Quebec', 'Saskatchewan','Prince Edward Island']

prov_ag = crop_yield[crop_yield['GEO'].isin(provs)] #Subset crop data to just provincial data (not national or regional)

prov_ag[["REF_DATE"]] = prov_ag[["REF_DATE"]].astype(str) #Change year to be a string

prov_ag=prov_ag.rename(columns = {'REF_DATE':'YEAR'})

prov_ag = prov_ag.replace({'-01-01': ''}, regex=True)
prov_ag[["YEAR"]] = prov_ag[["YEAR"]].astype(int)
prov_ag = prov_ag[prov_ag.YEAR >= 1940]
prov_ag = prov_ag[prov_ag.YEAR <= 2019]
prov_ag = prov_ag.reset_index()

#Might be able to make one function with temp/precip as an argument, but seems to get complicated within the apply
def inTemp(row):
  t = prov_ag.iloc[[row.name]] #Get row index of current row
  y = t['YEAR'] #Find the year associated with the row
  y = int(y) #Ensure it's an integer

  p = t['GEO'].astype("string").to_string() #Get province as string (redundancy needed)
  head, sep, p = p.partition('  ') #Clean extra space created by making the string
  p = p.lstrip() #Keep removing extra spaces
  test = temp.loc[temp['YEAR'] == y] #Get the temperatures for the given year
  v = test[p] #Select the temp for the given province within selected year
  return float(v) #Return temp

#Similar commenting as above, just adapted to precipitation data
def inPrecip(row):
  t = prov_ag.iloc[[row.name]]
  y = t['YEAR']
  y = int(y)

  p = t['GEO'].astype("string").to_string()
  head, sep, p = p.partition('  ')
  p = p.lstrip()
  test = precip.loc[precip['YEAR'] == y]
  v = test[p]
  return float(v)

print('')
print('Data formatting takes 6-10 minutes, thanks for waiting!')
print('')

#TAKES 3 MIN
#Add temperature column to crop yield data
prov_ag["TEMP"] = ''
prov_ag["TEMP"] = prov_ag.apply(inTemp, axis=1)

print('Temperature data is in, now for precipitation!')
print('')

#Add precipitation column to crop yield data
prov_ag["PRECIP"] = ''
prov_ag["PRECIP"] = prov_ag.apply(inPrecip, axis=1)

print('Data ready! Look for a GUI!')
print('')
"""

```
# This is formatted as code
```

## GUI Creation & MatPlotLib Integration"""

from tkinter import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter.messagebox

#crop_yield = pd.read_csv("dat.csv") # theoretically won't need this part once StatsCan gets back up and running
crop_yield = prov_ag

# Generates the values for the drop down menus and sorts the lists for easier readability
province_list = sorted(crop_yield["GEO"].unique())
crop_list = sorted(crop_yield["Type_of_crop"].unique())
prov_ag = crop_yield

# Error message generation for bad values (mostly in Newfoundland set)
def expected_vector():
  tkinter.messagebox.showerror("TypeError", "Expected non-empty vector for x: \nData has no value for province and crop selected")


class Graph:
  def __init__(self, Prov, CropTp, TempORPrecip):
    self.Prov = Prov
    self.CropTp = CropTp
    self.TempORPrecip = TempORPrecip
    self.__setData__()
    self.__display__()

  def __setData__(self):
    self.X = (prov_ag[(prov_ag.GEO == self.Prov) & 
                   (prov_ag.Type_of_crop == self.CropTp)
                 & (prov_ag.Harvest_disposition == 
                    'Average yield (kilograms per hectare)')
                ].dropna()["YEAR"]).values 
    self.production = (prov_ag[(prov_ag.GEO == self.Prov) & 
                   (prov_ag.Type_of_crop == self.CropTp)
                 & (prov_ag.Harvest_disposition == 
                    'Average yield (kilograms per hectare)')
                ].dropna()["VALUE"]).values           
    if self.TempORPrecip == 'TEMP':
      self.key = 'TEMP'
    else:
      self.key = 'PRECIP'      
    self.independentVAR = (prov_ag[(prov_ag.GEO == self.Prov) & 
                   (prov_ag.Type_of_crop == self.CropTp)
                 & (prov_ag.Harvest_disposition == 
                    'Average yield (kilograms per hectare)')
                ].dropna()[self.key]).values

  def __display__(self):
    
    self.max_temp =  max((prov_ag["TEMP"].dropna()).values)
    self.min_temp =  min((prov_ag["TEMP"].dropna()).values)
    self.max_precip =  max((prov_ag["PRECIP"].dropna()).values)
    self.max_yield = max((prov_ag[(prov_ag.Type_of_crop == self.CropTp) & 
                        (prov_ag.Harvest_disposition == 
                         'Average yield (kilograms per hectare)')]["VALUE"]
                .dropna()).values)

    try:
      fig, ax1 = plt.subplots()

      ax2 = ax1.twinx()
      ax1.plot(self.X, self.production, 'o', color = 'lightcoral', 
              label = 'Average Yield')
      ax1.set_ylim(0,1000 + self.max_yield) 
      ax1.set_xlabel('Year')
      ax1.set_ylabel('kilograms per hectare')  
      
      if self.key == 'TEMP':
        ax2.plot(self.X, self.independentVAR, 'o', color = 'peachpuff', 
              label = 'Temperature')
        ax2.set_ylim(self.min_temp-2, self.max_temp+2)
        ax2.set_ylabel('Celsius')
      else:
        ax2.plot(self.X, self.independentVAR, 'o', color = 'lightblue', 
              label = 'Precipitation') 
        ax2.set_ylim(0, self.max_precip+2)      
        ax2.set_ylabel('100mm') 

      fig.legend(loc='upper left', bbox_to_anchor=(0.12, 0.9))

      m, b = np.polyfit(self.X, self.production, 1)
      m1, b1 = np.polyfit(self.X, self.independentVAR, 1)

      ax1.plot(self.X, m*self.X+b, color='lightcoral')
      if self.key == "TEMP":
        ax2.plot(self.X, m1*self.X+b1, color='peachpuff')
      else:
        ax2.plot(self.X, m1*self.X+b1, color='lightblue')

      if self.key == "TEMP":
          climate1 = "Temperature"
      else:
          climate1 = "Precipitation"

      plt.title("Relationship between {} and Crop Yield ({}) \nin {} from 1940 to Present".format(climate1, self.CropTp, self.Prov))

      plt.show()
    except TypeError:
      expected_vector()

# Class for the main GUI - presents the user with options to select province, crop type, and climate type to 
# generate a plot, as well as to exit the application 
class MainGUI:
    def __display__(self):
        Graph()
    
    def __init__(self, master):
        self.master = master
        Frame1 = Frame(self.master)
        Frame1.grid()

        # Brief set of instructions
        self.prompt = Message(master, text="Choose a province, a type of crop, and one of temperature or precipitation to see the relationship.", fg = "white", bg = def_back, width = 400, justify="center")
        self.prompt.configure(font=("arial", 9, "bold"), borderwidth = 1, relief = GROOVE)
        self.prompt.grid(row = 1, column = 1, pady = 15, padx = 5, columnspan=2)

        # Creates dropdown menu for provinces
        self.Province = StringVar()
        self.Province.set("Alberta")
        self.ProvinceSelect = OptionMenu(master, self.Province, *province_list, command = lambda _: self.getProvince())
        self.ProvinceSelect.grid(row = 2, column = 2, pady = 5, padx = 5)
        self.ProvinceSelect["highlightthickness"]=0
        self.ProvinceSelect.config(bg = "Slategray3")
        self.ProvLabel = Label(master, text = "Select a province:", fg = "white", bg = def_back,)
        self.ProvLabel.grid(row = 2, column = 1, padx = 5)

        # Creates drop down menu for crop types
        self.CropType = StringVar()
        self.CropType.set("Barley")
        self.CropSelect = OptionMenu(master, self.CropType, *crop_list, command = lambda _: self.getCrop())
        self.CropSelect.grid(row = 3, column = 2, pady = 5, padx = 5)
        self.CropSelect["highlightthickness"]=0
        self.CropSelect.config(bg = "Slategray3")
        self.CropLabel = Label(master, text = "Select a crop:", fg = "white", bg = def_back,)
        self.CropLabel.grid(row = 3, column = 1, padx = 5)

        # Creates drop down menu for climate type
        self.ClimateType = StringVar()
        self.ClimateType.set("TEMP")
        self.ClimateSelect = OptionMenu(master, self.ClimateType, "TEMP", "PRECIP", command = lambda _: self.getClimate())
        self.ClimateSelect.grid(row = 4, column = 2, pady = 5, padx = 5)
        self.ClimateSelect.config(bg = "Slategray3")
        self.ClimateSelect["highlightthickness"]=0
        self.ClimateLabel = Label(master, text = "Temperature or Precipitation:", fg = "white", bg = def_back,)
        self.ClimateLabel.grid(row = 4, column = 1, padx = 5)

        self.interact()

    def interact(self):
        
        #First butto calls the Graph class functions and plots the data based on user input from the drop down menus
        self.button_1 = Button(self.master , text="Plot", command= lambda : Graph(self.Province.get(), self.CropType.get(), self.ClimateType.get()), bg="papayawhip")
        self.button_1.grid(row = 5, column = 2, pady = 10, padx = 5)  ##plot

        # Button that calls the _quit function to exit the program
        self.button_2 = Button(self.master , text="Quit", command=self._quit, bg="salmon")
        self.button_2.grid(row = 6, column = 2, pady = 10, padx = 5)

    # Destroys the mainloop instance    
    def _quit(self):
        window.quit()
        window.destroy()

    # The 3 functions below store the option selected via the drop down menus as a value to be worked with
    # If no option is selected, the default values of "Alberta", "Barley", and "TEMP" will be used
    def getProvince(self):
        global Province
        ProvinceGet = self.Province.get()

    def getCrop(self):
        global CropGet
        CropGet = self.CropType.get()

    def getClimate(self):
        global ClimateGet
        ClimateGet = self.ClimateType.get()

# calls the GUI and creates an instance
if __name__ == '__main__':

    window = Tk()
    window.title("Canadian Crop Yield Analysis")
    window.configure(bg = "SkyBlue4")

    def_back = "SkyBlue4"

    app1_inst = MainGUI(window)

    window.mainloop()

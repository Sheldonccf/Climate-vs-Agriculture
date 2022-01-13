# Climate-Change-and-Canada-Agricultural-Production-Analysis
Collaborators: Sheldon Chen, Lo Humeniuk, Benjamin Kelly, Will Power-Jenkins
19 December 2021

# Introduction
This program allows a user to visualize the historic environmental data spanning from 1940 up to 2019, 
and to observe whether there is a relationship between yearly crop yields and
precipitation and mean annual climate, gathered by province. Within the graphic user interface, a user has the option to select a province, type of crop, and temperature of
precipitation data to view a histogram showing the relationships within this data.

# Sources
Dataset A: 
Government of Canada. (2021). Historical data. 
Website (Statistics Canada): https://climate.weather.gc.ca/historical_data/search_historic_data_e.html

**We use Statistics Canada's Python API to download the crop yield data automatically from this source.**

Dataset B: 
Turner, A. (2019). 80 years of Canadian climate data. Kaggle. 
Link: https://www.kaggle.com/aturner374/eighty-years-of-canadian-climate-data

**This Dataset is included in the repository.**

# Library Installation Pre-requisites
*   numpy (np)
*   pandas (pd)
*   StatsCan (Statistics Canada Downloader)
*   tkinter (tk)
*   matplotlib.pyplot (plt)
*   sklearn
*   statsmodels (sm)
*   statsmodels.formula (smf)

# How to Execute the Program
<br />
**Please be advised that each file might take a maximum 6-10 min to run before the next round of code optimization**
<br />

## Installing the Pre-required Packages
Use pip install to install the above-mentioned packages. If pip install does not work on your system,
use conda install - c conda-forge stats_can. 

## Initialize the GUI Visualiation of Regressions Analysis
To execute, run the GUI.py file. The program may encounter a long runtime of up to 10 minutes due to 
data cleaning. While installation, downloads and data cleaning is completed the following figure should appear
in a pop-up window. The GUI we developed a main menu with three drop-down options for the user: 
type of crop, province, and either temperature or precipitation. **By selecting from the drop-down menu,
A user could view the change in average crop yield and temperature or precipitation in a Canadian province in
the past 80 years.**
<br />
<br />
<img src=https://user-images.githubusercontent.com/89536920/148701060-f6d913ad-8bc3-46f8-b486-bd99a312bb79.png width="400" height="350">
<br />Figure 1: Main menu showing instructions and buttons for province, crop, temperature/precipitation, plot, and quit.
<br />
<br />
**If a user selects a ‘bad value’ (i.e., attempts to view data that is not available), 
they will receive an error message explaining why the graph cannot be plotted.**
<br />
<br />
<img src=https://user-images.githubusercontent.com/89536920/148701122-ffd5a23e-f305-448d-9eee-01464b764523.png width="400" height="180">
<br />Figure 2: Error message noting: “Expected non-empty vector for x: Data has no value for province and crop selected.
<br />
<br />
**If a user selects an available set of data, the following window will pop out ploting the change of average crop
yield and temperature or precipitation change.**
<br />
<br />
<img src=https://user-images.githubusercontent.com/89536920/148701149-01b86ed1-6459-47db-a6c7-df508e67eb71.png width="400" height="350">
<br />Figure 3: Example graph showing data when Ontario (province), Barley (crop type) and Temperature are selected.
<br />
<br />
## See the Conclusion of Regression Analysis

To execute, run the Regression_Analysis.py file. The file should display the following image, outlining whether a linear correlation
exists between crop yield data and climate change
<br />
<br />
<img src=https://user-images.githubusercontent.com/89536920/148704230-4f7509d6-6848-4ffd-9a25-99bae0cf9dc7.png width="400" height="150">
<br />Figure 4: Example chart showing only the types of crop yield linearly correlated to temperature or precipitation change

## See the Tableau Visualization of Regression Analysis
<br />
<img src=https://user-images.githubusercontent.com/89536920/149256530-5fc82053-4ccc-45ad-a3a0-5e2bb67093be.JPG width="800" height="350">
Figure 5: Scatter plot of crop yields of different species vs temperature change in Canadian provinces in the past 80 years.
<br />
<br />
Link:
<br />
https://public.tableau.com/views/Canadian_Crop_Yield_Climate_Change_Analysis/TemperatureVScrop_yield?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link

## See the Tableau Visualization of Canadian Crop Yield Data
<br />
<img src=https://user-images.githubusercontent.com/89536920/149250209-7a419cb8-c844-4902-81cd-ff7317198100.png width="800" height="400">
Figure 6: Display of mapped data for metric tonnes of all crop types in 1997.
<br />
<br />
Link:
<br />
https://public.tableau.com/shared/DMJBHZYXR?:display_count=n&:origin=viz_share_link 

## Predicting Crop Yield with a Trained a Linear Regression Model （Not Live on GitHub yet)
<br />
Please run the “Prediction.py" to train the linear model and enter valid values of temperature or precipition to predict a corresponding crop yield for a agricultural species.
<br />
<br />
Please note that since through F-test fit of linear regression models, we concluded that linear correlations only exists for the following data entries, the linear model is only
trained for predicting crop yields associated with this dataframe(concluded from the previous section "Conlusion of Regression Analysis"):<br />
<br />
<img src=https://user-images.githubusercontent.com/89536920/148704230-4f7509d6-6848-4ffd-9a25-99bae0cf9dc7.png width="400" height="150">
<br />Figure 7: Example chart showing only the types of crop yield linearly correlated to temperature or precipitation change


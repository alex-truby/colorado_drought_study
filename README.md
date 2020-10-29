# A Study of Drought Trends in Colorado and Impact on Colorado Water Wells, 2000 - 2016
### *Galvanize DSI Capstone 1*
### *Alex Truby*

-------------

## Background and Motivating Questions 
The news cycle in the year of 2020 has been quite the wild ride. Living in Colorado, *just a few* of the topics of note have been drought and wildfire, seeing as many residents here have been personally effected by both. As a Colorado resident, both of these events are particularly concerning. As a water engineer however, I am more intrigued about any trends we might be realzing in drought over the years, and what impact it might have on Colorado water resources. As such, the goal of this capstone project is to explore the following questions:

* **Has drought severity increased in Colorado between the years of 2000 and 2016?**
* **Have groundwater well depth levels changed between the years of 2000 and 2016?**
* **Are there any signifanct differences between the drought indicators chosen for this study?**
* **What relationship, if any, is there between drought severity and water level depths in ground water wells in Colorado over the last twnety years?**


The search for drought a drought data set quickly led to the realization that there are, in fact, a few different indicators out there to measure drought. The three indices utilized in this study are as follows:
*  **Palmer Drought Severity Index (PDSI) -** Maintained by the National Center for Atmospheric Research (NCAR)  and the University Coporation for Atmospheric Research (UCAR) in Boulder and the University of Albany, the PDSI captures drought with a model  utilizing both termperature data and a physical water balance model. More information can be found [here](https://climatedataguide.ucar.edu/climate-data/palmer-drought-severity-index-pdsi).

<center>

| Drought Severity | PDSI Range     |
| ---------------- | -------------- |
| Extemely Drought | -4.0 or less   |
| Severe Drought   | -3.0 to -3.9   |
| Moderate Drought | -2.0 tp -2.9   |
| Near Normal      | -1.9 to 1.9    |
| Unusually Moist  | 2.0 to 2.9     |
| Very Moist       | 3.0 to 3.9     |
| Extremely Moist  | 4.0 and above  |
</center>





* **Standardized Precipitation Evapotranspiration Index (SPEI) -** The SPEI is an extension of the precipitaion index utilized in the PDSI model, but also includes potential surface water evapotranspiration. Because of this, the SPEI should also account for the impact on water demand from increased temperature. More information can be found [here](https://climatedataguide.ucar.edu/climate-data/standardized-precipitation-evapotranspiration-index-spei).
*  **United States Drought Monitor (UDSM) -** The USDM is published and mainted by the National Drought Mitigation Center at the University of Nebraska-Lincoln. The UDSM utilizes the PDSI as one of the inputs for the model, along with soil moisture, weekly streamflow measurements from the USGS, and Objective Drought Indicators from the Univserity. More information on this index can be found [here](https://droughtmonitor.unl.edu/About/AbouttheData/DroughtClassification.aspx).

Rather than blindly choosing one of the above indicators as the basis of this study,  all three were evaluated, and the reuslts from each compared. 

-----

## The Data

The below tabe gives a summary of the raw data sets that were pulled in for analysis.

|        |Source          | Initial Shape | Relevant Columns                 | Info/Comments        |Link to Data                                                                                                     |
| ------| --------------- | ------------- | -------------------------------- | -------------------- | --------------------------------------------------------------------------------------------------------------- |
|CO Water Well Level Depths| Colorado Data Catalog (DWR)| 22,486 x 47 | Measurement Date, County, Water Level Depth | Contains records for every registered water well in CO dating back to 1883 | [Link](https://data.colorado.gov/Water/DWR-Well-Water-Level/hfwh-wsgi) |
| PDSI | CDC Data Catalog | 4,551,576 x 5 | year, month, countyfips, pdsi    | See description above | [Link](https://data.cdc.gov/Environmental-Health-Toxicology/Palmer-Drought-Severity-Index-1895-2016/en5r-5ds4) | 
| SPEI | CDC Data Catalog | 4,551,576 x 5 | year, month, countyfips, pdsi    | See description above | [Link](https://data.cdc.gov/Environmental-Health-Toxicology/Palmer-Drought-Severity-Index-1895-2016/en5r-5ds4) |
|USDM  | CDC Data Catalog | 2,786,067 x 6 | Year, month, county, fips, value | See description above | [Link](https://data.cdc.gov/Environmental-Health-Toxicology/United-States-Drought-Monitor-2000-2016/spsk-9jj6) | 


As can be inferred by the table above, not all of the columns included in the data sets are relevant to the end goal of this study. The time period 2000 - 2016 was chosen for the focus of this study because that time  period contained the most overlap between the datasets for analysis. The county indicators and date formats in particular, were variable of interest that varied across all four tables. A dictionary was made from the USDM file to map county name with the corresponding fips value so that each of the files could be tied together on that identifier. Additionally, the dates for each file have been modified to allow grouping so that the quantifiable variables of interest (PDSI, SPEI, UDSM, and Water Level Depth) could be grouped by county, by month for the time period of interest. While there weren't many nulls in the drought index datasets, the ground water well levels were measured at inconsistent increments. The null values from this dataset were dropped, rather than set to zero, so as to not skew the averages when rolled up to a monthly or yearly level.  After many rounds of data cleaning, the shape of the final primary set of data used for this study has a shape of 13056  × 8 and contains the columns: **County Fips, Year, Month, PDSI, SPEI, USDM Values, Water Level Depth, Date**. The rows contain outline data for each county in Colorado (total of 64), averaged over each month from 2000 - 2016. The final data contains values that will help capture drought severity, drought length, and water well depths over this time period. 
  

## Exploratory Data Analysis
### **_Round 1_**
The first dive into the data set involved comparing a snapshot of each variable for the years 2000 and 2016. The null hypothesese assume that there is no differnece in drought severity between these two years (across all indices), as well as no difference in water well levels. 

Before running the hypothesis tests, histograms of the mean drought indices and water well levels were created in order to gain insight as to how the means of each variable may have shifted over this time frame. The values captured here represent the mean values across across all Colorado counties to get a better feel for the condition of the state as a whole.


![Histograms](./images/variable_histograms.png)


As illustrated in the charts above, there seems to be at least some shift across the board between 2000 and 2016.  It cannot be determined however, whether or not this is enough of a shift to be statistically meaningful without first running a hypothesis test...

As stated previously, the null hypthesis for each variable is that there is not a significant change between 2000 and 2016. A frequentist approach was used to run this test, assuming a significance threshold of 0.05. A t-test was then performed to obtain the p-value for each of the four hypothesis, with the following results:

|Variable       | p-value |
| ------------- | ------- |
|USDM           |  0.901  |
| PDSI          | 0.001   |
|SPEI           |  0.920  |
|Water Levels   | 0.095   |

The above results indicate that only in regards to the PDSI is there a signifance difference between the years 2000 and 2016, based on the significance level of 0.05. Unsurprisingly, these are also the two variables with the mort noticable shift in mean values illustrated in the histograms above.


### **_Round 2_**
The next step was to determine whether or not the difference in the variables between these two years was part of a larger trend, or if it was a one off occurance. And on the same note, even though the snapshot comparison may not have indicated a significant difference for the USDM and SPEI indicators over the years, might a continuous trend lead to a different conlusion?

To get a better understanding of the trends over the entire time period from 2000 - 2016, the following plots illustrate the mean values across across all Colorado counties for each month in this timeframe for each variable. Looking at the data in this continuous manner helps to paint a more clear pictures around what exactly was happending over this time frame. Again, the values captured here represent the mean values across across all Colorado counties for each month in this timeframe.

![Continuous Trends](./images/continuous_trends\.png)

While a direct comparison can't be made to the histograms providing only a snapshot presented previously, it seems as as though both PDSI and water level depths illustrate an overall change in slope over the entire time period. Let's dig deeper with another hypothesis test...

This time, rather than a standard t-test on two data sets, a linear regression ordinary least squares approach was used to find both the confidence interval for the slope over the alotted timeframe, as well as the p-value. Again, the null hypothesis here is that there is not a meaningful trend for any of the variables over the years 2000 - 2016. If the confidence interval contains zero, there is not enough evidence to state that the variable trends in a certain direction over this time period. The table below captures these results.

|Variable      | Confidence Interval   | p-value |
| ------------ | --------------------- | ------- |
| UDSM         | -0.005 to 0.001       | 0.234   |
| PDSI         | 0.010 to  0.019       | <0.01   |
| SPEI         | -0.001 to 0.003       | 0.196   |
| Water Levels | 0.619 to 2.062        | <0.01   |

The results above substantiate the previous conclusion that the PDSI has significantly changed over this time period, with a p-value of near zero and both the lower and upper end of the confidence interval containing positive slopes. Additionally, using the linear regression methodoly on the slope rather than simply comparing two snapshots in time indicates that there is also a significant change in water well levels over this time period. More weight will be put on the results of this methodology because it uses data over the entire time period, rather than just the start and end years. Therefor we can conclude the following: 1) Both the PDSI and water well levels *have* significantly changed from 2000 - 2016, and 2) There *is not* enough evidence to conlude that the UDSM and SPEI have significantly changed over these years.

I was a bit surprised at how *different* the results for the three drought indicators were, considering they should theoretically all be measuring the same thing. With the results of this linear regression, someone could hypothetically pick and choose which drought indicator to use as their null hyptohesis, and then point to statistics to "prove" their hypothesis, even though someone with an opposing hypothesis could also do the same thing... interesting.

## Round 3
After answering the questions around how each variable has changed over the specified time period, the next step was to determine if there are any meaningful relationships between them. I was particularly curious if there was any correlation between the PDSI and water level depths, since both of those have illustrated meaningful changes from 2000 - 2016.


#I was a little surprised at how different the results were for three drought indices, considering they should all three be theoretically measuring the same thing. 

![Correlation Matrix](./images/var_correlation_small.png) ![P-Val Matrix](./images/pval_matrix.png)


#plots to highlight

#make a chart of the palues for the correlation matrix - shading
#put in chart for three drought indices over time
#put in chart for water well change over time (remember to multiple * -1 to better illustrate decreasing water levels)



#hypothesis testing:

*null hypothesis 1: NO difference in drought indicators form 2000-2016 (run on all three)
*null hypothesis 2: NO difference in water level depths from 2000 - 2016



#no correlation between well water levels and drought
#would be intersting to extend the study to include other factors (population growth/decline, geology factors such as recharge time, etc. )

#after finding no correlation between these - wanted to focus on how drought and water level depths are trending over the state indiviually with time

## Citations
* Dai, Aiguo & National Center for Atmospheric Research Staff (Eds). Last modified 12 Dec 2019. "The Climate Data Guide: Palmer Drought Severity Index (PDSI)." Retrieved from https://climatedataguide.ucar.edu/climate-data/palmer-drought-severity-index-pdsi.
* Vicente-Serrano, Sergio M. & National Center for Atmospheric Research Staff (Eds). Last modified 18 Jul 2015. "The Climate Data Guide: Standardized Precipitation Evapotranspiration Index (SPEI)." Retrieved from https://climatedataguide.ucar.edu/climate-data/standardized-precipitation-evapotranspiration-index-spei.
* National Drought Mitigation Center. Last Modified 2020. "Drought Clasification". Retreived from https://droughtmonitor.unl.edu/About/AbouttheData/DroughtClassification.aspx.
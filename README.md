# MA705 Final Project

This repository contains files used in the MA705 dashboard project.

Use Markdown to write your readme.md file.  Here is a [cheatsheet](https://www.markdownguide.org/cheat-sheet/).

The final dashboard is deployed on Heroku [here](https://ma705bostonuniversities.herokuapp.com).

## Dashboard Description

This dashboard displays the Medicare Spending Per Beneficiary (MSPB) in contiguous states in US, and also explore what some variables may have influence on the MSPB.
The user can observe how plots (one map plot and two scatter plots) and table results change through selecting 'Yes'/'No' or both on 'Obamacare Checklist', and setting the range of 'Unemployment Rate Slider' and 'Smoking Rate SLider'.


### Data Sources

I use two datasets to build this dashboard.

The first dataset 'medical.csv' is the one that I had last semester for the group project in ST625 class taught by Prof. Chervey, 
my teammates and I found the .csv file from the website https://www.kff.org/state-category/medicare/medicare-enrollment-by-eligibility-category/
through searching some categories we were interested in to export, and we collected and added more columns like 'Obamacare' to this 
file and calculated the (Average) Medicare Spending Per Beneficiary through using Medicare Spending divided by Medicare_Beneficiaries.

The second dataset 'states.shp' is the one we used in MA705 class, which has geometry information corresponding to each state in the US, 
so I can create a new geo data frame through merging above two datasets on the state column that both datasets owned but have different names.
To better show states in the format as map, I removed states that are not in the contiguous US and also convert 0/1 in Obamacare variable to 'Yes'/'No' to make users understand better, and edit the column name through removing underscore '_' to show the table more clear.


### Other Comments

Anything you'd like to add

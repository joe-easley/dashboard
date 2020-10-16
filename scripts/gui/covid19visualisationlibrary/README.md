# Covid Data Visualisation tool

This project will query the government covid dashboard, and generate graphs.

Current supported queries supported:

- Using --dataType you can specify the data you want to search for
    - Deaths can be searched using: "newDeaths28DaysByDeathDate", "cumDeaths28DaysByDeathDate",
                            "cumDeaths28DaysByDeathDateRate"
        - Cases can be searched from nation down to local tier local authority
        
    - Cases can be searched using: "newCasesBySpecimenDate", "cumCasesBySpecimenDateRate", "newPillarOneTestsByPublishDate",
                            "newPillarTwoTestsByPublishDate", "newPillarTwoTestsByPublishDate",
                            "newPillarFourTestsByPublishDate"
        - Deaths can be searched for at nation and regional levels
        
- Locations: ltla, utla, nation
- Durations: fortnight, month, allTime or you can specify a number of days as an integer eg "100"

Build your query as below on the command line:

`python Visualisations.py --dataType="newCasesBySpecimenDate" --areaType="ltla" --areaName="manchester" --duration="allTime"
`

This can also be run using the gui. Run the gui_visualise.py script in cmd. This is still a bit buggy

`python gui_visualise.py`
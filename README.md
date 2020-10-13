# Covid Data Visualisation tool

This project will query the government covid dashboard, and generate graphs.

Current supported queries supported:
- Cases by specimen date
- Locations: ltla, utla, nation
- Durations: fortnight, month, allTime or you can specify a number of days

Build your query as below on the command line:

`python Visualisations.py --areaType="ltla" --areaName="manchester" --duration="allTime"
`
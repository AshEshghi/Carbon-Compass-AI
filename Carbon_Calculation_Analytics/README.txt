This ZIP contains Ashley's UPDATED analytics files ONLY, not a duplicate of Sahra's Data_Management folder.

Copy the Carbon_Calculation_Analytics folder, docs/ANALYTICS_UML.md, docs/INTEGRATION_NOTES.md,
and run_analytics_demo.py into your SHARED Carbon_Compass_AI repository. Place the existing
Data_Management folder from Sahra alongside Carbon_Calculation_Analytics.

From the repository root:
  python run_analytics_demo.py
  python -m unittest discover -s Carbon_Calculation_Analytics -p "test_*.py" -v

Do not replace Sahra's source files and do not commit local database files.

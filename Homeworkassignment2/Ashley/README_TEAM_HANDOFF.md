# HA2 — Ashley's contribution and team handoff

## What Ashley implements

- `CarbonProcessor`: a small **local** abstract parent class in Ashley's folder. It is only used to make her work self-contained while still demonstrating inheritance and polymorphism.
- `ScopeFilter`: keeps events with selected GHG scopes and returns `None` for discarded events.
- `EmissionTransformer`: calculates emissions from validated, configured factors and outputs **metric tonnes CO2e**.
- `demo_ashley.py` and `test_ashley_ha2.py`: independent demonstration and 21 unit tests.

**No dependency on** `Homeworkassignment2/shared`, Nooshin's modules, Sahra's Python modules, SQL databases, Flask, Streamlit, or external packages.

## Shared record contract for team integration

All processing stages should support `process(record: Mapping) -> dict | None`.

- A valid event is a dictionary containing `scope` or `scope_tag`.
- Purchased-electricity records from Sahra contain `record_id`, `building_id`, `timestamp`, and `electricity_kwh`. Ashley's `electricity_events()` helper adds `scope=2` without changing the original.
- `ScopeFilter.process()` returns a dictionary or `None` when rejected.
- `EmissionTransformer.process()` returns a dictionary with `emissions_kg_co2e` and `emissions_tonnes_co2e`.
- Büşra's pipeline should call `.process(event)` rather than checking a specific parent class using `isinstance()`.

Nooshin can independently implement `StreamProcessor` and `InsightProcessor` in her own folder. To integrate, the team only needs to agree on the method name and event structure. The _final_ group UML should accurately show that Ashley's classes inherit `CarbonProcessor`, while Nooshin's classes may use their own ABC. If the professor expects one common inheritance hierarchy across all processors, unify the parent classes at the final integration stage after team discussion, but this is **not required to test Ashley's module on its own**.

## Run without any teammates' code

From the repository root:

```powershell
python Homeworkassignment2/Ashley/demo_ashley.py
python -m unittest discover -s Homeworkassignment2/Ashley -p "test_*.py" -v
```

Or open `demo_ashley.py` in VS Code and click _Run Python File_.

## Homework submission

Push this `Homeworkassignment2/Ashley` folder to the team's `HomeworkAssignment2` branch (assignment-specific branch name). Add the UML in the submission README and include the team's single video link as required by HA2. Do not overwrite another student's folder.

## Emissions-factor limitation

The included factor `0.4 kg CO2e/kWh` is **illustrative**, not an official factor. Any real-company use needs a sourced factor that matches country, year, method, scope, and reporting boundary.

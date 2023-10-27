# simgen

Little python script to generate random Euroscope scenario files.

# Installation
1. Install Python: https://www.python.org/downloads/

# Usage

- Right click inside the simgen-folder in Windows Explorer and "Open in Terminal".

## Frankfurt
- Execute eddf.py for Frankfurt with the following parameters: 
- Runway can either be 25 or 07, the rates for each waypoints are aircraft per hour
  ```py
  eddf.py [RUNWAY] [KERAX] [ROLIS] [EMPAX] [SPESA] [UNOKO]
  ```

## Stuttgart
- Execute edds.py for Stuttgart with the following parameters: 
- Runway can either be 25 or 07, the rates for each waypoints are aircraft per hour
  ```py
  eddf.py [RUNWAY] [BADSO] [TEKSI] [GARMO] [LUPEN] [LBU]
  ```

## Tango/CTR
- Execute eduu_tgo.py for Tango with the following parameters: 
- The rates for each waypoints are aircraft per hour
  ```py
  eddf.py [DEGES] [IBAGA] [PITES] [POGOL] [DITAM]
  ```

  DEGES: Zürich DEPs to Hamburg or Berlin via ETAGO > AMOSA or ETAGO > HAREM > LOHRE

  IBAGA: Zürich ARRs via DKB > TEDGO

  PITES: Innsbruck ARRs via KRH > BATUB

  POGOL (OBAKI): München ARRs from France via LUPEN > ROKIL

  DITAM (SUREP): Frankfurt ARRs via EMPAX

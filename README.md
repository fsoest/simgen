# simgen

Little python script to generate random Euroscope scenario files.

# Installation
1. Install Python: https://www.python.org/downloads/

# Usage

- Right-click inside the simgen-folder in Windows Explorer and select "Open in Terminal" (if the option doesn't show up, try holding down shift while right-clicking).

## Frankfurt
- Execute **eddf.py** for Frankfurt with the following parameters: 
    - Runway can either be 25 or 07, the rates for each waypoint are aircraft per hour
      
  ```py
  python eddf.py [RUNWAY] [KERAX] [ROLIS] [EMPAX] [SPESA] [RASVO]
  ```
- Press **Enter** to execute. The file will be written to **\<simgenFolder\>\output_eddf.txt**

## Stuttgart
- Execute **edds.py** for Stuttgart with the following parameters: 
    - Runway can either be 25 or 07, the rates for each waypoint are aircraft per hour
      
  ```py
  python edds.py [RUNWAY] [BADSO] [TEKSI] [GARMO] [LUPEN] [LBU]
  ```
- Press **Enter** to execute. The file will be written to **\<simgenFolder\>\output_edds.txt**

## TGO
- Execute **eduu_tgo.py** for TGO with the following parameters: 
    - The rates for each waypoint are aircraft per hour
      
  ```py
  python eduu_tgo.py [DEGES] [IBAGA] [PITES] [POGOL] [DITAM]
  ```
- *Routes:*
     
     - *DEGES:* Zürich DEPs to Hamburg via ETAGO > AMOSA or Berlin via ETAGO > HAREM > LOHRE
     - *IBAGA:* Zürich ARRs via DKB > TEDGO
     - *PITES:* Innsbruck ARRs via KRH > BATUB
     - *POGOL (OBAKI):* München ARRs from France via LUPEN > ROKIL
     - *DITAM (SUREP):* Frankfurt ARRs via EMPAX

- Press **Enter** to execute. The file will be written to **\<simgenFolder\>\output_eduu_tgo.txt**



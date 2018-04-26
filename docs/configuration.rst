Configuration
==============


DHIS2 metadata
--------------

All metadata in DHIS2 is required to be configured before running this application.

.. note:: The Organisation Unit hierarchy in DHIS2 should be aligned with the VA Questionnaire.
          This application assumes it is set up correctly (however it auto-assigns the Organisation Unit to the program if not already assigned).

In order to install metadata, import the the following metadata files with DHIS2's Import/Export app.
Always do a "Dry run" first.

1. Import ``metadata/optionset_age_category.csv``
2. Import ``metadata/optionset_cause_of_death.csv``
3. Import ``metadata/optionset_ICD10.csv``
4. Import ``metadata/optionset_sex.csv``
5. Import ``metadata/dataelements.csv``
6. Import ``metadata/program.json``
7. (Import ``metadata/dashboard.json`` - TODO)

Application
------------

All configuration is defined in ``config.ini``. Note that there are no apostrophes (``"`` or ``'``) in this file.

[auth]
^^^^^^

auth_file
	A file path to where authentication details for DHIS2 and ODK Aggregate are stored - see ``dish.json`` for structure of the file.
	Keep it on a secure place and refer to its file path.

[logging]
^^^^^^^^^^

logfile
	Where the application should log to, e.g. ``/var/log/smartvadhis2.log``

level
	Minimum Log level - e.g. ``INFO`` logs all info messages, warnings, errors.
	Must be one of: ``DEBUG``, ``INFO``, ``WARNINGS``

[database]
^^^^^^^^^^

db_queries_log
	Whether to log all local database queries as well. Either ``true`` or ``false``.

db_name
	Name of the local database file, e.g. ``smartva-dhis2.db``

[odk]
^^^^^^

form_id
	Verbal Autopsy ODK Form ID, e.g. ``SmartVA_Bangla_v7``

sid_regex
	Regular Expression that matches a to Verbal Autopsy Study ID number, e.g. ``^VA_[0-9]{17}$``.
	Check regex with online tools, e.g. `regex101.com <https://regex101.com>`_.

[smartva]
^^^^^^^^^

ignore_columns
	Which CSV columns in the SmartVA CSV output to ignore for further processing.
	Must be delimited by commas ``,`` and without space, e.g. ``geography1,geography2,geography4,geography5,cause34``

algorithm_version
	With which version the CoD was obtained, e.g. ``Tariff 2.0``.

country
    Data origin country abbreviation. See below for full list.
hiv
    Data is from an HIV region

malaria
    Data is from a Malaria region.
hce
    Use Health Care Experience (HCE) variables.


For more information about SmartVA options refer to the SmartVA Help:
`PDF <http://www.healthdata.org/sites/default/files/files/Tools/SmartVA_Help.pdf>`_.


[dhis]
^^^^^^
program
	The Unique Identifier (UID) of the Verbal Autopsy DHIS2 program.

program_stage
	The Unique Identifier (UID) of the Verbal Autopsy DHIS2 program *stage*.

api_version
    DHIS2 API Version (e.g. ``28``)

For further mapping details see also the ``smartva/core/mapping.py`` module.


Org Unit details
-----------------

In order to determine the location of the Verbal Autopsy, you need to define the following steps:

1. Find out where the orgUnit is located in your aggregate CSV
2. ignore certain columns in the smartva.ignore_columns section of ``config.ini`` (see above)
3. In ``smartvadhis2/core/mapping.py``, update the csv_name property in the Orgunit class.


Country list
--------------

See section [smartva] above.

Country list:
- Unknown
- Afghanistan (AFG)
- Albania (ALB)
- Algeria (DZA)
- Andorra (AND)
- Angola (AGO)
- Antigua and Barbuda (ATG)
- Argentina (ARG)
- Armenia (ARM)
- Australia (AUS)
- Austria (AUT)
- Azerbaijan (AZE)
- Bahrain (BHR)
- Bangladesh (BGD)
- Barbados (BRB)
- Belarus (BLR)
- Belgium (BEL)
- Belize (BLZ)
- Benin (BEN)
- Bhutan (BTN)
- Bolivia (BOL)
- Bosnia and Herzegovina (BIH)
- Botswana (BWA)
- Brazil (BRA)
- Brunei (BRN)
- Bulgaria (BGR)
- Burkina Faso (BFA)
- Burundi (BDI)
- Cambodia (KHM)
- Cameroon (CMR)
- Canada (CAN)
- Cape Verde (CPV)
- Central African Republic (CAF)
- Chad (TCD)
- Chile (CHL)
- China (CHN)
- Colombia (COL)
- Comoros (COM)
- Congo (COG)
- Costa Rica (CRI)
- Cote d'Ivoire (CIV)
- Croatia (HRV)
- Cuba (CUB)
- Cyprus (CYP)
- Czech Republic (CZE)
- Democratic Republic of the Congo (COD)
- Denmark (DNK)
- Djibouti (DJI)
- Dominica (DMA)
- Dominican Republic (DOM)
- Ecuador (ECU)
- Egypt (EGY)
- El Salvador (SLV)
- Equatorial Guinea (GNQ)
- Eritrea (ERI)
- Estonia (EST)
- Ethiopia (ETH)
- Federated States of Micronesia (FSM)
- Fiji (FJI)
- Finland (FIN)
- France (FRA)
- Gabon (GAB)
- Georgia (GEO)
- Germany (DEU)
- Ghana (GHA)
- Greece (GRC)
- Grenada (GRD)
- Guatemala (GTM)
- Guinea (GIN)
- Guinea-Bissau (GNB)
- Guyana (GUY)
- Haiti (HTI)
- Honduras (HND)
- Hungary (HUN)
- Iceland (ISL)
- India (IND)
- Indonesia (IDN)
- Iran (IRN)
- Iraq (IRQ)
- Ireland (IRL)
- Israel (ISR)
- Italy (ITA)
- Jamaica (JAM)
- Japan (JPN)
- Jordan (JOR)
- Kazakhstan (KAZ)
- Kenya (KEN)
- Kiribati (KIR)
- Kuwait (KWT)
- Kyrgyzstan (KGZ)
- Laos (LAO)
- Latvia (LVA)
- Lebanon (LBN)
- Lesotho (LSO)
- Liberia (LBR)
- Libya (LBY)
- Lithuania (LTU)
- Luxembourg (LUX)
- Macedonia (MKD)
- Madagascar (MDG)
- Malawi (MWI)
- Malaysia (MYS)
- Maldives (MDV)
- Mali (MLI)
- Malta (MLT)
- Marshall Islands (MHL)
- Mauritania (MRT)
- Mauritius (MUS)
- Mexico (MEX)
- Moldova (MDA)
- Mongolia (MNG)
- Montenegro (MNE)
- Morocco (MAR)
- Mozambique (MOZ)
- Myanmar (MMR)
- Namibia (NAM)
- Nepal (NPL)
- Netherlands (NLD)
- New Zealand (NZL)
- Nicaragua (NIC)
- Niger (NER)
- Nigeria (NGA)
- North Korea (PRK)
- Norway (NOR)
- Oman (OMN)
- Pakistan (PAK)
- Palestine (PSE)
- Panama (PAN)
- Papua New Guinea (PNG)
- Paraguay (PRY)
- Peru (PER)
- Philippines (PHL)
- Poland (POL)
- Portugal (PRT)
- Qatar (QAT)
- Romania (ROU)
- Russia (RUS)
- Rwanda (RWA)
- Saint Lucia (LCA)
- Saint Vincent and the Grenadines (VCT)
- Samoa (WSM)
- Sao Tome and Principe (STP)
- Saudi Arabia (SAU)
- Senegal (SEN)
- Serbia (SRB)
- Seychelles (SYC)
- Sierra Leone (SLE)
- Singapore (SGP)
- Slovakia (SVK)
- Slovenia (SVN)
- Solomon Islands (SLB)
- Somalia (SOM)
- South Africa (ZAF)
- South Korea (KOR)
- Spain (ESP)
- Sri Lanka (LKA)
- Sudan (SDN)
- Suriname (SUR)
- Swaziland (SWZ)
- Sweden (SWE)
- Switzerland (CHE)
- Syria (SYR)
- Taiwan (TWN)
- Tajikistan (TJK)
- Tanzania (TZA)
- Thailand (THA)
- The Bahamas (BHS)
- The Gambia (GMB)
- Timor-Leste (TLS)
- Togo (TGO)
- Tonga (TON)
- Trinidad and Tobago (TTO)
- Tunisia (TUN)
- Turkey (TUR)
- Turkmenistan (TKM)
- Uganda (UGA)
- Ukraine (UKR)
- United Arab Emirates (ARE)
- United Kingdom (GBR)
- United States (USA)
- Uruguay (URY)
- Uzbekistan (UZB)
- Vanuatu (VUT)
- Venezuela (VEN)
- Vietnam (VNM)
- Yemen (YEM)
- Zambia (ZMB)
- Zimbabwe (ZWE)

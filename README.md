## Ontology exploration 
This repository is a very basic and intial exploration of the DIGIT RUBBER ontology. The DIGIT RUBBER ontology imports external ontologies like BFO (Basic Formal Ontology), RO (Relation Ontology), CHEBI (Chemical Entities of Biological Interest), and IAO (Information Artifact Ontology).


### Prerequisites

create a virtual environment and install the libraries required by running: 
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Ontology inspection workflow

This script is a very basic workflow to load the onotlogy: 
* inspect the ontology components providing a summary of metrics 
* provides a SPARQL query function to retrieve info about the onotolgy 
* loads the hierarchy into neo4j for better data visualization and interaction

#### Prequisities before running the inspection: 

Before running the script of `ontology_inspection_workflow.py`, installing of neo4j service is needed through the following steps: 
```
sudo apt update # Ensure your package manager has the latest package information
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add - # Add Neo4j Repository
echo 'deb https://debian.neo4j.com stable latest' | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt install neo4j
```

Neo4j requires Java 17. if java is not installed on your system 
```
sudo apt install openjdk-17-jre
java --version
```

Then start neo4j
```
sudo systemctl start neo4j
sudo systemctl status neo4j # make sure it is running
```

Open a browser and navigate to http://localhost:7474 to access the Neo4j Browser. The default login is `neo4j` with the password `neo4j` (you’ll be prompted to change it on first login). You could also run `cypher-shell` to change the credentials in the terminal. Make sure to change this line in the script with the new credentials of `<new username>` and `<new password` before running it: 
```
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("<new username>", "<new password>"))
```

Now run the inspection script via `python3 ontology_inspection_workflow.py`. A basic `digitrubber_overview.md` will be generated which has an overview of the onotlogy and the retrieved provided SPARQL query of rubber-related terms: 

#### DigitRubber Ontology Overview

##### Summary Metrics

|    | Metric                           |   Value |
|---:|:---------------------------------|--------:|
|  0 | Number of Classes                |    1419 |
|  1 | Number of Local Classes          |     600 |
|  2 | Number of Object Properties      |     153 |
|  3 | Number of Data Properties        |       3 |
|  4 | Number of Individuals            |     302 |
|  5 | Number of Axioms (Approx)        |    3465 |
|  6 | Number of Rules (SWRL)           |      18 |
|  7 | Number of Subclass Relationships |    1456 |
##### Rubber-Related Terms

|    | Class                                             | Label                                     |
|---:|:--------------------------------------------------|:------------------------------------------|
|  0 | http://purl.obolibrary.org/obo/CHEBI_28798        | rubber particle [chebi]                   |
|  1 | https://www.tib.eu/digitrubber#DIGITRUBBER_000048 | rubber [ita]                              |
|  2 | https://www.tib.eu/digitrubber#DIGITRUBBER_000177 | natural rubber [hsh]                      |
|  3 | https://www.tib.eu/digitrubber#DIGITRUBBER_000178 | natural rubber [ncit]                     |
|  4 | https://www.tib.eu/digitrubber#DIGITRUBBER_000179 | synthetic rubber [hsh]                    |
|  5 | https://www.tib.eu/digitrubber#DIGITRUBBER_000199 | raw rubber samples [ifnano]               |
|  6 | https://www.tib.eu/digitrubber#DIGITRUBBER_000289 | raw rubber [dik]                          |
|  7 | https://www.tib.eu/digitrubber#DIGITRUBBER_000290 | synthetic rubber [dik]                    |
|  8 | https://www.tib.eu/digitrubber#DIGITRUBBER_000291 | M-group rubber [dik]                      |
|  9 | https://www.tib.eu/digitrubber#DIGITRUBBER_000292 | ethylene propylene diene rubber [dik]     |
| 10 | https://www.tib.eu/digitrubber#DIGITRUBBER_000293 | diene rubber [dik]                        |
| 11 | https://www.tib.eu/digitrubber#DIGITRUBBER_000428 | rubber extruder screw [dik]               |
| 12 | https://www.tib.eu/digitrubber#DIGITRUBBER_000493 | scrap rubber [dik]                        |
| 13 | https://www.tib.eu/digitrubber#DIGITRUBBER_000642 | butadiene rubber BR [ifnano]              |
| 14 | https://www.tib.eu/digitrubber#DIGITRUBBER_000644 | butyl rubber BIIR [ifnano]                |
| 15 | https://www.tib.eu/digitrubber#DIGITRUBBER_000645 | EPDM rubber [ifnano]                      |
| 16 | https://www.tib.eu/digitrubber#DIGITRUBBER_000647 | nitrile rubber NBR [ifnano]               |
| 17 | https://www.tib.eu/digitrubber#DIGITRUBBER_000648 | fluororubber FKM [ifnano]                 |
| 18 | https://www.tib.eu/digitrubber#DIGITRUBBER_000649 | hydrogenated nitrile rubber HNBR [ifnano] |
| 19 | https://www.tib.eu/digitrubber#DIGITRUBBER_000650 | styrene-butadiene rubber SBR [ifnano]     |

To explore and visualize the ontology on the graph at http://localhost:7474, run for example Cypher query: `MATCH (n:Class)-[:HAS_SUBCLASS]->(m:Class) RETURN n, m") ` to retrieve the nodes of Class that has relationship type `HAS_SUBCLASS` : 

![demo](https://github.com/user-attachments/assets/aafcca30-9be7-4364-a14e-6cadc7b81a4b)

Next ToDo: 
- Include Reasoners to infer new facts from SWRL rules and axioms.
- Use owlready2's SPARQL engine or rdflib more flexibly.
- .....

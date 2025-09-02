import owlready2 as owl
from rdflib import Graph
import pandas as pd
from neo4j import GraphDatabase

# Step 1: Load the ontology with error handling
try:
    onto = owl.get_ontology("file://./digitrubber-full.owl").load()
except Exception as e:
    print(f"Error loading ontology: {e}")
    exit(1)

# Step 2: Inspect components
def get_overview():
    classes = list(onto.classes())
    obj_props = list(onto.object_properties())
    data_props = list(onto.data_properties())
    individuals = list(onto.individuals())
    rules = list(onto.rules())
    
    subclass_axioms = sum(len(list(cls.subclasses())) for cls in classes)
    property_assertions = sum(len(list(prop.domain)) + len(list(prop.range)) for prop in obj_props + data_props)
    
    axiom_count = len(classes) + len(obj_props) + len(data_props) + len(individuals) + len(rules) + subclass_axioms + property_assertions
    
    local_classes = [c for c in classes if str(c.iri).startswith("https://www.tib.eu/digitrubber#")]
    
    data = {
        "Metric": [
            "Number of Classes", "Number of Local Classes", "Number of Object Properties",
            "Number of Data Properties", "Number of Individuals", "Number of Axioms (Approx)",
            "Number of Rules (SWRL)", "Number of Subclass Relationships"
        ],
        "Value": [
            len(classes),
            len(local_classes),
            len(obj_props),
            len(data_props),
            len(individuals),
            axiom_count,
            len(rules),
            subclass_axioms
        ]
    }
    df = pd.DataFrame(data)
    
    print(f"Total Classes: {len(classes)}")
    print(f"Local DigitRubber Classes: {len(local_classes)}")
    print("Sample Class IRIs (first 5):", [c.iri for c in classes[:5]])
    print("Sample Local Class IRIs (first 5):", [c.iri for c in local_classes[:5]])
    print("Sample Object Properties:", [str(p) for p in obj_props[:10]])
    print(f"Total Subclass Relationships: {subclass_axioms}")
    
    return df

# Step 3: SPARQL Query
def query_ontology(sparql_query):
    try:
        g = Graph()
        g.parse("digitrubber-full.owl", format="xml")
        results = g.query(sparql_query)
        return pd.DataFrame([(str(r.get('class', '')), str(r.get('label', ''))) for r in results], 
                           columns=['Class', 'Label'])
    except Exception as e:
        print(f"SPARQL query error: {e}")
        return pd.DataFrame()

# Example queries
rubber_terms_query = """
PREFIX digitrubber: <https://www.tib.eu/digitrubber#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?class ?label WHERE {
    ?class rdfs:label ?label .
    FILTER(CONTAINS(LCASE(?label), "rubber"))
}
"""

# Function to load hierarchy to Neo4j
def load_to_neo4j(filter_local=True):
    try:
        # Connect to Neo4j
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j_now"))
        
        def add_class(tx, iri, label):
            tx.run("MERGE (c:Class {iri: $iri}) SET c.label = $label", iri=iri, label=label)
        
        def add_subclass(tx, parent_iri, child_iri):
            tx.run("""
                MATCH (p:Class {iri: $parent_iri})
                MATCH (c:Class {iri: $child_iri})
                MERGE (p)-[:HAS_SUBCLASS]->(c)
            """, parent_iri=parent_iri, child_iri=child_iri)
        
        with driver.session() as session:
            # Clear existing data
            session.run("MATCH (n:Class) DETACH DELETE n")
            
            classes_to_plot = [cls for cls in onto.classes() if not filter_local or str(cls.iri).startswith("https://www.tib.eu/digitrubber#")]
            if not classes_to_plot:
                print("Warning: No classes found to load into Neo4j.")
                print(f"Total classes: {len(list(onto.classes()))}")
                print(f"Local classes: {len([c for c in onto.classes() if str(c.iri).startswith('https://www.tib.eu/digitrubber#')])}")
                return
            
            for cls in classes_to_plot:
                label = str(cls).split('.')[-1]  # Cleaner label
                session.execute_write(add_class, cls.iri, label)
            
            edge_count = 0
            for cls in classes_to_plot:
                for sub in cls.subclasses():
                    if sub in classes_to_plot:
                        session.execute_write(add_subclass, cls.iri, sub.iri)
                        edge_count += 1
            
            print(f"Loaded {len(classes_to_plot)} classes and {edge_count} relationships into Neo4j.")
            print("To visualize: Open Neo4j Browser at http://localhost:7474, run Cypher query: MATCH (n:Class)-[:HAS_SUBCLASS]->(m:Class) RETURN n, m")
        
        driver.close()
    except Exception as e:
        print(f"Neo4j connection error: {e}")
        print("Ensure Neo4j is running ('sudo systemctl status neo4j') and the password is correct.")

# Step 4: Visualize class hierarchy using Neo4j
def visualize_hierarchy(filter_local=True):
    # Load to Neo4j
    load_to_neo4j(filter_local=filter_local)

# Step 5: Generate report
def generate_report():
    try:
        overview_df = get_overview()
        rubber_df = query_ontology(rubber_terms_query)
        
        with open("digitrubber_overview.md", "w") as f:
            f.write("# DigitRubber Ontology Overview\n")
            f.write("## Summary Metrics\n")
            try:
                f.write(overview_df.to_markdown())
            except ImportError:
                print("Warning: 'tabulate' not installed.")
                f.write(overview_df.to_string())
            f.write("\n## Rubber-Related Terms\n")
            try:
                f.write(rubber_df.to_markdown() if not rubber_df.empty else "No rubber terms found.\n")
            except ImportError:
                f.write(rubber_df.to_string() if not rubber_df.empty else "No rubber terms found.\n")
        
        visualize_hierarchy(filter_local=True)
        print("Report generated: digitrubber_overview.md")
    except Exception as e:
        print(f"Report generation error: {e}")

# Run the workflow
generate_report()
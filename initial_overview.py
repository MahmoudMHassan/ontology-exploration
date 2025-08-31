import owlready2 as owl
onto = owl.get_ontology("file://./digitrubber.owl").load()
local_classes = [c for c in onto.classes() if str(c.iri).startswith("https://www.tib.eu/digitrubber#")]
print(f"Local Classes: {len(local_classes)}", [c.iri for c in local_classes[:5]])
print(f"Subclass Relationships: {sum(len(list(cls.subclasses())) for cls in onto.classes())}")
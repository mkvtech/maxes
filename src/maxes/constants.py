import os.path
import xmlschema

PATH_BASE = "/vt/md/maxes/maxes"

PATH_XES_SCHEMA_2014 = os.path.join(PATH_BASE, "resources/xes2014-original.xsd")
# PATH_XES_SCHEMA_2014_EXTENDED = os.path.join(PATH_BASE, "resources/xes2014-extended.xsd")
PATH_XES_SCHEMA_2023 = os.path.join(PATH_BASE, "resources/xes2023-original.xsd")
PATH_XES_SCHEMA_2023_EXTENDED = os.path.join(
    PATH_BASE, "resources/xes2023-extended.xsd"
)

xml_schema_xes_2014 = xmlschema.XMLSchema(
    PATH_XES_SCHEMA_2014, namespace="http://www.xes-standard.org"
)
xml_schema_xes_2023 = xmlschema.XMLSchema(
    PATH_XES_SCHEMA_2023, namespace="http://www.xes-standard.org"
)

xml_schema_xes_2023_extended = xmlschema.XMLSchema(
    PATH_XES_SCHEMA_2023_EXTENDED, namespace="http://www.xes-standard.org"
)
"""Modified XES 2023 XML Schema that permits some meta attributes"""

CASE_CONCEPT_NAME = "case:concept:name"
CONCEPT_NAME = "concept:name"
LIFECYCLE_TRANSITION = "lifecycle:transition"
TIME_TIMESTAMP = "time:timestamp"

SPECIAL_XES_ATTRIBUTES = [
    CASE_CONCEPT_NAME,
    CONCEPT_NAME,
    LIFECYCLE_TRANSITION,
    TIME_TIMESTAMP,
]

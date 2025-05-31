import unittest
import xml.etree.ElementTree as ET

from maxes.xes_loader import XesLog, XesTrace, XesEvent, XesAttribute

from maxes.serialization.serialize import serialize_to_xes


class TestSerialize(unittest.TestCase):

    def test_serialize_1(self):
        log = XesLog(
            attributes=[
                XesAttribute("string", "log_a1", "abc", "abc"),
                XesAttribute("int", "log_a2", "999", 999),
            ],
            traces=[
                XesTrace(
                    attributes=[
                        XesAttribute("int", "t0_a1", "10000", 10000),
                        XesAttribute("int", "t0_a2", "10001", 10001),
                        XesAttribute("int", "t0_a3", "10002", 10002),
                    ],
                    events=[
                        XesEvent(attributes=[
                            XesAttribute("int", "t0_e0", "20000", 20000),
                        ]),
                        XesEvent(attributes=[
                            XesAttribute("int", "t0_e0", "20001", 20001),
                        ]),
                    ],
                ),
                XesTrace(
                    attributes=[
                        XesAttribute("int", "t0_a1", "10003", 10003),
                        XesAttribute("int", "t0_a2", "10004", 10004),
                        XesAttribute("int", "t0_a2", "10005", 10005),
                    ],
                    events=[
                        XesEvent(attributes=[
                            XesAttribute("int", "t0_e0", "20002", 20002),
                        ]),
                        XesEvent(attributes=[
                            XesAttribute("int", "t0_e0", "20003", 20003),
                        ]),
                        XesEvent(attributes=[
                            XesAttribute("int", "t0_e0", "20004", 20004),
                        ]),
                    ]
                )
            ]
        )

        result = serialize_to_xes(log)
        # result = ET.ElementTree(result)
        # result = ET.indent(result)
        result = ET.tostring(result, encoding="unicode")
        expected = "<log />"

        self.assertEqual(result, expected)

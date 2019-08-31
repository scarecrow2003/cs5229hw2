#!/usr/bin/python

"""
@Author <Name/Matricno>
Date :
"""

import httplib
import json


class flowStat(object):
    def __init__(self, server):
        self.server = server

    def get(self, switch):
        ret = self.rest_call({}, 'GET', switch)
        return json.loads(ret[2])

    def rest_call(self, data, action, switch):
        path = '/wm/core/switch/'+switch+"/flow/json"
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        #print path
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        conn.close()
        return ret

class StaticFlowPusher(object):
    def __init__(self, server):
        self.server = server

    def get(self, data):
        ret = self.rest_call({}, 'GET')
        return json.loads(ret[2])

    def set(self, data):
        ret = self.rest_call(data, 'POST')
        return ret[0] == 200

    def remove(self, objtype, data):
        ret = self.rest_call(data, 'DELETE')
        return ret[0] == 200

    def rest_call(self, data, action):
        path = '/wm/staticflowpusher/json'
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
        }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        # print ret
        conn.close()
        return ret


pusher = StaticFlowPusher('127.0.0.1')
flowget = flowStat('127.0.0.1')

# To insert the policies for the traffic applicable to path between S1 and S2
def S1toS2():
    # For switch S1, use q1, which limits to 1Mbps, to limit the traffic from h1 to h2
    S1H1ToH2Limit = {'switch': "00:00:00:00:00:00:00:01",
                     "name": "S1h1toh2limit",
                     "cookie": "0",
                     "priority": "2",
                     "in_port": "1",
                     "eth_type": "0x800",
                     "ipv4_src": "10.0.0.1",
                     "ipv4_dst": "10.0.0.2",
                     "active": "true",
                     "actions": "set_queue=1,output=2"}
    # For switch S2, use q1, which limits to 1Mbps, to limit the traffic from h1 to h2
    S2H1ToH2Limit = {'switch': "00:00:00:00:00:00:00:02",
                     "name": "S2h1toh2limit",
                     "cookie": "0",
                     "priority": "2",
                     "in_port": "2",
                     "eth_type": "0x800",
                     "ipv4_src": "10.0.0.1",
                     "ipv4_dst": "10.0.0.2",
                     "active": "true",
                     "actions": "set_queue=1,output=1"}
    pusher.set(S1H1ToH2Limit)
    pusher.set(S2H1ToH2Limit)

# To insert the policies for the traffic applicable to path between S2 and S3
def S2toS3():
    # For switch S2, block traffic from h2 to h3 for UDP port 1000 ~ 1007
    S2H2ToH3Block1 = {'switch': "00:00:00:00:00:00:00:02",
                        "name": "S2h2toh3block1",
                        "cookie": "0",
                        "priority": "2",
                        "in_port": "1",
                        "eth_type": "0x800",
                        "ipv4_src": "10.0.0.2",
                        "ipv4_dst": "10.0.0.3",
                        "ip_proto": "0x11",
                        "udp_dst": "0x03e8/0xfff8",
                        "active": "true",
                        "actions": ""}
    # For switch S2, block traffic from h2 to h3 for UDP port 1008 ~ 1023
    S2H2ToH3Block2 = {'switch': "00:00:00:00:00:00:00:02",
                      "name": "S2h2toh3block2",
                      "cookie": "0",
                      "priority": "2",
                      "in_port": "1",
                      "eth_type": "0x800",
                      "ipv4_src": "10.0.0.2",
                      "ipv4_dst": "10.0.0.3",
                      "ip_proto": "0x11",
                      "udp_dst": "0x03f0/0xfff0",
                      "active": "true",
                      "actions": ""}
    # For switch S2, block traffic from h2 to h3 for UDP port 1024 ~ 1087
    S2H2ToH3Block3 = {'switch': "00:00:00:00:00:00:00:02",
                      "name": "S2h2toh3block3",
                      "cookie": "0",
                      "priority": "2",
                      "in_port": "1",
                      "eth_type": "0x800",
                      "ipv4_src": "10.0.0.2",
                      "ipv4_dst": "10.0.0.3",
                      "ip_proto": "0x11",
                      "udp_dst": "0x0400/0xffc0",
                      "active": "true",
                      "actions": ""}
    # For switch S2, block traffic from h2 to h3 for UDP port 1088 ~ 1095
    S2H2ToH3Block4 = {'switch': "00:00:00:00:00:00:00:02",
                      "name": "S2h2toh3block4",
                      "cookie": "0",
                      "priority": "2",
                      "in_port": "1",
                      "eth_type": "0x800",
                      "ipv4_src": "10.0.0.2",
                      "ipv4_dst": "10.0.0.3",
                      "ip_proto": "0x11",
                      "udp_dst": "0x0440/0xfff8",
                      "active": "true",
                      "actions": ""}
    # For switch S2, block traffic from h2 to h3 for UDP port 1096 ~ 1099
    S2H2ToH3Block5 = {'switch': "00:00:00:00:00:00:00:02",
                      "name": "S2h2toh3block5",
                      "cookie": "0",
                      "priority": "2",
                      "in_port": "1",
                      "eth_type": "0x800",
                      "ipv4_src": "10.0.0.2",
                      "ipv4_dst": "10.0.0.3",
                      "ip_proto": "0x11",
                      "udp_dst": "0x0448/0xfffc",
                      "active": "true",
                      "actions": ""}
    # For switch S2, block traffic from h2 to h3 for UDP port 1100
    S2H2ToH3Block6 = {'switch': "00:00:00:00:00:00:00:02",
                      "name": "S2h2toh3block6",
                      "cookie": "0",
                      "priority": "2",
                      "in_port": "1",
                      "eth_type": "0x800",
                      "ipv4_src": "10.0.0.2",
                      "ipv4_dst": "10.0.0.3",
                      "ip_proto": "0x11",
                      "udp_dst": "1100",
                      "active": "true",
                      "actions": ""}

    # For switch S2, block traffic from h3 to h2 for UDP port 1000 ~1007
    S2H3ToH2Block1 = {'switch': "00:00:00:00:00:00:00:02",
                        "name": "S2h3toh2block1",
                        "cookie": "0",
                        "priority": "2",
                        "in_port": "3",
                        "eth_type": "0x800",
                        "ipv4_src": "10.0.0.3",
                        "ipv4_dst": "10.0.0.2",
                        "ip_proto": "0x11",
                        "udp_dst": "0x03e8/0xfff8",
                        "active": "true",
                        "actions": ""}
    # For switch S2, block traffic from h3 to h2 for UDP port 1008 ~1023
    S2H3ToH2Block2 = {'switch': "00:00:00:00:00:00:00:02",
                      "name": "S2h3toh2block2",
                      "cookie": "0",
                      "priority": "2",
                      "in_port": "3",
                      "eth_type": "0x800",
                      "ipv4_src": "10.0.0.3",
                      "ipv4_dst": "10.0.0.2",
                      "ip_proto": "0x11",
                      "udp_dst": "0x03f0/0xfff0",
                      "active": "true",
                      "actions": ""}
    # For switch S2, block traffic from h3 to h2 for UDP port 1024 ~1087
    S2H3ToH2Block3 = {'switch': "00:00:00:00:00:00:00:02",
                      "name": "S2h3toh2block3",
                      "cookie": "0",
                      "priority": "2",
                      "in_port": "3",
                      "eth_type": "0x800",
                      "ipv4_src": "10.0.0.3",
                      "ipv4_dst": "10.0.0.2",
                      "ip_proto": "0x11",
                      "udp_dst": "0x0400/0xffc0",
                      "active": "true",
                      "actions": ""}
    # For switch S2, block traffic from h3 to h2 for UDP port 1088 ~1095
    S2H3ToH2Block4 = {'switch': "00:00:00:00:00:00:00:02",
                      "name": "S2h3toh2block4",
                      "cookie": "0",
                      "priority": "2",
                      "in_port": "3",
                      "eth_type": "0x800",
                      "ipv4_src": "10.0.0.3",
                      "ipv4_dst": "10.0.0.2",
                      "ip_proto": "0x11",
                      "udp_dst": "0x0440/0xfff8",
                      "active": "true",
                      "actions": ""}
    # For switch S2, block traffic from h3 to h2 for UDP port 1096 ~1099
    S2H3ToH2Block5 = {'switch': "00:00:00:00:00:00:00:02",
                      "name": "S2h3toh2block5",
                      "cookie": "0",
                      "priority": "2",
                      "in_port": "3",
                      "eth_type": "0x800",
                      "ipv4_src": "10.0.0.3",
                      "ipv4_dst": "10.0.0.2",
                      "ip_proto": "0x11",
                      "udp_dst": "0x0448/0xfffc",
                      "active": "true",
                      "actions": ""}
    # For switch S2, block traffic from h3 to h2 for UDP port 1100
    S2H3ToH2Block6 = {'switch': "00:00:00:00:00:00:00:02",
                      "name": "S2h3toh2block6",
                      "cookie": "0",
                      "priority": "2",
                      "in_port": "3",
                      "eth_type": "0x800",
                      "ipv4_src": "10.0.0.3",
                      "ipv4_dst": "10.0.0.2",
                      "ip_proto": "0x11",
                      "udp_dst": "1100",
                      "active": "true",
                      "actions": ""}
    pusher.set(S2H2ToH3Block1)
    pusher.set(S2H2ToH3Block2)
    pusher.set(S2H2ToH3Block3)
    pusher.set(S2H2ToH3Block4)
    pusher.set(S2H2ToH3Block5)
    pusher.set(S2H2ToH3Block6)
    pusher.set(S2H3ToH2Block1)
    pusher.set(S2H3ToH2Block2)
    pusher.set(S2H3ToH2Block3)
    pusher.set(S2H3ToH2Block4)
    pusher.set(S2H3ToH2Block5)
    pusher.set(S2H3ToH2Block6)

    # For switch S3, block traffic from h2 to h3 for UDP port 1000 ~ 1007
    S3H2ToH3Block1 = {'switch': "00:00:00:00:00:00:00:03",
                        "name": "S3h2toh3block1",
                        "cookie": "0",
                        "priority": "2",
                        "in_port": "3",
                        "eth_type": "0x800",
                        "ipv4_src": "10.0.0.2",
                        "ipv4_dst": "10.0.0.3",
                        "ip_proto": "0x11",
                        "udp_dst": "0x03e8/0xfff8",
                        "active": "true",
                        "actions": ""}
    # For switch S3, block traffic from h2 to h3 for UDP port 1008 ~ 1023
    S3H2ToH3Block2 = {'switch': "00:00:00:00:00:00:00:03",
                      "name": "S3h2toh3block2",
                      "cookie": "0",
                      "priority": "2",
                      "in_port": "3",
                      "eth_type": "0x800",
                      "ipv4_src": "10.0.0.2",
                      "ipv4_dst": "10.0.0.3",
                      "ip_proto": "0x11",
                      "udp_dst": "0x03f0/0xfff0",
                      "active": "true",
                      "actions": ""}
    # For switch S3, block traffic from h2 to h3 for UDP port 1024 ~ 1087
    S3H2ToH3Block3 = {'switch': "00:00:00:00:00:00:00:03",
                      "name": "S3h2toh3block3",
                      "cookie": "0",
                      "priority": "2",
                      "in_port": "3",
                      "eth_type": "0x800",
                      "ipv4_src": "10.0.0.2",
                      "ipv4_dst": "10.0.0.3",
                      "ip_proto": "0x11",
                      "udp_dst": "0x0400/0xffc0",
                      "active": "true",
                      "actions": ""}
    # For switch S3, block traffic from h2 to h3 for UDP port 1088 ~ 1095
    S3H2ToH3Block4 = {'switch': "00:00:00:00:00:00:00:03",
                      "name": "S3h2toh3block4",
                      "cookie": "0",
                      "priority": "2",
                      "in_port": "3",
                      "eth_type": "0x800",
                      "ipv4_src": "10.0.0.2",
                      "ipv4_dst": "10.0.0.3",
                      "ip_proto": "0x11",
                      "udp_dst": "0x0440/0xfff8",
                      "active": "true",
                      "actions": ""}
    # For switch S3, block traffic from h2 to h3 for UDP port 1096 ~ 1099
    S3H2ToH3Block5 = {'switch': "00:00:00:00:00:00:00:03",
                      "name": "S3h2toh3block5",
                      "cookie": "0",
                      "priority": "2",
                      "in_port": "3",
                      "eth_type": "0x800",
                      "ipv4_src": "10.0.0.2",
                      "ipv4_dst": "10.0.0.3",
                      "ip_proto": "0x11",
                      "udp_dst": "0x0448/0xfffc",
                      "active": "true",
                      "actions": ""}
    # For switch S3, block traffic from h2 to h3 for UDP port 1100
    S3H2ToH3Block6 = {'switch': "00:00:00:00:00:00:00:03",
                      "name": "S3h2toh3block6",
                      "cookie": "0",
                      "priority": "2",
                      "in_port": "3",
                      "eth_type": "0x800",
                      "ipv4_src": "10.0.0.2",
                      "ipv4_dst": "10.0.0.3",
                      "ip_proto": "0x11",
                      "udp_dst": "1100",
                      "active": "true",
                      "actions": ""}

    # For switch S3, block traffic from h3 to h2 for UDP port 1000 ~1007
    S3H3ToH2Block1 = {'switch': "00:00:00:00:00:00:00:03",
                      "name": "S3h3toh2block1",
                      "cookie": "0",
                      "priority": "2",
                      "in_port": "1",
                      "eth_type": "0x800",
                      "ipv4_src": "10.0.0.3",
                      "ipv4_dst": "10.0.0.2",
                      "ip_proto": "0x11",
                      "udp_dst": "0x03e8/0xfff8",
                      "active": "true",
                      "actions": ""}
    # For switch S3, block traffic from h3 to h2 for UDP port 1008 ~1023
    S3H3ToH2Block2 = {'switch': "00:00:00:00:00:00:00:03",
                      "name": "S3h3toh2block2",
                      "cookie": "0",
                      "priority": "2",
                      "in_port": "1",
                      "eth_type": "0x800",
                      "ipv4_src": "10.0.0.3",
                      "ipv4_dst": "10.0.0.2",
                      "ip_proto": "0x11",
                      "udp_dst": "0x03f0/0xfff0",
                      "active": "true",
                      "actions": ""}
    # For switch S3, block traffic from h3 to h2 for UDP port 1024 ~1087
    S3H3ToH2Block3 = {'switch': "00:00:00:00:00:00:00:03",
                      "name": "S3h3toh2block3",
                      "cookie": "0",
                      "priority": "2",
                      "in_port": "1",
                      "eth_type": "0x800",
                      "ipv4_src": "10.0.0.3",
                      "ipv4_dst": "10.0.0.2",
                      "ip_proto": "0x11",
                      "udp_dst": "0x0400/0xffc0",
                      "active": "true",
                      "actions": ""}
    # For switch S3, block traffic from h3 to h2 for UDP port 1088 ~1095
    S3H3ToH2Block4 = {'switch': "00:00:00:00:00:00:00:03",
                      "name": "S3h3toh2block4",
                      "cookie": "0",
                      "priority": "2",
                      "in_port": "1",
                      "eth_type": "0x800",
                      "ipv4_src": "10.0.0.3",
                      "ipv4_dst": "10.0.0.2",
                      "ip_proto": "0x11",
                      "udp_dst": "0x0440/0xfff8",
                      "active": "true",
                      "actions": ""}
    # For switch S3, block traffic from h3 to h2 for UDP port 1096 ~1099
    S3H3ToH2Block5 = {'switch': "00:00:00:00:00:00:00:03",
                      "name": "S3h3toh2block5",
                      "cookie": "0",
                      "priority": "2",
                      "in_port": "1",
                      "eth_type": "0x800",
                      "ipv4_src": "10.0.0.3",
                      "ipv4_dst": "10.0.0.2",
                      "ip_proto": "0x11",
                      "udp_dst": "0x0448/0xfffc",
                      "active": "true",
                      "actions": ""}
    # For switch S3, block traffic from h3 to h2 for UDP port 1100
    S3H3ToH2Block6 = {'switch': "00:00:00:00:00:00:00:03",
                      "name": "S3h3toh2block6",
                      "cookie": "0",
                      "priority": "2",
                      "in_port": "1",
                      "eth_type": "0x800",
                      "ipv4_src": "10.0.0.3",
                      "ipv4_dst": "10.0.0.2",
                      "ip_proto": "0x11",
                      "udp_dst": "1100",
                      "active": "true",
                      "actions": ""}
    pusher.set(S3H2ToH3Block1)
    pusher.set(S3H2ToH3Block2)
    pusher.set(S3H2ToH3Block3)
    pusher.set(S3H2ToH3Block4)
    pusher.set(S3H2ToH3Block5)
    pusher.set(S3H2ToH3Block6)
    pusher.set(S3H3ToH2Block1)
    pusher.set(S3H3ToH2Block2)
    pusher.set(S3H3ToH2Block3)
    pusher.set(S3H3ToH2Block4)
    pusher.set(S3H3ToH2Block5)
    pusher.set(S3H3ToH2Block6)

# To insert the policies for the traffic applicable to path between S1 and S3
def S1toS3():
    # For switch S1
    S1H1ToH3Limit = {'switch': "00:00:00:00:00:00:00:01",
                     "name": "S1h1toh3limit",
                     "cookie": "0",
                     "priority": "2",
                     "in_port": "1",
                     "eth_type": "0x800",
                     "ipv4_src": "10.0.0.1",
                     "ipv4_dst": "10.0.0.3",
                     "active": "true",
                     "instruction_stat_trigger": "{\"flags\": [\"only_first\"],\"thresholds\": [{\"oxs_type\": \"byte_count\",\"value\": \"20000000\"}]}"}
    # For switch S3
    S3H1ToH3Limit = {'switch': "00:00:00:00:00:00:00:03",
                     "name": "S3h1toh3limit",
                     "cookie": "0",
                     "priority": "2",
                     "in_port": "2",
                     "eth_type": "0x800",
                     "ipv4_src": "10.0.0.1",
                     "ipv4_dst": "10.0.0.3",
                     "active": "true",
                     "instruction_stat_trigger": "{\"flags\": [\"only_first\"],\"thresholds\": [{\"oxs_type\": \"byte_count\",\"value\": \"20000000\"}]}"}

    pusher.set(S1H1ToH3Limit)
    pusher.set(S3H1ToH3Limit)


def staticForwarding():
    # Below 4 flows are for setting up the static forwarding for the path H1->S1->S2->H2 & vice-versa
    # Define static flow for Switch S1 for packet forwarding b/w h1 and h2
    S1Staticflow1 = {'switch': "00:00:00:00:00:00:00:01", "name": "S1h1toh2", "cookie": "0",
                     "priority": "1", "in_port": "1", "eth_type": "0x800", "ipv4_src": "10.0.0.1",
                     "ipv4_dst": "10.0.0.2", "active": "true", "actions": "output=2"}
    S1Staticflow2 = {'switch': "00:00:00:00:00:00:00:01", "name": "S1h2toh1", "cookie": "0",
                     "priority": "1", "in_port": "2", "eth_type": "0x800", "ipv4_src": "10.0.0.2",
                     "ipv4_dst": "10.0.0.1", "active": "true", "actions": "output=1"}
    # Define static flow for Switch S2 for packet forwarding b/w h1 and h2
    S2Staticflow1 = {'switch': "00:00:00:00:00:00:00:02", "name": "S2h2toh1", "cookie": "0",
                     "priority": "1", "in_port": "1", "eth_type": "0x800", "ipv4_src": "10.0.0.2",
                     "ipv4_dst": "10.0.0.1", "active": "true", "actions": "output=2"}
    S2Staticflow2 = {'switch': "00:00:00:00:00:00:00:02", "name": "S2h1toh2", "cookie": "0",
                     "priority": "1", "in_port": "2", "eth_type": "0x800", "ipv4_src": "10.0.0.1",
                     "ipv4_dst": "10.0.0.2", "active": "true", "actions": "output=1"}

    # Below 4 flows are for setting up the static forwarding for the path H1->S1->S3->H3 & vice-versa
    # Define static flow for Switch S1 for packet forwarding b/w h1 and h3
    S1Staticflow3 = {'switch': "00:00:00:00:00:00:00:01", "name": "S1h1toh3", "cookie": "0",
                     "priority": "1", "in_port": "1", "eth_type": "0x800", "ipv4_src": "10.0.0.1",
                     "ipv4_dst": "10.0.0.3", "active": "true", "actions": "output=3"}
    S1Staticflow4 = {'switch': "00:00:00:00:00:00:00:01", "name": "S1h3toh1", "cookie": "0",
                     "priority": "1", "in_port": "3", "eth_type": "0x800", "ipv4_src": "10.0.0.3",
                     "ipv4_dst": "10.0.0.1", "active": "true", "actions": "output=1"}
    # Define static flow for Switch S3 for packet forwarding b/w h1 and h3
    S3Staticflow1 = {'switch': "00:00:00:00:00:00:00:03", "name": "S3h3toh1", "cookie": "0",
                     "priority": "1", "in_port": "1", "eth_type": "0x800", "ipv4_src": "10.0.0.3",
                     "ipv4_dst": "10.0.0.1", "active": "true", "actions": "output=2"}
    S3Staticflow2 = {'switch': "00:00:00:00:00:00:00:03", "name": "S3h1toh3", "cookie": "0",
                     "priority": "1", "in_port": "2", "eth_type": "0x800", "ipv4_src": "10.0.0.1",
                     "ipv4_dst": "10.0.0.3", "active": "true", "actions": "output=1"}

    # Below 4 flows are for setting up the static forwarding for the path H2->S2->S3->H3 & vice-versa
    # Define static flow for Switch S1 for packet forwarding b/w h2 and h3
    S2Staticflow3 = {'switch': "00:00:00:00:00:00:00:02", "name": "S2h2toh3", "cookie": "0",
                     "priority": "1", "in_port": "1", "eth_type": "0x800", "ipv4_src": "10.0.0.2",
                     "ipv4_dst": "10.0.0.3", "active": "true", "actions": "output=3"}
    S2Staticflow4 = {'switch': "00:00:00:00:00:00:00:02", "name": "S2h3toh2", "cookie": "0",
                     "priority": "1", "in_port": "3", "eth_type": "0x800", "ipv4_src": "10.0.0.3",
                     "ipv4_dst": "10.0.0.2", "active": "true", "actions": "output=1"}
    # Define static flow for Switch S3 for packet forwarding b/w h2 and h3
    S3Staticflow3 = {'switch': "00:00:00:00:00:00:00:03", "name": "S3h3toh2", "cookie": "0",
                     "priority": "1", "in_port": "1", "eth_type": "0x800", "ipv4_src": "10.0.0.3",
                     "ipv4_dst": "10.0.0.2", "active": "true", "actions": "output=3"}
    S3Staticflow4 = {'switch': "00:00:00:00:00:00:00:03", "name": "S3h2toh3", "cookie": "0",
                     "priority": "1", "in_port": "2", "eth_type": "0x800", "ipv4_src": "10.0.0.2",
                     "ipv4_dst": "10.0.0.3", "active": "true", "actions": "output=1"}

    # Now, Insert the flows to the switches
    pusher.set(S1Staticflow1)
    pusher.set(S1Staticflow2)
    pusher.set(S1Staticflow3)
    pusher.set(S1Staticflow4)

    pusher.set(S2Staticflow1)
    pusher.set(S2Staticflow2)
    pusher.set(S2Staticflow3)
    pusher.set(S2Staticflow4)

    pusher.set(S3Staticflow1)
    pusher.set(S3Staticflow2)
    pusher.set(S3Staticflow3)
    pusher.set(S3Staticflow4)


if __name__ == '__main__':
    staticForwarding()
    S1toS2()
    S2toS3()
    S1toS3()
    pass

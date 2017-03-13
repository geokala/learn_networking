from learn_network.node import NodeManager

import yaml

from copy import deepcopy


class Runner(object):
    def __init__(self):
        self._nodes = NodeManager()
        self._objectives = []
        self._objective_stage = 0
        self._state_at_start_of_objective = None
        self._state_before_checking_objective = None

    def load_nodes_from_yaml(self, file_location):
        with open(file_location) as nodes_handle:
            nodes_data = nodes_handle.read()
        nodes_data = yaml.load(nodes_data)
        self._nodes.load_from_dict(nodes_data)

    def load_objectives_from_yaml(self, file_location):
        with open(file_location) as objectives_handle:
            objectives_data = objectives_handle.read()
        objectives_data = yaml.load(objectives_data).get('tasks', [])
        self._objectives.extend(objectives_data)

    def prepare_objective(self):
        current = self._objectives[self._objective_stage]

        for packet in current['packets']:
            self._nodes.add_packet(
                start_node=packet['node'],
                content=packet['contents'],
                start=packet['source'],
                destination=packet['destination'],
            )
        self._state_at_start_of_objective = deepcopy(
            self._nodes,
        )

    def route_packets(self, iterations=1):
        return self._nodes.run_network(iterations=iterations)

    def check_for_success(self):
        if self._objective_stage >= len(self._objectives):
            # All objectives completed, so yes- success... is!
            return True

        goal = self._objectives[self._objective_stage]['goal']

        results = {
            'pass': [],
            'fail': [],
        }
        for packet in goal['packets_received']:
            this_goal = deepcopy(packet)
            this_goal['type'] = 'packet_received'
            if self._nodes.packet_received(
                node=this_goal['node'],
                contents=this_goal['contents'],
                source=this_goal['source'],
                destination=this_goal['destination'],
            ):
                results['pass'].append(this_goal)
            else:
                results['fail'].append(this_goal)

        if len(results['fail']) == 0:
            # We succeeded! We can now move on to the next objective.
            self._objective_stage += 1

        return results

    def roll_back_to_start_of_objective(self):
        self.nodes = deepcopy(self._state_at_start_of_objective)

    def roll_back_to_before_check(self):
        self.nodes = deepcopy(self._state_before_checking_objective)
'''
Iterate over tasks in order, only continuing when current one complete.
After each successful task, prepare next task, while keeping existing state.
Task stuff should go in a goal/task runner/evaluator

nodes:
  - id: node1
    type: router
    position: 0,1
  - id: node2
    type: host
    position: 2,1

connections:
  - node1: eth1: 192.0.2.1
    node2: eth2: 192.0.2.2

tasks:
  - packets:
      - node: node1
        source: 192.0.2.1
        destination: 192.0.2.2
        contents: hello node 2
    goal:
      packets_received:
        node: node2
        source_ 192.0.2.1
        destination: 192.0.2.2
        contents: hello node 2
  - packets:
      - node: node2
        source: 192.0.2.2
        destination: 192.0.2.1
        contents: hello node 1
    goal:
      packets_received:
        node: node1
        source_ 192.0.2.2
        destination: 192.0.2.1
        contents: hello node 1
    '''

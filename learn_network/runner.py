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
        # TODO
        pass

    def prepare_objective(self):
        # TODO: Put in any new packets, etc from this objective
        # then deepcopy current nodemanager state to state at start of objective
        pass

    def check_for_success(self):
        # TODO: If objective number is greater than number of objectives, return True
        # Set current state to state_before_check
        # Then check for success
        # If success, set current objective += 1 and return True
        # Else, return False

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
  - id: node2
    type: host

connections:
  - node1: eth1: 192.0.2.1
    node2: eth2: 192.0.2.2

tasks:
  - packet:
      node: node1
      source: 192.0.2.1
      destination: 192.0.2.2
      contents: hello node 2
    goal:
      packet_received:
        node: node2
        source_ 192.0.2.1
        destination: 192.0.2.2
        contents: hello node 2
  - packet:
      node: node2
      source: 192.0.2.2
      destination: 192.0.2.1
      contents: hello node 1
    goal:
      packet_received:
        node: node1
        source_ 192.0.2.2
        destination: 192.0.2.1
        contents: hello node 1
    '''


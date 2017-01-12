

class Runner(object):
    # TODO:
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


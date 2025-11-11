    import networkx as nx

    class Neuron:
        def __init__(self, name, type='processing', activation_func=lambda x: x > 0):
            self.name = name
            self.type = type  # 'input', 'processing', 'output'
            self.activation_func = activation_func  # Simple threshold function
            self.value = 0  # Current activation value

        def activate(self, inputs):
            total = sum(inputs)
            self.value = 1 if self.activation_func(total) else 0
            return self.value

    class Brain:
        def __init__(self):
            self.graph = nx.DiGraph()  # Directed graph for connections

        def add_neuron(self, neuron):
            self.graph.add_node(neuron.name, neuron=neuron)

        def connect(self, from_name, to_name, weight=1):
            self.graph.add_edge(from_name, to_name, weight=weight)

        def process(self, input_values):
            # Set input values
            for node, data in self.graph.nodes(data=True):
                if data['neuron'].type == 'input':
                    data['neuron'].value = input_values.get(node, 0)

            # Propagate through graph (topological order)
            for node in nx.topological_sort(self.graph):
                data = self.graph.nodes[node]
                neuron = data['neuron']
                if neuron.type != 'input':
                    inputs = [self.graph.nodes[pred]['neuron'].value * self.graph[pred][node]['weight']
                            for pred in self.graph.predecessors(node)]
                    neuron.activate(inputs)

            # Get outputs
            outputs = {}
            for node, data in self.graph.nodes(data=True):
                if data['neuron'].type == 'output':
                    outputs[node] = data['neuron'].value
            return outputs
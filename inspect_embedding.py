import dimod
import dwave.inspector
from dwave.system import DWaveSampler, EmbeddingComposite

# Define problem
bqm = dimod.BQM.from_ising({}, {'ab': 1, 'bc': 1, 'ca': 1})

# Get sampler
sampler = EmbeddingComposite(DWaveSampler(solver=dict(qpu=True)))

# Sample with low chain strength
sampleset = sampler.sample(bqm, num_reads=1000, chain_strength=2.0)

dwave.inspector.show(sampleset)
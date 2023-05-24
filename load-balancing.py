import dimod
from dwave.system import LeapHybridCQMSampler

def build_model(jobs : list, T : int):
    cqm = dimod.ConstrainedQuadraticModel()
    n = len(jobs)
    x = [[dimod.Binary(f'x_{i}_{j}') for j in range(T)] for i in range(n)]
    i = 0
    for r,d in jobs:
        cqm.add_constraint(sum([x[i][j] for j in range(r, d+1)]) == 1 )
        for j in range(T):
            if j < r or j > d:
                cqm.add_constraint(x[i][j]==0)
        i=i+1
    cqm.set_objective(sum([sum([x[i][j] for i in range(n)]) * sum([sum([x[i][j] for i in range(n)]) for j in range(T) ])]))

    return cqm

job_lst = [[0,2],[1,3],[1,2],[2,3],[1,2]]
sampler = LeapHybridCQMSampler()
cqm = build_model(job_lst,4)
results = sampler.sample_cqm(cqm, time_limit=180, label='load balancing')
print( results)

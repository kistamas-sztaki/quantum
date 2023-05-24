import dimod
from dwave.system import LeapHybridCQMSampler

def build_model(jobs : list, T : int):
    cqm = dimod.ConstrainedQuadraticModel()
    n = len(jobs)
    x = [[dimod.Binary(f'x_{i}_{j}') for j in range(T)] for i in range(n) ]
    i = 0
    for r,d in jobs:
        cqm.add_constraint(sum([x[i][j] for j in range(r, d+1)]) == 1 )
        i=i+1
    cqm.set_objective(sum([sum([x[i][j] for i in range(n) if j >= jobs[i][0] and j<=jobs[i][1]]) **2 for j in range(T) ]))

    return cqm

job_lst = [[0,2],[1,3],[1,2],[2,3],[1,2]]


cqm = build_model(job_lst,4)

sampler = LeapHybridCQMSampler()
sampleset = sampler.sample_cqm(cqm, time_limit=180, label='load balancing')

feasible_sampleset = sampleset.filter(lambda row: row.is_feasible)  

if len(feasible_sampleset):      
   best = feasible_sampleset.first
   print("{} feasible solutions of {}.".format(
      len(feasible_sampleset), len(sampleset)))
   print("best: ",best) 
   i = 0
   for r,d in job_lst:
       print([best.sample[f'x_{i}_{j}'] for j in range(r,d+1)])
       i=i+1
import numpy as np
import matplotlib.pyplot as plt
import time


N_CITIES = 30  # DNA size
CROSS_RATE = 0.05
MUTATE_RATE = 0.05
POP_SIZE = 200
N_GENERATIONS = 1000
Sub_pop_size = 25






class GA(object):
    def __init__(self, DNA_size, cross_rate, mutation_rate, pop_size ,pop):
        self.DNA_size = DNA_size
        self.cross_rate = cross_rate
        self.mutate_rate = mutation_rate
        self.pop_size = pop_size
        if pop.any():
            self.pop=pop
        else:
            self.pop = np.random.rand(self.pop_size,self.DNA_size)*2-1

    def select(self, fitness):
        idx = np.random.choice(np.arange(self.pop_size), size=self.pop_size, replace=True, p=fitness/fitness.sum())
        return self.pop[idx]

    def crossover(self, parent, pop):
        if np.random.rand() < self.cross_rate:
            i_ = np.random.randint(0, self.pop_size, size=1)                        # select another individual from pop
            cross_points = np.random.randint(0, 2, self.DNA_size).astype(np.bool)   # choose crossover points
            parent[cross_points]=pop[i_,cross_points]
        return parent

    def mutate(self, child):
        for point in range(self.DNA_size):
            if np.random.rand() < self.mutate_rate:
                child[point]=child[point]+(np.random.rand()*2-1)
        return child

    def evolve(self, fitness):
        pop = self.select(fitness)
        pop_copy = pop.copy()
        for parent in pop:  # for every parent
            child = self.crossover(parent, pop_copy)
            child = self.mutate(child)
            parent[:] = child
        self.pop = pop
    # def get_fitness(self,distance):
    #     total_distance = np.empty((line_x.shape[0],line_x.shape[1]), dtype=np.float64)
    #     fitness = np.exp(total_distance)
    #     return fitness

# ga = GA(DNA_size=N_CITIES, cross_rate=CROSS_RATE, mutation_rate=MUTATE_RATE, pop_size=POP_SIZE)

# for generation in range(N_GENERATIONS):
#     t = time.time()
#     ga.evolve(fitness)
#     best_idx = np.argmax(fitness)
#     best_sub = best_idx//POP_SIZE
#     best_idx_one = best_idx-best_idx//POP_SIZE*POP_SIZE
#     env.plotting(lx[best_sub][best_idx_one], ly[best_sub][best_idx_one], total_distance[best_sub][best_idx_one])
#     if generation%migration_time==0:
#         ga.migration(fitness)
#         print("MIGRATION!!!!!!!!!!!!!!!!!!!!!")
#     print(ga.pop[best_sub][best_idx_one])
#     print('Gen:', generation,'|best sub: ', (best_sub),'| best fit: %.3f' % fitness[best_sub][best_idx_one],"| time:",time.time()-t )
#
#
# plt.ioff()
# plt.show()
import numpy as np
import matplotlib.pyplot as plt
import time


N_CITIES = 30  # DNA size
CROSS_RATE = 0.05
MUTATE_RATE = 0.05
POP_SIZE = 200
N_GENERATIONS = 1000
Sub_pop_size = 25
migration_time = 50
migration_number = 20

np.random.seed(10)





class GA(object):
    def __init__(self, DNA_size, cross_rate, mutation_rate, pop_size,Sub_pop_size ):
        self.DNA_size = DNA_size
        self.cross_rate = cross_rate
        self.mutate_rate = mutation_rate
        self.pop_size = pop_size
        self.sub_pop_size=Sub_pop_size
        self.pop = np.random.random((self.sub_pop_size,self.pop_size,self.DNA_size))

    # def translateDNA(self, DNA, city_position):     # get cities' coord in order
    #     line_x = np.empty_like(DNA, dtype=np.float64)
    #     line_y = np.empty_like(DNA, dtype=np.float64)
    #     for k, pop in enumerate(DNA):
    #         for i, d in enumerate(pop):
    #             city_coord = city_position[d]
    #             line_x[k, i, :] = city_coord[:, 0]
    #             line_y[k, i, :] = city_coord[:, 1]
    #     return line_x, line_y
    #
    # def get_fitness(self, line_x, line_y):
    #     total_distance = np.empty((line_x.shape[0],line_x.shape[1]), dtype=np.float64)
    #
    #     for x in range(Sub_pop_size):
    #         for i, (xs, ys) in enumerate(zip(line_x[x], line_y[x])):
    #             total_distance[x][i] = np.sum(np.sqrt(np.square(np.diff(xs)) + np.square(np.diff(ys))))
    #         fitness = np.exp(self.DNA_size * 2 / (total_distance))
    #     return fitness, total_distance

    def select(self, fitness):
        pop = self.pop
        for i,fit in enumerate(fitness):
            idx = np.random.choice(np.arange(self.pop_size), size=self.pop_size, replace=True, p=fit / fit.sum())
            pop[i][:]=pop[i][idx]
        return pop

    def crossover(self, parent, pop):
        if np.random.rand() < self.cross_rate:
            i_ = np.random.randint(0, self.pop_size, size=1)                        # select another individual from pop
            cross_points = np.random.randint(0, 2, self.DNA_size).astype(np.bool)   # choose crossover points
            parent[cross_points]=pop[i_,cross_points]
        return parent

    def mutate(self, child):
        for point in range(self.DNA_size):
            if np.random.rand() < self.mutate_rate:
                swap_point = np.random.randint(0, self.DNA_size)
                swapA, swapB = child[point], child[swap_point]
                child[point], child[swap_point] = swapB, swapA
                child[point]=child[point]*(np.random.rand()*4-2)
        return child

    def evolve(self, fitness):
        pop = self.select(fitness)
        pop_copy = pop.copy()
        for sup,sup_copy in zip(pop,pop_copy):
            for parent in sup:  # for every parent
                child = self.crossover(parent, sup_copy)
                child = self.mutate(child)
                parent[:] = child
        self.pop = pop
    def migration(self,fitness):
        pop = self.pop
        fitness_index = np.argsort(fitness)
        for x in range(Sub_pop_size):
            pop[x - 1][fitness_index[x - 1][:migration_number]] = pop[x][fitness_index[x][-migration_number:]]
        self.pop = pop





def translateDNA( DNA, city_position):  # get cities' coord in order
    line_x = np.empty_like(DNA, dtype=np.float64)
    line_y = np.empty_like(DNA, dtype=np.float64)
    for k,pop in enumerate(DNA):
        for i, d in enumerate(pop):
            city_coord = city_position[d]
            line_x[k,i, :] = city_coord[:, 0]
            line_y[k,i, :] = city_coord[:, 1]
    return line_x, line_y
class TravelSalesPerson(object):
    def __init__(self, n_cities):
        self.city_position = np.random.rand(n_cities, 2)
        plt.ion()

    def plotting(self, lx, ly, total_d):
        c_num = len(self.city_position)
        plt.cla()
        plt.title('MGA_3')
        colour = np.linspace(10,20,c_num)
        plt.scatter(self.city_position[:, 0].T, self.city_position[:, 1].T, s=100, c=colour)
        plt.plot(lx.T, ly.T, 'k--')
        plt.text(-0.05, -0.05, "Total distance=%.2f" % total_d, fontdict={'size': 10, 'color': 'red'})
        plt.xlim((-0.1, 1.1))
        plt.ylim((-0.1, 1.1))
        plt.pause(0.0000000000000000000000000000001)

env = TravelSalesPerson(N_CITIES)

ga = GA(DNA_size=N_CITIES, cross_rate=CROSS_RATE, mutation_rate=MUTATE_RATE, pop_size=POP_SIZE)




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
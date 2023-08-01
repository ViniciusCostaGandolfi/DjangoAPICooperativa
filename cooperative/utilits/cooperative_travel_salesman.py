import numpy as np
from ortools.linear_solver import pywraplp
import time 
import haversine as hs
from typing import List

class CooperativeTravelSalesman:
    def __init__(self, points: List[List[float]], use_longest_point: bool | None = None, use_last_point: bool | None = None):
        self.points = np.array(points)
        self.matriz = np.zeros((len(self.points), len(self.points)))
        self.calcula_distancia_entre_points()
        self.solver = pywraplp.Solver("Modelo de Transporte", pywraplp.Solver.SCIP_MIXED_INTEGER_PROGRAMMING)
        self.numeroDepoints = len(self.matriz)
        self.rangeI = np.arange(0, self.numeroDepoints)
        self.rangeJ = np.arange(0, self.numeroDepoints)
        self.rangeJLess = np.arange(0, self.numeroDepoints-1)
        self.ordem = []
        self.use_longest_point = use_longest_point
        self.use_last_point = use_last_point
        self.lat_lon_use_longest_point = None
        self.resposta = {"points": self.points.tolist()}

    def maximo_points_validos(self):
        if len(self.points) > 25:
            raise ValueError("Máximo de points por rota é 25!!!")

    def calcula_distancia_entre_points(self):
        for i in range(len(self.points)):
            for j in range(len(self.points)):
                self.matriz[i, j] = hs.haversine(self.points[i], self.points[j])

    def arruma_ordem(self):
        lista = [self.ordem[0][0], self.ordem[0][1]]
        while len(lista) <= len(self.ordem):
            for i in range(len(self.ordem)):
                if lista[-1] == self.ordem[i][0]:
                    lista.append(self.ordem[i][1])

        return lista

    def resolve(self):
        self.maximo_points_validos()
        tempo = time.time()
        x = {}
        for i in self.rangeI:
            for j in self.rangeJ:
                x[i, j] = self.solver.IntVar(0, 1, f"x[{i, j}]")

        y = {}
        for i in self.rangeI:
            for j in self.rangeJ:
                y[i, j] = self.solver.NumVar(0, self.solver.Infinity(), f"y[{i, j}]")


        for i in self.rangeI:
            self.solver.Add(self.solver.Sum([x[i, j] for j in self.rangeJ if i != j]) == 1, name='rest1_')
            
        for j in self.rangeJ:
            self.solver.Add(self.solver.Sum([x[i, j] for i in self.rangeI if i != j]) == 1, name='rest2_')
            
        for i in self.rangeI:
            for j in self.rangeJ:
                if i != j:
                    self.solver.Add(y[i, j] <= (self.numeroDepoints - 1) * x[i, j], name='rest3_')

        for j in self.rangeJLess:
            self.solver.Add(self.solver.Sum([y[i, j] for i in self.rangeI if i != j]) == 1 + self.solver.Sum([y[j, i] for i in self.rangeI if i != j]), name='rest4_')
            
        if isinstance(self.use_last_point, bool):
            last_point = len(self.rangeI) - 1
            self.solver.Add(x[last_point, 0] == 1)
            
        elif isinstance(self.use_longest_point, bool):
            longest_point = np.argmax(self.matriz[:, 0])
            self.lat_lon_use_longest_point = self.points[longest_point]
            print(self.use_longest_point)
            self.solver.Add(x[longest_point, 0] == 1)

        funcaoObjetivo = []
        for i in self.rangeI:
            for j in self.rangeJ:
                if i != j:
                    funcaoObjetivo.append(x[i, j] * self.matriz[i, j])

        self.solver.Minimize(self.solver.Sum(funcaoObjetivo))
        status = self.solver.Solve()

        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            self.resposta["distancia"] =  float(self.solver.Objective().Value())

            for i in self.rangeI:
                for j in self.rangeJ:
                    if x[i, j].solution_value() != 0:
                        self.ordem.append([int(i), int(j)])
            self.ordem = self.arruma_ordem()
            self.resposta['ordem'] = self.ordem
            # self.resposta['points'] = self.points[self.ordem]
            return self.resposta
        else:
            return {}

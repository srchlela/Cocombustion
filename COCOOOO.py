# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 15:30:47 2020

@author: guillaume.thomas
"""

from gurobipy import *

gdispo = 700000
coutfixeg = 100000
eff = 0.38
prod = 990000/eff
ratiocmin = 0.1
invs=500000


combustible, pci, achat, vente = multidict({
        'c':  [25/3.6, 75, 43.2],
        'g': [18/3.6, 190, 75],

})

combustibles, pcis, achats, ventes = multidict({
        'br': [8/3.6, 1, 115],
        'bf': [8/3.6, 1, 75],
        'rv': [8/3.6, 1, 75],

})

def profit(c):
    return pci[c]*eff*vente[c] - achat[c]

def profits(c):
    return pcis[c]*eff*ventes[c] - achats[c]


coco = Model('COCOmbustion')
coco.modelSense = GRB.MAXIMIZE

X = coco.addVars(combustible, 20, lb=0, vtype=GRB.CONTINUOUS)
Y= coco.addVars(combustibles, 20, lb=0, vtype=GRB.CONTINUOUS)
stock=coco.addVar(lb=0,vtype=GRB.BINARY)
inv=coco.addVar(lb=0,vtype=GRB.BINARY)

    

for i in range(20):
    
    coco.addConstr(quicksum(pci[c]*X[c,i] for c in combustible)
                   + quicksum(pcis[c]*Y[c,i] for c in combustibles)== prod)
    coco.addConstr((1-ratiocmin)*X['c',i] - ratiocmin*X['g',i] >= 0)
    coco.addConstr(X['g',i] - gdispo <= 0)
    coco.addConstr(sum(Y[c,i] for c in combustibles) <= 1500*365*(1+stock)
    

coco.setObjective(quicksum(profit(c)*X[c,i] for c in combustible for i in range(20))+quicksum(profits(c)*Y[c,i] for c in combustibles for i in range(20)) - stock*invs - coutfixeg,
                  GRB.MAXIMIZE)

        
coco.optimize()


print('------OPTI ECONOMIQUE ---------')
print()

Obj=coco.getObjective()
Opti=Obj.getValue()
print(f"Sur 20 ans le bénéfice est de : {Opti:.0f} euros")

for c in combustible:
    print(c, int((sum(X[c,i].x for i in range(20)))/1000),"Kt")

for c in combustibles:
    print(c, int((sum(Y[c,i].x for i in range(20)))/1000),"Kt")

print(stock.x)

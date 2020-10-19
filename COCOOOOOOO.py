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
        'br': [8/3.6, 1, 115],
        'bf': [8/3.6, 1, 75],
        'rv': [8/3.6, 1, 75],

})


def profit(c):
    return pci[c]*eff*vente[c] - achat[c]

#permet de faire la contrainte sur le stockage
l=[]
for c in range(2,5) :
    l.append(combustible[c])


coco = Model('COCOmbustion')
coco.modelSense = GRB.MAXIMIZE

X = coco.addVars(combustible, 20, lb=0, vtype=GRB.CONTINUOUS)
stock=coco.addVar(lb=0,vtype=GRB.BINARY)

    fgfffffdgsdfgfdgsd 

for i in range(20):
    
    coco.addConstr(quicksum(pci[c]*X[c,i] for c in combustible)== prod)
    coco.addConstr((1-ratiocmin)*X['c',i] - ratiocmin*X['g',i] >= 0)
    coco.addConstr(X['g',i] - gdispo <= 0)
    coco.addConstr((sum(X[c,i] for c in l )) <= stock*1500*365+1500*365 )
    

coco.setObjective(quicksum(profit(c)*X[c,i] for c in combustible for i in range(20))- stock*invs - coutfixeg,
                  GRB.MAXIMIZE)

        
coco.optimize()


print('------OPTI ECONOMIQUE ---------')
print()

Obj=coco.getObjective()
Opti=Obj.getValue()
print(f"Sur 20 ans le bénéfice est de : {Opti:.0f} euros")

for c in combustible:
    print(c, int((sum(X[c,i].x for i in range(20)))/1000),"Kt")

if stock.x ==1:
    print("En investissant dans 1500t/an de stockage bois en plus")



import random  
import matplotlib.pyplot as plt  

nums = []

# La valeur positive/négative de lambda détermine si la distribution est croissante ou décroissante.
# (Si lambda est négatif, 1024 sera la valeur la plus probable, et 128 la moins probable)
# (Si lambda est positif, 128 sera la valeur la plus probable, et 1024 la moins probable)  
lbda = -1.5
# Taille maximum/minimale des paquets
min_bound = 128
max_bound = 1024
    
for i in range(10000):  
    temp = random.expovariate(lbda) + min_bound
    nums.append(temp)  

# Iterement de l'ensemble des nombres générés
# pour qu'ils soient entre min_bound et max_bound
min_num = min(nums)
max_num = max(nums)
for i in range(len(nums)):
    # On normalise les nombres
    # entre min_bound et max_bound
    nums[i] = (nums[i] - min_num) / (max_num - min_num) * (max_bound - min_bound) + min_bound


# print
print(max(nums))
print(min(nums))

# plot un graph représentant la distribution exponentielle
plt.hist(nums, bins = 200)  
# Ajoute la valeur de lambda dans un texte dans le graphe
plt.text(600, 250, r'$\lambda$ = ' + str(lbda), bbox=dict(facecolor='grey', alpha=0.5))
plt.show() 
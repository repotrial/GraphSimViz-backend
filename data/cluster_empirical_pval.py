import pandas as pd

# user input: two types of network/data to be used for comparision (gene, variant, drug, symptom, comorbidity), and namespace (for now MONDO and ICD10) >> then we know what file to read
# if comorbidity is selected, MONDO option is not possible
path_to_local_distances = '/results/disease_gene_vs_disease_drug/local_distances.csv'
local_distances = pd.read_csv(str(path_to_local_distances))
# we need to decide if we want to give the option to user to select what distance type to use (topology_only or normalized_ranks) or we return the result for both? 
distance_types = list(set(local_distances['distance_type']))
all_nodes = set(local_distances['node'])
batch_len = len(all_nodes)*len(distance_types)

# user input set of diseases
node_ids = ['mondo.0004975', 'mondo.0000437' , 'mondo.0007739', 'mondo.0005180', 'mondo.0004976', 'mondo.0020128', 'mondo.0005301'] # this list is used for the paper

sum_local_distance_true = {'distance_type': [], 'sum_distance':[]}
for distance_type in distance_types:
    sum_true = 0.0
    for node_id in node_ids:
        true_distance = local_distances[(local_distances['node'] == node_id) & ~local_distances['permuted'] & (local_distances['distance_type'] == distance_type)]['distance'].to_list()[0]
        sum_true += true_distance
    sum_local_distance_true['distance_type'].append(distance_type)
    sum_local_distance_true['sum_distance'].append(sum_true)

sum_local_distance_random_list = []
for i in range(1, 1001):
    sum_local_distance_random = {'distance_type': [], 'sum_distance': []}
    ld_slice = local_distances.loc[i*batch_len:(i+1)*batch_len]
    for distance_type in distance_types:
        sum_random = 0.0
        for node_id in node_ids:
            rand_distance = ld_slice[(ld_slice['node'] == node_id) & ld_slice['permuted'] &
                                            (ld_slice['distance_type'] == distance_type)]['distance'].to_list()[0]
            sum_random += rand_distance
        sum_local_distance_random['distance_type'].append(distance_type)
        sum_local_distance_random['sum_distance'].append(sum_random)
    sum_local_distance_random_list.append(sum_local_distance_random)

p_values = {'distance_type': [], 'p_value': []}
if sum_local_distance_random_list[0].get('distance_type') == sum_local_distance_true.get('distance_type'):
    for dt in range(3):
        distance_type = sum_local_distance_random_list[0].get('distance_type')[dt]
        numleq = 0
        p_values['distance_type'].append(distance_type)
        for rd in sum_local_distance_random_list:
            if rd.get('sum_distance')[dt] <= sum_local_distance_true.get('sum_distance')[dt]:
                numleq += 1
        p_values['p_value'].append(float(numleq+1)/float(1000+1))

print(p_values)
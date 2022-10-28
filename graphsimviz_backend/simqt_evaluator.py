import os

import pandas as pd


# from graphsimviz_backend.tasks.task_hook import TaskHook
# import graphsimviz_backend.graphsimqt as graphsimqt


def get_data_dir():
    return "/usr/src/data/"


def get_network_comp_dir(networkType, network1, network2, id_space):
    id_space_suffix = '_' + id_space if id_space == 'ICD10' or id_space == 'UMLS' else ''
    dir1 = os.path.join(get_data_dir(), f'{network1}_vs_{network2}{id_space_suffix}')
    if networkType == 'drug-disease':
        return os.path.join(get_data_dir(), f'GED_drug_indication_distances_vs_DrPD{id_space_suffix}')
    if os.path.exists(dir1):
        return dir1
    dir2 = os.path.join(get_data_dir(), f'{network2}_vs_{network1}{id_space_suffix}')
    if os.path.exists(dir2):
        return dir2
    return None


def get_local_dist_file(dir):
    return os.path.join(dir, 'local_distances.csv')


def get_local_p_value_file(dir):
    return os.path.join(dir, 'local_empirical_p_values.csv')


def get_global_score_files(networkType, dir):
    if networkType == 'drug-disease':
        return [os.path.join(dir, 'global_empirical_p_values.csv'),
                os.path.join(dir, 'global_mwu_p_values_together.csv')]
    return [os.path.join(dir, 'global_empirical_p_values.csv'),
            os.path.join(dir, 'global_mwu_p_values.csv')]


def get_global_scores(global_files):
    global_p_values = pd.read_csv(str(global_files[0]))
    global_mwu_values = pd.read_csv(str(global_files[1]))
    return {'empirical_p_values': global_p_values.to_dict(), 'mwu_p_values': global_mwu_values.to_dict()}


def get_local_scores(path_to_local_p_values, node_ids):
    import pandas as pd
    local_p_values = pd.read_csv(str(path_to_local_p_values))
    local_p_values = local_p_values[local_p_values['node'].isin(node_ids)]
    local_values = {}
    for distance_type in set(local_p_values['distance_type']):
        p_values = local_p_values[['node', 'p_value','distance_type']]
        p_values = p_values[p_values['distance_type'] == distance_type]
        p_values = p_values.rename(columns={'p_value': 'local_p_value'})
        local_values[distance_type] = p_values.to_dict()
    return local_values


def get_cluster_scores(networkType, path_to_local_distances, node_ids, mwu):
    import pandas as pd
    import scipy.stats as sps

    p_values = {'distance_type': [], 'p_value': []}

    local_distances = pd.read_csv(str(path_to_local_distances))
    distance_types = list(set(local_distances['distance_type']))
    all_nodes = set(local_distances['node'])

    if mwu:
        for distance_type in distance_types:
            selection = (local_distances['distance_type'] == distance_type) & (local_distances['node'].isin(node_ids))
            p_values['distance_type'].append(distance_type)
            x = local_distances[selection & ~local_distances['permuted']]['distance'].to_numpy()
            y = local_distances[selection & local_distances['permuted']]['distance'].to_numpy()
            try:
                if len(node_ids) < 9:
                    _, mwu_p_value = sps.mannwhitneyu(x=x, y=y, alternative='less', method='asymptotic')
                else:
                    _, mwu_p_value = sps.mannwhitneyu(x=x, y=y, alternative='less')
            except ValueError:
                mwu_p_value = 1.0
            p_values['p_value'].append(mwu_p_value)


    else:
        batch_len = len(all_nodes) * len(distance_types)

        sum_local_distance_true = {'distance_type': [], 'sum_distance': []}
        for distance_type in distance_types:
            sum_true = 0.0
            for node_id in node_ids:
                try:
                    true_distance = local_distances[
                        (local_distances['node'] == node_id) &
                        ~local_distances['permuted'] & (
                                local_distances['distance_type'] == distance_type)]['distance'].to_list()[0]
                    sum_true += true_distance
                except:
                    # print(f'Node {node_id} not found in {distance_type} distance type')
                    pass
            sum_local_distance_true['distance_type'].append(distance_type)
            sum_local_distance_true['sum_distance'].append(sum_true)

        sum_local_distance_random_list = []
        for i in range(1, 1001):
            sum_local_distance_random = {'distance_type': [], 'sum_distance': []}
            ld_slice = local_distances.loc[i * batch_len:(i + 1) * batch_len]
            for distance_type in distance_types:
                sum_random = 0.0
                for node_id in node_ids:
                    try:
                        rand_distance = ld_slice[(ld_slice['node'] == node_id) & ld_slice['permuted'] &
                                                 (ld_slice['distance_type'] == distance_type)]['distance'].to_list()[0]
                        sum_random += rand_distance
                    except:
                        # print(f'Node {node_id} not found in {distance_type} distance type')
                        pass
                sum_local_distance_random['distance_type'].append(distance_type)
                sum_local_distance_random['sum_distance'].append(sum_random)
            sum_local_distance_random_list.append(sum_local_distance_random)

        if sum_local_distance_random_list[0].get('distance_type') == sum_local_distance_true.get('distance_type'):
            for dt in (range(3) if networkType != 'drug-disease' else range(1)):
                distance_type = sum_local_distance_random_list[0].get('distance_type')[dt]
                numleq = 0
                p_values['distance_type'].append(distance_type)
                for rd in sum_local_distance_random_list:
                    if rd.get('sum_distance')[dt] <= sum_local_distance_true.get('sum_distance')[dt]:
                        numleq += 1
                p_values['p_value'].append(float(numleq + 1) / float(1000 + 1))

    return pd.DataFrame.from_dict(p_values).to_dict()


def calculate_global_scores(networkType, network1, network2, id_space):
    dir = get_network_comp_dir(networkType, network1, network2, id_space)
    global_file = get_global_score_files(networkType, dir)
    return get_global_scores(global_file)


def calculate_cluster_scores(networkType, network1, network2, id_space, node_ids, mwu):
    dir = get_network_comp_dir(networkType, network1, network2, id_space)
    local_distances = get_local_dist_file(dir)
    return get_cluster_scores(networkType, local_distances, node_ids, mwu)


def calculate_local_scores(networkType, network1, network2, id_space, node_ids):
    dir = get_network_comp_dir(networkType, network1, network2, id_space)
    local_p_values = get_local_p_value_file(dir)
    print(local_p_values)
    return get_local_scores(local_p_values, node_ids)


def calculate(networkType, network1, network2, id_space, disorders, mwu):
    data_dir = get_network_comp_dir(networkType, network1, network2, id_space)
    local_dist_file = get_local_dist_file(data_dir)
    local_p_value_file = get_local_p_value_file(data_dir)

    # compute_empirical_p_values(
    scores = {'local': get_local_scores(local_p_value_file, disorders),
              'global': get_global_scores(get_global_score_files(networkType, data_dir)),
              'cluster': get_cluster_scores(networkType, local_dist_file, disorders, mwu)}

    return scores

    # data = hook.parameters
    # hook.set_progress(0.1, "Executing")
    # result = validate(tar=data["target"], tar_id=data["target_id"], mode="set",
    #                   runs=data["runs"],
    #                   replace=data["replace"], ref=None, ref_id=None, enriched=None,
    #                   background_model=data["background_model"], background_network=None, distance=data["distance"],
    #                   out_dir=data["out"],
    #                   uid=data["uid"], set_progress=hook.set_progress)
    # hook.set_files(files=result["files"], uid=data["uid"])
    # hook.set_results(results=result["result"])

import numpy as np
import torch
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score


import csv
import os

def write_csv_record(csv_path, record):
    """
    Write a record to a CSV file. Automatically updates column headers if new keys appear.
    """
    # Step 1: Load existing rows if file exists
    existing_rows = []
    existing_fieldnames = []
    if os.path.exists(csv_path):
        with open(csv_path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            existing_fieldnames = reader.fieldnames or []
            existing_rows = list(reader)

    # Step 2: Compute updated fieldnames (union of old + new)
    new_keys = list(record.keys())
    updated_fieldnames = sorted(set(existing_fieldnames).union(new_keys))  # sorted for consistency

    # Step 3: Rewrite the file with updated fieldnames
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=updated_fieldnames)
        writer.writeheader()

        # Write existing rows, filling missing keys with ""
        for row in existing_rows:
            completed_row = {key: row.get(key, "") for key in updated_fieldnames}
            writer.writerow(completed_row)

        # Write new record
        completed_record = {key: record.get(key, "") for key in updated_fieldnames}
        writer.writerow(completed_record)

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def save_model(model, name):
    torch.save(model, name)

def load_model(name):
    model = torch.load(name)
    return model

# taken from https://github.com/david-yoon/attentive-modality-hopping-for-SER
'''
list_y_ture : reference (label)
list_y_pred : predicted value
note        : do not consider "label imbalance"
'''


def unweighted_accuracy(list_y_true, list_y_pred):
    assert (len(list_y_true) == len(list_y_pred))

    y_true = np.array(list_y_true)
    y_pred = np.array(list_y_pred)

    return accuracy_score(y_true=y_true, y_pred=y_pred)


'''
list_y_ture : reference (label)
list_y_pred : predicted value
note        : compute accuracy for each class; then, average the computed accurcies
              consider "label imbalance"
'''


def weighted_accuracy(list_y_true, list_y_pred):
    assert (len(list_y_true) == len(list_y_pred))

    y_true = np.array(list_y_true)
    y_pred = np.array(list_y_pred)

    w = np.ones(y_true.shape[0])
    for idx, i in enumerate(np.bincount(y_true)):
        w[y_true == idx] = float(1 / i)

    return accuracy_score(y_true=y_true, y_pred=y_pred, sample_weight=w)

def weighted_precision(list_y_true, list_y_pred):
    wa = precision_score(y_true=list_y_true, y_pred=list_y_pred, average='weighted')
    return wa

def unweighted_precision(list_y_true, list_y_pred):
    uwa = precision_score(y_true=list_y_true, y_pred=list_y_pred, average='macro')
    return uwa

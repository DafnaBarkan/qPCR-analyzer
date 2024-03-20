import pytest
import xlrd
import importlib.util
import sys
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
from qPCR_analyzer import target_fnder, replicate_avg


def test_target_fnder_empty_df():
    test_data = {'Sample Name': [],
                 'Target Name': [],
                 'CT': []
                 }
    test_df = pd.DataFrame(test_data)
    with pytest.raises(SystemExit):
        target_fnder(test_df)

def test_samples_replicate_avg():
    test_data = {'Sample Name': ["sample1", "sample1", "sample1"],
                 'Target Name': ["target1", "target2", "target2"],
                 'CT': [1, 2, 3]
                 }
    test_df = pd.DataFrame(test_data)
    expected_result = ['sample1']
    result = replicate_avg(test_df).index.tolist()
    assert result == expected_result

def test_targets_replicate_avg():
    test_data = {'Sample Name': ["sample1", "sample1", "sample1"],
                 'Target Name': ["target1", "target2", "target2"],
                 'CT': [1, 2, 3]
                 }
    test_df = pd.DataFrame(test_data)
    expected_result = ["target1", "target2"]
    result = replicate_avg(test_df).columns.tolist()
    assert result == expected_result

def test_ct_targets_replicate_avg():
    test_data = {'Sample Name': ["sample1", "sample1", "sample1"],
                 'Target Name': ["target1", "target2", "target2"],
                 'CT': [1, 2, 3]
                 }
    test_df = pd.DataFrame(test_data)
    expected_result = [[1.0, 2.5]]
    result = replicate_avg(test_df).values.tolist()
    assert result == expected_result

def test_replicate_avg_empty_df():
    test_data = {'Sample Name': [],
                 'Target Name': [],
                 'CT': []
                 }
    test_df = pd.DataFrame(test_data)
    with pytest.raises(SystemExit):
        replicate_avg(test_df)





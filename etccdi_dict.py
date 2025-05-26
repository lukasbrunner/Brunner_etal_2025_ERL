#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
(c) by Lukas Brunner (lukas.brunner@uni-hamburg.de) 2024 under a MIT License (https://mit-license.org)

Summary:

"""
import pandas as pd


etccdi_indices = {
    # --- tasmax based ---
    # - percentile baseed -
    'tx90p': {
        'acronym': 'tx90p',
        'unit': '1',
        'valid_range': [0, 100],
        'base_variable': 'tasmax',
        'long_name': 'Amount of hot days',
        'description': 'Time period fraction of days when tasmax > daily 90th percentile',
        'valid_time_aggregation': ['year', 'month'],
        'threshold_based': True,
        'absolute_threshold': False,
    },
    'tx10p': {
        'acronym': 'tx10p',
        'unit': '1',
        'valid_range': [0, 100],
        'base_variable': 'tasmax',
        'long_name': 'Amount of cool days',
        'description': 'Time period fraction of days when tasmax < daily 10th percentile',
        'valid_time_aggregation': ['year', 'month'],
        'threshold_based': True,
        'absolute_threshold': False,
    },
    'wsdi': {
        'acronym': 'wsdi',
        'unit': 'day',
        'valid_range': [0, 366],
        'base_variable': 'tasmax',
        'long_name': 'Warm Spell Duration Index',
        'description': 'Time period count of days with at least 6 consecutive days when tasmax > daily 90th percentile',
        'valid_time_aggregation': ['year'],
        'threshold_based': True,
        'absolute_threshold': False,
    },
    # - absolute theshold based -
    'id': {
        'acronym': 'id',
        'unit': 'day',
        'valid_range': [0, 366],
        'base_variable': 'tasmax',
        'long_name': 'Number of icing days',
        'description': 'Time period count of days with when tasmax < 0degC',
        'valid_time_aggregation': ['year', 'month'],
        'threshold_based': True,
        'absolute_threshold': True,
    },
    'su': {
        'acronym': 'su',
        'unit': 'day',
        'valid_range': [0, 366],
        'base_variable': 'tasmax',
        'long_name': 'Number of summer days',
        'description': 'Time period count of days with when tasmax > 25degC',
        'valid_time_aggregation': ['year', 'month'],
        'threshold_based': True,
        'absolute_threshold': True,
    },
    # - no threshold -
    'txx': {
        'acronym': 'txx',
        'unit': 'same as input',
        'valid_range': None,
        'base_variable': 'tasmax',
        'long_name': 'Hottest daily maximum',
        'description': 'Time period maximum of daily tasmax',
        'valid_time_aggregation': ['year', 'month'],
        'threshold_based': False,
        'absolute_threshold': False,
    },
    'txn': {
        'acronym': 'txn',
        'unit': 'same as input',
        'valid_range': None,
        'base_variable': 'tasmax',
        'long_name': 'Coldest daily maximum',
        'description': 'Time period minimum of daily tasmax',
        'valid_time_aggregation': ['year', 'month'],
        'threshold_based': False,
        'absolute_threshold': False,
    },

    # --- tasmin based ---
    # - percentile based -
    'tn10p': {
        'acronym': 'tn10p',
        'unit': '1',
        'valid_range': [0, 100],
        'base_variable': 'tasmin',
        'long_name': 'Amount of cold nights',
        'description': 'Time period fraction of days when tasmin < daily 10th percentile',
        'valid_time_aggregation': ['year', 'month'],
        'threshold_based': True,
        'absolute_threshold': False,
    },
    'tn90p': {
        'acronym': 'tn90p',
        'unit': '1',
        'valid_range': [0, 100],
        'base_variable': 'tasmin',
        'long_name': 'Amount of warm nights',
        'description': 'Time period fraction of days when tasmin > daily 90th percentile',
        'valid_time_aggregation': ['year', 'month'],
        'threshold_based': True,
        'absolute_threshold': False,
    },
    'csdi': {
        'acronym': 'csdi',
        'unit': 'day',
        'valid_range': [0, 366],
        'base_variable': 'tasmin',
        'long_name': 'Cold Spell Duration Index',
        'description': 'Time period count of days with at least 6 consecutive days when tasmin < daily 10th percentile',
        'valid_time_aggregation': ['year'],
        'threshold_based': True,
        'absolute_threshold': False,
    },
    # - absolute theshold based -
    'fd': {
        'acronym': 'fd',
        'unit': 'day',
        'valid_range': [0, 366],
        'base_variable': 'tasmin',
        'long_name': 'Number of frost days',
        'description': 'Time period count of days with when tasmin < 0degC',
        'valid_time_aggregation': ['year', 'month'],
        'threshold_based': True,
        'absolute_threshold': True,
    },
    'tr': {
        'acronym': 'tr',
        'unit': 'day',
        'valid_range': [0, 366],
        'base_variable': 'tasmin',
        'long_name': 'Number of tropical nights',
        'description': 'Time period count of days with when tasmin > 20degC',
        'valid_time_aggregation': ['year', 'month'],
        'threshold_based': True,
        'absolute_threshold': True,
    },
    # - no threshold -
    'tnn' : {
        'acronym': 'tnn',
        'unit': 'same as input',
        'valid_range': None,
        'base_variable': 'tasmin',
        'long_name': 'Coldest daily minimum',
        'description': 'Time period minimum of daily tasmin',
        'valid_time_aggregation': ['year', 'month'],
        'threshold_based': False,
        'absolute_threshold': False,
    },
    'tnx': {
        'acronym': 'tnx',
        'unit': 'same as input',
        'valid_range': None,
        'base_variable': 'tasmin',
        'long_name': 'Warmest daily maxinium',
        'description': 'Time period maximum of daily tasmin',
        'valid_time_aggregation': ['year', 'month'],
        'threshold_based': False,
        'absolute_threshold': False,
    },

    # --- pr based ----
    # - percentile based -
    'r95p': {
        'acronym': 'r95p',
        'unit': 'same as input',
        'valid_range': None,
        'base_variable': 'pr',
        'long_name': 'Total precipitation from heavy rain days',
        'description': 'Time period total precipitation when pr > 95th percentile of wet day precipitation',
        'valid_time_aggregation': ['year', 'month'],
        'threshold_based': True,
        'absolute_threshold': False,
    },
    'r99p': {
        'acronym': 'r99p',
        'unit': 'same as input',
        'valid_range': None,
        'base_variable': 'pr',
        'long_name': 'Total precipitation from very heavy rain days',
        'description': 'Time period total precipitation when pr > 99th percentile of wet day precipitation',
        'valid_time_aggregation': ['year', 'month'],
        'threshold_based': True,
        'absolute_threshold': False,
    },
    # - absolute threshold based -
    'r10mm': {
        'acronym': 'r10mm',
        'unit': 'day',
        'valid_range': [0, 366],
        'base_variable': 'pr',
        'long_name': 'Number of heavy rain days',
        'description': 'Time period count of days when pr >= 10mm',
        'valid_time_aggregation': ['year', 'month'],
        'threshold_based': True,
        'absolute_threshold': True,
    },
    'r20mm': {
        'acronym': 'r20mm',
        'unit': 'day',
        'valid_range': [0, 366],
        'base_variable': 'pr',
        'long_name': 'Number of very heavy rain days',
        'description': 'Time period count of days when pr >= 20mm',
        'valid_time_aggregation': ['year', 'month'],
        'threshold_based': True,
        'absolute_threshold': True,
    }, 
    # - no threshold -
    'rx1day': {
        'acronym': 'rx1day',
        'unit': 'same as input',
        'valid_range': None,
        'base_variable': 'pr',
        'long_name': 'Maximum 1-day precipitation',
        'description': 'Maximum 1-day total precipitation',
        'valid_time_aggregation': ['year', 'month'],
        'threshold_based': False,
        'absolute_threshold': False,
    }, 
    'rx5day': {
        'acronym': 'rx5day',
        'unit': 'same as input',
        'valid_range': None,
        'base_variable': 'pr',
        'long_name': 'Maximum 5-day precipitation',
        'description': 'Maximum 5-day total precipitation',
        'valid_time_aggregation': ['year', 'month'],
        'threshold_based': False,
        'absolute_threshold': False,
    }, 
    'sdii': {
        'acronym': 'sdii',
        'unit': 'same as input',
        'valid_range': None,
        'base_variable': 'pr',
        'long_name': 'Simple precipitation intensity index',
        'description': 'Total precipitation on wet days (pr >= 1mm) divided by the number of wet days',
        'valid_time_aggregation': ['year', 'month'],
        'threshold_based': False,
        'absolute_threshold': False,
    }, 
    'cdd': {
        'acronym': 'cdd',
        'unit': 'day',
        'valid_range': [0, 366],
        'base_variable': 'pr',
        'long_name': 'Maximum dry spell length',
        'description': 'Number of consecutive dry days (pr < 1mm)',
        'valid_time_aggregation': ['year', 'month'],
        'threshold_based': False,
        'absolute_threshold': False,
    }, 
    'cwd': {
        'acronym': 'cwd',
        'unit': 'same as input',
        'valid_range': None,
        'base_variable': 'pr',
        'long_name': 'Maximum wet spell length',
        'description': 'Number of consecutive wet days (pr >= 1mm)',
        'valid_time_aggregation': ['year', 'month'],
        'threshold_based': False,
        'absolute_threshold': False,
    }, 
    'prcptot': {
        'acronym': 'prcptot',
        'unit': 'same as input',
        'valid_range': None,
        'base_variable': 'pr',
        'long_name': 'Total precipitation on wet days',
        'description': 'Time period total precipitation on wet days (pr >= 1mm)',
        'valid_time_aggregation': ['year', 'month'],
        'threshold_based': False,
        'absolute_threshold': False,
    }, 
    # --- tas based ----
    'gsl': {
        'acronym': 'gsl',
        'unit': 'day',
        'valid_range': None,
        'base_variable': 'tas',
        'long_name': 'Growing season length',
        'description': 'Annual count between first span of at least 6 days with tas > 5degC and first span of at lest 6 days with tas < 5degC at after July 1st. In the southern hemisphere this is definition is shifted by half a year to July 1st - June 30th',
        'valid_time_aggregation': ['year'],
        'threshold_based': True,
        'absolute_threshold': True,
    }, 
    # --- tasmin and tasmax based ----
    'dtr': {
        'acronym': 'dtr',
        'unit': 'same as input',
        'valid_range': None,
        'base_variable': 'tasmin, tasmax',
        'long_name': 'Daily temperature range',
        'description': 'Time period mean of daily difference tasmax - tasmin',
        'valid_time_aggregation': ['year', 'month'],
        'threshold_based': False,
        'absolute_threshold': False,
    }, 
}

etccdi_definitions = {
    'tx90p_thr': {
        'acronym': 'tx90p_thr',
        'unit': 'same as input',
        'valid_range': None,
        'base_variable': 'tasmax',
        'derived_indices': ['tx90p', 'wsdi'],
        'long_name': 'Daily 90th percentile of tasmax',
        'description': 'Daily 90th percentile of tasmax using a 5-day running window',
    },
    'tx10p_thr': {
        'acronym': 'tx10p_thr',
        'unit': 'same as input',
        'valid_range': None,
        'base_variable': 'tasmax',
        'derived_indices': ['tx10p'],
        'long_name': 'Daily 10th percentile of tasmax',
        'description': 'Daily 10th percentile of tasmax using a 5-day running window',
    },
    'tn90p_thr': {
        'acronym': 'tn90p_thr',
        'unit': 'same as input',
        'valid_range': None,
        'base_variable': 'tasmin',
        'derived_indices': ['tnp90p'],
        'long_name': 'Daily 90th percentile of tasmin',
        'description': 'Daily 90th percentile of tasmin using a 5-day running window',
    },
    'tn10p_thr': {
        'acronym': 'tn10p_thr',
        'unit': 'same as input',
        'valid_range': None,
        'base_variable': 'tasmin',
        'derived_indices': ['tn10p', 'csdi'],
        'long_name': 'Daily 10th percentile of tasmin',
        'description': 'Daily 10th percentile of tasmin using a 5-day running window',
    },
    'wd': {
        'acronym': 'wd',
        'unit': 'same as input',
        'valid_range': None,
        'base_variable': 'pr',
        'derived_indices': ['r95', 'r99', 'sdii', 'prcptot'],
        'long_name': 'Wet day',
        'description': 'Days with precipitation > 1mm',
    },
    'r95_thr': {
        'acronym': 'r95_thr',
        'unit': 'same as input',
        'valid_range': None,
        'base_variable': 'pr',
        'derived_indices': ['r95'],
        'long_name': '95th percentile of wet days',
        'description': 'Time period 95th percentile of days with precipitation > 1mm',
    },
    'r99_thr': {
        'acronym': 'r99_thr',
        'unit': 'same as input',
        'valid_range': None,
        'base_variable': 'pr',
        'derived_indices': ['r99'],
        'long_name': '99th percentile of wet days',
        'description': 'Time period 99th percentile of days with precipitation > 1mm',
    },
}


def print_etccdi_table(simple_table=True, columns=None):
    df = pd.DataFrame.from_dict(etccdi_indices).transpose()
    if simple_table:
        pd.set_option('display.max_colwidth', None)
        display(df[['unit', 'base_variable', 'long_name', 'description']])
        pd.set_option('display.max_colwidth', 50)
    elif columns is None:
        display(df)
    else:
        display(df[columns])


def print_etccdi_supplement_table(simple_table=True, columns=None):
    df = pd.DataFrame.from_dict(etccdi_definitions).transpose()
    if simple_table:
        pd.set_option('display.max_colwidth', None)
        display(df[['unit', 'base_variable', 'long_name', 'description', 'derived_indices']])
        pd.set_option('display.max_colwidth', 50)
    elif columns is None:
        display(df)
    else:
        display(df[columns])
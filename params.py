winter_params = {
    'max_zero_allowed_per_year': 270,
    'max_nan_allowed_per_year': 100,
}

fall_params = {
    'max_zero_allowed_per_year': 270,
    'max_nan_allowed_per_year': 100,
    'min_flow_rate': 1, # Don't calculate flow metrics if max flow is befow this value.
    'sigma': 0.2,  # Smaller filter to find fall flush peak
    'broad_sigma': 15,  # Larger filter to find wet season peak
    'wet_season_sigma': 12,  # Medium sigma to find wet season initation peak
    'peak_sensitivity': 0.005,  # smaller value detects more peaks
    'peak_sensitivity_wet': .005, # larger value used for detection of wet season initiation
    'max_flush_duration': 40,  # Maximum duration from start to end, for fall flush peak
    'min_flush_percentage': 0.10, # minimum flush, to satisfy the min required to be called a flush
    'wet_threshold_perc': 0.2, # Return to wet season flow must be certain percentage of that year's max flow
    'peak_detect_perc': 0.30, # The peak identified to search after for wet season initation
    'flush_threshold_perc': 0.30, # Size of flush peak, from rising limb to top of peak, has great enough change
    'min_flush_threshold': 1, # minimum allowable magnitude threshold for fall flush flow
    'date_cutoff': 75, # Latest accepted date for fall flush, in Julian Date counting from Oct 1st = 0. (i.e. Dec 15th = 75)
    'slope_sensitivity': 500 # Sets sensitivity of slope requirement for wet season start time. 
    # Increasing sensitivity decreases the slope value threshold, which can push the start time earlier. 
}

spring_params = {
    'max_zero_allowed_per_year': 270,
    'max_nan_allowed_per_year': 100,
    'max_peak_flow_date': 350,  # max search date for the peak flow date
    'search_window_left': 20,  # left side of search window set around max peak
    'search_window_right': 50,  # right side of search window set around max peak
    'peak_sensitivity': 0.1,  # smaller':> more peaks detection
    # Relative flow (Q-Qmin) of start of spring must be certain percentage of peak relative flow (Qmax-Qmin)
    'peak_filter_percentage': 0.5,
    # If filtered max flow is below this, automatically set spring timing to max flow
    'min_max_flow_rate': .1,
    'window_sigma': 10,  # Heavy filter to identify major peaks in entire water year
    # Smaller filter to identify small peaks in windowed data (smaller sigma val => less filter)
    'fit_sigma': 1.3,
    'sensitivity': 0.2,  # 0.1 - 10, 10 being the most sensitive
    # the detected date's flow has be certain percentage of the max flow in that region
    'min_percentage_of_max_flow': 0.5,
    'lag_time': 4,
    # Earliest accepted date for spring timing, in Julian Date couting from Oct 1st = 0 (i.e. February 15 = 138)
    'timing_cutoff': 138,
    # Don't calculate flow metrics if max flow is befow this value.
    'min_flow_rate': 1
}

summer_params = {
    'max_zero_allowed_per_year': 270,
    'max_nan_allowed_per_year': 100,
    'sigma': 7,  # scalar to set amount of smoothing
    'sensitivity': 900,  # increased sensitivity returns smaller threshold for derivative
    # identifies last major peak after which to search for start date
    'peak_sensitivity': 0.2,
    'max_peak_flow_date': 325,  # max search date for the peak flow date
    # require that summer start is below this flow threshold. Represents percentage of the flow difference between annual max flow and summer minimum.
    'min_summer_flow_percent': 0.125,
    # Don't calculate flow metrics if max flow is befow this value.
    'min_flow_rate': 1
}

general_params = {'annual_result_low_Percentille_filter': 0,
                  'annual_result_high_Percentille_filter': 100, 'max_nan_allowed_per_year': 100}

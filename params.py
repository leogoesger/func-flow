winter_params = {
    'max_zero_allowed_per_year': 360,
    'max_nan_allowed_per_year': 100,
}

fall_params = {
    'max_zero_allowed_per_year': 360,
    'max_nan_allowed_per_year': 100,
    'min_flow_rate': 5,
    'sigma': 0.2, # Smaller filter to find fall flush peak
    'wet_sigma': 10, # Larger filter to find wet season peak
    'peak_sensitivity': 0.005, # smaller is more peak
    'max_flush_duration': 40, # Maximum duration from start to end, for fall flush peak
    'min_flush_percentage': 0.10, # <- * min_flush, to satisfy the min required to be called a flush
    'wet_threshold_perc': 0.2, # Return to wet season flow must be certain percentage of that year's max flow
    'flush_threshold_perc': 0.30, # Size of flush peak, from rising limb to top of peak, has great enough change
    'min_flush_threshold': 1, # minimum allowable magnitude threshold for fall flush flow
    'date_cutoff': 75 # Latest accepted date for fall flush, in Julian Date counting from Oct 1st = 0. (i.e. Dec 15th = 75)
}

spring_params = {
    'max_zero_allowed_per_year': 360,
    'max_nan_allowed_per_year': 100,
    'max_peak_flow_date': 350, # max search date for the peak flow date
    'search_window_left': 20, # left side of search window set around max peak
    'search_window_right': 50, # right side of search window set around max peak
    'peak_sensitivity': 0.1, # smaller':> more peaks detection
    'peak_filter_percentage': 0.5, # Relative flow (Q-Qmin) of start of spring must be certain percentage of peak relative flow (Qmax-Qmin)
    'min_max_flow_rate': 2, # If filtered max flow is below this
    'window_sigma': 10, # Heavy filter to identify major peaks in entire water year
    'fit_sigma': 1.3, # Smaller filter to identify small peaks in windowed data (smaller sigma val => less filter)
    'sensitivity': 0.2, # 0.1 - 10, 0.1 being the most sensitive
    'min_percentage_of_max_flow': 0.5, # the detected date's flow has be certain percetage of the max flow in that region
    'lag_time': 4
}

summer_params = {
    'max_zero_allowed_per_year': 360,
    'max_nan_allowed_per_year': 100,
    'sigma': 7, # scalar to set amount of smoothing
    'sensitivity': 900, # increased sensitivity returns smaller threshold for derivative
    'peak_sensitivity': 0.2, # identifies last major peak after which to search for start date
    'max_peak_flow_date': 325, # max search date for the peak flow date
    'min_summer_flow_percent': 0.125 # require that summer start is below this flow threshold. Represents percentage of the flow difference between annual max flow and summer minimum.
}

general_params = {'annual_result_low_Percentille_filter': 20, 'annual_result_high_Percentille_filter': 80}

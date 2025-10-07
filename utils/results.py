def count_points(results):
    """Count the number of points in the results dictionary."""
    return sum(len(v) for v in results.values())

# def approve_results(results, approved_results):
#     """Approve the results by returning results approved by a template."""
#     last_results = []
    
#     for key, value in results.items():
#         if key in approved_results and approved_results[key] == 'on':
#             last_results.append(key)
#         else:
#             results[key] = []    
#     return {key: value for key, value in results.items()}

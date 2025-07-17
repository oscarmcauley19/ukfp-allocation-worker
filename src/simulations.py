import numpy as np
import pandas as pd
import random
import json

def get_probabilities(df, total):
  probabilities = df['applicants'].apply(lambda x: x / total)
  return probabilities

# get the random selection for an individual based on the probability
# distribution of the deaneries
def get_choice(probability_dist):
  # get the total number of options
  total = len(probability_dist.index)
  dist_list = [i+1 for i in range(total)]
  ratio_list = list(probability_dist)

  choice = []
  for i in range(total):
    total = len(dist_list)
    index = random.choices(population=range(total), weights=ratio_list, k=1)[0]
    choice.append(dist_list[index])
    del dist_list[index], ratio_list[index]

  return choice

# perform n runs and 
def all_runs(probs, places, total_applicants, num_simulations, user_choices, update_progress):
  probabilities = pd.DataFrame.copy(probs)
  total_options = len(probabilities.index)
  num_times_won = {}
  pos_and_place = []
  for i in range(num_simulations):
    slots_left = list(places)
    assignments = [-1 for _ in range(total_applicants)]
    current_index_per_person = [0 for _ in range(total_applicants)]
    user_index = random.choice(range(int(total_applicants)))
    whole_population = [get_choice(probabilities) for i in range(int(total_applicants))]
    whole_population.insert(user_index, user_choices)

    # First run
    for person in range(int(total_applicants)):
      favourite_places = whole_population[person]
      assigned = assignments[person] != -1
      current_index = current_index_per_person[person]

      # Attempt to assign the person to their favourite place
      if (not assigned) and (current_index < total_options):
        current_option = favourite_places[current_index]
        index_of_current_option = current_option - 1
        slots_remaining = slots_left[index_of_current_option]
        
        # If there are slots available, the person is assigned to their favourite place
        if slots_remaining > 0:
          assignments[person] = current_option
          slots_left[index_of_current_option] = slots_remaining - 1
          assigned = True
        else:
          # Otherwise, their next favourite place will be checked in the second run
          current_index_per_person[person] = current_index + 1
  
    # Second run
    for person in range(int(total_applicants)):
      favourite_places = whole_population[person]
      assigned = assignments[person] != -1
      current_index = current_index_per_person[person]
      
      # Keep trying to assign the person according to their preferences until they are assigned to one
      while (not assigned) and (current_index < total_options):
        current_option = favourite_places[current_index]
        index_of_current_option = current_option - 1
        slots_remaining = slots_left[index_of_current_option]

        # If there are slots available, the person is assigned to the current place
        if slots_remaining > 0:
          assignments[person] = current_option
          slots_left[index_of_current_option] = slots_remaining - 1
          assigned = True

        
        current_index_per_person[person] = current_index + 1
        current_index = current_index + 1

      if not assigned:
        # if the person is still not assigned, assign them to the first available slot
        for j in range(total_options):
          if slots_left[j] > 0:
            assignments[person] = j + 1
            slots_left[j] -= 1
            break

    user_result = assignments[user_index]

    if user_result in num_times_won:
      count = num_times_won[user_result]
      num_times_won[user_result] = count + 1
    else:
      num_times_won[user_result] = 1

    pos_and_place.append({'pos': user_index, 'place': [assignments[user_index]]})

    # update the progress
    update_progress((i/num_simulations) * 100)
  return num_times_won, pos_and_place

def perform_simulations(user_ranking, runs, update_progress):
    # import the deanery options from the JSON file
    deaneries = open('./src/data/deaneries.json')
    deaneries = json.load(deaneries)
    deaneries = pd.DataFrame(deaneries)

    # get the application ratio of each deanery
    total_applicants = deaneries['applicants'].sum()
    ratios = pd.DataFrame(deaneries['ratio'])

    # get the probability that an individual picks each deanery
    probabilities = get_probabilities(deaneries, total_applicants)

    places, results = all_runs(probabilities, deaneries['places'], total_applicants, runs, user_ranking, update_progress)
    update_progress(100)
    return places
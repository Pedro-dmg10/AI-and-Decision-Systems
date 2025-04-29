import search

class BAProblem(search.Problem):

    def __init__(self):
        self.n = 0  # Number of vessels
        self.s = 0  # Quay size 
        self.bap_matrix = []  # Matrix to store input data for vessels
        self.ai = []  # Arrival times
        self.pi = []  # Processing times
        self.si = []  # Length
        self.wi = []  # Weight
        self.ui = []  # Mooring start time
        self.vi = []  # Berth start position
        self.initial = None  # Initial state (no vessel has moored yet)
        # Set an initial placeholder state
        initial_state = tuple((-1, -1) for _ in range(self.n))  # No vessels moored initially
        
        # Call the superclass constructor with this initial state and None as goal
        super().__init__(initial_state)
        self.heuristic_cache = {}

    # Method to load the problem data from a file
    def load(self, fh):
        while True:
            line = fh.readline().strip().split()  # Read and split the line
            if line[0] == '#':  # Skip comments (lines starting with '#')
                continue
            else:
                self.s = int(line[0])
                self.n = int(line[1])
                break
        
        for _ in range(self.n):
            row = list(map(int, fh.readline().strip().split()))  
            self.bap_matrix.append(row)  # Add to vessel data matrix
            self.ai.append(row[0])  # Arrival time
            self.pi.append(row[1])  # Processing time
            self.si.append(row[2])  # Vessel length
            self.wi.append(row[3])  # Vessel weight

         # Initialize the state as a tuple where no vessels are moored (start time and berth position = -1)
        self.initial = tuple((-1, -1) for _ in range(self.n))

    # Method to generate possible actions based on the current state
    def actions(self, state):
        actions = []  # List to store valid actions

        # For each vessel that has not been allocated, generate the best possible action to it (allocate it as soon as possible)
        for vessel_idx, (ui, vi) in enumerate(state):
            if ui == -1 and vi == -1:  # If the vessel has not been allocated (ui and vi are -1)
                max_ui = 0 

                # Check the mooring times of other vessels to determine the earliest available start time
                for idx, (other_ui, other_vi) in enumerate(state):
                    if other_ui != -1 and other_vi != -1:  # If the vessel is already moored
                        max_ui = max(max_ui, other_ui + self.pi[idx])

                # If no vessels are moored yet, start at the vessel's arrival time
                if max_ui == 0:
                    max_ui = self.ai[vessel_idx]

                # Generate start times and berth positions
                action_found = False
                for start_time in range(self.ai[vessel_idx], max_ui + 1):  # Respect vessel arrival time
                    for berth_position in range(self.s - self.si[vessel_idx] + 1):  # Respect quay size
                        # Check if the action is valid (no conflicts)
                        if self.is_valid_action(state, vessel_idx, start_time, berth_position):
                            new_action = (vessel_idx, (start_time, berth_position))  
                            actions.append(new_action)  
                            action_found = True  # Action found for this vessel
                            break  # Break berth_position loop if action is found
                    if action_found:
                        break  # Break start_time loop if action is found

        return actions  

    # Method to check if an action is valid (no time or space conflicts)
    def is_valid_action(self, state, vessel_idx, start_time, berth_position):
        # Iterate over other vessels that have already been moored
        for idx, (other_ui, other_vi) in enumerate(state):
            if other_ui != -1 and other_vi != -1:  # Vessel is moored
                # Check for conflicts in mooring time (overlap of processing times)
                if not (start_time + self.pi[vessel_idx] <= other_ui or other_ui + self.pi[idx] <= start_time):
                    # Check for conflicts in berth position (overlap of berth positions)
                    if berth_position < other_vi + self.si[idx] and berth_position + self.si[vessel_idx] > other_vi:
                        return False  # Conflict found, return False
        return True  # No conflicts found, return True

    # Method to update the state after applying an action
    def result(self, state, action):
        new_state = list(state)  # Create a copy of the current state

        vessel_idx, (ui, vi) = action  # Unpack the action (vessel index, start time, berth position)
        new_state[vessel_idx] = (ui, vi)  # Update the state with the new action

        return tuple(new_state)  # Return the updated state as a tuple

    # Goal test to check if all vessels have valid start times and berth positions
    def goal_test(self, state):
        # Check if any vessel still has (-1, -1) as its state (not moored yet)
        for ui, vi in state:
            if ui == -1 or vi == -1:  # If any vessel is not moored
                return False  # Goal not achieved
        return True  # All vessels moored, goal achieved

    # Method to compute the path cost (objective function for Uniform Cost Search)
    def path_cost(self, c, state1, action, state2):
        total_cost = c  # Start with the current cost
        vessel_idx = action[0]  
        ui = state2[vessel_idx][0]  

        # Calculate the departure time for this vessel
        ci = ui + self.pi[vessel_idx]

        # Calculate the flow time (departure time - arrival time)
        fi = ci - self.ai[vessel_idx]

        # Add the weighted cost of this vessel (weight * flow time) to the total cost
        total_cost += self.wi[vessel_idx] * fi

        return total_cost  # Return the updated total cost

    def solve(self):
        
        node = search.astar_search(self, h=lambda n: self.h(n.state)) # Using A* search now
        if node is not None:
            actions = node.solution()
            solution = [(-1, -1)] * self.n

            for action in actions:
                vessel_idx, (start_time, berth_position) = action
                solution[vessel_idx] = (start_time, berth_position) 

            return solution  
        else:
            return None
        

    """
    This heuristic function ensures that the returned value is always an admissible estimate of the true cost to 
    reach the goal from any state in the search space. It is admissible because it never overestimates the true 
    cost of achieving the goal. This is achieved by considering the earliest possible mooring times and the most 
    efficient berth positions for each vessel without imposing constraints that would increase the estimated 
    cost beyond what is achievable in an optimal solution. 

    Since the heuristic calculates the cost based on the best possible action for each unmoored vessel, 
    it does not include delays or conflicts that would increase the actual cost, thus guaranteeing it is 
    an underestimate of or equal to the minimum cost path to the goal.
    """

    def h(self, state):

        if state in self.heuristic_cache:
            return self.heuristic_cache[state]
        
        heuristic = 0

        actions = []  # List to store valid actions

        # For each vessel that has not been allocated, generate the best possible action to it (allocate it as soon as possible)
        for vessel_idx, (ui, vi) in enumerate(state):
            if ui == -1 and vi == -1:  # If the vessel has not been allocated (ui and vi are -1)
                max_ui = 0 

                # Check the mooring times of other vessels to determine the earliest available start time
                for idx, (other_ui, other_vi) in enumerate(state):
                    if other_ui != -1 and other_vi != -1:  # If the vessel is already moored
                        max_ui = max(max_ui, other_ui + self.pi[idx])

                # If no vessels are moored yet, start at the vessel's arrival time
                if max_ui == 0:
                    max_ui = self.ai[vessel_idx]

                # Generate start times and berth positions
                action_found = False
                for start_time in range(self.ai[vessel_idx], max_ui + 1):  # Respect vessel arrival time
                    for berth_position in range(self.s - self.si[vessel_idx] + 1):  # Respect quay size
                        # Check if the action is valid (no conflicts)
                        if self.is_valid_action(state, vessel_idx, start_time, berth_position):
                            new_action = (vessel_idx, (start_time, berth_position))  
                            actions.append(new_action)  
                            action_found = True  # Action found for this vessel
                            break  # Break berth_position loop if action is found
                    if action_found:
                        break  # Break start_time loop if action is found

        for i, (ui, vi) in actions:
            ci = ui + self.pi[i]
            fi = ci - self.ai[i]
            heuristic += self.wi[i] * fi

        self.heuristic_cache[state] = heuristic

        return heuristic


if __name__ == "__main__":
    problem = BAProblem()

    # Open the file and pass the file object to the load method
    with open("ex104.dat", "r") as fh:
        problem.load(fh)

    print(problem.solve())


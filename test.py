def get_best_from_two(num1, num2):
    return num1 if int(num1) > int(num2) else num2

def tournament_ranking(items):
    ranking = []  # Final sorted ranking

    while items:
        # Run a tournament and get the best item
        current_round = items[:]
        while len(current_round) > 1:
            next_round = []
            for i in range(0, len(current_round), 2):
                if i + 1 < len(current_round):
                    winner = get_best_from_two(current_round[i], current_round[i + 1])
                    loser = current_round[i] if winner == current_round[i + 1] else current_round[i + 1]
                    next_round.append(winner)
                else:
                    next_round.append(current_round[i])  # Odd item advances
            current_round = next_round
        
        best_item = current_round[0]  # The last remaining item is the best
        ranking.append(best_item)  # Add it to the ranking
        items.remove(best_item)  # Remove it from the list and repeat
    
    return ranking

# Example usage
items = ["10", "14", "5", "30", "15", "1"]
sorted_items = tournament_ranking(items)
print("Sorted ranking:", sorted_items)

from enum import Enum
from collections import Counter

class Category(Enum):
    ONES = "ONES"
    TWOS = "TWOS"
    THREES = "THREES"
    FOURS = "FOURS"
    FIVES = "FIVES"
    SIXES = "SIXES"
    SEVENS = "SEVENS"
    EIGHTS = "EIGHTS"
    THREE_OF_A_KIND = "THREE_OF_A_KIND"
    FOUR_OF_A_KIND = "FOUR_OF_A_KIND"
    FULL_HOUSE = "FULL_HOUSE"
    SMALL_STRAIGHT = "SMALL_STRAIGHT"
    ALL_DIFFERENT = "ALL_DIFFERENT"
    LARGE_STRAIGHT = "LARGE_STRAIGHT"
    SCHOONER = "SCHOONER"
    CHANCE = "CHANCE"
  
def score(category_name: str, dice_roll: list[int]) -> int:
    if not all(1 <= num <= 8 for num in dice_roll):
        return 0 # returns 0 if the input of the dice is not a value between 1-8
    category_member = Category(category_name) # matches the string input to the corresponding category enum

    if category_member is None:
        raise ValueError(f"{category_name} is not a valid category")
    
    match category_member:
        case Category.ONES | Category.TWOS | Category.THREES | Category.FOURS |  \
             Category.FIVES | Category.SIXES | Category.SEVENS | Category.EIGHTS: #Any combination 
            value_map = {"ONES": 1, "TWOS": 2, "THREES": 3, "FOURS": 4, "FIVES": 5, "SIXES": 6, "SEVENS": 7, "EIGHTS": 8}
            #  the value_map dictionary is used to define each category with an int value for scoring
            return sum(num for num in dice_roll if num == value_map.get(category_member.name))
            # uses list comprehension to filter dice_roll list; only keeps the ints matching the category's dictionary int value
        case Category.THREE_OF_A_KIND: #At least three dice the same 
            if max(Counter(dice_roll).values()) >= 3:
                # Counter is used to count the frequency of each value
                # If we have at least 3 recurring integers, it's three of a kind
                return sum(dice_roll)
            else:
                return 0
        case Category.FOUR_OF_A_KIND: # At least four dice the same 
            if max(Counter(dice_roll).values()) >= 4:
                # Counter is used to count the frequency of each value
                # If we have at least 4 recurring integers, it's four of a kind
                return sum(dice_roll)
            else:
                return 0
        case Category.FULL_HOUSE: # Three of one number and two of another
            if len(Counter(dice_roll)) == 2 and 3 in Counter(dice_roll).values() and 2 in Counter(dice_roll).values():
                # Counter is used to count the frequency of each value
                # If there is a Counter frequency of 2 and another of 3; it's a full house
                return 25
            else:
                return 0
        case Category.SMALL_STRAIGHT: # Four sequential dice 
            dice_roll.sort() # sorting in asc order ensures consecutive order
            for i in range(len(dice_roll) - 3): # going up to -3 accounts for needingto check differences up to the 3rd from last int
                if dice_roll[i + 1] - dice_roll[i] == 1 and dice_roll[i + 2] - dice_roll[i + 1] == 1 and dice_roll[i + 3] - dice_roll[i + 2] == 1:
                    # checks for difference between adjacent elements
                    #if difference is 1 for 3 consecutive comparisons (current e, next e, e two positions ahead)
                    return 30
            return 0
        case Category.ALL_DIFFERENT: #No duplicate numbers 
            if len(set(dice_roll)) == len(dice_roll): # set removes duplicates; if len == len, they are all different
                return 35
            else:
                return 0
        case Category.LARGE_STRAIGHT: #Five sequential dice 
            dice_roll.sort() # sorting in asc order ensures consecutive order
            for i in range(len(dice_roll) - 4): # going up to -3 accounts for needingto check differences up to the 4th from last int
                if all(dice_roll[j] - dice_roll[j - 1] == 1 for j in range(i + 1, i + 5)):
                    # uses a list comprehension to check difference between all adjacent elements within range (curr->4 e's ahead)
                    # if all diffs are 1 in the list comprehension, it's a large straight
                    return 40
            
            return 0
        case Category.SCHOONER: #All dice the same
            if len(set(dice_roll)) == 1: # set removes duplicates; if length == 1, they are all the same
                return 50
            else:
                return 0
        case Category.CHANCE: #Any combination 
            return sum(dice_roll)
        case _:
            return 0
        
def topCategories(dice_roll: list[int]) -> list[Category] | Category:
  # Initialize a dictionary to store category scores
  category_scores = {}
  for category in Category:
      category_scores[category] = score(category.name, dice_roll.copy())
      # .copy() avoids modifying the original dice roll when calculating scores for different categories

  # Find the highest score
  highest_score = max(category_scores.values())

  # Filter categories with the highest score
  top_categories = [category for category, score in category_scores.items() if score == highest_score]

  # Return a single category if there's no tie, otherwise return the list
  return top_categories[0] if len(top_categories) == 1 else top_categories

if __name__ == "__main__":
    category_name = input("Enter category name: ")
    try:
        Category(category_name)
    except ValueError:
        valid_categories = ", ".join([str(c.name) for c in Category])
        print(f"Invalid Category Entered: {category_name}")
        print(f"Try a Valid Category: {valid_categories}")
        exit(1)

    dice_roll_str = input("Enter dice roll (5 comma-separated integers): ")
    try:
        dice_roll = [int(num) for num in dice_roll_str.split(",")]
        if len(dice_roll) > 5:
            raise ValueError("You may only roll 5 dice!")
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

    dice_roll = [int(num) for num in dice_roll_str.split(",")]
    score_result = score(category_name, dice_roll)
    print(f"Score for {category_name}: {score_result}")

    top_categories = topCategories(dice_roll)
    if isinstance(top_categories, list):
        top_categories_str = ", ".join([str(cat.name) for cat in top_categories])
        print(f"Top Categories: {top_categories_str}")
    else:
        print(f"Top Category: {top_categories.name}")
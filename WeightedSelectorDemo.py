"""
Demonstration script for Weighted Selector microservice
Shows the full call workflow - write request, wait, read response
Run this while the microservice is running in another terminal

Format: Results are returned as a single selected outcome
Example: "Rare" means the weighted selection chose "Rare" from the options
"""

import time


def demonstrate_weighted_selector():
    """Show how to call the weighted selector microservice"""
    
    print("=" * 60)
    print("WEIGHTED SELECTOR MICROSERVICE DEMONSTRATION")
    print("=" * 60)
    print("\nMake sure weighted_selector.py is running in another terminal!")
    print("Waiting 3 seconds to start...\n")
    time.sleep(3)
    
    # Test 1: Basic selection
    print("TEST 1: Loot rarity selection")
    print("-" * 60)
    print("Writing request: Common:60,Rare:30,Legendary:10")
    with open('weighted_selector.txt', 'w') as f:
        f.write('Common:60,Rare:30,Legendary:10')
    
    print("Waiting for microservice to process...")
    time.sleep(0.5)
    
    print("Reading result:")
    with open('weighted_selector.txt', 'r') as f:
        result = f.read()
    print(f"  Result: {result}")
    print(f"  (60% chance Common, 30% Rare, 10% Legendary)")
    print()
    
    # Test 2: Binary choice
    print("TEST 2: Binary choice (50/50)")
    print("-" * 60)
    print("Writing request: Heads:50,Tails:50")
    with open('weighted_selector.txt', 'w') as f:
        f.write('Heads:50,Tails:50')
    
    print("Waiting for microservice to process...")
    time.sleep(0.5)
    
    print("Reading result:")
    with open('weighted_selector.txt', 'r') as f:
        result = f.read()
    print(f"  Result: {result}")
    print(f"  (50% chance each)")
    print()
    
    # Test 3: Multiple outcomes
    print("TEST 3: Enemy encounter (4 options)")
    print("-" * 60)
    print("Writing request: Goblin:50,Orc:30,Dragon:15,Nothing:5")
    with open('weighted_selector.txt', 'w') as f:
        f.write('Goblin:50,Orc:30,Dragon:15,Nothing:5')
    
    print("Waiting for microservice to process...")
    time.sleep(0.5)
    
    print("Reading result:")
    with open('weighted_selector.txt', 'r') as f:
        result = f.read()
    print(f"  Result: {result}")
    print(f"  (Weighted by relative probability)")
    print()
    
    # Test 4: Error case - invalid format
    print("TEST 4: Error handling - invalid format")
    print("-" * 60)
    print("Writing request: invalid_input")
    with open('weighted_selector.txt', 'w') as f:
        f.write('invalid_input')
    
    print("Waiting for microservice to process...")
    time.sleep(0.5)
    
    print("Reading result:")
    with open('weighted_selector.txt', 'r') as f:
        result = f.read()
    print(f"  Result: {result}")
    print()
    
    # Test 5: Error case - only one outcome
    print("TEST 5: Error handling - only one outcome")
    print("-" * 60)
    print("Writing request: OnlyOne:100")
    with open('weighted_selector.txt', 'w') as f:
        f.write('OnlyOne:100')
    
    print("Waiting for microservice to process...")
    time.sleep(0.5)
    
    print("Reading result:")
    with open('weighted_selector.txt', 'r') as f:
        result = f.read()
    print(f"  Result: {result}")
    print()
    
    # Test 6: Error case - negative weight
    print("TEST 6: Error handling - negative weight")
    print("-" * 60)
    print("Writing request: Good:50,Bad:-10")
    with open('weighted_selector.txt', 'w') as f:
        f.write('Good:50,Bad:-10')
    
    print("Waiting for microservice to process...")
    time.sleep(0.5)
    
    print("Reading result:")
    with open('weighted_selector.txt', 'r') as f:
        result = f.read()
    print(f"  Result: {result}")
    print()
    
    print("=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    demonstrate_weighted_selector()

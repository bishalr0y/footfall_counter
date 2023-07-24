import statistics

predicted = [7, 6, 6, 7, 6, 9, 7, 6, 7, 6, 7, 8, 7, 7, 6, 7, 6, 5, 6, 4, 5, 6, 5, 5, 4, 4, 4, 4, 5, 5, 3, 4, 4, 4, 4, 5, 4, 4, 4, 5, 4, 5, 4, 4, 4, 4, 5, 5, 6, 5, 6, 5, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 5, 4, 4, 5, 6, 5, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 3, 3, 3, 3, 4, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5]  
actual = [6, 6, 6, 7, 7, 7, 6, 6, 6, 7, 7, 7, 7, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 6, 6, 6, 6, 6, 6, 6, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 6, 6, 5, 5, 6, 6, 6, 6, 5, 5, 5, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5]
percentages = []

print(len(predicted))
print(len(actual))


for i in range(len(predicted)):
    percentage = (predicted[i] / actual[i]) * 100
    percentages.append(percentage)

min_percentage = min(percentages)
max_percentage = max(percentages)

if max_percentage > 100:
    print("Old max: " + str(max_percentage))
    max_percentage = 100

avg_percentage = sum(percentages) / 100

print(percentages)
print(min_percentage)
print(max_percentage)
print(avg_percentage)
import json
#import scrape
import matplotlib.pyplot as plt

with open("houses.json", "r") as read_file:
    data = json.load(read_file)
    

##Hinta, neliöt, huonekpl, kerros, rakennusvuosi, Rak.Tyyppi, Kaupunginosa, Kaupunki

def average():
    sum = 0
    count = 0
    for i in data:
        sum += int(data[i][0])
        count+=1
    average = sum // count
    print("Average price for a house in Vantaa is: %s €" % average)


def perSquarePrice(squares, price):
    squares = int(squares)
    price = int(price)
    return price // squares

def averageValueOfDistrict():
    districts = {}

    for i in data:
        squarePrice = perSquarePrice(data[i][1][:2], data[i][0])
        key = data[i][6]
        districts.setdefault(key, [ ]).append(squarePrice)

    print(districts)
    average = {}
    for key in districts:
        sum = 0
        i = 0
        for price in districts[key]:
            sum += price
            i+=1
        average[key] = sum // i
    print("                         ")
    print(average)
    plt.bar(range(len(average)), list(average.values()), align='center')
    plt.xticks(range(len(average)), list(average.keys()), rotation=90)
    plt.show()





##Poistaa vastikkeet
def cleanJSON(data):
    for i in data:
        rent = data[i][1]
        if "/ kk" in rent:
            print(rent)
            del (data[i][1])
    with open('houses.json', 'w') as data_file:
        data = json.dump(data, data_file)



if __name__ == "__main__":
    averageValueOfDistrict()






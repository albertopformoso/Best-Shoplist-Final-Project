# Best-Shoplist-Final-Project

### Objective
Make a visual tool in which you can tell your shoping list and the program will search in multiple supermarkets wich is the cheapes option for you to buy.

As part of the service, the software will give you the option to make your shoping cart or if you prefer show you the nearest recommended supermarket.

### Following libraries were used
+ Tkinter
+ Time
+ Pandas
+ Regex
+ Pandastable
+ Tqdm
+ Selenium
+ Warnings

### Data used
All the data is generated via webscraping different supermarkets and saving it on .csv files which can be found in the 'data' folder.

The data was clasified in four columns:
+ Product name
+ Price
+ Weight (in kilograms)
+ Supermarket name

This structure let me identify the prefered products by the client, make comparisons between weight and price and to know in which supermarket are the best prices.

### Procedure
__Step 1 - Data Acquisition__
The most important and time consuming part of the project due to the web scraping. As the supermarket webpages are dynamic the best option to accomplish this goal is to use Selenium.

__Step 2 - Data Cleaning__
As the web scraping search for all posible coincidences in the multiple webpages some of the information obtaind are products not highly related to what the customer is searching for in the program, so cleaning the information to do the best selection of products is necesary.

__Step 3 - Filtering__
Here the software will filter by supermarket the 3 best options of each product the client is looking for. The program will filter by prefered brand and by price/weight ratio.
The tool will show all supermarket options so that the client can visualize all the best alternatives by supermarket if he wants to take another decision despite the software recommendations.

__Step 4 - Best Option Selection__
Once the data is filtered, here we will choose the best price/weight ratio of each product and choose the supermarket that gives us the cheapest total price.

__Step 5 - Shoping Cart Creation and Nearest Supermarket__
In this step I include two options so that the client decides what to do.

For the shoping cart creation the program will take the recommended shoping list created for the client and with Selenium search for the specific product on the supermarket webpage and add the items to the cart.

For the nearest supermarket option, with Selenium your location is obtained and then in google maps is dispayed the nearest supermarket in relation with were you are.

### Next Steps
+ Currently it has some limitations such as beign spesific with what you want, the fewer words the better, if you want to search by brand it has to be at the end of the string. So it needs an improvement in regex so it can decide more easly which is the product and which is the brand.
+ Improve the displayed information to a more user friendly design.
+ Make a more efficient scrap with Scrapy

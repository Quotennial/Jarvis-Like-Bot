from selenium import webdriver
import speech_recognition as sRec
import webbrowser
import string

#defining the recipie search
def search_recipe(search_term, num_results=3):
    
    #Open the website using Chrome
    url ="https://recipeland.com/recipes/by_ingredient"
    chromedriver = "/Users/user/pythoncode/chromedriver"
    driver =  webdriver.Chrome(chromedriver)
    driver.get(url)
    
    #Search for the ingredients 
    search_box=driver.find_element_by_id("recipes-by-ingredients")
    search_box.send_keys(search_term)
    search_box.submit
    search_box.send_keys(u'\ue007')
    
    #Save the results
    links = driver.find_elements_by_xpath("//h2//a")
    results =[]
    for link in links[:num_results]:
        #Print the title and the link
        title = link.get_attribute("title")
        href = link.get_attribute("href")
        print(title)
        print(href)
        results.append(href)
    return results

#defining the takeaway search
def takeaway(search_term, num_results=3):
    
    #Open the website using Chrome
    url ="https://deliveroo.co.uk/"
    chromedriver = "/Users/user/pythoncode/chromedriver"
    driver =  webdriver.Chrome(chromedriver)
    driver.get(url)
    
    #Search for the local eateries  
    search_box=driver.find_element_by_id("postcode")
    search_box.send_keys(search_term)
    search_box.submit
    search_box.send_keys(u'\ue007')

# The first selection menu
f = sRec.Recognizer()
with sRec.Microphone() as source:
    print("Hello I'm Jarvis, your night-in companion! Can I help you with this evening? \nCooking at home,\ngetting a food delivery,\nbooking a restaurant \nor other?")
    audio = f.listen(source)

if "delivery" in f.recognize_google(audio):
    # Get input for postcode
    postcode_input = input ("Please type your postcode \n")
    print("Searching for delivery in " + postcode_input)
    takeaway(postcode_input)
    print("Take your pick!")

if "restaurant" in f.recognize_google(audio):
    # get audio input for location
    f3 = sRec.Recognizer()
    url3 = 'https://www.yelp.com/search?cflt=restaurants&find_loc='
    with sRec.Microphone() as source:
        print("Great choice, which area would you like me to search?")
        audio3 = f3.listen(source)

        try:
            print("Ok, I'm searching for some restaurants near " + f3.recognize_google(audio3))
            webbrowser.open_new(url3+f3.recognize_google(audio3))
        except sRec.UnknownValueError:
            print("Oops, sorry I didn't understand what you said")
        except sRec.RequestError as e:
               print("Something went wrong with my hearing; {0}".format(e))

if "home" in f.recognize_google(audio):
    # get audio input for ingredients 
    f4 = sRec.Recognizer()
    url4 = 'https://recipeland.com/recipes/by_ingredient'
    with sRec.Microphone() as source:
        print("Cooking at home? Great, you'll need a recipe, what ingredients do you have? (Max 3) ")
        audio4 = f4.listen(source)
        ingredients = f4.recognize_google(audio4)

        try:
            print("I heard you say " + f4.recognize_google(audio4) + ". I'll search for some recipes now.")
            search_recipe(ingredients, 3)
        except sRec.UnknownValueError:
            print("Oops, sorry I didn't understand what you said")
        except sRec.RequestError as e:
               print("Something went wrong with my hearing; {0}".format(e))

if "other" in f.recognize_google(audio):
    # obtain audio from the microphone
    f5 = sRec.Recognizer()
    with sRec.Microphone() as source:
        print("Awesome, have a nice evening!")


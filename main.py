#  ------------------------------------------------------------------------------------------
# Libraries
#  ------------------------------------------------------------------------------------------
from tkinter import *
from tkinter.ttk import *
import time, pandas as pd, re
from pandastable import Table, TableModel
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import warnings; warnings.simplefilter('ignore')

#  ------------------------------------------------------------------------------------------
# Superama Web Scrap Search
#  ------------------------------------------------------------------------------------------
def superama_search(products):
    '''This function scrap Superama web site'''
    options = webdriver.ChromeOptions();
    options.add_argument('headless');
    options.add_argument('window-size=1920x1080')
    
    sup_product, sup_price, sup_weight_kg = [], [], []
    print('Seraching on Superama...')
    browser = webdriver.Chrome(chrome_options=options)
    #browser = webdriver.Chrome()
    for product in products:
        url = 'https://www.superama.com.mx/buscar/%s' % product
        
        #browser.maximize_window()
        browser.get(url)
        products = browser.find_elements_by_xpath('//*[@class="itemGrid"]')
        superama_lst = []
        for product in products:
            if product.text != '':
                superama_lst.append(product.text)


        for i in superama_lst:
            #print(''.join(i.split('\n')))
            sup_product.append(re.findall(r'^\D+',i.split('\n')[0].lower())[0].strip())

            sup_price.append(float(re.findall(r'\d+?\.\d+(?!.*\d+?\.\d+)',''.join(i.split('\n')))[-1].strip()))
            
            try:
                wheight = re.findall(r'k?g(?!.*k?g)',i.split('\n')[0].lower())[0].strip()
            except: pass
            try:
                temp = float(re.findall(r'\d+(?!.*\d+)',i.split('\n')[0].lower())[0].strip())
            except: pass
            
            try:
                if wheight == 'g':
                    sup_weight_kg.append(temp/1000)
                else:
                    sup_weight_kg.append(temp)
            except:
                sup_weight_kg.append(0)
        progress_bar['value'] += val
        master.update()
    browser.close()


    superama = {'product':sup_product,'price':sup_price,'weight_kg':sup_weight_kg}
    superama = pd.DataFrame(superama)
    superama['supermarket'] = 'superama'
    
    return superama

#  ------------------------------------------------------------------------------------------
# Walmart Web Scrap Search
#  ------------------------------------------------------------------------------------------
def walmart_search(products):
    '''This function scrap Walmart web site'''
    options = webdriver.ChromeOptions();
    options.add_argument('headless');
    options.add_argument('window-size=1920x1080')
    
    wal_product, wal_price, wal_weight_kg = [], [], []
    print('Seraching on Walmart...')
    browser = webdriver.Chrome(chrome_options=options)
    for product in products:
        url = 'https://super.walmart.com.mx/productos?Ntt=%s' % product
        
        #browser.maximize_window()
        browser.get(url)
        
        time.sleep(3)
        #closing pops
        try:
            cross = browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/button')
            cross.click()
        except: pass
        try:
            cross = browser.find_element_by_xpath('//*[@id="root"]/main/div[1]/div/div[2]/button')
            cross.click()
        except: pass
        
        products = browser.find_elements_by_xpath('//*[@data-testid="product"]')
        prices = browser.find_elements_by_xpath('//*[@data-testid="price"]')
        
        walmart_lst = []
        for i,j in zip(products, prices):
            walmart_lst.append(i.text+' '+j.text)
            
        for i in walmart_lst:
            #text = i
            price = [float(i) for i in re.findall(r'\d+?\.\d+(?!.*\d+?\.\d+)',i)] 
            if not price:
                continue
            else:
                try:
                    wal_price.append(min(price))
                except: wal_price.append(0)
                
                wal_product.append(re.findall(r'^\D+',i.split('\n')[0].lower())[0].strip())
                
                try:
                    wheight = re.findall(r'k?g(?!.*k?g)',i.split('\n')[0].lower())[0].strip()
                except: pass
                try:
                    temp = float(re.findall(r'\d+(?!.*\d+)',i.split('\n')[0].lower())[0].strip())
                except: pass

                try:
                    if wheight == 'g':
                        wal_weight_kg.append(temp/1000)
                    else:
                        wal_weight_kg.append(temp)
                except:
                    wal_weight_kg.append(0)
        progress_bar['value'] += val
        master.update()
    browser.close()
        
    walmart = {'product':wal_product,'price':wal_price,'weight_kg':wal_weight_kg}
    walmart = pd.DataFrame(walmart)
    walmart['supermarket'] = 'walmart'
    return walmart

#  ------------------------------------------------------------------------------------------
# Soriana Web Scrap Search
#  ------------------------------------------------------------------------------------------
def soriana_search(products):
    '''This function scrap Soriana web site'''
    options = webdriver.ChromeOptions();
    options.add_argument('headless');
    options.add_argument('window-size=1920x1080')
    
    sor_product, sor_price, sor_weight_kg = [], [], []
    print('Seraching on Soriana...')
    browser = webdriver.Chrome(chrome_options=options)
    for product in products:
        url = 'https://superentucasa.soriana.com/default.aspx?p=13365&postback=1&Txt_Bsq_Descripcion=%s&cantCeldas=0&minCeldas=0' % product
        
        #browser.maximize_window()
        browser.get(url)
        try:
            browser.find_element_by_xpath('/html/body/div[13]/div[2]/div[2]/button[2]').click()
        except: pass
        
        products = browser.find_elements_by_xpath('//*[@class="col-lg-3 col-md-4 col-sm-12 col-xs-12 product-item"]/div[2]/a[1]/h4[1]')
        prices = browser.find_elements_by_xpath('//*[@class="col-lg-3 col-md-4 col-sm-12 col-xs-12 product-item"]/div[2]/div[3]/h4[1]')
        
        soriana_lst = []
        for i,j in zip(products, prices):
            soriana_lst.append(i.text+' '+j.text)
        
        for product, price in zip(products, prices):
            #print(i)
            sor_product.append(re.findall(r'^\D+',product.text.lower())[0].strip())

            sor_price.append(float(re.findall(r'\d+?\.\d+(?!.*\d+?\.\d+)',price.text.lower())[-1].strip()))
            
            try:
                wheight = re.findall(r'k?g(?!.*k?g)',product.text.lower())[0].strip()
            except: pass
            try:
                temp = float(re.findall(r'\d+(?!.*\d+)',product.text.lower())[0].strip())
            except: pass
            
            try:
                if wheight == 'g':
                    sor_weight_kg.append(temp/1000)
                else:
                    sor_weight_kg.append(temp)
            except:
                sor_weight_kg.append(0)
        progress_bar['value'] += val
        master.update()
    browser.close()
    soriana = {'product':sor_product,'price':sor_price,'weight_kg':sor_weight_kg}
    soriana = pd.DataFrame(soriana)
    soriana['supermarket'] = 'soriana'

    if soriana.shape[0]==0:
        soriana = {'product':['none'],'price':[9999],'weight_kg':[0]}
        soriana = pd.DataFrame(soriana)
        soriana['supermarket'] = 'soriana'
        return soriana
    else:
        return soriana

#  ------------------------------------------------------------------------------------------
# LaComer Web Scrap Search
#  ------------------------------------------------------------------------------------------
def comer_search(products):
    '''This function scrap La Comer web site'''
    options = webdriver.ChromeOptions();
    options.add_argument('headless');
    options.add_argument('window-size=1920x1080')
    
    com_product, com_price, com_weight_kg = [], [], []
    print('Seraching on La Comer...')
    browser = webdriver.Chrome(chrome_options=options)
    #browser = webdriver.Chrome()
    for product in products:
        url = 'https://www.lacomer.com.mx/lacomer/goBusqueda.action?succId=287&ver=mislistas&succFmt=100&criterio=%s#/%s' % (product,product)
        
        #browser.maximize_window()
        browser.get(url)
        time.sleep(1)
        products = browser.find_elements_by_xpath('//*[@ng-repeat="resu in resultados"]/div/div[2]/div/div/div/a')
        weights = browser.find_elements_by_xpath('//*[@ng-repeat="resu in resultados"]/div/div[2]/div/div/div/p')
        prices = browser.find_elements_by_xpath('//*[@id="product_list"]/div/div[2]/div[2]/div/div/div/div[3]/div/div/span[2]')
        
#         comer_lst = []
#         for i,j,k in zip(products,prices,weights):
#             comer_lst.append(i.text+' '+j.text+' '+k.text)

        for product, price, weight in zip(products, prices, weights):
            #print(product.text, price.text, weight.text)
            com_product.append(re.findall(r'^\D+',product.text.lower())[0].strip())

            com_price.append(float(re.findall(r'\d+?\.\d+(?!.*\d+?\.\d+)',price.text.lower())[-1].strip()))
            
            try:
                wheight = re.findall(r'k?g(?!.*k?g)',weight.text.lower())[0].strip()
            except: pass
            try:
                temp = float(re.findall(r'\d+(?!.*\d+)',weight.text.lower())[0].strip())
            except: pass
            
            try:
                if wheight == 'g':
                    com_weight_kg.append(temp/1000)
                else:
                    com_weight_kg.append(temp)
            except:
                com_weight_kg.append(0)
        progress_bar['value'] += val
        master.update()
    time.sleep(1)
    browser.close()
    comer = {'product':com_product,'price':com_price,'weight_kg':com_weight_kg}
    comer = pd.DataFrame(comer)
    comer['supermarket'] = 'La Comer'
    progress_bar['value'] += val
    return comer

#  ------------------------------------------------------------------------------------------
# Best Option Selector
#  ------------------------------------------------------------------------------------------
def best_options(shop_lst, df):
    '''This function removes the outliers and obtains
        the possible best options of each product'''
    
    df_clean = pd.DataFrame()
    for product in shop_lst:
        product = product.split()[0]
        #print(product, type(product))
        current_df = df[df['product'].astype(str).str.contains(r'%s' % product)]
        
        q1_weight, q3_weight = current_df['weight_kg'].quantile([0.05,0.95])
        q1_price, q3_price = current_df['price'].quantile([0.05,0.95])
        
        current_df = current_df[(current_df['weight_kg']>q1_weight) & (current_df['weight_kg']<q3_weight)]
        current_df = current_df[(current_df['price']>q1_price) & (current_df['price']<q3_price)]
        
        current_df['price/weight'] =  current_df['price']/current_df['weight_kg']
        current_df = current_df.sort_values('price/weight', ascending=True)[:3]
        df_clean = pd.concat([df_clean, current_df])
        
    df_clean.drop('price/weight', axis=1, inplace=True)
    df_clean.drop_duplicates(subset=['product'], keep='first', inplace = True)
    df_clean.reset_index(drop=True, inplace=True)
    return df_clean

# Final shoplist print -----------------------------------------------------------------
def final_shoplist(df, super_name):
    '''This function prints the best market to shop'''
    
    print('\nThe best supermarket for you is %s' % super_name.capitalize())
    print('Recommended shoplist:')
    print(df.to_markdown())

def filter_selection(df, shop_lst):
    temp_df = pd.DataFrame()
    for product in shop_lst:
        brand = product.split()[-1]
        product = product.split()[0]
        if product != brand:
            temp = df[df['product'].astype(str).str.contains(r'%s' % product)]
            temp = temp[temp['product'].astype(str).str.contains(r'%s' % brand)]
            temp['rel'] = temp['price']/temp['weight_kg']
            temp = temp[temp['rel'] == temp['rel'].min()]
            temp.drop('rel', axis=1, inplace=True)
            temp.drop_duplicates(subset=['price','weight_kg'], keep='first', inplace=True)
            temp_df = pd.concat([temp_df, temp], axis = 0).reset_index(drop=True)
        else:
            temp = df[df['product'].astype(str).str.contains(r'%s' % product)]
            temp['rel'] = temp['price']/temp['weight_kg']
            temp = temp[temp['rel'] == temp['rel'].min()]
            temp.drop('rel', axis=1, inplace=True)
            temp.drop_duplicates(subset=['price','weight_kg'], keep='first', inplace=True)
            temp_df = pd.concat([temp_df, temp], axis = 0).reset_index(drop=True)
    return temp_df

#  ------------------------------------------------------------------------------------------
# Shoping Cart Creator
#  ------------------------------------------------------------------------------------------

# Superama -------------------------------
def shop_cart(df, shoplist, name):
    '''This function creates the shopping cart of the best supermarket'''
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    k=0; i = 1
    flag = False
    
    if name == 'superama':
        driver.get('https://www.superama.com.mx/buscar/%s' % shoplist[k])
        #driver.maximize_window()

        while flag == False:
            if k >= len(shoplist):
                cart = driver.find_element_by_xpath('//*[@id="cartBoxIconShoppingCart"]')
                cart.click()
                flag = True
            try:
                prod = driver.find_element_by_xpath('//*[@id="resultadoProductosBusqueda"]/li[%s]/div/div[2]/p/a' % i).text.lower()
                pri = driver.find_element_by_xpath('//*[@id="resultadoProductosBusqueda"]/li[%s]/div/p' % i).text.split()[-1]
                if bool(re.search(r'%s' % df['product'][k],prod)) and bool(re.search(r'%s' % df['price'][k],pri)):
                    agg = driver.find_element_by_xpath('//*[@id="resultadoProductosBusqueda"]/li[%s]/div/div[3]/div[2]' % i)
                    agg.click()
                    k += 1
                    i = 0
                    if k >= len(shoplist):
                        cart = driver.find_element_by_xpath('//*[@id="cartBoxIconShoppingCart"]')
                        cart.click()
                        flag = True
                    else:
                        driver.get('https://www.superama.com.mx/buscar/%s' % shoplist[k])
#                 elif superama_df.shape[0] == i:
#                         k += 1
#                         driver.get('https://www.superama.com.mx/buscar/%s' % shoplist[k])
                i += 1
            except: pass

# Walmart --------------------------------------        
    shape = df.shape[0]
    if name == 'walmart':
        driver.get('https://super.walmart.com.mx/productos?Ntt=%s' % df['product'][k])
        #driver.maximize_window()
        
        while flag == False:
            if k >= shape:
                cart = driver.find_element_by_xpath('//*[@id="headerId"]/a[3]')
                cart.click()
                flag = True
            
            time.sleep(1)
            #closing pops
            try:
                cross = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/button')
                cross.click()
            except: pass
            time.sleep(1)
            try:
                cross = driver.find_element_by_xpath('//*[@id="root"]/main/div[1]/div/div[2]/button')
                cross.click()
            except: pass
            # Making the cart
            try:
                prod = driver.find_element_by_xpath('//*[@id="scrollToTopComponent"]/section/div/div[3]/div[2]/div/div/div[%s]/div[2]/a/p' % i).text.lower()
                pri = driver.find_element_by_xpath('//*[@id="scrollToTopComponent"]/section/div/div[3]/div[2]/div/div/div[%s]/div[3]/div[1]/p' % i).text.split('/')[0]
                if i < 30:
                    element = driver.find_element_by_xpath('//*[@id="scrollToTopComponent"]/section/div/div[3]/div[2]/div/div/div[%s]/div[2]/a/p' % i)
                    element.location_once_scrolled_into_view
                if bool(re.search(r'%s' % df['product'][k],prod)) and bool(re.search(r'%s' % df['price'][k],pri)):
                    agg = driver.find_element_by_xpath('//*[@id="scrollToTopComponent"]/section/div/div[3]/div[2]/div/div/div[%s]/div[4]/div/button' % i)
                    agg.click()
                    k+=1
                    i=0
                    if k >= shape:
                        cart = driver.find_element_by_xpath('//*[@id="headerId"]/a[3]')
                        cart.click()
                        flag = True
                    driver.get('https://super.walmart.com.mx/productos?Ntt=%s' % df['product'][k])
                i += 1
                if i == 30:
                    print('An error occured we could not complete your shopping cart')
                    break
            except:
                pass

# Soriana -------------------------------            
    if name == 'soriana':
        driver.close()
        label = Label(master, text = '\nSorry, option currently not supported for Soriana', font='Helvetica 9'); label.pack()
        
# La Comer -------------------------------
    if name == 'la comer':
        url = 'https://www.lacomer.com.mx/lacomer/goBusqueda.action?succId=287&ver=mislistas&succFmt=100&criterio=%s#/%s' % (df['product'][k],df['product'][k])
        driver.get(url)
        #driver.maximize_window()
        
        while flag == False:
            if k >= shape:
                try:
                    time.sleep(1)
                    cart = driver.find_element_by_xpath('//*[@id="header"]/div[1]/div[1]/div/div[7]/div/div[3]/div/div/a')
                    cart.click()
                except: pass
                flag = True
            # Making the cart
            try:
                prod = driver.find_element_by_xpath('//*[@id="product_list"]/div/div[2]/div[2]/div/div[%s]/div/div[2]/div/div/div/a/strong' % i).text.lower()
                pri = driver.find_element_by_xpath('//*[@id="product_list"]/div/div[2]/div[2]/div/div[%s]/div/div[3]/div/div/span[2]' % i).text.lower()

                if bool(re.search(r'%s' % df['product'][k], prod)) and bool(re.search(r'%s' % df['price'][k],pri)):
                    #print(prod, pri)
                    time.sleep(1)
                    cart = driver.find_element_by_xpath('//*[@id="product_list"]/div/div[2]/div[2]/div/div[%s]/div/div[1]/a/div[1]/div' % i)
                    ActionChains(driver).move_to_element(cart).perform()
                    time.sleep(1)
                    p_id = driver.find_element_by_xpath('//*[@id="product_list"]/div/div[2]/div[2]/div/div[%s]/div/div[1]/a/div[1]/div/img'%i).get_attribute('src')
                    p_id = re.findall(r'\/(\d+)\_',p_id)[0]
                    time.sleep(1)
                    cart = driver.find_element_by_xpath('//*[@id="btn_addtoCart_%s"]'%p_id)
                    cart.click()
                    time.sleep(1)
                    try:
                        driver.find_element_by_xpath('//*[@id="modal_confirm_sucursal"]/div/div/div/div[5]/button[2]').click()
                    except: pass
                    k+=1
                    i=0
                    if k >= shape:
                        time.sleep(1)
                        cart = driver.find_element_by_xpath('//*[@id="header"]/div[1]/div[1]/div/div[7]/div/div[3]/div/div/a')
                        cart.click()
                        flag = True
                    time.sleep(1)
                    url = 'https://www.lacomer.com.mx/lacomer/goBusqueda.action?succId=287&ver=mislistas&succFmt=100&criterio=%s#/%s' % (df['product'][k],df['product'][k])
                    driver.get(url)
                    time.sleep(2)
                i+=1
            except:
                pass

def location(name):
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", { "profile.default_content_setting_values.geolocation": 1})
    chrome_options.add_argument("start-maximized")
    driver = webdriver.Chrome(chrome_options = chrome_options)

    driver.get('https://www.where-am-i.net/')
    time.sleep(1)
    localization = driver.find_element_by_xpath('//*[@id="lbllat"]').text+', '+driver.find_element_by_xpath('//*[@id="lbllng"]').text

    driver.get('https://www.google.com.mx/maps/')
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="searchbox-directions"]').click()
    time.sleep(1)
    loc = driver.find_element_by_xpath('//*[@id="sb_ifc51"]/input')
    loc.clear()
    loc.send_keys(localization)

    superm = driver.find_element_by_xpath('//*[@id="sb_ifc52"]/input')
    superm.clear()
    superm.send_keys(name)
    superm.send_keys(Keys.ENTER)

def recommended_list(df):
    newWindow = Toplevel(master) 
    newWindow.title("Recommended shop list") 
    newWindow.geometry("700x600") 
    #df = pd.read_csv('data/recommended_shoping_list.csv')
    
    f = Frame(newWindow)
    f.pack(fill=BOTH, expand = 1)
    table = Table(f, dataframe=df, showtoolbar=True, showstatusbar=True)
    table.show()

def multiple_lists(df):
    newWindow2 = Toplevel(master) 
    newWindow2.title("Best options shop list") 
    newWindow2.geometry("700x600") 
    #df = pd.read_csv('data/market_prices.csv')
    
    f = Frame(newWindow2)
    f.pack(fill=BOTH, expand = 1)
    table = Table(f, dataframe=df, showtoolbar=True, showstatusbar=True)
    table.show()

#  ------------------------------------------------------------------------------------------
# Window settings
#  ------------------------------------------------------------------------------------------
master = Tk()
master.title('Shoplist')
#master.resizable(False,True)
master.iconbitmap('iFruit.ico')
master.geometry("600x350")
#master['bg'] = '#363537'

#  ------------------------------------------------------------------------------------------
# Window widgets
#  ------------------------------------------------------------------------------------------
label = Label(master, text = 'Welcome to Shoplist!', font='Helvetica 14'); label.pack()

textbox = Text(master, font = 'Helvetica 14',width=50, height=3); textbox.pack()

boton = Button(master, text = "Go", command = lambda: main_run(textbox.get('1.0','end-1c')))
boton.pack()

#  ------------------------------------------------------------------------------------------
# Main
#  ------------------------------------------------------------------------------------------
def main_run(txt):
    print('Your shopping list:', txt)
    
    # txt to list --------------------------
    shop_lst = txt.split(',')
    shop_lst = [x.strip().lower() for x in shop_lst]
    label = Label(master, text = '\nSearching...', font='Helvetica 9'); label.pack()
    global progress_bar
    progress_bar = Progressbar(master, orient = 'horizontal', mode='determinate', maximum=100, value=0)
    progress_bar.pack()
    progress_bar['value'] = 0
    global val
    val = 100/(4*len(shop_lst)) # percentage grow by store (4 stores to search 'x' elements)
    master.update()
    # Web scraping -------------------------
    superama_df = superama_search(shop_lst); master.update()
    walmart_df  = walmart_search(shop_lst); master.update()
    soriana_df  = soriana_search(shop_lst); master.update()
    comer_df    = comer_search(shop_lst); master.update()
    
    # Selection of products ----------------
    superama_df = best_options(shop_lst, superama_df)
    walmart_df  = best_options(shop_lst, walmart_df)
    soriana_df  = best_options(shop_lst, soriana_df)
    comer_df    = best_options(shop_lst, comer_df)
    
    full_df = pd.concat([superama_df, walmart_df, soriana_df, comer_df], axis=0).reset_index(drop=True)
    print('Best options by supermarket:')
    print(full_df.to_markdown())
    full_df.to_csv('data/market_prices.csv')
    
    superama_best = filter_selection(superama_df, shop_lst)
    walmart_best  = filter_selection(walmart_df, shop_lst)
    soriana_best  = filter_selection(soriana_df, shop_lst)
    comer_best    = filter_selection(comer_df, shop_lst)
        
    supermarkets = {superama_best['price'].sum():'superama', walmart_best['price'].sum():'walmart',
                    soriana_best['price'].sum():'soriana', comer_best['price'].sum():'la comer'}
#     print(supermarkets)
#     display(pd.concat([superama_best, walmart_best, soriana_best, comer_best],axis=0))

    mv = min(supermarkets.keys())
    for df in [superama_best, walmart_best, soriana_best,comer_best]:
        if df.shape[0] != len(shop_lst):
            del supermarkets[mv]
            mv = min(supermarkets.keys())
    
    mv = min(supermarkets.keys())
#     print(supermarkets)
#     print(mv)

    
    if (supermarkets[mv] == 'superama') and (len(shop_lst)==superama_best.shape[0]):
        final_shoplist(superama_best, 'superama')
        name = 'superama'
        final_list = superama_best
    elif (supermarkets[mv] == 'walmart') and (len(shop_lst)==walmart_best.shape[0]):
        final_shoplist(walmart_best, 'walmart')
        name = 'walmart'
        final_list = walmart_best
    elif (supermarkets[mv] == 'soriana') and (len(shop_lst)==soriana_best.shape[0]):
        final_shoplist(soriana_best, 'soriana')
        name = 'soriana'
        final_list = soriana_best
    elif (supermarkets[mv] == 'la comer') and (len(shop_lst)==comer_best.shape[0]):
        final_shoplist(comer_best, 'la comer')
        name = 'la comer'
        final_list = comer_best
    else:
        print('error')
        final_shoplist(walmart_best, 'walmart')
        name = 'walmart'
        final_list = walmart_best

    final_list.to_csv('data/recommended_shoping_list.csv')
    
    progress_bar.pack_forget()
    label.pack_forget()
    label = Label(master, text = '\nReady!', font='Helvetica 9'); label.pack()
    msg = Label(master, text = '\nSelect an option:', font='Helvetica 9'); msg.pack()
    
    show = Button(master, text = "Show recommended list", command = lambda: recommended_list(final_list))
    show.pack()
    
    show2 = Button(master, text = "Show best options list", command = lambda: multiple_lists(full_df))
    show2.pack()
    
    scart = Button(master, text = "Make my shopping cart!", command = lambda: shop_cart(final_list, shop_lst, name.lower()))
    scart.pack()
    near = Button(master, text = "Show me the nearest supermarket", command = lambda: location(name.lower()))
    near.pack()

master.mainloop()





import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

def accessToWeb(address):
    driver.get(address)

def fillLoginData(_userName, _password):
    element = driver.find_element_by_id("login_field") 
    element.send_keys(_userName)#user_session_username

    element = driver.find_element_by_id('password')
    element.send_keys(_password)

    element.send_keys(Keys.RETURN)
    print("execute login :",_userName, _password)
    return element

def fillGistDesc(descr):
    element  = driver.find_element_by_name('gist[description]')
    assert element is not None, "description field is missing"
    element.send_keys(descr)
    
def getGistFileHeaderElement(gistElem):
    return gistElem.find_element_by_name("gist[contents][][name]")

def getGistTextArea(gistElem):
    return gistElem.find_element_by_class_name("CodeMirror-code")

def getListOfGistElements():
    listOfGistFiles = driver.find_elements_by_class_name("js-gist-file")
    assert len(listOfGistFiles) > 0, "number of file must be greater than 0"
    return listOfGistFiles

def getGistElementByFileName(fileName):
    allElems = getListOfGistElements()
    for gistElem in allElems:
        if getGistFileHeaderElement(gistElem).get_attribute('value') == fileName:
            return gistElem
    return None

def getDeleteButton(fromGistElem = None):
    gistElem = fromGistElem if fromGistElem is not None else driver
    deleteBtnElm = gistElem.find_element_by_css_selector("button.btn.btn-sm.btn-danger")
    assert deleteBtnElm is not None, "delete button is missing"
    return deleteBtnElm

def updateContent(gistElem, content):
    contenElmnt = getGistTextArea(gistElem)
    assert contenElmnt is not None, "Content field must exist"
    contenElmnt.send_keys(content)
    
def UpdateGist():
    element = None
    try:
        element = driver.find_element_by_name("gist[public]")
    except:
        print("element doesnt exist")
    
    if element == None:
        element = driver.find_element_by_css_selector("button.btn.btn-primary")    
    assert element is not None, "update button is missing"
    element.click()

def caseCreateNewGist(exptedFileName = "dummyFilesss.json"):
    fillGistDesc('this is dummy gist description')

    gistFiles = getListOfGistElements()
    gistfile = gistFiles[0]
    content = '{"title": "this is only for dummy test"}'
    fileHeaderElem = getGistFileHeaderElement(gistfile)
    fileHeaderElem.send_keys(exptedFileName)
    fileName = fileHeaderElem.get_attribute('value')
    assert exptedFileName == fileName, "expected file Name is : {0}".format(exptedFileName)

    updateContent(gistfile, content)

    UpdateGist()

def caseUpdateExistingGist(gistFileName):
    editBtnElem = driver.find_element_by_css_selector("a.btn.btn-sm")
    assert editBtnElem is not None, "edit button is missing"
    editBtnElem.click()
    
    wait = True
    while(wait):
        try:
            descElem = driver.find_element_by_name('gist[description]')
            wait = descElem is None
        except:
            wait = False
    
    gistFile = getGistElementByFileName(gistFileName)
    assert gistFile is not None, "gist file with expected file name must exist : {0}".format(gistFileName)
    content = '{"title": "this is only for dummy test", "update" : "this update line"}'
    updateContent(gistFile, content)

    UpdateGist()

def caseDeleteExistingGistFile(fileName = ""):
    editBtnElem = driver.find_element_by_css_selector("a.btn.btn-sm")
    assert editBtnElem is not None, "edit button is missing"
    editBtnElem.click()

    deleteBtnElem = None
    gistFiles = getListOfGistElements()
    if len(gistFiles) == 1:
        deleteBtnElem = getDeleteButton()
    elif len(gistFiles)> 1:
        gistFile = getGistElementByFileName(fileName)
        deleteBtnElem = getDeleteButton(gistFile)
    
    if deleteBtnElem is not None:
        deleteBtnElem.click()
        driver.switch_to.alert.accept()
        

def caseCheckingExpectedElementExistency():
    pass

if __name__ == "__main__":
    f = open("githubCredential.json",)
    cred = json.load(f)
    f.close()
    userName = cred["userName"]
    password = cred["password"]
    exptedFileName = "DummyFile Gist TBD2.json"
    accessToWeb('https://github.com/login')

    fillLoginData(userName,password)
    
    accessToWeb('https://gist.github.com/')

    caseCreateNewGist(exptedFileName)

    caseUpdateExistingGist(exptedFileName)

    caseDeleteExistingGistFile(exptedFileName)


    driver.close() #uncomment if needed


def return_titles(driver, by, class_name):
    titles = [title for title in driver.find_elements(by.CLASS_NAME, class_name)]
    print("title",titles)
    return titles

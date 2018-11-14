# README #

Cerebot is an automated script that uses Asana API and Google Drive API to automate repetitive processes used by the human-I-T company. Asana is widely used by human-I-T to inventory and edit items, so we found a much more efficient method. Cerebot has 3 features: inventory, wipe, destroy. All of these features basically move Asana tasks from one project to another and fills out its custom fields.  

![image1](https://user-images.githubusercontent.com/30359951/40583438-ad541dca-6143-11e8-975d-2e3bc595b5f6.png)

## Inventory ##
Inventory items quickly! Fill out the custom fields on the top, then scan each item's barcode to inventory. The selected items will then be placed into an Asana project called Inventory, each with its own custom field.

![image2](https://user-images.githubusercontent.com/30359951/40583447-f3f4ebd8-6143-11e8-8ca4-2d45a186d20c.png)

## Cert Check ##
Wiping hard drives! The cert check goes through the Asana tasks in the Inventory project, and attaches a pdf file that was created from our server that wipes hard drives. The server holds up to 15 hard drives, and sends a pdf file to a google drive folder, where Cerebot checks. The Cerebot locates the bar code in the Google Drive folder, and then attaches to the Asana task with its respective bar code.

![image3](https://user-images.githubusercontent.com/30359951/40583464-2aa63952-6144-11e8-89eb-cf551c34fea9.png)

## Destruction ##
Sending hard drives into destruction! Cerebot goes through the Asana tasks that was filled out by the user and puts them into the "Destruction" project in Asana. These hard drives will be thrown to the E-waste pile, to be completely destroyed and scrapped.

![image4](https://user-images.githubusercontent.com/30359951/40583474-4b107978-6144-11e8-83aa-6f7ad0858d5c.png)


### Installation ###
1. Download python and add it to your PATH
2. Download Git (for pip)
3. Go to your repository in Git
4. Type in 'pip install httplib2'
5. Type in 'pip install --upgrade google-api-python-client'
6. Type in 'pip install asana'
7. Run asana-automate.py

### Contribution guidelines ###
* Writing code - Mainly Patrick, main developer. Preston - Optimized and debugged code.
* Writing tests - Preston - Wrote over 100 test cases for duplication errors
* Code review - Preston - Reviewed Patrick's code

### Who do I talk to? ###

* humanit@patriick.com - Main Programmer
* prestonwong7@gmail.com - Debugger and Optimizations

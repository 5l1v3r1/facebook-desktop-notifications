from unofficial_graph_api import fetch_json
from unofficial_graph_api import basic_functions
import random
import requests
import notify2
import time
import sys
import os

# stores previous timestamp so that new message will not repeat
old_timestamp = 0

# initialise the d-bus connection 
notify2.init("Facebook Desktop Notifier")

# uid = 0

online = True

# notify2 uses caching images with same name, 
# so to change the image name everytime to not repeat same 
# thumbnail in every notifications
image_path = 'tmp' + str(random.randint(9939, 9199182)) + '.png'

url='https://www.facebook.com/messages/'

cookies = {
    'xs': 'YOUR_ACCESS_TOKEN_HERE', # REPLACE IT WITH YOUR ACCESS TOKEN
    'c_user': 'YOUR_USER_ID_HERE'   # REPLACE IT WITH YOUR USER ID
}


jsscript_index = 0

# Downloads thumbnail for notifications
def thumbnail_downloader(icon_url, indx):
    import shutil
    response = requests.get(icon_url, stream=True)
    with open(image_path, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

# main function to check and update values
def update():
    if cookies['xs'] == 'YOUR_ACCESS_TOKEN_HERE' \
        or cookies['c_user'] == 'YOUR_USER_ID_HERE' :
        print('please provide access token before continuing in cookies variable of fdn.py')
        exit(0)

    global old_timestamp
    response = requests.get(url, cookies=cookies)

    # Facebook use to change index of json provider js function
    # to escape scraping (or maybe it's a react feature, IDK)

    try:
        # using this in case of index id already configured
        jsd = fetch_json.get_json(response.content, script_id)
    except:
        # at first time it configures the json provider script index
        #   and stores in jsscript_index variable to avoid keep calling
        #   index configuring function from autotroubleshoot
        jsscript_index = fetch_json.auto_troubleshoot(response.content)
        jsd = fetch_json.get_json(response.content, jsscript_index)

    uid = 0
    while True:
        try:
            # base filter for accessing required infos
            inbox_data = jsd['require'][48][3][1]["graphqlPayload"]["thread_list"]["viewer"]["message_threads"]["nodes"][uid]
            ## file = open('timestamp.txt', 'a')
            
            # check for new message
            unseen_count = basic_functions.get_unread_message_count(inbox_data)
            user_id = basic_functions.get_user_id(inbox_data)
            
            # and checking if user id is not equal to own user id
            if unseen_count > 0 and \
                user_id != str(cookies['c_user']):
                
                # dtoring all infos in variables
                message = basic_functions.get_last_message(inbox_data)
                user_name = basic_functions.get_user_name(inbox_data)
                latest_timestamp = basic_functions.get_timestamp(inbox_data)
                ## old_timestamp = file.read()
                
                # checking for timestamp to avoid same notification
                # which already been displayed before
                if latest_timestamp != str(old_timestamp):
                    old_timestamp = latest_timestamp
                    ## file.write(str(latest_timestamp))
                    ## pass

                else:
                    break

                # getting thumbnail link in variable
                icon = basic_functions.get_icon(inbox_data)
                # downloading thumbnail
                thumbnail_downloader(icon, uid)
            
                ##print(user_name + ':' + message)
                
                # create Notification object 
                ## print(icon)
                notifier = notify2.Notification(user_name, message + '        (' + str(unseen_count) + ')' , os.path.abspath(image_path))
                
                # set urgency level 
                notifier.set_urgency(notify2.URGENCY_NORMAL)
                notifier.show()
                
                # removing thumbnail after uses
                os.remove(image_path)
                
                ## time.sleep(5)                
            ## user_id = inbox_data['last_message']['nodes'][0]['snippet']['message_sender']['messaging_actor']['id']

            else:
                pass
            uid += 1
        
        except Exception as e:
        ##    print(e)
            break

    ## print(icon)
        ## file.flush()
        ## file.close()

if __name__ == '__main__':
    try:
        if sys.argv[1] == "-v" or "--vesrion":
            print("Facebook Desktop Notifier v1.1")
    except:
        while online:
            update()
            # time.sleep(5)

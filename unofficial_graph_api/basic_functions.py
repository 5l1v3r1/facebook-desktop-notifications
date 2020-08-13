def get_unread_message_count(fetch_filter):
    unread_count = fetch_filter['unread_count']
    return unread_count

def get_last_message(fetch_filter):
    message = fetch_filter['last_message']['nodes'][0]['snippet']
    return message

def get_user_id(fetch_filter):
    user_id = fetch_filter['last_message']['nodes'][0]['message_sender']['messaging_actor']['id']
    return user_id

def get_user_name(fetch_filter):
    user_name = fetch_filter['all_participants']['edges'][0]['node']['messaging_actor']['name']
    return user_name

def get_icon(fetch_filter):
    icon = fetch_filter['all_participants']['edges'][0]['node']['messaging_actor']['big_image_src']['uri']
    return icon

def get_timestamp(fetch_filter):
    stamp = fetch_filter['last_message']['nodes'][0]['timestamp_precise']
    return stamp
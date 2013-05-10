def carl_to_dict(carl):
    info = {}
    if carl:
        info['carlnetid'] = carl.carlnetid
        info['first_name'] = carl.first_name
        info['last_name'] = carl.last_name
        info['directory_url'] = carl.directory_url
        info['photo'] = carl.photo
        info['email'] = carl.email
    return info
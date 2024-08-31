trackme = {
    '10.220.249.232': ["mrjones"],
}
ssh_user = 'timekpr-next-remote'
ssh_password = 'timekpr-next-remote'
ssh_timekpra_bin = '/usr/bin/timekpra'
ssh_key = './id_timekpr'

gotify =[
    # set to True to enable, update with you token and URL
    {
        'enabled': False,
        'token': 'token1-here',
        'url': 'http://url2-here.com'
    },
    # Uncomment if you want to send alerts to more than one user - add as many as you'd like!
    # {
    #     'enabled': False,
    #     'token': 'token1-here',
    #     'url': 'http://url2-here.com'
    # }
]
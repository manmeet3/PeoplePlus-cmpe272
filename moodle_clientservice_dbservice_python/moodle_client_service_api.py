import requests

def config(function):
        token = '202329a6f2b9220187ee8d09c611fcd8'# d9790b0194ddc40d9ed1b2253e11a419 ; 2bdb462ca65b5d37c65a0be9035c40f4
        url = 'http://18.225.11.231/moodle/webservice/rest/server.php?wstoken={0}&wsfunction={1}'.format(token, function) #&moodlewsformat=json
        return url

users = {'users[0][email]': 'test@mydept.edu',
        'users[0][firstname]': 'Test',
        'users[0][lastname]': 'Test1',
        'users[0][createpassword]': 1,
        'users[0][username]': 'Testst'}

'''
my $params = {
    'wstoken' => '6749ad13bc4af',
    'wsfunction' => 'moodle_user_get_users_by_id',
    'userids[0]' => '1'.
    };
    select_method = {
            "moodle_course_get_courses": moodle_course_get_courses,
            core_course_get_courses_by_field
            "moodle_course_create_courses": moodle_course_create_courses,
            "moodle_user_get_users_by_id": moodle_user_get_users_by_id,
            "moodle_user_create_users": moodle_user_create_users,
            "moodle_user_update_users": moodle_user_update_users,
            "moodle_enrol_manual_enrol_users": moodle_enrol_manual_enrol_users,
            "not_implemented_yet": not_implemented_yet,
        }
'''
#response = requests.post(url,json=users)
#print(response.status_code)




payload = {
    "wstoken": "2bdb462ca65b5d37c65a0be9035c40f4",
    "wsfunction":"core_course_get_courses"
}

response2 = requests.get(url, params=payload)
print("2:",response2.status_code)
print(response2.content)

###############################
function = 'core_course_get_courses' # core_course_get_courses;core_user_create_users

## get courses
url = config('core_course_get_courses')
response =requests.get(url)
print(response.status_code)
print(response.content)



#create user
print('####core_user_create_users')
token = "2bdb462ca65b5d37c65a0be9035c40f4"
function='core_user_create_users'


users = {'users[0][email]': 'email@local.host',
         'users[0][firstname]': 'test2',
         'users[0][lastname]': 'test22',
         'users[0][createpassword]': 1,
         'users[0][username]': 'username'}
responce= requests.post(url,params=users)
print(response.content)

################################

moodle_create_token = '2bdb462ca65b5d37c65a0be9035c40f4'

payload = {
    "wstoken":moodle_create_token,
    "moodlewsrestformat":"json",
    "wsfunction":"core_course_create_courses",
    "cources[0][fullname]": "PeoplePlus_Course_3",
    "cources[0][shortname]": "cource_3",
    "cources[0][categoryid]": 1,
    "cources[0][visible]": 1,
     "cources[0][idnumber]": 3
    }

r=requests.post(target, params=payload)
print(r.status_code)
print(r.content)
###################################
url ='http://localhost/webservice/restful/server.php/core_course_get_courses'
payload = {"Authorization":'2bdb462ca65b5d37c65a0be9035c40f4', "options[ids][0]":1}
r=requests.post(target, json=payload)
print(r.status_code)
print(r.content)

##create course: core_course_create_courses
print('core_course_get_courses_by_field:')
url = config('core_course_get_courses_by_field')
params = {"field" : "2"}


response = requests.post(url,json=params)
print(response.status_code)
print(response.content)


#create user
print('####core_user_create_users')
token = "2bdb462ca65b5d37c65a0be9035c40f4"
function='core_user_create_users'
#url = 'http://localhost/webservice/rest/server.php?wstoken={0}&wsfunction={1}&moodlewsformat=json'.format(token,function)
url = config('core_user_create_users')

users = {"users[0][createpassword]": 1, "users[0][username]": "testuser5", "users[0][auth]": "manual", "users[0][firstname]": "test5", "users[0][lastname]": "lastname_test5","users[0][email]": "abc5@gmail.com",}
response= requests.post(url,params=users)
print(response.status_code)
print(response.content)




##create course: core_course_create_courses
print('core_course_create_courses:')
url = config('core_course_create_courses')


cources = {"courses[0][fullname]": "PeoplePlus_Course_7",
           "cources[0][shortname]": "shortname",
           "cources[0][categoryid]": 1,
           "cources[0][idnumber]": "6",
           "courses[0][summaryformat]": 1,
           "courses[0][format]": "topics",
           "courses[0][showgrades]": 1,
           "courses[0][newsitems]": 5,
           "courses[0][maxbytes]": 0,
           "courses[0][showreports]": 0,
           "courses[0][visible]": 1,
           "courses[0][groupmode]": 0,
           "courses[0][groupmodeforce]": 0,
           "courses[0][defaultgroupingid]": 0,}

new_url= "http://localhost/webservice/rest/server.php?wstoken=54aa88fde406ef9d73d74e9b66103132&wsfunction=core_course_create_courses&moodlewsformat=json"
response = requests.post(url,params=cources)
print(response.status_code)
print(response.content)

#core_role_assign_roles
print('core_role_assign_roles:')
url = config('core_role_assign_roles')
assignments = {"assignments[0][roleid]": 5,"assignments[0][userid]": 6, }
response= requests.post(url,params=assignments)
print(response.status_code)
print(response.content)


#core_role_unassign_roles
print('core_role_unassign_roles:')
url = config('core_role_unassign_roles')
unassignments = {"unassignments[0][roleid]": 5,"unassignments[0][userid]": 6, }
response= requests.post(url,params=unassignments)
print(response.status_code)
print(response.content)

An Enterprise Software Application for managing employees in an organization, end-to-end.
Based on Scotch.io's [Tutorial](https://scotch.io/tutorials/build-a-crud-web-app-with-python-and-flask-part-one)

## Architecture
### High Level Design
#### High Level
![High Level](https://raw.githubusercontent.com/manmeet3/PeoplePlus-cmpe272/master/artifacts/high-level.png)
#### Activity Diagram
![Activity Diagram](https://raw.githubusercontent.com/manmeet3/PeoplePlus-cmpe272/master/artifacts/activity-diagram.png)
#### User Roles
![User Roles](https://raw.githubusercontent.com/manmeet3/PeoplePlus-cmpe272/master/artifacts/user-roles.png)
### Single Sign-On with Keycloak
#### SSO Configuration
![SSO Configuration](https://raw.githubusercontent.com/manmeet3/PeoplePlus-cmpe272/master/artifacts/sso-configuration.png)
#### SSO Sequence
![SSO Sequence](https://raw.githubusercontent.com/manmeet3/PeoplePlus-cmpe272/master/artifacts/sso-sequence.png)

### Database Design
#### DB High Level
![DB High Level](https://raw.githubusercontent.com/manmeet3/PeoplePlus-cmpe272/master/artifacts/db-high-level.png)
#### DB Employees
![DB Employees](https://raw.githubusercontent.com/manmeet3/PeoplePlus-cmpe272/master/artifacts/emp-db-design.png)
#### DB LMS
![DB LMS](https://raw.githubusercontent.com/manmeet3/PeoplePlus-cmpe272/master/artifacts/lms-db-design.png)

### Running the App
export FLASK_CONFIG='development'  
export FLASK_APP=app/__init__.py  
export FLASK_APP=run.py  
flask run -h localhost -p 3000  

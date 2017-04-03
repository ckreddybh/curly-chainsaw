django-api/task_management
================
task management api 


# Prerequisites
- pip install the requirements.txt
- make sure you are in task_management dir

# User details
| usernaem  |  password | user type |
|--:|--:|--:|
|  ck | ck  | admin |
|  student | student  | student |
|  student2 |  student  | student |
|  student3 |  student  | student |
|  student4 |  student  | student |

# Setup
Use fixtures to load intial data:
- `python manage.py loaddata initial_data.yaml`
 
###Run examples
- `python manage.py runserver`


## Convention used
- for `admin` user type `1`
- for `student` user type `2`
- `TASK STATUS ((1, 'todo'), (2, 'doing'), (3, 'done'), (5, 'approve'), (4, 'disapprove'))`
- every request expect a valid username and password i.e `logid` and `logpass` should be send as along with the required params 
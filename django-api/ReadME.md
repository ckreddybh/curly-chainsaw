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
- every request expect a valid username and password i.e `logid` and `logpass` should be send along with the required params 

## Post urls
- `127.0.0.1:8000/task/statusupdate/` to change task status
- `127.0.0.1:8000/task/assigneeupdate/` to add assignee you can give multiple assignees (comma separate)
- `127.0.0.1:8000/task/assigneedelete/` to delete assignee you can give multiple assignees (comma separate)
- `127.0.0.1:8000/task/taskdelete/` to delete a task excepts task_id
- `127.0.0.1:8000/task/taskcreate/` to create a task 
- `127.0.0.1:8000/task/user/` to create new user in db

## Get urls
- `127.0.0.1:8000/task/taskcreate/` to list all tasks (admin can list all tasks/ student can list only his tasks )
- `127.0.0.1:8000/task/user/` to list all users 



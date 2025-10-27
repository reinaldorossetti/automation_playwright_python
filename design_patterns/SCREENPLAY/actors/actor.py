

from questions.login_question import LoginQuestion
from tasks.login_task import LoginTask


class Actor:
    
    def web_perform(self, task):
        return self.browser_type_launch_args(task)

    def browser_type_launch_args(self, browser_type_launch_args):
        return {
            **browser_type_launch_args,
            "headless": False,  # Set headless to False
        }

def prepare_actor_login_task(page):
    return LoginTask(page)

def prepare_actor_login_question(page):
    return LoginQuestion(page)